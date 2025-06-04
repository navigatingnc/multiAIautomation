#!/usr/bin/env python3
"""
Google Trends data collection script for market research tool.
This script collects trending topics and related queries from Google Trends.
"""

import os
import json
import time
import pandas as pd
from pytrends.request import TrendReq
from datetime import datetime

# Setup output directory
OUTPUT_DIR = '../data/google_trends'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def setup_pytrends():
    """Initialize the pytrends API with appropriate parameters."""
    print("Setting up Google Trends API connection...")
    # Fixed initialization to avoid method_whitelist error
    return TrendReq(hl='en-US', tz=360, timeout=(10, 25), retries=2, backoff_factor=0.1, 
                   requests_args={'headers': {'User-Agent': 'Mozilla/5.0'}})

def get_trending_searches(pytrends, geo='US'):
    """Get daily and real-time trending searches."""
    print(f"Getting trending searches for {geo}...")
    
    # Daily trending searches
    try:
        daily_trends = pytrends.trending_searches(pn=geo)
        daily_trends_file = os.path.join(OUTPUT_DIR, f'daily_trends_{geo}_{datetime.now().strftime("%Y%m%d")}.csv')
        daily_trends.to_csv(daily_trends_file)
        print(f"Daily trends saved to {daily_trends_file}")
    except Exception as e:
        print(f"Error getting daily trends: {e}")
        daily_trends = pd.DataFrame()
    
    # Real-time trending searches
    try:
        realtime_trends = pytrends.realtime_trending_searches(pn=geo)
        realtime_trends_file = os.path.join(OUTPUT_DIR, f'realtime_trends_{geo}_{datetime.now().strftime("%Y%m%d")}.csv')
        realtime_trends.to_csv(realtime_trends_file)
        print(f"Real-time trends saved to {realtime_trends_file}")
    except Exception as e:
        print(f"Error getting real-time trends: {e}")
        realtime_trends = pd.DataFrame()
    
    return daily_trends, realtime_trends

def explore_categories(pytrends):
    """Get category suggestions for market research."""
    print("Exploring Google Trends categories...")
    
    # List of broad categories to explore
    categories = [
        "Business & Industrial", 
        "Health", 
        "Science", 
        "Technology", 
        "Finance",
        "Food & Drink",
        "Home & Garden",
        "Travel",
        "Education"
    ]
    
    category_data = {}
    
    for category in categories:
        try:
            # Get category suggestions
            suggestions = pytrends.categories()
            
            # Find the category ID
            category_id = None
            for cat_id, cat_name in suggestions.items():
                if category.lower() in cat_name.lower():
                    category_id = cat_id
                    break
            
            if category_id:
                # Get rising topics in this category
                pytrends.build_payload(kw_list=[category], cat=category_id, timeframe='today 3-m')
                related_topics = pytrends.related_topics()
                related_queries = pytrends.related_queries()
                
                category_data[category] = {
                    'id': category_id,
                    'related_topics': related_topics,
                    'related_queries': related_queries
                }
                
                # Save category data
                with open(os.path.join(OUTPUT_DIR, f'category_{category.replace(" & ", "_").replace(" ", "_").lower()}_{datetime.now().strftime("%Y%m%d")}.json'), 'w') as f:
                    # Convert DataFrame to dict for JSON serialization
                    category_json = {
                        'id': category_id,
                        'related_queries': {k: {inner_k: v.to_dict() if isinstance(v, pd.DataFrame) else None 
                                              for inner_k, v in inner_v.items()}
                                          for k, inner_v in related_queries.items()}
                    }
                    json.dump(category_json, f)
                
                print(f"Saved data for category: {category}")
            else:
                print(f"Could not find category ID for: {category}")
                
        except Exception as e:
            print(f"Error exploring category {category}: {e}")
    
    return category_data

def analyze_interest_over_time(pytrends, keywords):
    """Analyze interest over time for specific keywords."""
    print(f"Analyzing interest over time for keywords: {keywords}")
    
    timeframes = ['today 3-m', 'today 12-m', 'today 5-y']
    
    for timeframe in timeframes:
        try:
            pytrends.build_payload(keywords, timeframe=timeframe)
            interest_over_time = pytrends.interest_over_time()
            
            if not interest_over_time.empty:
                filename = f'interest_over_time_{"-".join(keywords)}_{timeframe.replace(" ", "_")}_{datetime.now().strftime("%Y%m%d")}.csv'
                interest_over_time.to_csv(os.path.join(OUTPUT_DIR, filename))
                print(f"Saved interest over time data for {timeframe} to {filename}")
        except Exception as e:
            print(f"Error analyzing interest over time for {timeframe}: {e}")

def analyze_interest_by_region(pytrends, keywords):
    """Analyze interest by region for specific keywords."""
    print(f"Analyzing interest by region for keywords: {keywords}")
    
    try:
        pytrends.build_payload(keywords, timeframe='today 12-m')
        
        # Interest by region
        interest_by_region = pytrends.interest_by_region(resolution='COUNTRY')
        if not interest_by_region.empty:
            filename = f'interest_by_region_{"-".join(keywords)}_{datetime.now().strftime("%Y%m%d")}.csv'
            interest_by_region.to_csv(os.path.join(OUTPUT_DIR, filename))
            print(f"Saved interest by region data to {filename}")
            
        # Interest by US region
        pytrends.build_payload(keywords, geo='US', timeframe='today 12-m')
        interest_by_us_region = pytrends.interest_by_region(resolution='REGION')
        if not interest_by_us_region.empty:
            filename = f'interest_by_us_region_{"-".join(keywords)}_{datetime.now().strftime("%Y%m%d")}.csv'
            interest_by_us_region.to_csv(os.path.join(OUTPUT_DIR, filename))
            print(f"Saved interest by US region data to {filename}")
            
    except Exception as e:
        print(f"Error analyzing interest by region: {e}")

def find_emerging_markets(pytrends):
    """Find potentially emerging markets based on rising queries."""
    print("Finding potentially emerging markets...")
    
    # Keywords that might indicate emerging markets
    market_indicators = [
        "startup trends", 
        "emerging industry", 
        "growing market", 
        "new technology",
        "market gap",
        "underserved market",
        "market opportunity",
        "industry disruption",
        "innovation trends"
    ]
    
    emerging_markets = {}
    
    for indicator in market_indicators:
        try:
            pytrends.build_payload([indicator], timeframe='today 12-m')
            related_queries = pytrends.related_queries()
            
            if indicator in related_queries and related_queries[indicator]['rising'] is not None:
                emerging_markets[indicator] = related_queries[indicator]['rising'].to_dict()
                
                # Save to file
                filename = f'emerging_markets_{indicator.replace(" ", "_")}_{datetime.now().strftime("%Y%m%d")}.csv'
                related_queries[indicator]['rising'].to_csv(os.path.join(OUTPUT_DIR, filename))
                print(f"Saved emerging markets data for '{indicator}' to {filename}")
                
        except Exception as e:
            print(f"Error finding emerging markets for {indicator}: {e}")
    
    # Save consolidated results
    with open(os.path.join(OUTPUT_DIR, f'emerging_markets_consolidated_{datetime.now().strftime("%Y%m%d")}.json'), 'w') as f:
        json.dump(emerging_markets, f)
    
    return emerging_markets

def main():
    """Main function to run Google Trends analysis."""
    print("Starting Google Trends data collection...")
    
    # Setup pytrends
    pytrends = setup_pytrends()
    
    # Get trending searches
    daily_trends, realtime_trends = get_trending_searches(pytrends)
    
    # Explore categories
    category_data = explore_categories(pytrends)
    
    # Analyze specific market sectors
    market_sectors = [
        ["renewable energy", "sustainable products"],
        ["telemedicine", "digital health"],
        ["remote work", "collaboration tools"],
        ["ai services", "machine learning"],
        ["elder care", "aging population"],
        ["mental health", "wellness"],
        ["food delivery", "meal kits"],
        ["online education", "e-learning"]
    ]
    
    for sector in market_sectors:
        analyze_interest_over_time(pytrends, sector)
        analyze_interest_by_region(pytrends, sector)
        time.sleep(1)  # Avoid rate limiting
    
    # Find emerging markets
    emerging_markets = find_emerging_markets(pytrends)
    
    print("Google Trends data collection completed.")

if __name__ == "__main__":
    main()
