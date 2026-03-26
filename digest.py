import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def send_digest(articles):
    """
    Send a digest email with top 5 articles sorted by prelims_score.
    
    Args:
        articles: List of dicts with title, category, prelims_score, exam_angle, summary
    """
    # Sort by prelims_score descending and take top 5
    top_articles = sorted(articles, key=lambda x: x.get('prelims_score', 0), reverse=True)[:5]
    
    if not top_articles:
        logger.warning("No articles to send in digest")
        return
    
    # Get SMTP credentials from environment
    smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', 587))
    smtp_user = os.environ.get('SMTP_USER')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    from_email = os.environ.get('SMTP_FROM_EMAIL', smtp_user)
    from_name = os.environ.get('SMTP_FROM_NAME', 'UPSC News Digest')
    recipient = os.environ.get('DIGEST_RECIPIENT')
    
    if not all([smtp_user, smtp_password, recipient]):
        raise ValueError("Missing required environment variables: SMTP_USER, SMTP_PASSWORD, or DIGEST_RECIPIENT")
    
    # Build HTML email
    html_content = build_html_email(top_articles)
    
    # Create email message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'UPSC Daily Digest - Top {len(top_articles)} Articles'
    msg['From'] = f'{from_name} <{from_email}>'
    msg['To'] = recipient
    
    # Attach HTML content
    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)
    
    # Send email
    try:
        logger.info(f"Connecting to SMTP server {smtp_host}:{smtp_port}...")
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        
        logger.info(f"Digest email sent successfully to {recipient}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send digest email: {e}")
        raise


def build_html_email(articles):
    """
    Build HTML email content with article cards.
    
    Args:
        articles: List of article dicts
        
    Returns:
        str: HTML content
    """
    # Category color mapping
    category_colors = {
        'Polity': '#3B82F6',
        'Economy': '#10B981',
        'Environment': '#22C55E',
        'Science & Tech': '#8B5CF6',
        'International Relations': '#F59E0B',
        'History & Culture': '#EC4899',
        'Social Issues': '#EF4444',
        'Security & Defence': '#6366F1'
    }
    
    cards_html = ""
    for article in articles:
        category = article.get('category', 'General')
        color = category_colors.get(category, '#6B7280')
        
        cards_html += f"""
        <div style="background: white; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="display: flex; align-items: center; margin-bottom: 12px;">
                <span style="background: {color}; color: white; padding: 4px 12px; border-radius: 4px; font-size: 12px; font-weight: 600; margin-right: 10px;">
                    {category}
                </span>
                <span style="background: #FEF3C7; color: #92400E; padding: 4px 12px; border-radius: 4px; font-size: 12px; font-weight: 600;">
                    Prelims Score: {article.get('prelims_score', 'N/A')}/10
                </span>
            </div>
            <h2 style="color: #1F2937; font-size: 18px; margin: 0 0 12px 0; font-weight: 600;">
                {article.get('title', 'No Title')}
            </h2>
            <div style="background: #F3F4F6; padding: 12px; border-left: 3px solid {color}; margin-bottom: 12px; border-radius: 4px;">
                <p style="margin: 0; color: #374151; font-size: 14px; font-style: italic;">
                    <strong>Exam Angle:</strong> {article.get('exam_angle', 'N/A')}
                </p>
            </div>
            <p style="color: #4B5563; font-size: 14px; line-height: 1.6; margin: 0;">
                {article.get('summary', 'No summary available')}
            </p>
        </div>
        """
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; background-color: #F9FAFB; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 8px 8px 0 0; text-align: center;">
                <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 700;">
                    📰 UPSC Daily Digest
                </h1>
                <p style="color: #E0E7FF; margin: 8px 0 0 0; font-size: 14px;">
                    Top {len(articles)} Articles for Your Preparation
                </p>
            </div>
            <div style="background: #F3F4F6; padding: 20px;">
                {cards_html}
            </div>
            <div style="background: #1F2937; padding: 20px; border-radius: 0 0 8px 8px; text-align: center;">
                <p style="color: #9CA3AF; margin: 0; font-size: 12px;">
                    This digest was automatically generated for UPSC preparation
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html


if __name__ == "__main__":
    # Test with sample articles
    test_articles = [
        {
            "title": "New Digital Public Infrastructure for Healthcare Launched",
            "category": "Science & Tech",
            "prelims_score": 9,
            "exam_angle": "Important for understanding government's digital governance initiatives and healthcare reforms.",
            "summary": "Government launches comprehensive DPI for healthcare under Ayushman Bharat Digital Mission. Will integrate health databases and enable telemedicine in rural areas using blockchain and AI technologies."
        },
        {
            "title": "India-US Trade Agreement Negotiations Progress",
            "category": "International Relations",
            "prelims_score": 8,
            "exam_angle": "Relevant for understanding bilateral trade relations and India's foreign policy priorities.",
            "summary": "Trade ministers discuss tariff reductions and market access. Focus on technology transfer and defense cooperation as part of broader strategic partnership."
        },
        {
            "title": "Supreme Court Ruling on Article 370",
            "category": "Polity",
            "prelims_score": 10,
            "exam_angle": "Critical constitutional development affecting federal structure and special provisions.",
            "summary": "SC upholds abrogation of Article 370, impacting Jammu & Kashmir's special status. Landmark judgment with implications for constitutional law and center-state relations."
        }
    ]
    
    print("Testing digest email...\n")
    
    try:
        send_digest(test_articles)
        print("✓ Digest email sent successfully!")
    except Exception as e:
        print(f"✗ Error: {e}")
