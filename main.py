import streamlit as st
from openai import OpenAI
from elevenlabs import ElevenLabs
from dotenv import load_dotenv
import os

# Load .env keys
load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=os.getenv("ORGANIZATION_ID"),
    project=os.getenv("PROJECT_ID")
)

# Initialize ElevenLabs client
elevenlabs_client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
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