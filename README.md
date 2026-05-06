# LoreKraft — Streamlit + Google AI Studio API

LoreKraft is an AI-powered fantasy RPG prototype inspired by the idea of turning tabletop storytelling into a visual, player-driven comic adventure.

## Features

- AI Dungeon Master
- Character builder
- Interactive player choices
- Custom player actions
- Quest log
- Inventory updates
- NPC emotion tracking
- AI-generated fantasy comic panels

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Get a Gemini API key

Create an API key in Google AI Studio.

### 3. Add your API key

Create this file:

```bash
.streamlit/secrets.toml
```

Add:

```toml
GEMINI_API_KEY = "your_api_key_here"
```

### 4. Run the app

```bash
streamlit run app.py
```

## Deploy to Streamlit Community Cloud

1. Upload `app.py`, `requirements.txt`, and this README to GitHub.
2. Go to Streamlit Community Cloud.
3. Create a new app from your GitHub repo.
4. Add this secret in the app settings:

```toml
GEMINI_API_KEY = "your_api_key_here"
```

## Notes

The app uses Gemini for story generation and Gemini image generation for comic-style panels. If image generation is unavailable in your account or region, the story features should still work.
