#!/usr/bin/env python3
"""
OpenReview ACL Paper Scraper
============================
This script fetches paper submissions from OpenReview for ACL-related venues.
ACL Rolling Review (ARR) uses OpenReview, which may include:
- Accepted papers
- Rejected papers (if publicly visible)
- Papers under review

OpenReview API: https://api.openreview.net/
"""

import requests
import pandas as pd
import json
import os
import time
from datetime import datetime
from tqdm import tqdm
from typing import List, Dict, Optional
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# OpenReview API base URL
OPENREVIEW_API = "https://api2.openreview.net"

# ACL-related venues on OpenReview
OPENREVIEW_VENUES = {
    # ACL Rolling Review
    'arr': [
        'aclweb.org/ACL/ARR/2023',
        'aclweb.org/ACL/ARR/2024',
        'aclweb.org/ACL/ARR/2025',
    ],
    # ACL main conferences (if available on OpenReview)
    'acl': [
        'aclweb.org/ACL/2023/Conference',
        'aclweb.org/ACL/2024/Conference',
        'aclweb.org/ACL/2025/Conference',
    ],
    'emnlp': [
        'EMNLP/2023/Conference',
        'EMNLP/2024/Conference',
    ],
    'naacl': [
        'aclweb.org/NAACL/2024/Conference',
    ],
}


class OpenReviewScraper:
    """Scraper for OpenReview papers."""
    
    def __init__(self, output_dir: str = "data"):
        self.output_dir = output_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Research Paper Scraper)',
            'Accept': 'application/json',
        })
        os.makedirs(output_dir, exist_ok=True)
    
    def get_venue_submissions(self, venue_id: str, limit: int = 1000) -> List[Dict]:
        """Get all submissions for a venue using OpenReview API."""
        logger.info(f"Fetching submissions for venue: {venue_id}")
        
        all_notes = []
        offset = 0
        
        while True:
            try:
                # Try the v2 API first
                url = f"{OPENREVIEW_API}/notes"
                params = {
                    'invitation': f"{venue_id}/-/Submission",
                    'limit': min(limit, 1000),
                    'offset': offset,
                }
                
                response = self.session.get(url, params=params, timeout=30)
                
                if response.status_code == 404:
                    # Try alternative invitation patterns
                    alt_invitations = [
                        f"{venue_id}/-/Blind_Submission",
                        f"{venue_id}/-/Full_Submission",
                        f"{venue_id}/Submission",
                    ]
                    for alt_inv in alt_invitations:
                        params['invitation'] = alt_inv
                        response = self.session.get(url, params=params, timeout=30)
                        if response.status_code == 200:
                            break
                
                if response.status_code != 200:
                    logger.warning(f"Failed to fetch {venue_id}: {response.status_code}")
                    break
                
                data = response.json()
                notes = data.get('notes', [])
                
                if not notes:
                    break
                
                all_notes.extend(notes)
                offset += len(notes)
                
                logger.info(f"Fetched {len(all_notes)} submissions so far...")
                
                if len(notes) < 1000:
                    break
                
                time.sleep(0.5)  # Be polite
                
            except requests.RequestException as e:
                logger.error(f"Request error: {e}")
                break
        
        return all_notes
    
    def parse_submission(self, note: Dict, venue_id: str) -> Dict:
        """Parse a submission note into a structured format."""
        content = note.get('content', {})
        
        # Handle different content formats (v1 vs v2 API)
        def get_value(field):
            val = content.get(field, '')
            if isinstance(val, dict):
                return val.get('value', '')
            return val
        
        # Extract authors
        authors = get_value('authors')
        if isinstance(authors, str):
            authors = [a.strip() for a in authors.split(',')]
        elif not isinstance(authors, list):
            authors = []
        
        # Determine paper status from various fields
        status = 'submitted'  # Default
        decision = get_value('decision') or get_value('final_decision')
        if decision:
            decision_lower = decision.lower()
            if 'accept' in decision_lower:
                status = 'accepted'
            elif 'reject' in decision_lower:
                status = 'rejected'
            elif 'withdraw' in decision_lower:
                status = 'withdrawn'
        
        # Check for acceptance/rejection in venue or invitation
        venue = note.get('venue', '')
        if 'Reject' in venue:
            status = 'rejected'
        elif 'Accept' in venue:
            status = 'accepted'
        
        return {
            'paper_id': note.get('id', ''),
            'title': get_value('title'),
            'authors': authors,
            'authors_str': ', '.join(authors) if authors else '',
            'abstract': get_value('abstract'),
            'keywords': get_value('keywords'),
            'venue_id': venue_id,
            'venue': venue,
            'status': status,
            'decision': decision,
            'url': f"https://openreview.net/forum?id={note.get('id', '')}",
            'pdf_url': f"https://openreview.net/pdf?id={note.get('id', '')}" if note.get('id') else '',
            'created_date': datetime.fromtimestamp(note.get('cdate', 0) / 1000).isoformat() if note.get('cdate') else '',
            'modified_date': datetime.fromtimestamp(note.get('mdate', 0) / 1000).isoformat() if note.get('mdate') else '',
            'scraped_at': datetime.now().isoformat(),
        }
    
    def search_papers(self, query: str, venue: str = None, limit: int = 100) -> List[Dict]:
        """Search for papers using OpenReview's search API."""
        logger.info(f"Searching for: {query}")
        
        url = f"{OPENREVIEW_API}/notes/search"
        params = {
            'query': query,
            'limit': limit,
        }
        if venue:
            params['venue'] = venue
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                return data.get('notes', [])
        except requests.RequestException as e:
            logger.error(f"Search error: {e}")
        
        return []
    
    def get_venue_info(self, venue_id: str) -> Optional[Dict]:
        """Get information about a venue."""
        url = f"{OPENREVIEW_API}/groups"
        params = {'id': venue_id}
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                groups = data.get('groups', [])
                return groups[0] if groups else None
        except requests.RequestException as e:
            logger.error(f"Error fetching venue info: {e}")
        
        return None
    
    def scrape_arr_cycles(self, years: List[str] = None) -> pd.DataFrame:
        """Scrape ACL Rolling Review cycles."""
        if years is None:
            years = ['2023', '2024', '2025']
        
        all_papers = []
        
        # ARR has monthly cycles
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
        
        for year in years:
            for month in months:
                venue_id = f"aclweb.org/ACL/ARR/{year}/{month}"
                logger.info(f"Trying ARR cycle: {venue_id}")
                
                submissions = self.get_venue_submissions(venue_id)
                
                for note in submissions:
                    paper = self.parse_submission(note, venue_id)
                    if paper.get('title'):
                        paper['arr_cycle'] = f"{month} {year}"
                        all_papers.append(paper)
                
                if submissions:
                    logger.info(f"Found {len(submissions)} papers in {month} {year}")
                
                time.sleep(0.3)
        
        return pd.DataFrame(all_papers)
    
    def scrape_all(self, venue_ids: List[str] = None) -> pd.DataFrame:
        """Scrape all specified venues."""
        if venue_ids is None:
            venue_ids = []
            for venues in OPENREVIEW_VENUES.values():
                venue_ids.extend(venues)
        
        all_papers = []
        
        for venue_id in tqdm(venue_ids, desc="Scraping venues"):
            submissions = self.get_venue_submissions(venue_id)
            
            for note in submissions:
                paper = self.parse_submission(note, venue_id)
                if paper.get('title'):
                    all_papers.append(paper)
            
            logger.info(f"Found {len(submissions)} papers in {venue_id}")
            time.sleep(0.5)
        
        return pd.DataFrame(all_papers)
    
    def save_results(self, df: pd.DataFrame, filename: str = "openreview_papers"):
        """Save results to multiple formats."""
        if df.empty:
            logger.warning("No papers to save")
            return
        
        # Save to CSV
        csv_path = os.path.join(self.output_dir, f"{filename}.csv")
        df.to_csv(csv_path, index=False, encoding='utf-8')
        logger.info(f"Saved {len(df)} papers to {csv_path}")
        
        # Save to JSON
        json_path = os.path.join(self.output_dir, f"{filename}.json")
        df.to_json(json_path, orient='records', indent=2, force_ascii=False)
        logger.info(f"Saved to {json_path}")
        
        # Save summary
        summary = {
            'total_papers': len(df),
            'by_status': df['status'].value_counts().to_dict() if 'status' in df.columns else {},
            'by_venue': df['venue_id'].value_counts().to_dict() if 'venue_id' in df.columns else {},
            'accepted': len(df[df['status'] == 'accepted']) if 'status' in df.columns else 0,
            'rejected': len(df[df['status'] == 'rejected']) if 'status' in df.columns else 0,
            'scraped_at': datetime.now().isoformat(),
        }
        
        summary_path = os.path.join(self.output_dir, f"{filename}_summary.json")
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved summary to {summary_path}")


def main():
    """Main function to run the OpenReview scraper."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Scrape OpenReview papers for ACL venues')
    parser.add_argument('--mode', choices=['arr', 'venues', 'all'], default='all',
                        help='Scraping mode: arr (ACL Rolling Review), venues, or all')
    parser.add_argument('--years', nargs='+', default=['2023', '2024', '2025'],
                        help='Years to scrape')
    parser.add_argument('--output', '-o', default='data',
                        help='Output directory')
    parser.add_argument('--filename', default='openreview_papers',
                        help='Output filename prefix')
    
    args = parser.parse_args()
    
    logger.info("Starting OpenReview Scraper")
    logger.info(f"Mode: {args.mode}")
    logger.info(f"Years: {args.years}")
    
    scraper = OpenReviewScraper(output_dir=args.output)
    
    if args.mode == 'arr':
        df = scraper.scrape_arr_cycles(years=args.years)
    elif args.mode == 'venues':
        venue_ids = []
        for venues in OPENREVIEW_VENUES.values():
            venue_ids.extend(venues)
        df = scraper.scrape_all(venue_ids)
    else:
        # Scrape both ARR and direct venues
        df_arr = scraper.scrape_arr_cycles(years=args.years)
        
        venue_ids = []
        for key, venues in OPENREVIEW_VENUES.items():
            if key != 'arr':
                venue_ids.extend(venues)
        df_venues = scraper.scrape_all(venue_ids)
        
        df = pd.concat([df_arr, df_venues], ignore_index=True)
    
    if not df.empty:
        # Remove duplicates based on paper_id
        df = df.drop_duplicates(subset=['paper_id'], keep='first')
        scraper.save_results(df, filename=args.filename)
        
        print(f"\n{'='*60}")
        print(f"Scraping complete!")
        print(f"Total papers: {len(df)}")
        if 'status' in df.columns:
            print(f"\nPapers by status:")
            print(df['status'].value_counts().to_string())
    else:
        print("No papers found.")


if __name__ == "__main__":
    main()

