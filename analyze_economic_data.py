#!/usr/bin/env python3
"""
Economic and census data analysis script for market research tool.
This script aggregates and analyzes economic indicators and census data
to identify patterns and potential market opportunities.
"""

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import glob

# Setup directories
DATA_DIR = '../data'
OUTPUT_DIR = '../results'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_economic_indicators():
    """Load economic indicators data from JSON files."""
    print("Loading economic indicators data...")
    
    # Find the most recent economic indicators file
    economic_files = glob.glob(os.path.join(DATA_DIR, 'news', 'economic_indicators_*.json'))
    if not economic_files:
        print("No economic indicators files found.")
        return None
    
    # Sort by date (newest first)
    latest_file = sorted(economic_files)[-1]
    print(f"Loading economic data from {latest_file}")
    
    with open(latest_file, 'r') as f:
        economic_data = json.load(f)
    
    return economic_data

def load_news_analysis():
    """Load news analysis data from JSON files."""
    print("Loading news analysis data...")
    
    # Find all news analysis files
    analysis_files = glob.glob(os.path.join(DATA_DIR, 'news', 'analysis_*.json'))
    if not analysis_files:
        print("No news analysis files found.")
        return []
    
    all_analyses = []
    for file in analysis_files:
        with open(file, 'r') as f:
            analysis = json.load(f)
            all_analyses.append(analysis)
    
    print(f"Loaded {len(all_analyses)} news analysis files.")
    return all_analyses

def load_scraped_trends():
    """Load scraped market trends data from JSON files."""
    print("Loading scraped market trends data...")
    
    # Find the most recent scraped trends file
    trend_files = glob.glob(os.path.join(DATA_DIR, 'news', 'scraped_trends_*.json'))
    if not trend_files:
        print("No scraped trends files found.")
        return None
    
    # Sort by date (newest first)
    latest_file = sorted(trend_files)[-1]
    print(f"Loading scraped trends from {latest_file}")
    
    with open(latest_file, 'r') as f:
        trend_data = json.load(f)
    
    return trend_data

def analyze_economic_growth_sectors(economic_data):
    """Analyze economic growth sectors from economic indicators."""
    print("Analyzing economic growth sectors...")
    
    if not economic_data or 'economic_indicators' not in economic_data:
        print("No economic indicators data available for analysis.")
        return {}
    
    # Extract GDP growth data
    gdp_indicator = economic_data['economic_indicators'].get('NY.GDP.MKTP.KD.ZG', {})
    gdp_data = gdp_indicator.get('data', {})
    growth_sectors = gdp_indicator.get('growth_sectors', [])
    
    # Create a DataFrame for GDP growth
    gdp_df = pd.DataFrame(list(gdp_data.items()), columns=['Country', 'GDP_Growth'])
    gdp_df = gdp_df.sort_values('GDP_Growth', ascending=False)
    
    # Create visualization
    plt.figure(figsize=(10, 6))
    sns.barplot(x='GDP_Growth', y='Country', data=gdp_df)
    plt.title('GDP Growth by Country')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'gdp_growth_by_country.png'))
    plt.close()
    
    # Extract investment data
    investment_indicator = economic_data['economic_indicators'].get('NE.GDI.TOTL.ZS', {})
    investment_data = investment_indicator.get('data', {})
    hot_investment_areas = investment_indicator.get('hot_investment_areas', [])
    
    # Create a DataFrame for investment
    investment_df = pd.DataFrame(list(investment_data.items()), columns=['Country', 'Investment_GDP_Ratio'])
    investment_df = investment_df.sort_values('Investment_GDP_Ratio', ascending=False)
    
    # Create visualization
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Investment_GDP_Ratio', y='Country', data=investment_df)
    plt.title('Investment as % of GDP by Country')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'investment_by_country.png'))
    plt.close()
    
    # Combine growth sectors and investment areas
    growth_analysis = {
        'gdp_growth': gdp_df.to_dict(orient='records'),
        'growth_sectors': growth_sectors,
        'investment_data': investment_df.to_dict(orient='records'),
        'hot_investment_areas': hot_investment_areas
    }
    
    # Save analysis
    with open(os.path.join(OUTPUT_DIR, 'economic_growth_analysis.json'), 'w') as f:
        json.dump(growth_analysis, f, indent=2)
    
    return growth_analysis

def analyze_underserved_markets(economic_data):
    """Analyze potentially underserved markets from economic indicators."""
    print("Analyzing potentially underserved markets...")
    
    if not economic_data or 'market_indicators' not in economic_data:
        print("No market indicators data available for analysis.")
        return {}
    
    # Extract underserved markets data
    underserved_markets = economic_data['market_indicators'].get('underserved_markets', {}).get('data', [])
    
    if not underserved_markets:
        print("No underserved markets data available.")
        return {}
    
    # Create a DataFrame for underserved markets
    markets_df = pd.DataFrame(underserved_markets)
    
    # Sort by gap score (highest first)
    markets_df = markets_df.sort_values('gap_score', ascending=False)
    
    # Create visualization
    plt.figure(figsize=(10, 6))
    sns.barplot(x='gap_score', y='market', data=markets_df)
    plt.title('Underserved Markets by Gap Score')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'underserved_markets_gap_score.png'))
    plt.close()
    
    # Count barriers to entry
    all_barriers = []
    for market in underserved_markets:
        all_barriers.extend(market.get('barriers', []))
    
    barrier_counts = pd.Series(all_barriers).value_counts()
    
    # Create visualization for barriers
    plt.figure(figsize=(10, 6))
    barrier_counts.plot(kind='bar')
    plt.title('Common Barriers to Entry in Underserved Markets')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'underserved_markets_barriers.png'))
    plt.close()
    
    # Analyze by growth potential
    growth_potential_counts = markets_df['growth_potential'].value_counts()
    
    # Create visualization for growth potential
    plt.figure(figsize=(8, 8))
    plt.pie(growth_potential_counts, labels=growth_potential_counts.index, autopct='%1.1f%%')
    plt.title('Underserved Markets by Growth Potential')
    plt.savefig(os.path.join(OUTPUT_DIR, 'underserved_markets_growth_potential.png'))
    plt.close()
    
    # Save analysis
    underserved_analysis = {
        'markets': markets_df.to_dict(orient='records'),
        'barrier_counts': barrier_counts.to_dict(),
        'growth_potential_distribution': growth_potential_counts.to_dict()
    }
    
    with open(os.path.join(OUTPUT_DIR, 'underserved_markets_analysis.json'), 'w') as f:
        json.dump(underserved_analysis, f, indent=2)
    
    return underserved_analysis

def analyze_emerging_technologies(economic_data):
    """Analyze emerging technologies with market potential."""
    print("Analyzing emerging technologies...")
    
    if not economic_data or 'market_indicators' not in economic_data:
        print("No market indicators data available for analysis.")
        return {}
    
    # Extract emerging technologies data
    emerging_tech = economic_data['market_indicators'].get('emerging_technologies', {}).get('data', [])
    
    if not emerging_tech:
        print("No emerging technologies data available.")
        return {}
    
    # Create a DataFrame for emerging technologies
    tech_df = pd.DataFrame(emerging_tech)
    
    # Sort by market readiness (highest first)
    tech_df = tech_df.sort_values('market_readiness', ascending=False)
    
    # Create visualization
    plt.figure(figsize=(10, 6))
    sns.barplot(x='market_readiness', y='technology', data=tech_df)
    plt.title('Emerging Technologies by Market Readiness')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'emerging_technologies_readiness.png'))
    plt.close()
    
    # Count adoption barriers
    all_barriers = []
    for tech in emerging_tech:
        all_barriers.extend(tech.get('adoption_barriers', []))
    
    barrier_counts = pd.Series(all_barriers).value_counts()
    
    # Create visualization for barriers
    plt.figure(figsize=(10, 6))
    barrier_counts.plot(kind='bar')
    plt.title('Common Adoption Barriers for Emerging Technologies')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'emerging_technologies_barriers.png'))
    plt.close()
    
    # Analyze by investment trend
    investment_trend_counts = tech_df['investment_trend'].value_counts()
    
    # Create visualization for investment trends
    plt.figure(figsize=(8, 8))
    plt.pie(investment_trend_counts, labels=investment_trend_counts.index, autopct='%1.1f%%')
    plt.title('Emerging Technologies by Investment Trend')
    plt.savefig(os.path.join(OUTPUT_DIR, 'emerging_technologies_investment.png'))
    plt.close()
    
    # Save analysis
    tech_analysis = {
        'technologies': tech_df.to_dict(orient='records'),
        'barrier_counts': barrier_counts.to_dict(),
        'investment_trend_distribution': investment_trend_counts.to_dict()
    }
    
    with open(os.path.join(OUTPUT_DIR, 'emerging_technologies_analysis.json'), 'w') as f:
        json.dump(tech_analysis, f, indent=2)
    
    return tech_analysis

def analyze_news_sentiment(news_analyses):
    """Analyze sentiment from news analyses."""
    print("Analyzing news sentiment...")
    
    if not news_analyses:
        print("No news analyses available.")
        return {}
    
    # Extract sentiment data from all analyses
    sentiment_data = []
    for analysis in news_analyses:
        query = analysis.get('query', 'unknown')
        sentiment = analysis.get('sentiment', {})
        if sentiment:
            sentiment_data.append({
                'query': query,
                'average_compound': sentiment.get('average_compound', 0),
                'positive_percentage': sentiment.get('positive_percentage', 0),
                'negative_percentage': sentiment.get('negative_percentage', 0),
                'neutral_percentage': sentiment.get('neutral_percentage', 0)
            })
    
    if not sentiment_data:
        print("No sentiment data available in news analyses.")
        return {}
    
    # Create DataFrame
    sentiment_df = pd.DataFrame(sentiment_data)
    
    # Sort by average compound sentiment (highest first)
    sentiment_df = sentiment_df.sort_values('average_compound', ascending=False)
    
    # Create visualization
    plt.figure(figsize=(12, 8))
    sns.barplot(x='average_compound', y='query', data=sentiment_df)
    plt.title('News Sentiment by Market Query')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'news_sentiment_by_query.png'))
    plt.close()
    
    # Create stacked bar chart for sentiment distribution
    plt.figure(figsize=(12, 8))
    sentiment_df_plot = sentiment_df.set_index('query')
    sentiment_distribution = sentiment_df_plot[['positive_percentage', 'neutral_percentage', 'negative_percentage']]
    sentiment_distribution.plot(kind='bar', stacked=True)
    plt.title('Sentiment Distribution by Market Query')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'sentiment_distribution_by_query.png'))
    plt.close()
    
    # Save analysis
    sentiment_analysis = {
        'sentiment_by_query': sentiment_df.to_dict(orient='records'),
        'highest_sentiment_markets': sentiment_df.head(5)['query'].tolist(),
        'lowest_sentiment_markets': sentiment_df.tail(5)['query'].tolist()
    }
    
    with open(os.path.join(OUTPUT_DIR, 'news_sentiment_analysis.json'), 'w') as f:
        json.dump(sentiment_analysis, f, indent=2)
    
    return sentiment_analysis

def analyze_scraped_trends(trend_data):
    """Analyze scraped market trends data."""
    print("Analyzing scraped market trends...")
    
    if not trend_data or 'underserved_market_mentions' not in trend_data:
        print("No underserved market mentions available in scraped data.")
        return {}
    
    # Extract underserved market mentions
    market_mentions = trend_data.get('underserved_market_mentions', [])
    
    if not market_mentions:
        print("No market mentions data available.")
        return {}
    
    # Create DataFrame
    mentions_df = pd.DataFrame(market_mentions)
    
    # Sort by mention count (highest first)
    mentions_df = mentions_df.sort_values('mention_count', ascending=False)
    
    # Create visualization for mention counts
    plt.figure(figsize=(10, 6))
    sns.barplot(x='mention_count', y='market', data=mentions_df)
    plt.title('Underserved Markets by Mention Count')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'market_mentions_count.png'))
    plt.close()
    
    # Create visualization for sentiment scores
    plt.figure(figsize=(10, 6))
    sns.barplot(x='sentiment_score', y='market', data=mentions_df)
    plt.title('Underserved Markets by Sentiment Score')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'market_mentions_sentiment.png'))
    plt.close()
    
    # Count growth indicators
    all_indicators = []
    for mention in market_mentions:
        all_indicators.extend(mention.get('growth_indicators', []))
    
    indicator_counts = pd.Series(all_indicators).value_counts()
    
    # Create visualization for growth indicators
    plt.figure(figsize=(10, 6))
    indicator_counts.plot(kind='bar')
    plt.title('Common Growth Indicators for Underserved Markets')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'market_growth_indicators.png'))
    plt.close()
    
    # Save analysis
    mentions_analysis = {
        'market_mentions': mentions_df.to_dict(orient='records'),
        'top_mentioned_markets': mentions_df.head(5)['market'].tolist(),
        'growth_indicator_counts': indicator_counts.to_dict()
    }
    
    with open(os.path.join(OUTPUT_DIR, 'market_mentions_analysis.json'), 'w') as f:
        json.dump(mentions_analysis, f, indent=2)
    
    return mentions_analysis

def analyze_website_trends(trend_data):
    """Analyze trends from website scraping."""
    print("Analyzing website trends...")
    
    if not trend_data or 'trends' not in trend_data:
        print("No website trends available in scraped data.")
        return {}
    
    # Extract website trends
    website_trends = trend_data.get('trends', [])
    
    if not website_trends:
        print("No website trends data available.")
        return {}
    
    # Flatten trends from all websites
    all_trends = []
    for website in website_trends:
        source = website.get('source', 'Unknown')
        for trend in website.get('trends', []):
            trend_copy = trend.copy()
            trend_copy['source'] = source
            all_trends.append(trend_copy)
    
    # Create DataFrame
    trends_df = pd.DataFrame(all_trends)
    
    # Count sectors
    all_sectors = []
    for trend in all_trends:
        all_sectors.extend(trend.get('sectors', []))
    
    sector_counts = pd.Series(all_sectors).value_counts()
    
    # Create visualization for sectors
    plt.figure(figsize=(12, 8))
    sector_counts.plot(kind='bar')
    plt.title('Trending Sectors from Website Analysis')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'trending_sectors.png'))
    plt.close()
    
    # Count sentiment categories
    sentiment_counts = trends_df['sentiment'].value_counts()
    
    # Create visualization for sentiment
    plt.figure(figsize=(8, 8))
    plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%')
    plt.title('Trend Sentiment Distribution')
    plt.savefig(os.path.join(OUTPUT_DIR, 'trend_sentiment_distribution.png'))
    plt.close()
    
    # Save analysis
    website_analysis = {
        'trends': trends_df.to_dict(orient='records'),
        'sector_counts': sector_counts.to_dict(),
        'sentiment_distribution': sentiment_counts.to_dict(),
        'top_sectors': sector_counts.head(10).index.tolist()
    }
    
    with open(os.path.join(OUTPUT_DIR, 'website_trends_analysis.json'), 'w') as f:
        json.dump(website_analysis, f, indent=2)
    
    return website_analysis

def main():
    """Main function to run economic and census data analysis."""
    print("Starting economic and census data analysis...")
    
    # Load data
    economic_data = load_economic_indicators()
    news_analyses = load_news_analysis()
    scraped_trends = load_scraped_trends()
    
    # Analyze economic growth sectors
    growth_analysis = analyze_economic_growth_sectors(economic_data)
    
    # Analyze underserved markets
    underserved_analysis = analyze_underserved_markets(economic_data)
    
    # Analyze emerging technologies
    tech_analysis = analyze_emerging_technologies(economic_data)
    
    # Analyze news sentiment
    sentiment_analysis = analyze_news_sentiment(news_analyses)
    
    # Analyze scraped trends
    mentions_analysis = analyze_scraped_trends(scraped_trends)
    
    # Analyze website trends
    website_analysis = analyze_website_trends(scraped_trends)
    
    # Combine all analyses
    combined_analysis = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'economic_growth': growth_analysis,
        'underserved_markets': underserved_analysis,
        'emerging_technologies': tech_analysis,
        'news_sentiment': sentiment_analysis,
        'market_mentions': mentions_analysis,
        'website_trends': website_analysis
    }
    
    # Save combined analysis
    with open(os.path.join(OUTPUT_DIR, 'combined_market_analysis.json'), 'w') as f:
        json.dump(combined_analysis, f, indent=2)
    
    print("Economic and census data analysis completed.")
    print(f"Results saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
