import feedparser
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def fetch_articles():
    """
    Fetch articles from PIB, The Hindu, and Indian Express RSS feeds.
    
    Returns:
        list: List of dicts with title, content, and source fields (15 articles total, 5 from each source)
    """
    feeds = [
        {
            "name": "PIB",
            "url": "https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=3"
        },
        {
            "name": "The Hindu",
            "url": "https://www.thehindu.com/news/national/feeder/default.rss"
        },
        {
            "name": "Indian Express",
            "url": "https://indianexpress.com/section/india/feed/"
        }
    ]
    
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    articles = []
    
    for feed_info in feeds:
        feed_name = feed_info["name"]
        feed_url = feed_info["url"]
        
        try:
            logger.info(f"Fetching articles from {feed_name}...")
            
            # Parse feed with custom User-Agent header
            feed = feedparser.parse(feed_url, request_headers={"User-Agent": user_agent})
            
            # Check if feed was parsed successfully
            if feed.bozo and hasattr(feed, 'bozo_exception'):
                logger.warning(f"Feed parsing warning for {feed_name}: {feed.bozo_exception}")
            
            # Extract up to 5 most recent articles
            entries = feed.entries[:5]
            
            for entry in entries:
                article = {
                    "title": entry.get("title", "No title"),
                    "content": entry.get("description", entry.get("summary", "No content available")),
                    "source": feed_name,
                    "url": entry.get("link", "#"),
                    "published": entry.get("published", "Recently")
                }
                articles.append(article)
            
            logger.info(f"Successfully fetched {len(entries)} articles from {feed_name}")
            
        except Exception as e:
            logger.error(f"Error fetching articles from {feed_name}: {e}")
            continue
    
    logger.info(f"Total articles fetched: {len(articles)}")
    return articles


if __name__ == "__main__":
    # Test the scraper
    print("Fetching articles from RSS feeds...\n")
    
    articles = fetch_articles()
    
    print(f"\nFetched {len(articles)} articles:\n")
    print("=" * 80)
    
    for i, article in enumerate(articles, 1):
        print(f"\n{i}. [{article['source']}] {article['title']}")
        print(f"   URL: {article['url']}")
        print(f"   Published: {article['published']}")
        print(f"   Content preview: {article['content'][:150]}...")
        print("-" * 80)
