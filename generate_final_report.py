#!/usr/bin/env python3
"""
Final report generation script for market research tool.
This script compiles all results into a final report for the user.
"""

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import shutil

# Setup directories
RESULTS_DIR = '../results'
OUTPUT_DIR = '../results/final_report'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def copy_key_files():
    """Copy key files to the final report directory."""
    print("Copying key files to final report directory...")
    
    # List of key files to copy
    key_files = [
        'underserved_markets_report.md',
        'market_validation_report.md',
        'top_underserved_markets.png',
        'market_validation_scatter.png',
        'validated_market_size.png',
        'validated_market_cagr.png',
        'market_score_components.png',
        'trending_sectors.png',
        'market_mentions_sentiment.png'
    ]
    
    # Copy each file if it exists
    for file in key_files:
        src_path = os.path.join(RESULTS_DIR, file)
        dst_path = os.path.join(OUTPUT_DIR, file)
        
        if os.path.exists(src_path):
            shutil.copy2(src_path, dst_path)
            print(f"Copied {file} to final report directory")
        else:
            print(f"Warning: {file} not found in results directory")

def load_validated_profiles():
    """Load the validated market profiles."""
    print("Loading validated market profiles...")
    
    profiles_file = os.path.join(RESULTS_DIR, 'validated_market_profiles.json')
    if not os.path.exists(profiles_file):
        print(f"Validated profiles file not found: {profiles_file}")
        return []
    
    with open(profiles_file, 'r') as f:
        profiles = json.load(f)
    
    return profiles

def generate_executive_summary(validated_profiles):
    """Generate an executive summary of the market research findings."""
    print("Generating executive summary...")
    
    # Count validated markets
    validated_count = sum(1 for p in validated_profiles if p.get('validation', {}).get('is_validated', False))
    
    # Get top markets by validation score
    top_markets = []
    for profile in validated_profiles:
        if profile.get('validation', {}).get('is_validated', False):
            top_markets.append({
                'name': profile.get('market_name', ''),
                'validation_score': profile.get('validation', {}).get('validation_score', 0),
                'market_size': profile.get('validation', {}).get('market_size_usd_billions', 0),
                'cagr': profile.get('validation', {}).get('cagr_percent', 0)
            })
    
    # Sort by validation score
    top_markets.sort(key=lambda x: x['validation_score'], reverse=True)
    top_markets = top_markets[:5]  # Get top 5
    
    # Create executive summary
    summary = f"""# Automated Market Research Tool: Executive Summary
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview

This report presents the findings of our automated market research tool designed to identify underserved markets with high growth potential. The tool analyzed multiple data sources including economic indicators, news sentiment, web trends, and market mentions to identify and validate promising market opportunities.

## Key Findings

- **{validated_count} validated underserved markets** were identified with strong growth potential
- Market opportunities span multiple sectors including healthcare, technology, sustainability, and education
- Validation confirms substantial market sizes and strong growth projections (CAGR)
- Common barriers to entry include infrastructure limitations, regulatory challenges, and initial investment requirements

## Top 5 Underserved Market Opportunities

"""
    
    # Add top markets to summary
    for i, market in enumerate(top_markets, 1):
        summary += f"""### {i}. {market['name']}
- **Validation Score:** {market['validation_score']:.1f}/10
- **Estimated Market Size:** ${market['market_size']:.1f} Billion
- **Projected CAGR:** {market['cagr']:.1f}%

"""
    
    # Add methodology summary
    summary += """## Methodology

Our automated market research approach followed these key steps:

1. **Data Collection:** Gathered data from multiple sources including economic indicators, news articles, and web trends
2. **Data Analysis:** Processed and analyzed data to identify patterns and correlations
3. **Market Identification:** Applied scoring criteria to identify potential underserved markets
4. **Validation:** Cross-referenced findings with external datasets and authoritative sources
5. **Reporting:** Compiled comprehensive reports with visualizations and actionable insights

## Next Steps

Based on these findings, we recommend:

1. Conducting deeper market research into the top 3 identified opportunities
2. Developing specific business concepts tailored to each validated market
3. Creating detailed financial models and funding requirements
4. Establishing key performance indicators for measuring success
5. Prioritizing markets based on alignment with organizational capabilities and strategic goals

"""
    
    # Save executive summary
    with open(os.path.join(OUTPUT_DIR, 'executive_summary.md'), 'w') as f:
        f.write(summary)
    
    print(f"Executive summary saved to {os.path.join(OUTPUT_DIR, 'executive_summary.md')}")
    
    return summary

def generate_final_report():
    """Generate the final comprehensive report."""
    print("Generating final comprehensive report...")
    
    # Load executive summary
    exec_summary_path = os.path.join(OUTPUT_DIR, 'executive_summary.md')
    if not os.path.exists(exec_summary_path):
        print(f"Executive summary not found: {exec_summary_path}")
        return
    
    with open(exec_summary_path, 'r') as f:
        exec_summary = f.read()
    
    # Load market report
    market_report_path = os.path.join(OUTPUT_DIR, 'underserved_markets_report.md')
    if not os.path.exists(market_report_path):
        print(f"Market report not found: {market_report_path}")
        return
    
    with open(market_report_path, 'r') as f:
        market_report = f.read()
        # Remove the title as we'll use our own
        market_report = '\n'.join(market_report.split('\n')[1:])
    
    # Load validation report
    validation_report_path = os.path.join(OUTPUT_DIR, 'market_validation_report.md')
    if not os.path.exists(validation_report_path):
        print(f"Validation report not found: {validation_report_path}")
        return
    
    with open(validation_report_path, 'r') as f:
        validation_report = f.read()
        # Remove the title as we'll use our own
        validation_report = '\n'.join(validation_report.split('\n')[1:])
    
    # Combine into final report
    final_report = f"""# Automated Market Research Tool: Final Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Table of Contents

1. Executive Summary
2. Underserved Market Opportunities
3. Market Validation
4. Methodology
5. Recommendations
6. Appendix: Data Sources and Visualizations

---

# 1. Executive Summary

{exec_summary.split('# Automated Market Research Tool: Executive Summary')[1]}

---

# 2. Underserved Market Opportunities

{market_report}

---

# 3. Market Validation

{validation_report}

---

# 4. Methodology

## Data Collection and Processing

The automated market research tool collected and processed data from multiple sources:

1. **Economic Indicators:** GDP growth, inflation rates, unemployment, private consumption, domestic investment, and foreign direct investment data across major economies.

2. **News Analysis:** Sentiment analysis of news articles related to market opportunities, emerging industries, and business trends.

3. **Web Trends:** Analysis of business and technology publications for mentions of underserved markets and emerging opportunities.

4. **Market Mentions:** Frequency and sentiment analysis of market mentions across business and technology sources.

## Market Identification Process

Markets were identified and scored using a multi-factor methodology:

1. **Gap Score:** Quantitative measure of how underserved a market is based on economic indicators
2. **Mention Score:** Frequency of market mentions in business and technology publications
3. **Sentiment Score:** Positive sentiment associated with the market in news and publications
4. **Growth Alignment:** Alignment with identified economic growth sectors
5. **Technology Alignment:** Connection to emerging technologies with high market readiness
6. **Sector Alignment:** Alignment with trending business sectors

## Validation Methodology

Identified markets were validated using:

1. Market size estimates from industry reports and economic databases
2. Compound Annual Growth Rate (CAGR) projections
3. Supporting economic and demographic indicators
4. Cross-referencing with authoritative market research sources

---

# 5. Recommendations

## Strategic Recommendations

1. **Prioritize Top 3 Markets:** Focus initial efforts on the highest-scoring validated markets
2. **Conduct Deep-Dive Research:** Perform detailed competitive analysis within each priority market
3. **Develop MVP Concepts:** Create minimum viable product concepts for each target market
4. **Test Business Models:** Validate business model assumptions with potential customers
5. **Create Financial Projections:** Develop detailed financial models and funding requirements

## Implementation Roadmap

1. **Month 1-2:** Conduct detailed market research on top opportunities
2. **Month 3-4:** Develop product concepts and business models
3. **Month 5-6:** Test concepts with potential customers
4. **Month 7-8:** Refine business plans based on feedback
5. **Month 9-12:** Develop go-to-market strategy and secure funding

---

# 6. Appendix: Data Sources and Visualizations

## Key Visualizations

- Top Underserved Markets by Opportunity Score
- Market Validation Scatter Plot
- Validated Market Size Comparison
- Projected CAGR by Market
- Market Score Components Analysis
- Trending Sectors Analysis
- Market Mentions Sentiment Analysis

## Data Sources

- Economic indicators and market data
- News and web trend analysis
- Market validation datasets
- Industry reports and publications

"""
    
    # Save final report
    with open(os.path.join(OUTPUT_DIR, 'final_report.md'), 'w') as f:
        f.write(final_report)
    
    print(f"Final report saved to {os.path.join(OUTPUT_DIR, 'final_report.md')}")
    
    # Convert to PDF using manus-md-to-pdf utility
    try:
        pdf_path = os.path.join(OUTPUT_DIR, 'automated_market_research_report.pdf')
        md_path = os.path.join(OUTPUT_DIR, 'final_report.md')
        os.system(f"manus-md-to-pdf {md_path} {pdf_path}")
        print(f"PDF report generated at {pdf_path}")
    except Exception as e:
        print(f"Error generating PDF: {e}")

def create_structured_prompts(validated_profiles):
    """Create structured prompts for AI processing."""
    print("Creating structured prompts for AI processing...")
    
    prompts = []
    
    # Generate prompts for top validated markets
    for profile in validated_profiles:
        if profile.get('validation', {}).get('is_validated', False):
            market_name = profile.get('market_name', '')
            
            # Create business plan prompt
            business_plan_prompt = f"""Create a business plan for a startup targeting the {market_name} market.

Market Information:
- Market Size: ${profile.get('validation', {}).get('market_size_usd_billions', 0):.1f} Billion
- CAGR: {profile.get('validation', {}).get('cagr_percent', 0):.1f}%
- Key Barriers: {', '.join(profile.get('barriers_to_entry', []))}
- Target Demographics: {', '.join(profile.get('target_demographics', []))}

The business plan should include:
1. Executive Summary
2. Market Analysis
3. Product/Service Description
4. Business Model
5. Marketing Strategy
6. Financial Projections
7. Funding Requirements
8. Implementation Timeline"""
            
            prompts.append({
                'market': market_name,
                'prompt_type': 'business_plan',
                'prompt': business_plan_prompt
            })
            
            # Create product concept prompt
            product_concept_prompt = f"""Design a product concept for the {market_name} market.

Market Information:
- Market Size: ${profile.get('validation', {}).get('market_size_usd_billions', 0):.1f} Billion
- CAGR: {profile.get('validation', {}).get('cagr_percent', 0):.1f}%
- Target Demographics: {', '.join(profile.get('target_demographics', []))}
- Potential Business Models: {', '.join(profile.get('business_model_suggestions', []))}

The product concept should include:
1. Product Description
2. Key Features and Benefits
3. Target User Personas
4. Unique Value Proposition
5. Technology Requirements
6. Development Roadmap
7. Pricing Strategy
8. Go-to-Market Approach"""
            
            prompts.append({
                'market': market_name,
                'prompt_type': 'product_concept',
                'prompt': product_concept_prompt
            })
    
    # Save structured prompts
    with open(os.path.join(OUTPUT_DIR, 'structured_prompts.json'), 'w') as f:
        json.dump(prompts, f, indent=2)
    
    print(f"Structured prompts saved to {os.path.join(OUTPUT_DIR, 'structured_prompts.json')}")
    
    return prompts

def main():
    """Main function to generate the final report."""
    print("Starting final report generation...")
    
    # Copy key files to final report directory
    copy_key_files()
    
    # Load validated profiles
    validated_profiles = load_validated_profiles()
    
    if not validated_profiles:
        print("Failed to load validated profiles. Exiting.")
        return
    
    # Generate executive summary
    generate_executive_summary(validated_profiles)
    
    # Generate final report
    generate_final_report()
    
    # Create structured prompts for AI processing
    create_structured_prompts(validated_profiles)
    
    print("Final report generation completed.")
    print(f"Results saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
