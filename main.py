import streamlit as st
from openai import OpenAI
from elevenlabs import ElevenLabs
from dotenv import load_dotenv
import os

# Load .env keys (for local development)
load_dotenv()

# Get API keys - prioritize Streamlit secrets for cloud deployment
try:
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    organization_id = st.secrets.get("ORGANIZATION_ID")
    project_id = st.secrets.get("PROJECT_ID") 
    elevenlabs_api_key = st.secrets["ELEVENLABS_API_KEY"]
except KeyError:
    # Fall back to environment variables for local development
    openai_api_key = os.getenv("OPENAI_API_KEY")
    organization_id = os.getenv("ORGANIZATION_ID")
    project_id = os.getenv("PROJECT_ID")
    elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

# Check if API keys are available
if not openai_api_key:
    st.error("❌ OpenAI API key not found. Please set it in Streamlit secrets or environment variables.")
    st.stop()

if not elevenlabs_api_key:
    st.error("❌ ElevenLabs API key not found. Please set it in Streamlit secrets or environment variables.")
    st.stop()

# Initialize OpenAI client
client = OpenAI(
    api_key=openai_api_key,
    organization=organization_id,
    project=project_id
)

# Initialize ElevenLabs client
elevenlabs_client = ElevenLabs(
    api_key=elevenlabs_api_key
)

# Streamlit App
st.set_page_config(page_title="AI Storyteller with Voice 🎙️", page_icon="🎙️")
st.title("🎙️ AI Storyteller with Voice")

prompt = st.text_input("Enter your story prompt:")

# Voice mapping for user-friendly names
voice_map = {
    "Adam": "pNInz6obpgDQGcFmaJgB",
    "Rachel": "21m00Tcm4TlvDq8ikWAM", 
    "Domi": "AZnzlk1XvdvUeBnXmlld",
    "Bella": "EXAVITQu4vr4xnSDxMaL",
    "Josh": "VR6AewLTigWG4xSOukaG",
    "Lily": "pFZP5JQG7iQjIQuC4Bku",
    "Grace": "oWAxZDx7w5VEj9dCyTzz",
    "Callum": "N2lVS1w4EtoT3dr4eOWO"
}

voice_choice = st.selectbox("Choose a voice:", list(voice_map.keys()))

if prompt:
    with st.spinner("Generating your story..."):
        try:
            # Generate Story using new OpenAI API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Write a short, engaging story based on: {prompt}"}]
            )
            story = response.choices[0].message.content.strip()
            
            st.subheader("📝 Your AI-Generated Story:")
            st.write(story)

            # Generate Voice using text-to-speech
            audio = elevenlabs_client.text_to_speech.convert(
                voice_id=voice_map[voice_choice],
                text=story,
                model_id="eleven_monolingual_v1"
            )
            
            # Save audio to file
            with open("story.mp3", "wb") as f:
                for chunk in audio:
                    f.write(chunk)

            st.subheader("🔊 Listen to Your Story:")
            with open("story.mp3", "rb") as audio_file:
                st.audio(audio_file.read(), format="audio/mp3")

            st.success("Done! Feel free to try another story.")
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Please check your API keys and try again.")

# Optional: Add cleanup
if os.path.exists("story.mp3"):
    try:
        os.remove("story.mp3")
    except:
        pass  # Ignore cleanup errors
