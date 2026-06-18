# 🚀 GemSight

An intelligent, visually stunning Streamlit dashboard that turns your raw CSV/Excel data into interactive, presentation-ready visualizations in seconds. Powered by Google's **Gemini Pro** and featuring a premium, Spotify-inspired dark UI.

## ✨ Features
- **Neon Dark Theme**: A sleek, distraction-free UI (`#121212` background with `#38bdf8` neon blue accents), customized pill-shaped buttons, and glassmorphic-inspired flat metric cards.
- **Instant 2x2 EDA Grid**: Upload your data and instantly receive an AI-generated 2x2 grid of four distinct Plotly graphs—giving you an immediate, comprehensive overview of your dataset without writing a single line of code.
- **Conversational Analytics**: Chat with your data! Ask Gemini to generate specific charts or find insights, and it will write and execute the Python code on the fly.
- **Safe Execution Sandbox**: The AI operates on a deep copy of your dataframe within a strictly controlled execution environment, guaranteeing that your original data is never mutated or corrupted.
- **Smart Memory Management**: Implements a sliding window for conversation history, ensuring the app never crashes from token limits, even during marathon analysis sessions.
- **Massive Dataset Support**: Intelligently samples large datasets to extract schema definitions, making upload and analysis blazingly fast.

## 🛠️ Tech Stack
- **Frontend/UI**: [Streamlit](https://streamlit.io/) with Custom CSS
- **Visualizations**: [Plotly Express & Graph Objects](https://plotly.com/python/)
- **Data Manipulation**: [Pandas](https://pandas.pydata.org/)
- **AI/LLM**: [Google Generative AI (Gemini Pro)](https://ai.google.dev/)

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/ai-dashboard-generator.git
cd ai-dashboard-generator
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
streamlit run app.py
```

### 4. Provide your API Key
Create a folder named `.streamlit` in the root directory. Inside it, create a file named `secrets.toml` and add your **Google Gemini API Key**:
```toml
GEMINI_API_KEY = "your_api_key_here"
```

## 📸 Screenshots
*(Add screenshots or GIFs of your gorgeous UI here before sharing on LinkedIn!)*

## 🤝 Contributing
Contributions, issues, and feature requests are welcome!

## 📝 License
This project is open source and available under the [MIT License](LICENSE).
