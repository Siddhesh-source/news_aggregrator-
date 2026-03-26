import json
import os
from pathlib import Path
import shutil

# Your Quatarly API key
API_KEY = "qua-ddbpsb3gs3u0pm6ciq8l5irdif7rvymwg27q"

# Path to settings.json
settings_path = Path.home() / ".factory" / "settings.json"

# Models to add
models = [
    {
        "model": "claude-sonnet-4-6-20250929",
        "id": "custom:claude-sonnet-4-6-20250929-0",
        "index": 0,
        "baseUrl": "https://api.quatarly.cloud/",
        "apiKey": API_KEY,
        "displayName": "claude-sonnet-4-6-20250929",
        "noImageSupport": False,
        "provider": "anthropic"
    },
    {
        "model": "claude-opus-4-6-thinking",
        "id": "custom:claude-opus-4-6-thinking-1",
        "index": 1,
        "baseUrl": "https://api.quatarly.cloud/",
        "apiKey": API_KEY,
        "displayName": "claude-opus-4-6-thinking",
        "noImageSupport": False,
        "provider": "anthropic"
    },
    {
        "model": "claude-haiku-4-5-20251001",
        "id": "custom:claude-haiku-4-5-20251001-2",
        "index": 2,
        "baseUrl": "https://api.quatarly.cloud/",
        "apiKey": API_KEY,
        "displayName": "claude-haiku-4-5-20251001",
        "noImageSupport": False,
        "provider": "anthropic"
    },
    {
        "model": "gemini-3.1-pro",
        "id": "custom:gemini-3.1-pro-3",
        "index": 3,
        "baseUrl": "https://api.quatarly.cloud/v1",
        "apiKey": API_KEY,
        "displayName": "gemini-3.1-pro",
        "noImageSupport": False,
        "provider": "openai"
    },
    {
        "model": "gemini-3-flash",
        "id": "custom:gemini-3-flash-4",
        "index": 4,
        "baseUrl": "https://api.quatarly.cloud/v1",
        "apiKey": API_KEY,
        "displayName": "gemini-3-flash",
        "noImageSupport": False,
        "provider": "openai"
    },
    {
        "model": "gpt-5.1",
        "id": "custom:gpt-5.1-5",
        "index": 5,
        "baseUrl": "https://api.quatarly.cloud/v1",
        "apiKey": API_KEY,
        "displayName": "gpt-5.1",
        "noImageSupport": False,
        "provider": "openai"
    },
    {
        "model": "gpt-5.1-codex",
        "id": "custom:gpt-5.1-codex-6",
        "index": 6,
        "baseUrl": "https://api.quatarly.cloud/v1",
        "apiKey": API_KEY,
        "displayName": "gpt-5.1-codex",
        "noImageSupport": False,
        "provider": "openai"
    },
    {
        "model": "gpt-5.1-codex-max",
        "id": "custom:gpt-5.1-codex-max-7",
        "index": 7,
        "baseUrl": "https://api.quatarly.cloud/v1",
        "apiKey": API_KEY,
        "displayName": "gpt-5.1-codex-max",
        "noImageSupport": False,
        "provider": "openai"
    },
    {
        "model": "gpt-5.2",
        "id": "custom:gpt-5.2-8",
        "index": 8,
        "baseUrl": "https://api.quatarly.cloud/v1",
        "apiKey": API_KEY,
        "displayName": "gpt-5.2",
        "noImageSupport": False,
        "provider": "openai"
    },
    {
        "model": "gpt-5.2-codex",
        "id": "custom:gpt-5.2-codex-9",
        "index": 9,
        "baseUrl": "https://api.quatarly.cloud/v1",
        "apiKey": API_KEY,
        "displayName": "gpt-5.2-codex",
        "noImageSupport": False,
        "provider": "openai"
    },
    {
        "model": "gpt-5.3-codex",
        "id": "custom:gpt-5.3-codex-10",
        "index": 10,
        "baseUrl": "https://api.quatarly.cloud/v1",
        "apiKey": API_KEY,
        "displayName": "gpt-5.3-codex",
        "noImageSupport": False,
        "provider": "openai"
    }
]

def main():
    print("Quatarly Custom Models Setup for Factory AI Droid")
    print("=" * 50)
    
    # Check if settings file exists
    if not settings_path.exists():
        print(f"❌ Settings file not found at: {settings_path}")
        print("\nPlease ensure Factory AI Droid is installed and you've logged in.")
        print("Run 'droid' command and login to create the settings file.")
        return
    
    # Backup original settings
    backup_path = settings_path.with_suffix('.json.backup')
    shutil.copy2(settings_path, backup_path)
    print(f"✓ Backup created: {backup_path}")
    
    # Read current settings
    with open(settings_path, 'r', encoding='utf-8') as f:
        settings = json.load(f)
    
    # Add or update customModels
    if 'customModels' not in settings:
        settings['customModels'] = []
    
    # Remove existing Quatarly models to avoid duplicates
    settings['customModels'] = [
        m for m in settings['customModels']
        if not m.get('baseUrl', '').startswith('https://api.quatarly.cloud')
    ]
    
    # Add new models
    settings['customModels'].extend(models)
    
    # Write updated settings
    with open(settings_path, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2)
    
    print(f"✓ Added {len(models)} Quatarly models to settings.json")
    print("\nModels added:")
    for model in models:
        print(f"  • {model['displayName']} ({model['provider']})")
    
    print("\n✓ Setup complete!")
    print("\nRestart Factory AI Droid to see the new models.")

if __name__ == "__main__":
    main()
