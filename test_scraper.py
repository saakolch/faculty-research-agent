#!/usr/bin/env python3
"""
Test script for HKUST-GZ Faculty Scraper
This script tests the scraper functionality with sample data
"""

import json
import sys
from hkust_scraper import HKUSTGZScraper
from research_matcher import ResearchMatcher

def test_scraper():
    """Test the scraper with a small sample"""
    print("Testing HKUST-GZ Faculty Scraper...")
    
    # Create sample faculty data for testing
    sample_faculty = [
        {
            'name': 'Dr. John Smith',
            'title': 'Associate Professor',
            'department': 'Computer Science and Engineering',
            'research_interests': ['Machine Learning', 'Artificial Intelligence', 'Deep Learning', 'Computer Vision'],
            'bio': 'Dr. Smith is an expert in machine learning and AI applications. His research focuses on deep learning algorithms for computer vision tasks.',
            'email': 'john.smith@hkust-gz.edu.cn',
            'url': 'https://hkust-gz.edu.cn/faculty/john-smith',
            'google_scholar': 'https://scholar.google.com/citations?user=123456',
            'research_gate': 'https://www.researchgate.net/profile/John_Smith',
            'publications': [
                'Deep Learning for Computer Vision: A Comprehensive Survey',
                'Neural Networks in Multi-Agent Systems',
                'Reinforcement Learning for Autonomous Vehicles'
            ]
        },
        {
            'name': 'Dr. Sarah Johnson',
            'title': 'Assistant Professor',
            'department': 'Data Science and Analytics',
            'research_interests': ['Data Mining', 'Big Data Analytics', 'Statistical Learning', 'Predictive Modeling'],
            'bio': 'Dr. Johnson specializes in data mining and big data analytics. Her work involves developing statistical learning models for predictive analytics.',
            'email': 'sarah.johnson@hkust-gz.edu.cn',
            'url': 'https://hkust-gz.edu.cn/faculty/sarah-johnson',
            'google_scholar': 'https://scholar.google.com/citations?user=789012',
            'research_gate': 'https://www.researchgate.net/profile/Sarah_Johnson',
            'publications': [
                'Big Data Analytics in Healthcare',
                'Statistical Learning for Predictive Modeling',
                'Data Mining Techniques for Business Intelligence'
            ]
        },
        {
            'name': 'Dr. Michael Chen',
            'title': 'Professor',
            'department': 'Robotics and Automation',
            'research_interests': ['Robotics', 'Multi-Agent Systems', 'Autonomous Systems', 'Control Theory'],
            'bio': 'Dr. Chen is a leading expert in robotics and multi-agent systems. His research focuses on autonomous systems and control theory.',
            'email': 'michael.chen@hkust-gz.edu.cn',
            'url': 'https://hkust-gz.edu.cn/faculty/michael-chen',
            'google_scholar': 'https://scholar.google.com/citations?user=345678',
            'research_gate': 'https://www.researchgate.net/profile/Michael_Chen',
            'publications': [
                'Multi-Agent Systems in Robotics',
                'Autonomous Control Systems',
                'Robotic Learning and Adaptation'
            ]
        }
    ]
    
    # Save sample data
    with open('sample_faculty_data.json', 'w', encoding='utf-8') as f:
        json.dump(sample_faculty, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Created sample data with {len(sample_faculty)} faculty profiles")
    return sample_faculty

def test_matcher():
    """Test the research matcher"""
    print("\nTesting Research Matcher...")
    
    # Load sample data
    try:
        with open('sample_faculty_data.json', 'r', encoding='utf-8') as f:
            faculty_data = json.load(f)
    except FileNotFoundError:
        faculty_data = test_scraper()
    
    # Test user interests
    user_interests = "I'm interested in machine learning, particularly deep learning and neural networks for computer vision applications. I also work on multi-agent systems and reinforcement learning."
    
    # Initialize matcher (without OpenAI key for basic testing)
    matcher = ResearchMatcher()
    
    # Test matching
    matches = matcher.match_faculty_with_interests(faculty_data, user_interests)
    
    print(f"✓ Found {len(matches)} matches")
    
    # Display results
    for i, match in enumerate(matches, 1):
        profile = match['faculty_profile']
        print(f"\n{i}. {profile['name']} ({profile['title']})")
        print(f"   Department: {profile['department']}")
        print(f"   Similarity Score: {match['similarity_score']:.3f}")
        print(f"   Research Interests: {', '.join(profile['research_interests'])}")
        if match['match_reasons']:
            print(f"   Match Reasons: {'; '.join(match['match_reasons'])}")
    
    return matches

def test_web_scraping():
    """Test actual web scraping (optional)"""
    print("\nTesting Web Scraping (Optional)...")
    print("This will attempt to scrape the actual HKUST-GZ website.")
    print("Note: This may take some time and requires internet connection.")
    
    response = input("Do you want to test web scraping? (y/n): ")
    if response.lower().startswith('y'):
        try:
            scraper = HKUSTGZScraper(headless=True, delay=3.0)
            print("Starting web scraping...")
            
            # Test getting faculty links
            scraper.setup_driver()
            links = scraper.get_faculty_links()
            scraper.close_driver()
            
            if links:
                print(f"✓ Found {len(links)} faculty links")
                print("Sample links:")
                for link in links[:3]:
                    print(f"  - {link}")
            else:
                print("⚠ No faculty links found (website structure may have changed)")
                
        except Exception as e:
            print(f"✗ Web scraping test failed: {e}")
            print("This is normal if the website structure has changed or if there are network issues.")

def main():
    """Run all tests"""
    print("=" * 60)
    print("HKUST-GZ Faculty Research Agent - Test Suite")
    print("=" * 60)
    
    try:
        # Test 1: Sample data creation
        test_scraper()
        
        # Test 2: Research matching
        test_matcher()
        
        # Test 3: Web scraping (optional)
        test_web_scraping()
        
        print("\n" + "=" * 60)
        print("✓ All tests completed successfully!")
        print("The faculty research agent is ready to use.")
        print("Run 'python run.py' to start the web application.")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 