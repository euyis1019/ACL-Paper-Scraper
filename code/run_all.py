#!/usr/bin/env python3
"""
Combined ACL Paper Scraper
==========================
Runs both ACL Anthology and OpenReview scrapers to collect comprehensive paper data.
"""

import os
import sys
import pandas as pd
from datetime import datetime
import json
import logging

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from acl_scraper import ACLScraper
from openreview_scraper import OpenReviewScraper

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Run all scrapers and combine results."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run all ACL paper scrapers')
    parser.add_argument('--years', nargs='+', default=['2023', '2024', '2025'],
                        help='Years to scrape')
    parser.add_argument('--venues', nargs='+', default=['acl', 'naacl', 'emnlp'],
                        help='ACL venues to scrape')
    parser.add_argument('--output', '-o', default='data',
                        help='Output directory')
    parser.add_argument('--details', action='store_true',
                        help='Fetch detailed paper info (slower)')
    parser.add_argument('--skip-anthology', action='store_true',
                        help='Skip ACL Anthology scraping')
    parser.add_argument('--skip-openreview', action='store_true',
                        help='Skip OpenReview scraping')
    
    args = parser.parse_args()
    
    os.makedirs(args.output, exist_ok=True)
    
    all_dfs = []
    
    # 1. Scrape ACL Anthology
    if not args.skip_anthology:
        print("\n" + "="*60)
        print("STEP 1: Scraping ACL Anthology (accepted papers)")
        print("="*60)
        
        try:
            acl_scraper = ACLScraper(output_dir=args.output)
            df_anthology = acl_scraper.scrape_all(
                venues=args.venues,
                years=args.years,
                get_details=args.details
            )
            
            if not df_anthology.empty:
                df_anthology['source'] = 'acl_anthology'
                acl_scraper.save_results(df_anthology, filename='acl_anthology_papers')
                all_dfs.append(df_anthology)
                print(f"Found {len(df_anthology)} papers from ACL Anthology")
        except Exception as e:
            logger.error(f"Error scraping ACL Anthology: {e}")
    
    # 2. Scrape OpenReview
    if not args.skip_openreview:
        print("\n" + "="*60)
        print("STEP 2: Scraping OpenReview (may include rejected papers)")
        print("="*60)
        
        try:
            openreview_scraper = OpenReviewScraper(output_dir=args.output)
            df_openreview = openreview_scraper.scrape_arr_cycles(years=args.years)
            
            if not df_openreview.empty:
                df_openreview['source'] = 'openreview'
                openreview_scraper.save_results(df_openreview, filename='openreview_papers')
                all_dfs.append(df_openreview)
                print(f"Found {len(df_openreview)} papers from OpenReview")
        except Exception as e:
            logger.error(f"Error scraping OpenReview: {e}")
    
    # 3. Combine and deduplicate
    print("\n" + "="*60)
    print("STEP 3: Combining and deduplicating results")
    print("="*60)
    
    if all_dfs:
        df_combined = pd.concat(all_dfs, ignore_index=True)
        
        # Normalize titles for deduplication
        df_combined['title_normalized'] = df_combined['title'].str.lower().str.strip()
        df_combined = df_combined.drop_duplicates(subset=['title_normalized'], keep='first')
        df_combined = df_combined.drop(columns=['title_normalized'])
        
        # Save combined results
        csv_path = os.path.join(args.output, 'all_acl_papers.csv')
        df_combined.to_csv(csv_path, index=False, encoding='utf-8')
        
        json_path = os.path.join(args.output, 'all_acl_papers.json')
        df_combined.to_json(json_path, orient='records', indent=2, force_ascii=False)
        
        # Generate comprehensive summary
        summary = {
            'total_papers': len(df_combined),
            'by_source': df_combined['source'].value_counts().to_dict() if 'source' in df_combined.columns else {},
            'by_venue': df_combined['venue'].value_counts().to_dict() if 'venue' in df_combined.columns else {},
            'by_year': df_combined['year'].value_counts().to_dict() if 'year' in df_combined.columns else {},
            'by_status': df_combined['status'].value_counts().to_dict() if 'status' in df_combined.columns else {},
            'accepted_count': len(df_combined[df_combined['status'] == 'accepted']) if 'status' in df_combined.columns else 0,
            'rejected_count': len(df_combined[df_combined['status'] == 'rejected']) if 'status' in df_combined.columns else 0,
            'scraped_at': datetime.now().isoformat(),
            'years_scraped': args.years,
            'venues_scraped': args.venues,
        }
        
        summary_path = os.path.join(args.output, 'all_papers_summary.json')
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        # Print final summary
        print("\n" + "="*60)
        print("SCRAPING COMPLETE!")
        print("="*60)
        print(f"\nTotal unique papers: {len(df_combined)}")
        
        if 'source' in df_combined.columns:
            print(f"\nBy Source:")
            print(df_combined['source'].value_counts().to_string())
        
        if 'status' in df_combined.columns:
            print(f"\nBy Status:")
            print(df_combined['status'].value_counts().to_string())
        
        if 'venue' in df_combined.columns:
            print(f"\nBy Venue (top 10):")
            print(df_combined['venue'].value_counts().head(10).to_string())
        
        if 'year' in df_combined.columns:
            print(f"\nBy Year:")
            print(df_combined['year'].value_counts().to_string())
        
        print(f"\nOutput files saved to: {os.path.abspath(args.output)}/")
        print(f"  - all_acl_papers.csv")
        print(f"  - all_acl_papers.json")
        print(f"  - all_papers_summary.json")
    else:
        print("No papers found from any source.")


if __name__ == "__main__":
    main()

