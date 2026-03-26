import os
import sys
from dotenv import load_dotenv
from src.agents import fetch_articles, analyse_article, send_digest

# Load environment variables
load_dotenv()

# Fix Windows console encoding issues
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


def main():
    """
    Main orchestrator for the UPSC news digest pipeline.
    """
    try:
        # Step 1: Fetch articles from RSS feeds
        print("[SCRAPER AGENT] Fetching articles...")
        articles = fetch_articles()
        
        if not articles:
            print("[ERROR] No articles fetched. Exiting.")
            return
        
        print(f"[SCRAPER AGENT] Fetched {len(articles)} articles\n")
        
        # Step 2: Analyze each article with Gemini
        analyzed_articles = []
        
        for article in articles:
            title = article['title']
            content = article['content']
            source = article['source']
            
            print(f"[ANALYSER AGENT] Analysing: {title}")
            
            try:
                analysis = analyse_article(title, content)
                
                # Combine original article data with analysis
                analyzed_article = {
                    'title': title,
                    'source': source,
                    'url': article.get('url', '#'),
                    'published': article.get('published', 'Recently'),
                    'category': analysis['category'],
                    'prelims_score': analysis['prelims_score'],
                    'mains_score': analysis['mains_score'],
                    'exam_angle': analysis['exam_angle'],
                    'summary': analysis['summary']
                }
                
                analyzed_articles.append(analyzed_article)
                
                print(f"  → Category: {analysis['category']}, Prelims Score: {analysis['prelims_score']}/10\n")
                
            except Exception as e:
                print(f"  → Error analyzing article: {e}\n")
                continue
        
        if not analyzed_articles:
            print("[ERROR] No articles were successfully analyzed. Exiting.")
            return
        
        print(f"[ANALYSER AGENT] Successfully analyzed {len(analyzed_articles)} articles\n")
        
        # Step 3: Send digest email
        print("[DIGEST AGENT] Sending email digest...")
        send_digest(analyzed_articles)
        
        # Step 4: Success
        print("[DONE] Digest delivered successfully")
        
    except Exception as e:
        print(f"[ERROR] Pipeline failed: {e}")
        raise


if __name__ == "__main__":
    main()
