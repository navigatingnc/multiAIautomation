#!/usr/bin/env python3
"""
Reddit data collection script for market research tool.
This script collects trending topics and discussions from Reddit using PMAW.
"""

import os
import json
import time
import pandas as pd
from pmaw import PushshiftAPI
from datetime import datetime, timedelta
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import Counter

# Download NLTK resources
nltk.download('vader_lexicon', quiet=True)

# Setup output directory
OUTPUT_DIR = '../data/reddit'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def setup_pmaw():
    """Initialize the PMAW API."""
    print("Setting up PMAW API connection...")
    return PushshiftAPI()

def get_subreddit_posts(api, subreddit, days_back=30, limit=500):
    """Get recent posts from a specific subreddit."""
    print(f"Getting posts from r/{subreddit} for the past {days_back} days...")
    
    # Calculate start timestamp
    start_time = int((datetime.now() - timedelta(days=days_back)).timestamp())
    
    try:
        # Get submissions
        submissions = api.search_submissions(subreddit=subreddit, 
                                           after=start_time,
                                           limit=limit)
        
        # Convert to DataFrame
        submissions_df = pd.DataFrame(submissions)
        
        if not submissions_df.empty:
            # Save to file
            filename = f'submissions_{subreddit}_{datetime.now().strftime("%Y%m%d")}.csv'
            submissions_df.to_csv(os.path.join(OUTPUT_DIR, filename))
            print(f"Saved {len(submissions_df)} submissions from r/{subreddit} to {filename}")
        else:
            print(f"No submissions found for r/{subreddit}")
            
        return submissions_df
    
    except Exception as e:
        print(f"Error getting posts from r/{subreddit}: {e}")
        return pd.DataFrame()

def get_keyword_posts(api, keywords, days_back=30, limit=500):
    """Get recent posts containing specific keywords."""
    print(f"Getting posts containing keywords: {keywords} for the past {days_back} days...")
    
    # Calculate start timestamp
    start_time = int((datetime.now() - timedelta(days=days_back)).timestamp())
    
    all_submissions = []
    
    for keyword in keywords:
        try:
            # Get submissions
            submissions = api.search_submissions(q=keyword, 
                                               after=start_time,
                                               limit=limit)
            
            # Convert to list and add keyword info
            submissions_list = list(submissions)
            for submission in submissions_list:
                submission['search_keyword'] = keyword
                
            all_submissions.extend(submissions_list)
            
            print(f"Found {len(submissions_list)} submissions for keyword '{keyword}'")
            time.sleep(1)  # Avoid rate limiting
            
        except Exception as e:
            print(f"Error getting posts for keyword '{keyword}': {e}")
    
    # Convert to DataFrame
    if all_submissions:
        submissions_df = pd.DataFrame(all_submissions)
        
        # Save to file
        keywords_str = "_".join(keywords).replace(" ", "_")
        filename = f'keyword_submissions_{keywords_str}_{datetime.now().strftime("%Y%m%d")}.csv'
        submissions_df.to_csv(os.path.join(OUTPUT_DIR, filename))
        print(f"Saved {len(submissions_df)} keyword submissions to {filename}")
        
        return submissions_df
    else:
        print("No submissions found for the specified keywords")
        return pd.DataFrame()

def analyze_sentiment(text):
    """Analyze sentiment of text using NLTK's VADER."""
    if not text or pd.isna(text):
        return {'compound': 0, 'pos': 0, 'neu': 0, 'neg': 0}
    
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(text)

def extract_topics(submissions_df):
    """Extract common topics and themes from submissions."""
    if submissions_df.empty or 'title' not in submissions_df.columns:
        return {}
    
    # Combine titles and selftext for analysis
    all_text = ""
    for _, row in submissions_df.iterrows():
        all_text += " " + str(row.get('title', ''))
        selftext = row.get('selftext', '')
        if selftext and not pd.isna(selftext):
            all_text += " " + selftext
    
    # Simple word frequency analysis (could be enhanced with NLP techniques)
    words = all_text.lower().split()
    # Filter out common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 
                 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'about', 'like', 
                 'through', 'over', 'before', 'between', 'after', 'since', 'without', 
                 'under', 'of', 'that', 'this', 'these', 'those', 'it', 'i', 'we', 
                 'they', 'he', 'she', 'you', 'me', 'him', 'her', 'them', 'my', 'your', 
                 'his', 'our', 'their'}
    filtered_words = [word for word in words if word not in stop_words and len(word) > 3]
    
    # Count word frequencies
    word_counts = Counter(filtered_words)
    
    # Return top words
    return dict(word_counts.most_common(50))

def analyze_subreddit_data(submissions_df, subreddit):
    """Analyze data from a subreddit."""
    if submissions_df.empty:
        return {}
    
    analysis = {
        'subreddit': subreddit,
        'post_count': len(submissions_df),
        'date_range': {
            'min': submissions_df['created_utc'].min() if 'created_utc' in submissions_df.columns else None,
            'max': submissions_df['created_utc'].max() if 'created_utc' in submissions_df.columns else None
        },
        'common_topics': extract_topics(submissions_df)
    }
    
    # Add sentiment analysis if text columns exist
    if 'title' in submissions_df.columns:
        # Apply sentiment analysis to titles
        submissions_df['title_sentiment'] = submissions_df['title'].apply(analyze_sentiment)
        
        # Extract compound sentiment scores
        title_sentiments = [s.get('compound', 0) for s in submissions_df['title_sentiment'] if s]
        
        if title_sentiments:
            analysis['sentiment'] = {
                'average_compound': sum(title_sentiments) / len(title_sentiments),
                'positive_percentage': sum(1 for s in title_sentiments if s > 0.05) / len(title_sentiments),
                'negative_percentage': sum(1 for s in title_sentiments if s < -0.05) / len(title_sentiments),
                'neutral_percentage': sum(1 for s in title_sentiments if -0.05 <= s <= 0.05) / len(title_sentiments)
            }
    
    # Save analysis to file
    analysis_file = os.path.join(OUTPUT_DIR, f'analysis_{subreddit}_{datetime.now().strftime("%Y%m%d")}.json')
    with open(analysis_file, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"Saved analysis for r/{subreddit} to {analysis_file}")
    
    return analysis

def main():
    """Main function to run Reddit data collection and analysis."""
    print("Starting Reddit data collection...")
    
    # Setup PMAW
    api = setup_pmaw()
    
    # List of business and market-related subreddits
    business_subreddits = [
        'Entrepreneur', 
        'startups', 
        'smallbusiness',
        'business',
        'marketing',
        'SideProject',
        'investing',
        'technology',
        'futurology',
        'economics'
    ]
    
    # Collect data from business subreddits
    all_subreddit_data = {}
    for subreddit in business_subreddits:
        submissions_df = get_subreddit_posts(api, subreddit, days_back=60)
        if not submissions_df.empty:
            analysis = analyze_subreddit_data(submissions_df, subreddit)
            all_subreddit_data[subreddit] = analysis
        time.sleep(2)  # Avoid rate limiting
    
    # Save consolidated subreddit analysis
    with open(os.path.join(OUTPUT_DIR, f'all_subreddit_analysis_{datetime.now().strftime("%Y%m%d")}.json'), 'w') as f:
        json.dump(all_subreddit_data, f, indent=2)
    
    # Market-related keywords to search across Reddit
    market_keywords = [
        "underserved market",
        "market opportunity",
        "emerging industry",
        "growing market",
        "market gap",
        "industry disruption",
        "unmet needs",
        "market trends",
        "business opportunity",
        "startup idea"
    ]
    
    # Collect posts by keywords
    keyword_submissions = get_keyword_posts(api, market_keywords, days_back=90, limit=300)
    
    # Analyze keyword data if available
    if not keyword_submissions.empty:
        # Group by search keyword
        keyword_groups = keyword_submissions.groupby('search_keyword')
        
        keyword_analysis = {}
        for keyword, group in keyword_groups:
            # Basic analysis for each keyword
            topic_counts = extract_topics(group)
            
            # Calculate average scores
            avg_score = group['score'].mean() if 'score' in group.columns else 0
            
            keyword_analysis[keyword] = {
                'post_count': len(group),
                'average_score': avg_score,
                'common_topics': topic_counts
            }
        
        # Save keyword analysis
        with open(os.path.join(OUTPUT_DIR, f'keyword_analysis_{datetime.now().strftime("%Y%m%d")}.json'), 'w') as f:
            json.dump(keyword_analysis, f, indent=2)
        
        keyword_analysis_file = os.path.join(OUTPUT_DIR, f'keyword_analysis_{datetime.now().strftime("%Y%m%d")}.json')
        print(f"Saved keyword analysis to {keyword_analysis_file}")
    
    print("Reddit data collection completed.")

if __name__ == "__main__":
    main()
