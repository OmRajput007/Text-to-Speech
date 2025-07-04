🎙️ Voice Storyteller AI
AI-powered app that generates unique stories from prompts and narrates them using realistic AI voices.

🚀 Features
✅ Enter any prompt to generate a personalized story
✅ High-quality AI voice narration (powered by ElevenLabs)
✅ Clean, simple web interface with Streamlit
✅ Supports multiple voice options
✅ Fully configurable with .env for security

🛠️ Tech Stack
OpenAI GPT-3.5 Turbo — AI Story Generation

ElevenLabs — Realistic AI Voice Narration

Streamlit — Rapid Web App Framework

Python, dotenv

⚡ Setup & Installation
Clone the Repository

bash
Copy
Edit
git clone https://github.com/yourusername/voice-storyteller-ai.git
cd voice-storyteller-ai
Install Dependencies

bash
Copy
Edit
pip install -r requirements.txt
Add .env File

Create a .env file in the root folder:

ini
Copy
Edit
OPENAI_API_KEY=sk-...
OPENAI_ORG_ID=org-...
OPENAI_PROJECT_ID=proj-...
ELEVENLABS_API_KEY=...
Run the App

bash
Copy
Edit
streamlit run app.py
🎧 Example

🧩 Future Improvements
Audio download option

More voice selections

API integration for external apps

Branded SaaS-ready deployment

💡 License
For educational and demo purposes. Customize for your own use cases.
