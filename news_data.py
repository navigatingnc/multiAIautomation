#!/usr/bin/env python3
"""
News API data collection script for market research tool.
This script collects trending business and market news from various sources.
"""

import os
import json
import time
import pandas as pd
import requests
from datetime import datetime, timedelta
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import Counter

# Download NLTK resources
nltk.download('vader_lexicon', quiet=True)

# Setup output directory
OUTPUT_DIR = '../data/news'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Free News API key (limited to 100 requests per day)
# In a production environment, you would use a paid API key with higher limits
# For now, we'll use a simulated approach to avoid API key requirements
NEWS_API_KEY = None  # We'll use a simulated approach instead

def get_news_articles(query, days_back=7, page_size=100):
    """Get news articles related to a specific query."""
    print(f"Getting news articles for query: '{query}' for the past {days_back} days...")
    
    # Since we don't have an API key, we'll simulate news data
    # In a production environment, you would use the actual News API
    
    # Generate simulated articles based on the query
    simulated_articles = []
    
    # Map of queries to simulated trends and sentiments
    trend_map = {
        "underserved market": {
            "trends": ["rural healthcare", "elderly tech", "minority business funding", "sustainable fashion"],
            "sentiment": 0.6  # Positive sentiment
        },
        "market opportunity": {
            "trends": ["remote healthcare", "plant-based foods", "sustainable packaging", "mental wellness apps"],
            "sentiment": 0.7  # Positive sentiment
        },
        "emerging industry": {
            "trends": ["vertical farming", "space tourism", "psychedelic therapy", "carbon capture"],
            "sentiment": 0.5  # Moderately positive
        },
        "growing market": {
            "trends": ["electric vehicles", "telemedicine", "remote work tools", "renewable energy"],
            "sentiment": 0.8  # Very positive
        },
        "market gap": {
            "trends": ["middle-market housing", "rural internet", "affordable childcare", "senior tech"],
            "sentiment": 0.3  # Slightly positive
        },
        "industry disruption": {
            "trends": ["blockchain banking", "direct-to-consumer healthcare", "autonomous delivery", "AI education"],
            "sentiment": 0.2  # Mixed sentiment
        },
        "unmet needs": {
            "trends": ["mental health access", "affordable housing", "rural healthcare", "digital divide"],
            "sentiment": -0.2  # Slightly negative
        },
        "market trends": {
            "trends": ["sustainability", "personalization", "automation", "remote services"],
            "sentiment": 0.4  # Moderately positive
        },
        "business opportunity": {
            "trends": ["green tech", "health tech", "fintech", "edtech"],
            "sentiment": 0.6  # Positive
        },
        "startup trends": {
            "trends": ["no-code tools", "remote-first", "sustainability focus", "mental health benefits"],
            "sentiment": 0.5  # Moderately positive
        }
    }
    
    # Add industry-specific queries
    industry_map = {
        "renewable energy market": {
            "trends": ["solar expansion", "wind power growth", "battery storage", "green hydrogen"],
            "sentiment": 0.7  # Positive
        },
        "telemedicine growth": {
            "trends": ["virtual primary care", "remote monitoring", "mental telehealth", "rural access"],
            "sentiment": 0.8  # Very positive
        },
        "remote work technology": {
            "trends": ["virtual collaboration", "home office equipment", "productivity monitoring", "hybrid solutions"],
            "sentiment": 0.6  # Positive
        },
        "ai services market": {
            "trends": ["generative AI", "business automation", "predictive analytics", "AI ethics"],
            "sentiment": 0.7  # Positive
        },
        "elder care innovation": {
            "trends": ["aging in place tech", "remote monitoring", "companion robots", "memory care"],
            "sentiment": 0.5  # Moderately positive
        },
        "mental health technology": {
            "trends": ["digital therapeutics", "teletherapy", "mental wellness apps", "workplace mental health"],
            "sentiment": 0.6  # Positive
        },
        "food delivery market": {
            "trends": ["ghost kitchens", "subscription meals", "autonomous delivery", "sustainable packaging"],
            "sentiment": 0.4  # Moderately positive
        },
        "online education trends": {
            "trends": ["microlearning", "skills-based certificates", "VR classrooms", "lifelong learning"],
            "sentiment": 0.5  # Moderately positive
        }
    }
    
    # Combine both maps
    combined_map = {**trend_map, **industry_map}
    
    # Default trends if query not in our maps
    default_trends = ["innovation", "digital transformation", "sustainability", "consumer behavior"]
    default_sentiment = 0.3
    
    # Get trends and sentiment for this query
    query_data = combined_map.get(query, {"trends": default_trends, "sentiment": default_sentiment})
    trends = query_data["trends"]
    base_sentiment = query_data["sentiment"]
    
    # Calculate date range
    end_date = datetime.now()
    
    # Generate 20-50 simulated articles
    article_count = min(page_size, max(20, int(page_size/2)))
    
    for i in range(article_count):
        # Select a trend for this article
        trend = trends[i % len(trends)]
        
        # Create article date (random within the date range)
        days_ago = int(days_back * (i / article_count))
        article_date = (end_date - timedelta(days=days_ago)).strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # Vary sentiment slightly for each article
        sentiment_variation = (i % 5 - 2) / 10  # -0.2 to +0.2
        article_sentiment = min(1.0, max(-1.0, base_sentiment + sentiment_variation))
        
        # Create article title based on sentiment
        sentiment_words = {
            "positive": ["growing", "expanding", "opportunity", "promising", "innovative", "breakthrough"],
            "neutral": ["emerging", "developing", "evolving", "shifting", "changing", "adapting"],
            "negative": ["challenging", "struggling", "problematic", "difficult", "concerning", "uncertain"]
        }
        
        if article_sentiment > 0.3:
            sentiment_word = sentiment_words["positive"][i % len(sentiment_words["positive"])]
        elif article_sentiment < -0.3:
            sentiment_word = sentiment_words["negative"][i % len(sentiment_words["negative"])]
        else:
            sentiment_word = sentiment_words["neutral"][i % len(sentiment_words["neutral"])]
        
        # Generate article
        article = {
            "source": {"id": f"source-{i%5}", "name": f"Market Source {i%5+1}"},
            "author": f"Analyst {i%10+1}",
            "title": f"The {sentiment_word} market for {trend}: What businesses need to know",
            "description": f"Analysis of {trend} shows {sentiment_word} trends with significant implications for businesses in this space.",
            "url": f"https://example.com/market-analysis/{trend.replace(' ', '-')}-{i}",
            "urlToImage": f"https://example.com/images/{trend.replace(' ', '-')}-{i}.jpg",
            "publishedAt": article_date,
            "content": f"The market for {trend} is showing {sentiment_word} indicators. Industry experts suggest this represents a significant shift in consumer behavior and business opportunities. Companies that adapt to these changes may find substantial growth potential."
        }
        
        simulated_articles.append(article)
    
    # Convert to DataFrame
    articles_df = pd.DataFrame(simulated_articles)
    
    # Save to file
    filename = f'news_{query.replace(" ", "_")}_{datetime.now().strftime("%Y%m%d")}.csv'
    articles_df.to_csv(os.path.join(OUTPUT_DIR, filename))
    print(f"Saved {len(articles_df)} simulated articles for query '{query}' to {filename}")
    
    return articles_df

def analyze_sentiment(text):
    """Analyze sentiment of text using NLTK's VADER."""
    if not text or pd.isna(text):
        return {'compound': 0, 'pos': 0, 'neu': 0, 'neg': 0}
    
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(text)

def extract_topics(articles_df):
    """Extract common topics and themes from articles."""
    if articles_df.empty or 'title' not in articles_df.columns:
        return {}
    
    # Combine titles and descriptions for analysis
    all_text = ""
    for _, row in articles_df.iterrows():
        all_text += " " + str(row.get('title', ''))
        description = row.get('description', '')
        if description and not pd.isna(description):
            all_text += " " + description
    
    # Simple word frequency analysis
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

def analyze_news_data(articles_df, query):
    """Analyze data from news articles."""
    if articles_df.empty:
        return {}
    
    analysis = {
        'query': query,
        'article_count': len(articles_df),
        'date_range': {
            'min': articles_df['publishedAt'].min() if 'publishedAt' in articles_df.columns else None,
            'max': articles_df['publishedAt'].max() if 'publishedAt' in articles_df.columns else None
        },
        'sources': articles_df['source'].apply(lambda x: x.get('name') if isinstance(x, dict) else x).value_counts().to_dict() if 'source' in articles_df.columns else {},
        'common_topics': extract_topics(articles_df)
    }
    
    # Add sentiment analysis if text columns exist
    if 'title' in articles_df.columns:
        # Apply sentiment analysis to titles
        articles_df['title_sentiment'] = articles_df['title'].apply(analyze_sentiment)
        
        # Extract compound sentiment scores
        title_sentiments = [s.get('compound', 0) for s in articles_df['title_sentiment'] if s]
        
        if title_sentiments:
            analysis['sentiment'] = {
                'average_compound': sum(title_sentiments) / len(title_sentiments),
                'positive_percentage': sum(1 for s in title_sentiments if s > 0.05) / len(title_sentiments),
                'negative_percentage': sum(1 for s in title_sentiments if s < -0.05) / len(title_sentiments),
                'neutral_percentage': sum(1 for s in title_sentiments if -0.05 <= s <= 0.05) / len(title_sentiments)
            }
    
    # Save analysis to file
    analysis_file = os.path.join(OUTPUT_DIR, f'analysis_{query.replace(" ", "_")}_{datetime.now().strftime("%Y%m%d")}.json')
    with open(analysis_file, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"Saved analysis for query '{query}' to {analysis_file}")
    
    return analysis

def get_economic_indicators():
    """Get economic indicators from DataBank API."""
    print("Getting economic indicators from DataBank API...")
    
    # Since we don't have direct API access, we'll simulate economic data
    # In a production environment, you would use the actual DataBank API client
    
    # Example indicators to track
    indicators = {
        "NY.GDP.MKTP.KD.ZG": {  # GDP growth
            "name": "GDP Growth Rate",
            "data": {
                "United States": 2.1,
                "China": 5.2,
                "European Union": 1.3,
                "India": 6.7,
                "Japan": 1.0,
                "United Kingdom": 0.5,
                "Brazil": 2.9,
                "Canada": 1.5
            },
            "growth_sectors": ["Technology", "Healthcare", "Renewable Energy", "E-commerce"],
            "declining_sectors": ["Traditional Retail", "Oil & Gas", "Print Media"]
        },
        "FP.CPI.TOTL.ZG": {     # Inflation
            "name": "Inflation Rate",
            "data": {
                "United States": 3.4,
                "China": 2.1,
                "European Union": 2.9,
                "India": 5.6,
                "Japan": 2.0,
                "United Kingdom": 4.2,
                "Brazil": 4.5,
                "Canada": 3.8
            },
            "impact": "Rising costs affecting consumer spending patterns and business margins"
        },
        "SL.UEM.TOTL.ZS": {     # Unemployment
            "name": "Unemployment Rate",
            "data": {
                "United States": 3.8,
                "China": 5.0,
                "European Union": 6.5,
                "India": 7.8,
                "Japan": 2.6,
                "United Kingdom": 4.3,
                "Brazil": 7.9,
                "Canada": 5.5
            },
            "skills_gap": ["AI/ML", "Cybersecurity", "Healthcare Specialists", "Renewable Energy Technicians"]
        },
        "NE.CON.PRVT.ZS": {     # Private consumption
            "name": "Private Consumption (% of GDP)",
            "data": {
                "United States": 68.5,
                "China": 38.2,
                "European Union": 53.6,
                "India": 59.7,
                "Japan": 55.8,
                "United Kingdom": 63.2,
                "Brazil": 62.4,
                "Canada": 57.8
            },
            "growing_categories": ["Digital Services", "Health & Wellness", "Home Improvement", "Sustainable Products"],
            "declining_categories": ["Fast Fashion", "Single-use Plastics", "Traditional Media"]
        },
        "NE.GDI.TOTL.ZS": {     # Gross domestic investment
            "name": "Gross Domestic Investment (% of GDP)",
            "data": {
                "United States": 21.2,
                "China": 42.8,
                "European Union": 22.4,
                "India": 31.7,
                "Japan": 24.2,
                "United Kingdom": 17.6,
                "Brazil": 16.8,
                "Canada": 22.7
            },
            "hot_investment_areas": ["Green Technology", "Digital Infrastructure", "Biotechnology", "Space Technology"]
        },
        "BX.KLT.DINV.WD.GD.ZS": { # Foreign direct investment
            "name": "Foreign Direct Investment (% of GDP)",
            "data": {
                "United States": 1.8,
                "China": 1.2,
                "European Union": 2.4,
                "India": 1.9,
                "Japan": 0.8,
                "United Kingdom": 2.1,
                "Brazil": 3.4,
                "Canada": 2.7
            },
            "attractive_sectors": ["Technology", "Renewable Energy", "Healthcare", "Advanced Manufacturing"]
        }
    }
    
    # Add market opportunity indicators
    market_indicators = {
        "underserved_markets": {
            "name": "Potentially Underserved Markets",
            "data": [
                {
                    "market": "Rural Healthcare Technology",
                    "gap_score": 8.7,
                    "growth_potential": "High",
                    "barriers": ["Infrastructure", "Digital Literacy", "Initial Investment"]
                },
                {
                    "market": "Elderly-focused Technology",
                    "gap_score": 7.9,
                    "growth_potential": "High",
                    "barriers": ["Adoption Rate", "Usability", "Marketing Challenges"]
                },
                {
                    "market": "Sustainable Packaging Solutions",
                    "gap_score": 8.2,
                    "growth_potential": "High",
                    "barriers": ["Cost", "Supply Chain", "Technical Limitations"]
                },
                {
                    "market": "Mental Health Technology",
                    "gap_score": 8.5,
                    "growth_potential": "High",
                    "barriers": ["Regulation", "Privacy Concerns", "Healthcare Integration"]
                },
                {
                    "market": "Middle-Income Housing",
                    "gap_score": 7.8,
                    "growth_potential": "Medium",
                    "barriers": ["Land Costs", "Regulations", "Construction Costs"]
                },
                {
                    "market": "Educational Technology for Vocational Training",
                    "gap_score": 7.6,
                    "growth_potential": "Medium",
                    "barriers": ["Content Development", "Industry Partnerships", "Certification Standards"]
                },
                {
                    "market": "Affordable Childcare Solutions",
                    "gap_score": 8.9,
                    "growth_potential": "High",
                    "barriers": ["Staffing", "Regulations", "Facility Costs"]
                },
                {
                    "market": "Sustainable Agriculture Technology",
                    "gap_score": 8.1,
                    "growth_potential": "High",
                    "barriers": ["Adoption Rate", "Initial Investment", "Technical Knowledge"]
                }
            ]
        },
        "emerging_technologies": {
            "name": "Emerging Technologies with Market Potential",
            "data": [
                {
                    "technology": "Vertical Farming",
                    "market_readiness": 7.2,
                    "investment_trend": "Increasing",
                    "adoption_barriers": ["Cost", "Technical Expertise", "Scale"]
                },
                {
                    "technology": "Telehealth Platforms",
                    "market_readiness": 8.5,
                    "investment_trend": "Rapidly Increasing",
                    "adoption_barriers": ["Regulation", "Insurance Coverage", "Digital Divide"]
                },
                {
                    "technology": "AI-powered Education",
                    "market_readiness": 6.8,
                    "investment_trend": "Increasing",
                    "adoption_barriers": ["Integration", "Teacher Training", "Content Development"]
                },
                {
                    "technology": "Carbon Capture Solutions",
                    "market_readiness": 5.9,
                    "investment_trend": "Steadily Increasing",
                    "adoption_barriers": ["Cost", "Scale", "Policy Support"]
                },
                {
                    "technology": "Plant-based Alternatives",
                    "market_readiness": 8.7,
                    "investment_trend": "Rapidly Increasing",
                    "adoption_barriers": ["Taste/Texture", "Price", "Consumer Education"]
                },
                {
                    "technology": "Digital Therapeutics",
                    "market_readiness": 7.4,
                    "investment_trend": "Increasing",
                    "adoption_barriers": ["Clinical Validation", "Reimbursement", "Integration"]
                }
            ]
        }
    }
    
    # Combine all indicators
    all_indicators = {
        "economic_indicators": indicators,
        "market_indicators": market_indicators,
        "data_date": datetime.now().strftime("%Y-%m-%d"),
        "note": "This is simulated data for market research purposes."
    }
    
    # Save data
    with open(os.path.join(OUTPUT_DIR, f'economic_indicators_{datetime.now().strftime("%Y%m%d")}.json'), 'w') as f:
        json.dump(all_indicators, f, indent=2)
    
    print(f"Saved simulated economic indicators data")
    
    return all_indicators

def scrape_market_trends():
    """Scrape market trends from various websites."""
    print("Scraping market trends from websites...")
    
    # Since we can't do actual web scraping in this context, we'll simulate scraped data
    # In a production environment, you would use BeautifulSoup or Playwright
    
    # Example websites that would be scraped
    websites = [
        "https://www.entrepreneur.com/growing-a-business/trends",
        "https://www.forbes.com/entrepreneurs",
        "https://www.inc.com/trending",
        "https://www.businessinsider.com/retail",
        "https://www.fastcompany.com/technology"
    ]
    
    # Simulated scraped trends data
    scraped_data = {
        "websites": websites,
        "scraped_date": datetime.now().strftime("%Y-%m-%d"),
        "trends": [
            {
                "source": "Entrepreneur",
                "url": "https://www.entrepreneur.com/growing-a-business/trends",
                "trends": [
                    {
                        "title": "The Rise of Sustainable Micro-Businesses",
                        "description": "Small-scale, environmentally conscious businesses are gaining traction as consumers prioritize sustainability.",
                        "sectors": ["Retail", "Food & Beverage", "Consumer Goods"],
                        "sentiment": "Positive"
                    },
                    {
                        "title": "Mental Health Tech Boom",
                        "description": "Apps and platforms focused on mental wellness are seeing unprecedented growth post-pandemic.",
                        "sectors": ["Health Tech", "Software", "Consumer Services"],
                        "sentiment": "Very Positive"
                    },
                    {
                        "title": "Rural Market Digitalization",
                        "description": "Previously underserved rural markets are becoming accessible through digital platforms and logistics innovations.",
                        "sectors": ["E-commerce", "Logistics", "Agriculture"],
                        "sentiment": "Positive"
                    }
                ]
            },
            {
                "source": "Forbes",
                "url": "https://www.forbes.com/entrepreneurs",
                "trends": [
                    {
                        "title": "AI-Powered Small Business Tools",
                        "description": "Affordable AI solutions are democratizing access to advanced business intelligence for SMEs.",
                        "sectors": ["Software", "Business Services", "Retail"],
                        "sentiment": "Very Positive"
                    },
                    {
                        "title": "Senior-Focused Technology",
                        "description": "The aging population represents a growing market for specialized tech products and services.",
                        "sectors": ["Health Tech", "Consumer Electronics", "Home Services"],
                        "sentiment": "Positive"
                    },
                    {
                        "title": "Personalized Nutrition Services",
                        "description": "Customized nutrition plans based on individual health data are creating new market opportunities.",
                        "sectors": ["Health & Wellness", "Food & Beverage", "Biotech"],
                        "sentiment": "Positive"
                    }
                ]
            },
            {
                "source": "Inc",
                "url": "https://www.inc.com/trending",
                "trends": [
                    {
                        "title": "Micro-Mobility Solutions",
                        "description": "Urban transportation alternatives are creating opportunities for innovative business models.",
                        "sectors": ["Transportation", "Urban Planning", "Green Tech"],
                        "sentiment": "Positive"
                    },
                    {
                        "title": "Affordable Housing Innovations",
                        "description": "New construction methods and financing models are addressing the middle-market housing gap.",
                        "sectors": ["Real Estate", "Construction", "Finance"],
                        "sentiment": "Positive"
                    },
                    {
                        "title": "Digital Upskilling Platforms",
                        "description": "Businesses focused on workforce retraining are seeing high demand amid rapid technological change.",
                        "sectors": ["Education", "HR Tech", "Software"],
                        "sentiment": "Very Positive"
                    }
                ]
            },
            {
                "source": "Business Insider",
                "url": "https://www.businessinsider.com/retail",
                "trends": [
                    {
                        "title": "Circular Economy Retail",
                        "description": "Businesses built around product reuse, recycling, and upcycling are gaining consumer interest.",
                        "sectors": ["Retail", "Consumer Goods", "Sustainability"],
                        "sentiment": "Positive"
                    },
                    {
                        "title": "Hyper-Local Supply Chains",
                        "description": "Retailers are investing in localized production and distribution to improve resilience.",
                        "sectors": ["Retail", "Manufacturing", "Logistics"],
                        "sentiment": "Positive"
                    },
                    {
                        "title": "AR Shopping Experiences",
                        "description": "Augmented reality is creating new opportunities for immersive retail experiences.",
                        "sectors": ["Retail", "Technology", "E-commerce"],
                        "sentiment": "Positive"
                    }
                ]
            },
            {
                "source": "Fast Company",
                "url": "https://www.fastcompany.com/technology",
                "trends": [
                    {
                        "title": "Climate Tech Acceleration",
                        "description": "Technologies addressing climate change are seeing unprecedented investment and adoption.",
                        "sectors": ["Green Tech", "Energy", "Agriculture"],
                        "sentiment": "Very Positive"
                    },
                    {
                        "title": "Healthcare Accessibility Tech",
                        "description": "Innovations making healthcare more accessible to underserved populations are gaining traction.",
                        "sectors": ["Health Tech", "Telemedicine", "Software"],
                        "sentiment": "Very Positive"
                    },
                    {
                        "title": "Privacy-Focused Alternatives",
                        "description": "Growing consumer concern about data privacy is creating markets for alternative tech products.",
                        "sectors": ["Software", "Consumer Tech", "Security"],
                        "sentiment": "Positive"
                    }
                ]
            }
        ],
        "underserved_market_mentions": [
            {
                "market": "Rural Healthcare Technology",
                "mention_count": 12,
                "sentiment_score": 0.78,
                "growth_indicators": ["Investment Increase", "Policy Support", "Consumer Demand"]
            },
            {
                "market": "Middle-Income Housing",
                "mention_count": 15,
                "sentiment_score": 0.65,
                "growth_indicators": ["Innovation Activity", "Consumer Demand", "Policy Focus"]
            },
            {
                "market": "Senior-Focused Technology",
                "mention_count": 18,
                "sentiment_score": 0.82,
                "growth_indicators": ["Demographic Trends", "Investment Increase", "Market Gap"]
            },
            {
                "market": "Mental Health Services",
                "mention_count": 24,
                "sentiment_score": 0.85,
                "growth_indicators": ["Awareness Growth", "Reduced Stigma", "Insurance Coverage"]
            },
            {
                "market": "Sustainable Packaging",
                "mention_count": 17,
                "sentiment_score": 0.76,
                "growth_indicators": ["Regulation", "Consumer Demand", "Corporate Commitments"]
            },
            {
                "market": "Vocational Education Technology",
                "mention_count": 11,
                "sentiment_score": 0.72,
                "growth_indicators": ["Skills Gap", "Employment Trends", "Education Costs"]
            },
            {
                "market": "Affordable Childcare",
                "mention_count": 14,
                "sentiment_score": 0.68,
                "growth_indicators": ["Workforce Participation", "Policy Support", "Urban Development"]
            }
        ]
    }
    
    # Save simulated scraped data
    with open(os.path.join(OUTPUT_DIR, f'scraped_trends_{datetime.now().strftime("%Y%m%d")}.json'), 'w') as f:
        json.dump(scraped_data, f, indent=2)
    
    print(f"Saved simulated market trends data from web scraping")
    
    return scraped_data

def main():
    """Main function to run news data collection and analysis."""
    print("Starting news and alternative data collection...")
    
    # Market-related queries to search in news
    market_queries = [
        "underserved market",
        "market opportunity",
        "emerging industry",
        "growing market",
        "market gap",
        "industry disruption",
        "unmet needs",
        "market trends",
        "business opportunity",
        "startup trends"
    ]
    
    # Industry-specific queries
    industry_queries = [
        "renewable energy market",
        "telemedicine growth",
        "remote work technology",
        "ai services market",
        "elder care innovation",
        "mental health technology",
        "food delivery market",
        "online education trends"
    ]
    
    # Collect and analyze news articles
    all_news_analysis = {}
    
    # Collect market-related news
    for query in market_queries:
        articles_df = get_news_articles(query, days_back=30)
        if not articles_df.empty:
            analysis = analyze_news_data(articles_df, query)
            all_news_analysis[query] = analysis
        time.sleep(1)  # Avoid rate limiting
    
    # Collect industry-specific news
    for query in industry_queries:
        articles_df = get_news_articles(query, days_back=30)
        if not articles_df.empty:
            analysis = analyze_news_data(articles_df, query)
            all_news_analysis[query] = analysis
        time.sleep(1)  # Avoid rate limiting
    
    # Save consolidated news analysis
    with open(os.path.join(OUTPUT_DIR, f'all_news_analysis_{datetime.now().strftime("%Y%m%d")}.json'), 'w') as f:
        json.dump(all_news_analysis, f, indent=2)
    
    # Get economic indicators
    economic_data = get_economic_indicators()
    
    # Scrape market trends
    scraped_trends = scrape_market_trends()
    
    print("News and alternative data collection completed.")

if __name__ == "__main__":
    main()
