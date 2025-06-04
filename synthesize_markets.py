#!/usr/bin/env python3
"""
Market synthesis script for market research tool.
This script synthesizes findings from all data sources to identify underserved markets.
"""

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Setup directories
RESULTS_DIR = '../results'
OUTPUT_DIR = '../results'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_combined_analysis():
    """Load the combined market analysis data."""
    print("Loading combined market analysis data...")
    
    combined_file = os.path.join(RESULTS_DIR, 'combined_market_analysis.json')
    if not os.path.exists(combined_file):
        print(f"Combined analysis file not found: {combined_file}")
        return None
    
    with open(combined_file, 'r') as f:
        combined_data = json.load(f)
    
    return combined_data

def identify_top_underserved_markets(combined_data):
    """Identify top underserved markets by cross-referencing all data sources."""
    print("Identifying top underserved markets...")
    
    if not combined_data:
        print("No combined data available for analysis.")
        return []
    
    # Extract relevant data from different analyses
    underserved_markets = combined_data.get('underserved_markets', {}).get('markets', [])
    market_mentions = combined_data.get('market_mentions', {}).get('market_mentions', [])
    news_sentiment = combined_data.get('news_sentiment', {}).get('sentiment_by_query', [])
    growth_sectors = combined_data.get('economic_growth', {}).get('growth_sectors', [])
    hot_investment_areas = combined_data.get('economic_growth', {}).get('hot_investment_areas', [])
    emerging_tech = combined_data.get('emerging_technologies', {}).get('technologies', [])
    trending_sectors = combined_data.get('website_trends', {}).get('top_sectors', [])
    
    # Create a scoring system for underserved markets
    market_scores = {}
    
    # Score from economic indicators' underserved markets
    for market in underserved_markets:
        market_name = market.get('market', '')
        if not market_name:
            continue
            
        if market_name not in market_scores:
            market_scores[market_name] = {
                'name': market_name,
                'total_score': 0,
                'gap_score': 0,
                'mention_score': 0,
                'sentiment_score': 0,
                'growth_alignment': 0,
                'tech_alignment': 0,
                'sector_alignment': 0,
                'barriers': [],
                'growth_potential': '',
                'sources': []
            }
        
        # Add gap score (0-10 scale)
        gap_score = market.get('gap_score', 0)
        market_scores[market_name]['gap_score'] = gap_score
        market_scores[market_name]['total_score'] += gap_score
        
        # Add growth potential
        market_scores[market_name]['growth_potential'] = market.get('growth_potential', '')
        if market.get('growth_potential') == 'High':
            market_scores[market_name]['total_score'] += 3
        elif market.get('growth_potential') == 'Medium':
            market_scores[market_name]['total_score'] += 1.5
            
        # Add barriers
        market_scores[market_name]['barriers'] = market.get('barriers', [])
        
        # Add source
        market_scores[market_name]['sources'].append('economic_indicators')
    
    # Score from market mentions
    for mention in market_mentions:
        market_name = mention.get('market', '')
        if not market_name:
            continue
            
        if market_name not in market_scores:
            market_scores[market_name] = {
                'name': market_name,
                'total_score': 0,
                'gap_score': 0,
                'mention_score': 0,
                'sentiment_score': 0,
                'growth_alignment': 0,
                'tech_alignment': 0,
                'sector_alignment': 0,
                'barriers': [],
                'growth_potential': '',
                'sources': []
            }
        
        # Add mention score (normalized to 0-10 scale)
        mention_count = mention.get('mention_count', 0)
        mention_score = min(10, mention_count / 3)  # Scale: max 10 points for 30+ mentions
        market_scores[market_name]['mention_score'] = mention_score
        market_scores[market_name]['total_score'] += mention_score
        
        # Add sentiment score (normalized to 0-5 scale)
        sentiment = mention.get('sentiment_score', 0)
        sentiment_score = min(5, sentiment * 5)  # Scale: max 5 points for sentiment 1.0
        market_scores[market_name]['sentiment_score'] = sentiment_score
        market_scores[market_name]['total_score'] += sentiment_score
        
        # Add source
        if 'web_scraping' not in market_scores[market_name]['sources']:
            market_scores[market_name]['sources'].append('web_scraping')
    
    # Score from alignment with growth sectors and investment areas
    for market_name, market_data in market_scores.items():
        # Check alignment with growth sectors
        market_words = market_name.lower().split()
        
        # Growth sector alignment
        growth_alignment = 0
        for sector in growth_sectors:
            sector_words = sector.lower().split()
            if any(word in market_words for word in sector_words):
                growth_alignment += 1
        
        # Scale growth alignment (0-3)
        growth_alignment = min(3, growth_alignment)
        market_data['growth_alignment'] = growth_alignment
        market_data['total_score'] += growth_alignment
        
        # Investment area alignment
        for area in hot_investment_areas:
            area_words = area.lower().split()
            if any(word in market_words for word in area_words):
                market_data['total_score'] += 1
                
        # Emerging tech alignment
        tech_alignment = 0
        for tech in emerging_tech:
            tech_name = tech.get('technology', '').lower()
            tech_words = tech_name.split()
            if any(word in market_words for word in tech_words):
                tech_alignment += 1
        
        # Scale tech alignment (0-3)
        tech_alignment = min(3, tech_alignment)
        market_data['tech_alignment'] = tech_alignment
        market_data['total_score'] += tech_alignment
        
        # Trending sector alignment
        sector_alignment = 0
        for sector in trending_sectors:
            sector_words = sector.lower().split()
            if any(word in market_words for word in sector_words):
                sector_alignment += 1
        
        # Scale sector alignment (0-3)
        sector_alignment = min(3, sector_alignment)
        market_data['sector_alignment'] = sector_alignment
        market_data['total_score'] += sector_alignment
    
    # Convert to list and sort by total score
    market_list = list(market_scores.values())
    market_list.sort(key=lambda x: x['total_score'], reverse=True)
    
    # Save the ranked markets
    with open(os.path.join(OUTPUT_DIR, 'ranked_underserved_markets.json'), 'w') as f:
        json.dump(market_list, f, indent=2)
    
    # Create visualization of top markets
    top_markets = market_list[:10]
    top_markets_df = pd.DataFrame(top_markets)
    
    plt.figure(figsize=(12, 8))
    sns.barplot(x='total_score', y='name', data=top_markets_df)
    plt.title('Top Underserved Markets by Opportunity Score')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'top_underserved_markets.png'))
    plt.close()
    
    # Create visualization of score components for top 5 markets
    top5_markets = market_list[:5]
    components = ['gap_score', 'mention_score', 'sentiment_score', 
                 'growth_alignment', 'tech_alignment', 'sector_alignment']
    
    component_data = []
    for market in top5_markets:
        for component in components:
            component_data.append({
                'market': market['name'],
                'component': component,
                'score': market[component]
            })
    
    component_df = pd.DataFrame(component_data)
    
    plt.figure(figsize=(14, 8))
    sns.barplot(x='score', y='market', hue='component', data=component_df)
    plt.title('Score Components for Top 5 Underserved Markets')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'market_score_components.png'))
    plt.close()
    
    return market_list

def analyze_market_barriers(market_list):
    """Analyze barriers to entry for identified underserved markets."""
    print("Analyzing market barriers...")
    
    if not market_list:
        print("No market list available for barrier analysis.")
        return {}
    
    # Extract all barriers
    all_barriers = []
    market_barriers = {}
    
    for market in market_list:
        market_name = market.get('name', '')
        barriers = market.get('barriers', [])
        
        if market_name and barriers:
            market_barriers[market_name] = barriers
            all_barriers.extend(barriers)
    
    # Count barrier frequencies
    barrier_counts = pd.Series(all_barriers).value_counts()
    
    # Create visualization
    plt.figure(figsize=(12, 8))
    barrier_counts.plot(kind='bar')
    plt.title('Common Barriers to Entry in Underserved Markets')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'common_market_barriers.png'))
    plt.close()
    
    # Create barrier analysis
    barrier_analysis = {
        'barrier_counts': barrier_counts.to_dict(),
        'market_specific_barriers': market_barriers
    }
    
    # Save barrier analysis
    with open(os.path.join(OUTPUT_DIR, 'market_barrier_analysis.json'), 'w') as f:
        json.dump(barrier_analysis, f, indent=2)
    
    return barrier_analysis

def create_market_opportunity_profiles(market_list, combined_data):
    """Create detailed profiles for top underserved market opportunities."""
    print("Creating market opportunity profiles...")
    
    if not market_list or not combined_data:
        print("Missing data for creating market opportunity profiles.")
        return []
    
    # Select top 10 markets
    top_markets = market_list[:10]
    
    # Extract relevant data for enriching profiles
    economic_indicators = combined_data.get('economic_growth', {})
    emerging_tech = combined_data.get('emerging_technologies', {}).get('technologies', [])
    website_trends = combined_data.get('website_trends', {}).get('trends', [])
    
    # Create detailed profiles
    market_profiles = []
    
    for market in top_markets:
        market_name = market.get('name', '')
        if not market_name:
            continue
        
        # Create base profile
        profile = {
            'market_name': market_name,
            'opportunity_score': market.get('total_score', 0),
            'gap_score': market.get('gap_score', 0),
            'growth_potential': market.get('growth_potential', ''),
            'barriers_to_entry': market.get('barriers', []),
            'data_sources': market.get('sources', []),
            'related_technologies': [],
            'related_trends': [],
            'target_demographics': [],
            'business_model_suggestions': []
        }
        
        # Find related technologies
        market_keywords = market_name.lower().split()
        
        for tech in emerging_tech:
            tech_name = tech.get('technology', '').lower()
            if any(keyword in tech_name for keyword in market_keywords):
                profile['related_technologies'].append({
                    'name': tech.get('technology', ''),
                    'market_readiness': tech.get('market_readiness', 0),
                    'investment_trend': tech.get('investment_trend', ''),
                    'adoption_barriers': tech.get('adoption_barriers', [])
                })
        
        # Find related trends
        for trend in website_trends:
            trend_title = trend.get('title', '').lower()
            trend_desc = trend.get('description', '').lower()
            
            if any(keyword in trend_title or keyword in trend_desc for keyword in market_keywords):
                profile['related_trends'].append({
                    'title': trend.get('title', ''),
                    'description': trend.get('description', ''),
                    'source': trend.get('source', ''),
                    'sectors': trend.get('sectors', []),
                    'sentiment': trend.get('sentiment', '')
                })
        
        # Generate target demographics based on market name
        if 'elderly' in market_name.lower() or 'senior' in market_name.lower() or 'aging' in market_name.lower():
            profile['target_demographics'].append('Seniors (65+)')
            profile['target_demographics'].append('Adult children of seniors')
            profile['target_demographics'].append('Healthcare providers')
        
        if 'rural' in market_name.lower():
            profile['target_demographics'].append('Rural communities')
            profile['target_demographics'].append('Small town residents')
            profile['target_demographics'].append('Agricultural sector')
        
        if 'health' in market_name.lower() or 'wellness' in market_name.lower() or 'care' in market_name.lower():
            profile['target_demographics'].append('Health-conscious consumers')
            profile['target_demographics'].append('Healthcare providers')
            profile['target_demographics'].append('Insurance companies')
        
        if 'education' in market_name.lower() or 'learning' in market_name.lower() or 'training' in market_name.lower():
            profile['target_demographics'].append('Students')
            profile['target_demographics'].append('Working professionals')
            profile['target_demographics'].append('Educational institutions')
        
        if 'housing' in market_name.lower() or 'home' in market_name.lower():
            profile['target_demographics'].append('First-time homebuyers')
            profile['target_demographics'].append('Middle-income families')
            profile['target_demographics'].append('Real estate developers')
        
        if 'childcare' in market_name.lower():
            profile['target_demographics'].append('Working parents')
            profile['target_demographics'].append('Single-parent households')
            profile['target_demographics'].append('Employers with parent employees')
        
        # Generate business model suggestions based on market name
        if 'technology' in market_name.lower() or 'tech' in market_name.lower():
            profile['business_model_suggestions'].append('SaaS subscription model')
            profile['business_model_suggestions'].append('Hardware + software solution')
            profile['business_model_suggestions'].append('B2B enterprise sales')
        
        if 'healthcare' in market_name.lower() or 'health' in market_name.lower():
            profile['business_model_suggestions'].append('Telehealth platform')
            profile['business_model_suggestions'].append('Insurance partnerships')
            profile['business_model_suggestions'].append('Direct-to-consumer health services')
        
        if 'education' in market_name.lower() or 'learning' in market_name.lower():
            profile['business_model_suggestions'].append('Freemium learning platform')
            profile['business_model_suggestions'].append('B2B institutional sales')
            profile['business_model_suggestions'].append('Certification programs')
        
        if 'sustainable' in market_name.lower() or 'packaging' in market_name.lower():
            profile['business_model_suggestions'].append('B2B supplier model')
            profile['business_model_suggestions'].append('Circular economy approach')
            profile['business_model_suggestions'].append('Subscription refill service')
        
        if 'rural' in market_name.lower():
            profile['business_model_suggestions'].append('Hub and spoke distribution')
            profile['business_model_suggestions'].append('Mobile service delivery')
            profile['business_model_suggestions'].append('Community partnership model')
        
        # Add to profiles list
        market_profiles.append(profile)
    
    # Save market profiles
    with open(os.path.join(OUTPUT_DIR, 'market_opportunity_profiles.json'), 'w') as f:
        json.dump(market_profiles, f, indent=2)
    
    return market_profiles

def generate_market_summary_report(market_profiles):
    """Generate a summary report of identified underserved markets."""
    print("Generating market summary report...")
    
    if not market_profiles:
        print("No market profiles available for report generation.")
        return
    
    # Create markdown report
    report = f"""# Underserved Market Opportunities Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

This report identifies high-potential underserved markets based on comprehensive analysis of economic indicators, market trends, news sentiment, and web scraping data. The markets are ranked by opportunity score, which combines multiple factors including market gap, mention frequency, sentiment, and alignment with growth sectors.

## Top Underserved Market Opportunities

"""
    
    # Add each market to the report
    for i, profile in enumerate(market_profiles, 1):
        report += f"""### {i}. {profile['market_name']}

**Opportunity Score:** {profile['opportunity_score']:.2f}  
**Growth Potential:** {profile['growth_potential']}  
**Key Barriers to Entry:** {', '.join(profile['barriers_to_entry'])}

**Market Overview:**  
{profile['market_name']} represents a significant opportunity based on data from {', '.join(profile['data_sources'])}. 
This market shows strong alignment with current economic growth sectors and emerging technologies.

**Target Demographics:**
"""
        
        for demographic in profile['target_demographics']:
            report += f"- {demographic}\n"
        
        report += "\n**Potential Business Models:**\n"
        
        for model in profile['business_model_suggestions']:
            report += f"- {model}\n"
        
        if profile['related_technologies']:
            report += "\n**Related Technologies:**\n"
            for tech in profile['related_technologies'][:3]:  # Limit to top 3
                report += f"- {tech['name']} (Market Readiness: {tech['market_readiness']}, Trend: {tech['investment_trend']})\n"
        
        if profile['related_trends']:
            report += "\n**Related Market Trends:**\n"
            for trend in profile['related_trends'][:3]:  # Limit to top 3
                report += f"- {trend['title']} ({trend['source']})\n"
        
        report += "\n---\n\n"
    
    # Add methodology section
    report += """## Methodology

The underserved markets were identified using a multi-factor scoring system that incorporates:

1. **Gap Score:** Quantifies the degree to which a market is underserved based on economic indicators
2. **Mention Score:** Measures the frequency of market mentions in business and technology publications
3. **Sentiment Score:** Evaluates the positive sentiment associated with the market in news and publications
4. **Growth Alignment:** Assesses alignment with identified economic growth sectors
5. **Technology Alignment:** Measures connection to emerging technologies with high market readiness
6. **Sector Alignment:** Evaluates alignment with trending business sectors

## Next Steps

For each identified market opportunity, we recommend:

1. Conducting targeted consumer research to validate market demand
2. Analyzing competitive landscape to identify specific niches
3. Developing minimum viable product concepts
4. Testing business model assumptions with potential customers
5. Creating detailed financial projections and funding requirements

"""
    
    # Save report
    with open(os.path.join(OUTPUT_DIR, 'underserved_markets_report.md'), 'w') as f:
        f.write(report)
    
    print(f"Market summary report saved to {os.path.join(OUTPUT_DIR, 'underserved_markets_report.md')}")

def main():
    """Main function to run market synthesis."""
    print("Starting market synthesis...")
    
    # Load combined analysis data
    combined_data = load_combined_analysis()
    
    if not combined_data:
        print("Failed to load combined analysis data. Exiting.")
        return
    
    # Identify top underserved markets
    market_list = identify_top_underserved_markets(combined_data)
    
    # Analyze market barriers
    barrier_analysis = analyze_market_barriers(market_list)
    
    # Create market opportunity profiles
    market_profiles = create_market_opportunity_profiles(market_list, combined_data)
    
    # Generate market summary report
    generate_market_summary_report(market_profiles)
    
    print("Market synthesis completed.")
    print(f"Results saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
