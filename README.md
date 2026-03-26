# NewsNexus - Autonomous UPSC Intelligence System

Autonomous AI-powered news aggregation and analysis for UPSC preparation. Fetches articles from PIB, The Hindu, and Indian Express, analyzes with Gemini AI, and delivers premium newsletter-style digest via email.

## Features

- **Autonomous Scraping**: Multi-source RSS feed aggregation
- **AI Analysis**: Gemini-powered UPSC relevance scoring (Prelims/Mains)
- **Premium Newsletter**: Aeon-inspired email design
- **Detailed PDF**: Comprehensive analysis with exam angles and revision notes
- **Automated Delivery**: Scheduled daily digest

## Project Structure

```
News_aggregrator/
├── src/
│   ├── agents/              # Core agents
│   │   ├── scraper.py       # RSS scraper
│   │   ├── analyser.py      # Gemini analyzer
│   │   └── digest.py        # Email & PDF generator
│   └── utils/               # Utilities
│       └── pdf_generator.py # PDF generation
├── config/
│   └── .env.example         # Environment template
├── output/                  # Generated files
├── main.py                  # Main orchestrator
└── requirements.txt         # Dependencies
```

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp config/.env.example .env
# Edit .env with your credentials:
# - GEMINI_API_KEY
# - SMTP_USER, SMTP_PASSWORD
# - DIGEST_RECIPIENT
```

## Usage

```bash
# Run once
python main.py

# Schedule quarterly
python setup_quatarly.py
```

## Output

- Email digest with top 5 articles
- PDF analysis in `output/` directory
- HTML preview for testing

## Architecture

**Workflow**: Scraper → Analyser → Digest → Email

**Agents**:
- Scraper: Fetches from PIB, The Hindu, Indian Express
- Analyser: Scores articles for UPSC relevance
- Digest: Generates premium newsletter + PDF

## Design

Premium newsletter aesthetic:
- Dark header, muted colors
- Editorial layout, natural flow
- Professional typography
- Sophisticated spacing

## License

MIT
