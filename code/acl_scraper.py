#!/usr/bin/env python3
"""
ACL Paper Scraper
=================
This script scrapes paper information from ACL Anthology (2023-2025).
It collects metadata including title, authors, abstract, venue, year, and URLs.

ACL Anthology URL structure:
- https://aclanthology.org/events/acl-2023/
- https://aclanthology.org/events/acl-2024/
- etc.

Note: ACL Anthology only contains accepted papers. 
Rejected papers are typically not publicly available.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os
import time
import re
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

# Constants
BASE_URL = "https://aclanthology.org"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

# ACL venues to scrape (main conferences)
ACL_VENUES = {
    'acl': 'ACL',           # Annual Meeting of the ACL
    'naacl': 'NAACL',       # North American Chapter of ACL
    'emnlp': 'EMNLP',       # Empirical Methods in NLP
    'eacl': 'EACL',         # European Chapter of ACL
    'findings': 'Findings', # Findings of ACL/EMNLP/NAACL
    'tacl': 'TACL',         # Transactions of ACL
}

YEARS = ['2023', '2024', '2025']


class ACLScraper:
    """Scraper for ACL Anthology papers."""
    
    def __init__(self, output_dir: str = "data"):
        self.output_dir = output_dir
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        os.makedirs(output_dir, exist_ok=True)
        
    def get_page(self, url: str, retries: int = 3) -> Optional[BeautifulSoup]:
        """Fetch a page and return BeautifulSoup object."""
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                return BeautifulSoup(response.text, 'lxml')
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
        return None
    
    def get_event_proceedings(self, venue: str, year: str) -> List[str]:
        """Get all proceeding URLs for a venue and year."""
        event_url = f"{BASE_URL}/events/{venue}-{year}/"
        logger.info(f"Fetching event page: {event_url}")
        
        soup = self.get_page(event_url)
        if not soup:
            logger.warning(f"Could not fetch event page for {venue}-{year}")
            return []
        
        # Find all proceeding links
        proceedings = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Match proceedings URLs like /volumes/2023.acl-long/
            if re.match(rf'/volumes/\d+\.{venue}', href):
                full_url = BASE_URL + href if href.startswith('/') else href
                if full_url not in proceedings:
                    proceedings.append(full_url)
        
        logger.info(f"Found {len(proceedings)} proceedings for {venue}-{year}")
        return proceedings
    
    def get_volume_papers(self, volume_url: str) -> List[Dict]:
        """Get all papers from a volume page."""
        logger.info(f"Fetching volume: {volume_url}")
        
        soup = self.get_page(volume_url)
        if not soup:
            return []
        
        papers = []
        
        # Find paper entries - they're typically in a list with class 'paper-abstract'
        paper_elements = soup.find_all('p', class_='d-sm-flex')
        
        if not paper_elements:
            # Alternative: look for paper links directly
            paper_elements = soup.find_all('span', class_='d-block')
        
        for element in paper_elements:
            try:
                paper_info = self.parse_paper_element(element, volume_url)
                if paper_info:
                    papers.append(paper_info)
            except Exception as e:
                logger.debug(f"Error parsing paper element: {e}")
                continue
        
        return papers
    
    def parse_paper_element(self, element, volume_url: str) -> Optional[Dict]:
        """Parse a paper element to extract metadata."""
        # Find the paper title - it's in <strong><a class=align-middle href=...>Title</a></strong>
        strong_elem = element.find('strong')
        if not strong_elem:
            return None
        
        title_link = strong_elem.find('a', class_='align-middle')
        if not title_link:
            title_link = strong_elem.find('a')
        
        if not title_link:
            return None
        
        title = title_link.get_text(strip=True)
        paper_url = title_link.get('href', '')
        
        # Skip if it's a PDF link or bib link (not a paper page)
        if paper_url.endswith('.pdf') or paper_url.endswith('.bib'):
            return None
        
        if paper_url.startswith('/'):
            paper_url = BASE_URL + paper_url
        
        # Extract paper ID from URL
        paper_id = paper_url.rstrip('/').split('/')[-1] if paper_url else ''
        
        # Find authors - they're in <a href=/people/...> tags within the same span as the title
        authors = []
        # Look for all author links in the element (they have /people/ in href)
        author_elements = element.find_all('a', href=lambda x: x and '/people/' in x)
        for author in author_elements:
            author_name = author.get_text(strip=True)
            if author_name and author_name not in authors:
                authors.append(author_name)
        
        # Extract venue and year from volume URL
        venue = ''
        year = ''
        match = re.search(r'/(\d{4})\.(\w+)', volume_url)
        if match:
            year = match.group(1)
            venue = match.group(2)
        
        # Extract track type (long, short, demo, etc.) from paper_id
        track = ''
        if paper_id:
            parts = paper_id.split('.')
            if len(parts) >= 2:
                track_parts = parts[1].split('-')
                if len(track_parts) >= 2:
                    track = track_parts[1]  # e.g., 'long', 'short', 'demos'
        
        return {
            'paper_id': paper_id,
            'title': title,
            'authors': authors,
            'authors_str': ', '.join(authors),
            'url': paper_url,
            'venue': venue.upper() if venue else '',
            'track': track,
            'year': year,
            'volume_url': volume_url,
            'status': 'accepted',  # ACL Anthology only has accepted papers
            'scraped_at': datetime.now().isoformat()
        }
    
    def get_paper_details(self, paper_url: str) -> Dict:
        """Get detailed information for a single paper."""
        soup = self.get_page(paper_url)
        if not soup:
            return {}
        
        details = {}
        
        # Get abstract
        abstract_elem = soup.find('div', class_='card-body acl-abstract')
        if abstract_elem:
            abstract_span = abstract_elem.find('span')
            if abstract_span:
                details['abstract'] = abstract_span.get_text(strip=True)
        
        # Get PDF link
        pdf_link = soup.find('a', class_='btn-primary', href=lambda x: x and x.endswith('.pdf'))
        if pdf_link:
            details['pdf_url'] = pdf_link['href']
        
        # Get DOI
        doi_elem = soup.find('a', href=lambda x: x and 'doi.org' in str(x))
        if doi_elem:
            details['doi'] = doi_elem['href']
        
        # Get venue info from breadcrumb
        breadcrumb = soup.find('nav', {'aria-label': 'breadcrumb'})
        if breadcrumb:
            items = breadcrumb.find_all('li')
            if len(items) >= 2:
                details['full_venue'] = items[-2].get_text(strip=True)
        
        return details
    
    def scrape_venue_year(self, venue: str, year: str, get_details: bool = False) -> List[Dict]:
        """Scrape all papers for a specific venue and year."""
        all_papers = []
        
        # Get all proceedings for this venue/year
        proceedings = self.get_event_proceedings(venue, year)
        
        if not proceedings:
            # Try alternative URL patterns
            alt_urls = [
                f"{BASE_URL}/volumes/{year}.{venue}-long/",
                f"{BASE_URL}/volumes/{year}.{venue}-short/",
                f"{BASE_URL}/volumes/{year}.{venue}-main/",
            ]
            for alt_url in alt_urls:
                papers = self.get_volume_papers(alt_url)
                if papers:
                    all_papers.extend(papers)
        else:
            for proc_url in tqdm(proceedings, desc=f"Processing {venue}-{year}"):
                papers = self.get_volume_papers(proc_url)
                all_papers.extend(papers)
                time.sleep(0.5)  # Be polite to the server
        
        # Optionally get detailed info for each paper
        if get_details and all_papers:
            logger.info(f"Fetching details for {len(all_papers)} papers...")
            for paper in tqdm(all_papers, desc="Fetching paper details"):
                if paper.get('url'):
                    details = self.get_paper_details(paper['url'])
                    paper.update(details)
                    time.sleep(0.3)
        
        return all_papers
    
    def scrape_all(self, venues: List[str] = None, years: List[str] = None, 
                   get_details: bool = False) -> pd.DataFrame:
        """Scrape papers from all specified venues and years."""
        if venues is None:
            venues = list(ACL_VENUES.keys())
        if years is None:
            years = YEARS
        
        all_papers = []
        
        for venue in venues:
            for year in years:
                logger.info(f"Scraping {venue.upper()} {year}...")
                papers = self.scrape_venue_year(venue, year, get_details)
                all_papers.extend(papers)
                logger.info(f"Found {len(papers)} papers for {venue.upper()} {year}")
        
        df = pd.DataFrame(all_papers)
        return df
    
    def save_results(self, df: pd.DataFrame, filename: str = "acl_papers"):
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
        
        # Save summary statistics
        summary = {
            'total_papers': len(df),
            'by_venue': df['venue'].value_counts().to_dict() if 'venue' in df.columns else {},
            'by_year': df['year'].value_counts().to_dict() if 'year' in df.columns else {},
            'scraped_at': datetime.now().isoformat(),
        }
        
        summary_path = os.path.join(self.output_dir, f"{filename}_summary.json")
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved summary to {summary_path}")


def main():
    """Main function to run the scraper."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Scrape ACL Anthology papers')
    parser.add_argument('--venues', nargs='+', default=['acl', 'naacl', 'emnlp'],
                        help='Venues to scrape (default: acl naacl emnlp)')
    parser.add_argument('--years', nargs='+', default=['2023', '2024', '2025'],
                        help='Years to scrape (default: 2023 2024 2025)')
    parser.add_argument('--output', '-o', default='data',
                        help='Output directory (default: data)')
    parser.add_argument('--details', action='store_true',
                        help='Fetch detailed info (abstract, PDF URL) for each paper')
    parser.add_argument('--filename', default='acl_papers',
                        help='Output filename prefix (default: acl_papers)')
    
    args = parser.parse_args()
    
    logger.info("Starting ACL Paper Scraper")
    logger.info(f"Venues: {args.venues}")
    logger.info(f"Years: {args.years}")
    
    scraper = ACLScraper(output_dir=args.output)
    df = scraper.scrape_all(
        venues=args.venues,
        years=args.years,
        get_details=args.details
    )
    
    if not df.empty:
        scraper.save_results(df, filename=args.filename)
        print(f"\n{'='*60}")
        print(f"Scraping complete!")
        print(f"Total papers: {len(df)}")
        if 'venue' in df.columns:
            print(f"\nPapers by venue:")
            print(df['venue'].value_counts().to_string())
        if 'year' in df.columns:
            print(f"\nPapers by year:")
            print(df['year'].value_counts().to_string())
    else:
        print("No papers found.")


if __name__ == "__main__":
    main()

