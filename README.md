# UPSC News Digest

Automated daily digest of top UPSC-relevant articles from PIB, The Hindu, and Indian Express.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
```

## Run

```bash
python main.py
```

Fetches articles → Analyzes with Gemini → Emails top 5 by prelims score.
