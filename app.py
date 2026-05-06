
import base64
import json
import os
from io import BytesIO
from typing import Dict, List, Optional

import streamlit as st
from google import genai
from google.genai import types
from PIL import Image


# -----------------------------
# LoreKraft: AI Dungeon + Comic Visuals
# -----------------------------

st.set_page_config(
    page_title="LoreKraft",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)

TEXT_MODEL = "gemini-2.5-flash"
# You can change this to a newer image model available in your AI Studio account.
IMAGE_MODEL = "gemini-2.5-flash-image"


LOREKRAFT_SYSTEM_PROMPT = """
You are LoreKraft, an AI Dungeon Master for a visual fantasy role-playing story app.

Style:
- Immersive, cinematic, fantasy adventure tone.
- Write like a storybook/comic narrator.
- Keep scenes concise enough for a web app.
- Always give the player meaningful choices.
- Maintain continuity with the character, inventory, allies, enemies, setting, and previous choices.

Safety:
- Keep content PG-13 fantasy.
- Avoid graphic gore or sexual content.

Output strictly as JSON with this exact schema:
{
  "title": "short scene title",
  "story": "2-4 vivid paragraphs of story",
  "choices": ["choice 1", "choice 2", "choice 3"],
  "visual_prompt": "detailed prompt for a fantasy comic panel, no text in image",
  "npc_emotion": "one emotion word",
  "inventory_update": ["item 1", "item 2"],
  "quest_log": ["quest objective 1", "quest objective 2"]
}
"""


def get_api_key() -> Optional[str]:
    """Read Gemini API key from Streamlit secrets or environment variable."""
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    return os.getenv("GEMINI_API_KEY")


@st.cache_resource
def get_client(api_key: str):
    return genai.Client(api_key=api_key)


def extract_json(text: str) -> Dict:
    """Gemini usually follows JSON, but this protects against markdown fences."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json", "").replace("```", "").strip()

    start = cleaned.find("{")
    end = cleaned.rfind("}") + 1
    if start >= 0 and end > start:
        cleaned = cleaned[start:end]

    return json.loads(cleaned)


def generate_scene(client, character: Dict, history: List[Dict], player_choice: str = "") -> Dict:
    history_text = "\n".join(
        [
            f"Scene {i+1}: {h.get('title', '')}\nPlayer chose: {h.get('player_choice', '')}\nOutcome: {h.get('story', '')[:700]}"
            for i, h in enumerate(history[-5:])
        ]
    )

    prompt = f"""
{LOREKRAFT_SYSTEM_PROMPT}

PLAYER CHARACTER:
{json.dumps(character, indent=2)}

RECENT STORY HISTORY:
{history_text if history_text else "No previous scenes. Start the adventure."}

PLAYER'S LATEST CHOICE:
{player_choice if player_choice else "Start the story with an exciting opening scene."}

Create the next interactive RPG scene.
"""

    response = client.models.generate_content(
        model=TEXT_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.9,
            response_mime_type="application/json",
        ),
    )

    return extract_json(response.text)


def generate_image(client, visual_prompt: str) -> Optional[Image.Image]:
    prompt = f"""
Create a single cinematic fantasy comic-book panel for LoreKraft.

Requirements:
- No text, no captions, no speech bubbles.
- Mystical forest / ancient map / tabletop RPG atmosphere when appropriate.
- Dramatic lighting, painterly fantasy art, highly detailed.
- Keep it PG-13.

Scene:
{visual_prompt}
"""

    try:
        response = client.models.generate_content(
            model=IMAGE_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"]
            ),
        )

        for part in response.candidates[0].content.parts:
            if getattr(part, "inline_data", None):
                image_bytes = part.inline_data.data
                return Image.open(BytesIO(image_bytes))
    except Exception as e:
        st.warning(f"Image generation skipped: {e}")

    return None


def add_scene_to_history(scene: Dict, player_choice: str = ""):
    scene_copy = dict(scene)
    scene_copy["player_choice"] = player_choice
    st.session_state.history.append(scene_copy)


def reset_game():
    st.session_state.history = []
    st.session_state.character_created = False
    st.session_state.character = {}
    st.session_state.current_scene = None
    st.session_state.current_image = None


# -----------------------------
# Session defaults
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []
if "character_created" not in st.session_state:
    st.session_state.character_created = False
if "character" not in st.session_state:
    st.session_state.character = {}
if "current_scene" not in st.session_state:
    st.session_state.current_scene = None
if "current_image" not in st.session_state:
    st.session_state.current_image = None


# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
    .main {
        background: radial-gradient(circle at top, #182034 0, #0d1117 45%, #07090d 100%);
    }
    .block-container {
        padding-top: 1.5rem;
    }
    .hero-card {
        padding: 1.3rem;
        border-radius: 22px;
        background: linear-gradient(135deg, rgba(44, 62, 80, .95), rgba(20, 25, 35, .95));
        border: 1px solid rgba(255,255,255,.12);
        box-shadow: 0 12px 35px rgba(0,0,0,.35);
    }
    .scene-card {
        padding: 1.2rem;
        border-radius: 20px;
        background: rgba(255,255,255,.06);
        border: 1px solid rgba(255,255,255,.1);
    }
    .small-muted {
        color: #b7c0d8;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.title("🗺️ LoreKraft")
    st.caption("AI Dungeon Master + visual comic panels")

    api_key = get_api_key()

    if not api_key:
        st.error("Add your Gemini API key first.")
        st.code(
            """
# .streamlit/secrets.toml
GEMINI_API_KEY = "your_api_key_here"
            """.strip()
        )
        st.stop()

    client = get_client(api_key)

    st.divider()
    st.subheader("Character Builder")

    with st.form("character_form"):
        name = st.text_input("Character name", value=st.session_state.character.get("name", "Astra"))
        role = st.selectbox(
            "Class",
            ["Ranger", "Mage", "Rogue", "Paladin", "Bard", "Druid", "Warrior"],
            index=0,
        )
        species = st.selectbox(
            "Ancestry",
            ["Human", "Elf", "Dwarf", "Tiefling", "Halfling", "Dragonborn", "Custom"],
            index=1,
        )
        personality = st.text_area(
            "Personality",
            value=st.session_state.character.get(
                "personality",
                "Curious, brave, sarcastic under pressure, loyal to friends."
            ),
        )
        goal = st.text_area(
            "Main quest goal",
            value=st.session_state.character.get(
                "goal",
                "Find the lost Moonstone Map before the shadow guild reaches it."
            ),
        )
        world = st.text_area(
            "World vibe",
            value=st.session_state.character.get(
                "world",
                "Mystical forests, forgotten ruins, candlelit taverns, ancient maps, strange magic."
            ),
        )

        submitted = st.form_submit_button("Create / Update Character")

    if submitted:
        st.session_state.character = {
            "name": name,
            "class": role,
            "ancestry": species,
            "personality": personality,
            "goal": goal,
            "world": world,
        }
        st.session_state.character_created = True
        st.success("Character saved.")

    if st.button("Reset Adventure"):
        reset_game()
        st.rerun()


# -----------------------------
# Main page
# -----------------------------
st.markdown(
    """
    <div class="hero-card">
        <h1>✨ LoreKraft</h1>
        <p class="small-muted">
        Build a fantasy RPG story where Gemini acts as the AI Dungeon Master and turns major scenes into comic-style visuals.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

if not st.session_state.character_created:
    st.info("Start by creating your character in the sidebar.")
    st.stop()

col_left, col_right = st.columns([1.05, 0.95], gap="large")

with col_left:
    st.subheader("📜 Story")

    if st.session_state.current_scene is None:
        if st.button("Begin Adventure", type="primary"):
            with st.spinner("The ancient scroll is opening..."):
                scene = generate_scene(client, st.session_state.character, st.session_state.history)
                add_scene_to_history(scene)
                st.session_state.current_scene = scene
                st.session_state.current_image = generate_image(client, scene["visual_prompt"])
                st.rerun()
    else:
        scene = st.session_state.current_scene
        st.markdown(f"### {scene.get('title', 'Untitled Scene')}")
        st.markdown(f"<div class='scene-card'>{scene.get('story', '')}</div>", unsafe_allow_html=True)

        st.write("")
        st.markdown("#### What do you do next?")

        choices = scene.get("choices", [])
        for idx, choice in enumerate(choices):
            if st.button(choice, key=f"choice_{idx}", use_container_width=True):
                with st.spinner("The Dungeon Master is reshaping the story..."):
                    next_scene = generate_scene(
                        client,
                        st.session_state.character,
                        st.session_state.history,
                        player_choice=choice,
                    )
                    add_scene_to_history(next_scene, choice)
                    st.session_state.current_scene = next_scene
                    st.session_state.current_image = generate_image(client, next_scene["visual_prompt"])
                    st.rerun()

        custom_choice = st.text_input("Or type your own action")
        if st.button("Submit Custom Action", use_container_width=True):
            if custom_choice.strip():
                with st.spinner("The world responds to your decision..."):
                    next_scene = generate_scene(
                        client,
                        st.session_state.character,
                        st.session_state.history,
                        player_choice=custom_choice.strip(),
                    )
                    add_scene_to_history(next_scene, custom_choice.strip())
                    st.session_state.current_scene = next_scene
                    st.session_state.current_image = generate_image(client, next_scene["visual_prompt"])
                    st.rerun()

with col_right:
    st.subheader("🎨 Comic Panel")

    if st.session_state.current_image:
        st.image(st.session_state.current_image, use_container_width=True)
    else:
        st.info("Your AI-generated scene visual will appear here.")

    if st.session_state.current_scene:
        scene = st.session_state.current_scene
        st.markdown("#### 🧠 NPC Mood")
        st.write(scene.get("npc_emotion", "unknown"))

        st.markdown("#### 🎒 Inventory")
        inv = scene.get("inventory_update", [])
        if inv:
            for item in inv:
                st.write(f"- {item}")
        else:
            st.write("No items yet.")

        st.markdown("#### 🧭 Quest Log")
        quests = scene.get("quest_log", [])
        if quests:
            for q in quests:
                st.write(f"- {q}")
        else:
            st.write("No active quests yet.")

st.divider()

with st.expander("📚 Adventure History"):
    if not st.session_state.history:
        st.write("No scenes yet.")
    for i, h in enumerate(st.session_state.history, start=1):
        st.markdown(f"**Scene {i}: {h.get('title', 'Untitled')}**")
        if h.get("player_choice"):
            st.caption(f"Choice: {h['player_choice']}")
        st.write(h.get("story", "")[:500] + ("..." if len(h.get("story", "")) > 500 else ""))

with st.expander("🛠️ Future Features to Add"):
    st.write(
        """
        - Save/load campaigns with a database
        - Multiplayer shared sessions
        - Character portrait generator
        - DM mode for manually editing scenes
        - Sound effects and music
        - Map generation
        - Marketplace for reusable monsters, NPCs, and locations
        """
    )
