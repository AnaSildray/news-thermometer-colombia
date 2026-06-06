"""
Web scraper for Colombian news portals
Extracts articles and comments from multiple sources
"""

import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
from typing import List, Dict
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .sources import NEWS_SOURCES

logger = logging.getLogger(__name__)

class NewsScraper:
    """Scraper for Colombian news websites"""
    
    def __init__(self, timeout=10, retries=3):
        self.timeout = timeout
        self.retries = retries
        self.session = self._create_session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def _create_session(self):
        """Create a requests session with retry strategy"""
        session = requests.Session()
        retry_strategy = Retry(
            total=self.retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session
    
    def _get_page(self, url: str) -> BeautifulSoup:
        """Fetch and parse a webpage"""
        try:
            response = self.session.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            logger.warning(f"Error fetching {url}: {str(e)}")
            return None
    
    def _extract_comments(self, text: str) -> List[str]:
        """Extract or simulate comments from text"""
        if not text:
            return []
        
        # Simulated comments for demo purposes
        # In production, these would come from actual comment sections
        sample_comments = [
            "Excelente noticia para el país",
            "Esto es preocupante para nuestro futuro",
            "Información interesante sobre la actualidad",
            "Muy importante que se conozca esto",
            "Qué noticia tan negativa",
            "Este es un buen avance para Colombia",
            "No estoy de acuerdo con esto",
            "Esperemos que mejore la situación"
        ]
        
        import random
        num_comments = random.randint(3, 8)
        return random.sample(sample_comments, min(num_comments, len(sample_comments)))
    
    def scrape_el_tiempo(self, limit: int = 5) -> List[Dict]:
        """Scrape El Tiempo news"""
        articles = []
        try:
            url = "https://www.eltiempo.com/colombia"
            soup = self._get_page(url)
            
            if not soup:
                return articles
            
            # Find article elements
            article_elements = soup.find_all('article', limit=limit)
            
            for article_elem in article_elements[:limit]:
                try:
                    title_elem = article_elem.find('h2')
                    link_elem = article_elem.find('a')
                    
                    if title_elem and link_elem:
                        title = title_elem.get_text(strip=True)
                        link = link_elem.get('href', '')
                        
                        if title and link:
                            comments = self._extract_comments(title)
                            articles.append({
                                'title': title[:100],
                                'url': link if link.startswith('http') else 'https://www.eltiempo.com' + link,
                                'source': 'El Tiempo',
                                'published_at': datetime.now().isoformat(),
                                'comments': comments
                            })
                except Exception as e:
                    logger.debug(f"Error parsing El Tiempo article: {str(e)}")
                    continue
        
        except Exception as e:
            logger.warning(f"Error scraping El Tiempo: {str(e)}")
        
        return articles
    
    def scrape_caracol(self, limit: int = 5) -> List[Dict]:
        """Scrape Caracol Noticias"""
        articles = []
        try:
            url = "https://www.caracolnoticias.com"
            soup = self._get_page(url)
            
            if not soup:
                return articles
            
            article_elements = soup.find_all('article', limit=limit)
            
            for article_elem in article_elements[:limit]:
                try:
                    title_elem = article_elem.find('h2')
                    link_elem = article_elem.find('a')
                    
                    if title_elem and link_elem:
                        title = title_elem.get_text(strip=True)
                        link = link_elem.get('href', '')
                        
                        if title and link:
                            comments = self._extract_comments(title)
                            articles.append({
                                'title': title[:100],
                                'url': link if link.startswith('http') else 'https://www.caracolnoticias.com' + link,
                                'source': 'Caracol Noticias',
                                'published_at': datetime.now().isoformat(),
                                'comments': comments
                            })
                except Exception as e:
                    logger.debug(f"Error parsing Caracol article: {str(e)}")
                    continue
            
            time.sleep(1)
        except Exception as e:
            logger.warning(f"Error scraping Caracol: {str(e)}")
        
        return articles
    
    def scrape_rcn(self, limit: int = 5) -> List[Dict]:
        """Scrape RCN Noticias"""
        articles = []
        try:
            url = "https://www.rcnradio.com"
            soup = self._get_page(url)
            
            if not soup:
                return articles
            
            article_elements = soup.find_all('article', limit=limit)
            
            for article_elem in article_elements[:limit]:
                try:
                    title_elem = article_elem.find('h2')
                    link_elem = article_elem.find('a')
                    
                    if title_elem and link_elem:
                        title = title_elem.get_text(strip=True)
                        link = link_elem.get('href', '')
                        
                        if title and link:
                            comments = self._extract_comments(title)
                            articles.append({
                                'title': title[:100],
                                'url': link if link.startswith('http') else 'https://www.rcnradio.com' + link,
                                'source': 'RCN Noticias',
                                'published_at': datetime.now().isoformat(),
                                'comments': comments
                            })
                except Exception as e:
                    logger.debug(f"Error parsing RCN article: {str(e)}")
                    continue
            
            time.sleep(1)
        except Exception as e:
            logger.warning(f"Error scraping RCN: {str(e)}")
        
        return articles
    
    def scrape_lafm(self, limit: int = 5) -> List[Dict]:
        """Scrape La FM news"""
        articles = []
        try:
            url = "https://www.lafm.com.co"
            soup = self._get_page(url)
            
            if not soup:
                return articles
            
            article_elements = soup.find_all('article', limit=limit)
            
            for article_elem in article_elements[:limit]:
                try:
                    title_elem = article_elem.find('h2')
                    link_elem = article_elem.find('a')
                    
                    if title_elem and link_elem:
                        title = title_elem.get_text(strip=True)
                        link = link_elem.get('href', '')
                        
                        if title and link:
                            comments = self._extract_comments(title)
                            articles.append({
                                'title': title[:100],
                                'url': link if link.startswith('http') else 'https://www.lafm.com.co' + link,
                                'source': 'La FM',
                                'published_at': datetime.now().isoformat(),
                                'comments': comments
                            })
                except Exception as e:
                    logger.debug(f"Error parsing La FM article: {str(e)}")
                    continue
            
            time.sleep(1)
        except Exception as e:
            logger.warning(f"Error scraping La FM: {str(e)}")
        
        return articles
    
    def scrape_all(self, limit: int = 5) -> List[Dict]:
        """Scrape all configured news sources"""
        all_articles = []
        
        logger.info(f"Starting scrape of all sources (limit={limit} per source)")
        
        # Scrape from each source
        all_articles.extend(self.scrape_el_tiempo(limit=limit))
        all_articles.extend(self.scrape_caracol(limit=limit))
        all_articles.extend(self.scrape_rcn(limit=limit))
        all_articles.extend(self.scrape_lafm(limit=limit))
        
        logger.info(f"Scraped {len(all_articles)} articles from all sources")
        
        return all_articles
    
    def get_available_sources(self) -> Dict[str, str]:
        """Get list of available news sources"""
        return {
            'el_tiempo': 'El Tiempo',
            'caracol': 'Caracol Noticias',
            'rcn': 'RCN Noticias',
            'lafm': 'La FM'
        }
