import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import argparse
import os
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("wikipedia_scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WikipediaScraper:
    """
    A class to scrape information from Wikipedia based on keywords.
    """
    def __init__(self):
        self.base_url = "https://en.wikipedia.org/wiki/"
        self.search_url = "https://en.wikipedia.org/w/index.php?search="
        self.session = requests.Session()
        # Set a user agent to avoid being blocked
        self.session.headers.update({
            'User-Agent': 'WikipediaScraper/1.0 (Educational Project; contact@example.com)'
        })
    
    def search_wikipedia(self, keyword):
        """
        Search Wikipedia for a keyword and return the URL of the best match.
        """
        logger.info(f"Searching for: {keyword}")
        
        # Replace spaces with '+' for the search URL
        search_term = keyword.replace(' ', '+')
        search_response = self.session.get(f"{self.search_url}{search_term}")
        
        # Check if we were redirected directly to an article
        if "/wiki/" in search_response.url and "index.php?search=" not in search_response.url:
            logger.info(f"Direct match found: {search_response.url}")
            return search_response.url
        
        # If not redirected, parse the search results
        soup = BeautifulSoup(search_response.text, 'html.parser')
        search_results = soup.select('.mw-search-result-heading a')
        
        if search_results:
            # Get the first result URL
            first_result = search_results[0].get('href')
            full_url = f"https://en.wikipedia.org{first_result}"
            logger.info(f"Best match found: {full_url}")
            return full_url
        
        logger.warning(f"No results found for: {keyword}")
        return None
    
    def get_article_content(self, url):
        """
        Extract relevant content from a Wikipedia article.
        """
        logger.info(f"Fetching content from: {url}")
        
        response = self.session.get(url)
        if response.status_code != 200:
            logger.error(f"Failed to retrieve article: {response.status_code}")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title
        title = soup.select_one('#firstHeading').text.strip()
        
        # Extract summary (first paragraph of the article)
        paragraphs = soup.select('#mw-content-text p')
        summary = ""
        for p in paragraphs:
            # Skip empty paragraphs or those with only images
            if p.text.strip() and not p.find('img'):
                summary = p.text.strip()
                break
        
        # Extract infobox data if available
        infobox_data = {}
        infobox = soup.select_one('.infobox')
        if infobox:
            rows = infobox.select('tr')
            for row in rows:
                header = row.select_one('th')
                data = row.select_one('td')
                if header and data:
                    key = header.text.strip()
                    value = data.text.strip()
                    infobox_data[key] = value
        
        # Extract sections and their content
        sections = {}
        current_section = None
        
        for element in soup.select('#mw-content-text > div > h2, #mw-content-text > div > h3, #mw-content-text > div > p'):
            if element.name in ['h2', 'h3']:
                # Remove the edit section links from the heading text
                for span in element.select('.mw-editsection'):
                    span.decompose()
                current_section = element.text.strip()
                sections[current_section] = ""
            elif element.name == 'p' and current_section:
                sections[current_section] += element.text.strip() + " "
        
        # Extract references
        references = []
        refs = soup.select('.reference-text')
        for ref in refs:
            references.append(ref.text.strip())
        
        # Extract all links
        links = []
        for link in soup.select('#mw-content-text a'):
            href = link.get('href', '')
            if href.startswith('/wiki/') and ':' not in href:
                links.append({
                    'text': link.text.strip(),
                    'url': f"https://en.wikipedia.org{href}"
                })
        
        # Extract images
        images = []
        for img in soup.select('.image img'):
            src = img.get('src', '')
            if not src.startswith('http'):
                src = f"https:{src}"
            images.append({
                'src': src,
                'alt': img.get('alt', '')
            })
        
        article_data = {
            'title': title,
            'url': url,
            'summary': summary,
            'infobox': infobox_data,
            'sections': sections,
            'references': references,
            'links': links,
            'images': images
        }
        
        return article_data
    
    def scrape_keywords(self, keywords, output_dir='output'):
        """
        Scrape Wikipedia for a list of keywords and save the results.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        results = []
        
        for keyword in keywords:
            url = self.search_wikipedia(keyword)
            if url:
                article_data = self.get_article_content(url)
                if article_data:
                    article_data['keyword'] = keyword
                    results.append(article_data)
                    
                    # Save individual article data as JSON
                    filename = re.sub(r'[^\w\s]', '', keyword).replace(' ', '_').lower()
                    pd.DataFrame([article_data]).to_json(
                        f"{output_dir}/{filename}.json", 
                        orient='records', 
                        lines=True
                    )
                    logger.info(f"Saved data for '{keyword}' to {filename}.json")
            
            # Add a small delay to avoid overloading Wikipedia's servers
            import time
            time.sleep(1)
        
        if results:
            # Create a summary CSV with basic information
            summary_data = []
            for item in results:
                summary_data.append({
                    'keyword': item['keyword'],
                    'title': item['title'],
                    'url': item['url'],
                    'summary': item['summary'][:200] + '...' if len(item['summary']) > 200 else item['summary']
                })
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_csv(f"{output_dir}/wikipedia_summary_{timestamp}.csv", index=False)
            logger.info(f"Saved summary to wikipedia_summary_{timestamp}.csv")
        
        return results

def main():
    parser = argparse.ArgumentParser(description='Scrape Wikipedia articles based on keywords')
    parser.add_argument('--keywords', nargs='+', required=True, help='Keywords to search for')
    parser.add_argument('--output', default='output', help='Output directory for scraped data')
    
    args = parser.parse_args()
    
    scraper = WikipediaScraper()
    results = scraper.scrape_keywords(args.keywords, args.output)
    
    print(f"Scraped {len(results)} articles successfully!")

if __name__ == "__main__":
    main()
