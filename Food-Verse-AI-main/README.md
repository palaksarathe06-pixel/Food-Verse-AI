# 🍽️ Food Verse AI — Multimodal Food Intelligence Agent

**Skill Wallet Capstone Project 3** · Platform ID: `6ac4ca021dcde6d7857c169a`

A production-ready application leveraging Google Gemini's Multimodal Suite to analyze food through images, videos, audio, and text: estimating nutrition, detecting spoilage, monitoring commercial kitchen hygiene from video/photos, assisting cooking with voice/fridge scans, and crafting personalized 7-day meal plans.

---

## 🚀 Multimodal Intelligence Pillars

| Tab | Feature | Modality | Description |
|-----|---------|----------|-------------|
| 🍽️ | **Nutrition Audit** | Image + Text | Upload meal photos → AI identifies dish, cuisine, ingredients, full macro donut chart, health score & allergen alerts |
| 🥬 | **Freshness Diagnostic** | Image + Text | Upload perishable item photos → Classifies stage (Fresh / Moderately Fresh / Spoiled) with confidence gauge & storage advice |
| 🏪 | **Kitchen Hygiene** | Video + Image | Upload surveillance video clips (MP4/MOV) or photos → Audits glove usage, hairnets, cross-contamination & food safety |
| 👨‍🍳 | **Recipe Assistant** | Voice + Photo + Text | Scan fridge photos, record audio/voice notes, or type pantry ingredients → AI generates recipes with cooking steps |
| 📅 | **Meal Planner** | Text + Reasoning | Enter profile → BMR/TDEE calculation → Adaptive 7-day meal schedule with automated grocery list and 1-click JSON export |

---

## 🛠️ Tech Stack

- **Frontend & App Engine:** Python 3.9+ with Streamlit
- **Multimodal AI Models:** Google Gemini Suite (`gemini-3.5-flash-lite`, `gemini-3.8-flash` with auto-fallback)
- **Computer Vision & Video:** OpenCV (`opencv-python-headless`) + Pillow
- **Data Visualization:** Plotly interactive charts
- **Zero External Databases:** Completely lightweight and self-contained

---

## ⚡ Quick Start (Local)

```bash
# 1. Clone the repository
git clone https://github.com/Parikshit-7Yami/Food-Verse-AI.git
cd Food-Verse-AI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

---

## 🎮 Demo & Live AI Mode

- **Live AI Mode:** Automatically configured with Gemini API key via background integration or environment variable `GEMINI_API_KEY`.
- **Demo Mode:** Every tab includes a built-in **"Try Demo"** button allowing full interactive exploration without API calls.

---

## ☁️ Deploy to Render Portal

1. Log in to **[render.com](https://render.com/)** and click **New +** → **Web Service**.
2. Connect your GitHub repository: `https://github.com/Parikshit-7Yami/Food-Verse-AI`.
3. Configure the Web Service:
   - **Runtime:** `Python 3`
   - **Branch:** `main`
   - **Build Command:**
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command:**
     ```bash
     streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true --server.enableCORS false
     ```
   - **Plan:** `Free`
4. Under **Environment Variables**, add:
   - **Key:** `GEMINI_API_KEY`
   - **Value:** `<your-gemini-api-key>`
   - *(Optional)* **Key:** `PYTHON_VERSION` → **Value:** `3.11.8`
5. Click **Create Web Service**. Render will build and deploy your live URL.

---

## 📁 Project Structure

```
Food-Verse-AI/
├── app.py                    # Main Streamlit entry point & navigation
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml           # Streamlit theme & dark styling
├── tabs/
│   ├── __init__.py
│   ├── tab_nutrition.py      # Tab 1: Food Recognition & Nutrition
│   ├── tab_freshness.py      # Tab 2: Freshness & Spoilage
│   ├── tab_hygiene.py        # Tab 3: Kitchen Hygiene & Video Audit
│   ├── tab_recipe.py         # Tab 4: Multimodal Recipe Assistant
│   └── tab_meal_planner.py   # Tab 5: Personalized Meal Planner
├── utils/
│   ├── __init__.py
│   ├── gemini_client.py      # Multimodal Gemini API wrapper & fallback
│   ├── demo_data.py          # Demo fallback datasets
│   ├── prompts.py            # AI prompt templates
│   └── styles.py             # Custom glassmorphic CSS
└── README.md
```

---

## 📜 License

Built for the Skill Wallet Capstone Program (Platform ID: `6ac4ca021dcde6d7857c169a`).
