# LoreKraft 🗺️✨

### From Scrolls to Screens — Reimagining Storytelling Through AI

LoreKraft is an AI-powered fantasy storytelling platform that transforms interactive role-playing adventures into immersive visual experiences. Inspired by the creativity of tabletop RPGs and the accessibility of modern AI, LoreKraft combines dynamic narrative generation, character-driven decision making, and cinematic comic-style visuals into one interactive web application.

Built using **Streamlit** and **Google Gemini AI**, the platform acts as a personalized AI Dungeon Master that adapts the story based on player choices while generating rich fantasy scenes and evolving questlines in real time.

---

## 🌟 Project Vision

LoreKraft was created to explore how AI can modernize storytelling while preserving the imagination and collaborative spirit of traditional role-playing games.

The goal is to create a platform where:

* Every player experiences a unique story
* AI adapts to user decisions dynamically
* Fantasy worlds feel alive and visually immersive
* Storytelling becomes accessible to both gamers and casual users

This project was inspired by the idea of blending:

* Tabletop RPG mechanics
* AI-generated narratives
* Visual world-building
* Interactive web applications

---

## 🚀 Live Demo

### 🔗 Streamlit Application

[https://lorekraft-lkagj2jo4c8ziuue4dt85r.streamlit.app/](https://lorekraft-lkagj2jo4c8ziuue4dt85r.streamlit.app/)

### 📝 Medium Article

[https://medium.com/@bhashyam.srija1103/from-scrolls-to-screens-weaving-the-web-of-lorekraft-746b8adf62df](https://medium.com/@bhashyam.srija1103/from-scrolls-to-screens-weaving-the-web-of-lorekraft-746b8adf62df)

### 🎨 Figma Prototype

[https://www.figma.com/proto/ldks56uQDxrdEqqgvdeZP3/Lorekraft?embed_origin=cdn.embedly.com&kind=proto&node-id=19-55&starting-point-node-id=19%3A55](https://www.figma.com/proto/ldks56uQDxrdEqqgvdeZP3/Lorekraft?embed_origin=cdn.embedly.com&kind=proto&node-id=19-55&starting-point-node-id=19%3A55)

---

# ✨ Features

## 🧙 AI Dungeon Master

Gemini AI dynamically generates story scenes, quests, characters, and branching narrative paths based on player decisions.

## 🎭 Character Creation

Players can customize:

* Character name
* Class
* Ancestry
* Personality
* World setting
* Main quest objective

## 📖 Interactive Storytelling

Every choice impacts the direction of the adventure, creating personalized fantasy experiences.

## 🎨 AI-Generated Visual Panels

The application generates cinematic fantasy scene prompts and supports AI-generated comic-style visuals for immersive storytelling.

## 🎒 Inventory & Quest Tracking

LoreKraft keeps track of:

* Player inventory
* Active quests
* NPC moods/emotions
* Story progression

## 🌌 Fantasy World Building

Each session creates an evolving fantasy universe filled with:

* Ancient ruins
* Mystical forests
* Hidden guilds
* Dynamic encounters
* Lore-driven adventures

---

# 🛠️ Tech Stack

| Technology                   | Purpose                              |
| ---------------------------- | ------------------------------------ |
| Python                       | Backend logic                        |
| Streamlit                    | Interactive web app framework        |
| Google Gemini API            | AI storytelling and scene generation |
| Imagen / Gemini Image Models | AI-generated visuals                 |
| Pillow (PIL)                 | Image processing                     |
| Figma                        | UI/UX design prototyping             |

---

# 📂 Project Structure

```bash
LoreKraft/
│
├── app.py
├── requirements.txt
├── README.md
└── .streamlit/
    └── secrets.toml
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone the Repository

```bash
git clone <your-repository-link>
cd LoreKraft
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Configure API Key

Create a `.streamlit/secrets.toml` file:

```toml
GEMINI_API_KEY = "your_google_ai_studio_api_key"
```

---

## 4️⃣ Run the Application

```bash
streamlit run app.py
```

---

# 🧠 How It Works

1. The player creates a fantasy character
2. Gemini AI generates an opening story scene
3. The player chooses actions or writes custom responses
4. The AI adapts the story dynamically
5. Inventory, quests, and NPC emotions evolve over time
6. AI-generated visuals enhance immersion

---

# 🎯 Future Enhancements

Planned future improvements include:

* Multiplayer storytelling sessions
* Save/load campaign system
* Character portrait generation
* AI-generated fantasy maps
* Voice narration
* Soundtrack integration
* NPC memory system
* Marketplace for custom campaigns and assets
* Expanded combat mechanics

---

# 📚 Inspiration

LoreKraft was inspired by:

* Tabletop RPGs like Dungeons & Dragons
* Fantasy storytelling games
* AI-assisted creative tools
* Interactive fiction platforms
* Modern visual novel experiences

The project explores how generative AI can enhance creativity instead of replacing it.

---

# 👩‍💻 Author

**Srija Bhashyam**

MS in Computer Science — UC Riverside
Passionate about AI, storytelling, analytics, and interactive user experiences.

---

# 📜 License

This project is intended for educational, creative, and portfolio purposes.
