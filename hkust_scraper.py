import time
import json
import logging
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from retrying import retry

class HKUSTGZScraper:
    """Scraper for HKUST-GZ faculty directory"""
    
    def __init__(self, headless: bool = True, delay: float = 2.0):
        self.headless = headless
        self.delay = delay
        self.driver = None
        self.ua = UserAgent()
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_driver(self):
        """Setup Chrome WebDriver with appropriate options"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(f"--user-agent={self.ua.random}")
        
        # Disable images and CSS for faster loading
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.notifications": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)
        
    def close_driver(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
    
    def get_faculty_directory_url(self) -> str:
        """Get the main faculty directory URL for HKUST-GZ"""
        return "https://hkust-gz.edu.cn/en/faculty"
    
    def get_faculty_links(self) -> List[str]:
        """Extract all faculty profile links from the directory page"""
        faculty_links = []
        
        try:
            directory_url = self.get_faculty_directory_url()
            self.logger.info(f"Accessing faculty directory: {directory_url}")
            
            self.driver.get(directory_url)
            time.sleep(self.delay)
            
            # Wait for the page to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Look for faculty profile links
            selectors = [
                "a[href*='faculty']",
                "a[href*='profile']", 
                ".faculty-member a",
                ".faculty-card a",
                ".member a",
                "a[href*='staff']"
            ]
            
            for selector in selectors:
                try:
                    links = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for link in links:
                        href = link.get_attribute('href')
                        if href and 'faculty' in href.lower():
                            faculty_links.append(href)
                            self.logger.info(f"Found faculty link: {href}")
                except Exception as e:
                    self.logger.warning(f"Selector {selector} failed: {e}")
                    continue
            
            # Remove duplicates
            faculty_links = list(set(faculty_links))
            self.logger.info(f"Found {len(faculty_links)} unique faculty links")
            
        except Exception as e:
            self.logger.error(f"Error getting faculty links: {e}")
            
        return faculty_links
    
    def extract_faculty_profile(self, profile_url: str) -> Dict:
        """Extract detailed information from a faculty profile page"""
        profile_data = {
            'url': profile_url,
            'name': '',
            'title': '',
            'department': '',
            'research_interests': [],
            'publications': [],
            'education': '',
            'bio': '',
            'email': '',
            'phone': '',
            'office': '',
            'website': '',
            'google_scholar': '',
            'research_gate': '',
            'linkedin': ''
        }
        
        try:
            self.logger.info(f"Extracting profile from: {profile_url}")
            self.driver.get(profile_url)
            time.sleep(self.delay)
            
            # Wait for page to load
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Get page source and parse with BeautifulSoup
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Extract name
            name_selectors = [
                'h1', 'h2', '.name', '.faculty-name', '.profile-name',
                '[class*="name"]', '[id*="name"]'
            ]
            for selector in name_selectors:
                try:
                    name_elem = soup.select_one(selector)
                    if name_elem and name_elem.get_text().strip():
                        profile_data['name'] = name_elem.get_text().strip()
                        break
                except:
                    continue
            
            # Extract title/position
            title_selectors = [
                '.title', '.position', '.rank', '.designation',
                '[class*="title"]', '[class*="position"]'
            ]
            for selector in title_selectors:
                try:
                    title_elem = soup.select_one(selector)
                    if title_elem and title_elem.get_text().strip():
                        profile_data['title'] = title_elem.get_text().strip()
                        break
                except:
                    continue
            
            # Extract department
            dept_selectors = [
                '.department', '.school', '.faculty', '.division',
                '[class*="department"]', '[class*="school"]'
            ]
            for selector in dept_selectors:
                try:
                    dept_elem = soup.select_one(selector)
                    if dept_elem and dept_elem.get_text().strip():
                        profile_data['department'] = dept_elem.get_text().strip()
                        break
                except:
                    continue
            
            # Extract research interests
            research_selectors = [
                '.research-interests', '.research-areas', '.interests',
                '[class*="research"]', '[class*="interest"]'
            ]
            for selector in research_selectors:
                try:
                    research_elem = soup.select_one(selector)
                    if research_elem:
                        interests_text = research_elem.get_text().strip()
                        # Split by common delimiters
                        interests = [interest.strip() for interest in 
                                   interests_text.replace(',', ';').split(';') 
                                   if interest.strip()]
                        profile_data['research_interests'] = interests
                        break
                except:
                    continue
            
            # Extract publications
            pub_selectors = [
                '.publications', '.papers', '.research-output',
                '[class*="publication"]', '[class*="paper"]'
            ]
            for selector in pub_selectors:
                try:
                    pub_elements = soup.select(selector)
                    publications = []
                    for elem in pub_elements:
                        pub_text = elem.get_text().strip()
                        if pub_text and len(pub_text) > 10:  # Minimum length for a publication
                            publications.append(pub_text)
                    profile_data['publications'] = publications
                    break
                except:
                    continue
            
            # Extract contact information
            email_selectors = ['a[href^="mailto:"]', '.email', '[class*="email"]']
            for selector in email_selectors:
                try:
                    email_elem = soup.select_one(selector)
                    if email_elem:
                        email = email_elem.get('href', '').replace('mailto:', '') or email_elem.get_text().strip()
                        if '@' in email:
                            profile_data['email'] = email
                            break
                except:
                    continue
            
            # Extract bio
            bio_selectors = [
                '.bio', '.biography', '.about', '.description',
                '[class*="bio"]', '[class*="about"]'
            ]
            for selector in bio_selectors:
                try:
                    bio_elem = soup.select_one(selector)
                    if bio_elem and bio_elem.get_text().strip():
                        profile_data['bio'] = bio_elem.get_text().strip()
                        break
                except:
                    continue
            
            # Extract social/ academic links
            links = soup.find_all('a', href=True)
            for link in links:
                href = link.get('href', '').lower()
                if 'scholar.google.com' in href:
                    profile_data['google_scholar'] = link.get('href')
                elif 'researchgate.net' in href:
                    profile_data['research_gate'] = link.get('href')
                elif 'linkedin.com' in href:
                    profile_data['linkedin'] = link.get('href')
                elif 'http' in href and not any(x in href for x in ['scholar.google.com', 'researchgate.net', 'linkedin.com']):
                    profile_data['website'] = link.get('href')
            
            self.logger.info(f"Successfully extracted profile for: {profile_data['name']}")
            
        except Exception as e:
            self.logger.error(f"Error extracting profile from {profile_url}: {e}")
        
        return profile_data
    
    def scrape_all_faculty(self) -> List[Dict]:
        """Scrape all faculty profiles from HKUST-GZ"""
        all_profiles = []
        
        try:
            self.setup_driver()
            faculty_links = self.get_faculty_links()
            
            if not faculty_links:
                self.logger.warning("No faculty links found. Trying alternative approach...")
                # You might need to implement alternative scraping methods here
                return all_profiles
            
            self.logger.info(f"Starting to scrape {len(faculty_links)} faculty profiles")
            
            for i, link in enumerate(faculty_links, 1):
                try:
                    self.logger.info(f"Scraping profile {i}/{len(faculty_links)}")
                    profile_data = self.extract_faculty_profile(link)
                    
                    if profile_data['name']:  # Only add if we got some data
                        all_profiles.append(profile_data)
                    
                    # Save progress periodically
                    if i % 5 == 0:
                        self.save_progress(all_profiles, f"progress_{i}.json")
                    
                    time.sleep(self.delay)  # Be respectful to the server
                    
                except Exception as e:
                    self.logger.error(f"Error scraping profile {link}: {e}")
                    continue
            
            self.logger.info(f"Successfully scraped {len(all_profiles)} faculty profiles")
            
        except Exception as e:
            self.logger.error(f"Error in scrape_all_faculty: {e}")
        
        finally:
            self.close_driver()
        
        return all_profiles
    
    def save_progress(self, profiles: List[Dict], filename: str):
        """Save scraped data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(profiles, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Progress saved to {filename}")
        except Exception as e:
            self.logger.error(f"Error saving progress: {e}")
    
    def load_progress(self, filename: str) -> List[Dict]:
        """Load previously scraped data from JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading progress: {e}")
            return []

if __name__ == "__main__":
    # Test the scraper
    scraper = HKUSTGZScraper(headless=False, delay=3.0)
    profiles = scraper.scrape_all_faculty()
    
    # Save final results
    scraper.save_progress(profiles, "hkust_gz_faculty_profiles.json")
    print(f"Scraped {len(profiles)} faculty profiles") 