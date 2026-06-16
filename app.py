import streamlit as st
import os
from gtts import gTTS

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="बालकहानियाँ - Kids Story World",
    page_icon="📚",
    layout="centered"
)

# --- KID-FRIENDLY THEME WITH CSS BOUNCING ANIMATION ---
st.markdown("""
    <style>
    .main { background-color: #FFFDF0; }
    h1 { color: #FF4B4B; text-align: center; font-family: 'Comic Sans MS', sans-serif; }
    .story-box { background-color: #FFFFFF; padding: 25px; border-radius: 15px; 
                 border: 3px solid #FFD700; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); min-height: 150px; }
    .story-text { font-size: 24px; color: #333333; line-height: 1.6; font-weight: bold; }
    
    /* This creates a smooth talking/bouncing animation for the 2D characters */
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-15px); }
    }
    .animated-character {
        font-size: 100px;
        text-align: center;
        animation: bounce 1.2s infinite ease-in-out;
        margin: 0;
        padding: 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- STORY DATA ---
STORY_SCENES = [
    {"text": "एक समय की बात है, एक घने जंगल में एक बड़ा ही पराक्रमी शेर रहता था। वह दोपहर में पेड़ की छांव में सो रहा था।", "fallback_emoji": "🦁💤"},
    {"text": "तभी वहाँ एक छोटा सा चूहा आया और शेर की पीठ पर चढ़कर कूदने लगा। शेर की नींद टूट गई और उसने गुस्से में चूहे को पकड़ लिया।", "fallback_emoji": "🐭🐾"},
    {"text": "चूहा रोने लगा और बोला, 'हे राजा! मुझे माफ कर दीजिए, मैं भविष्य में आपकी मदद करूँगा।' शेर हँसा और उसने चूहे को छोड़ दिया।", "fallback_emoji": "🐭🙏"},
    {"text": "कुछ दिनों बाद, शिकारियों ने शेर को एक मजबूत जाल में पकड़ लिया। शेर जोर-जोर से दहाड़ने लगा।", "fallback_emoji": "🦁🕸️"},
    {"text": "शेर की आवाज सुनकर छोटा चूहा वहाँ आया। उसने अपने नुकीले दांतों से जाल को काट दिया और शेर को आजाद कर दिया।", "fallback_emoji": "🐭✂️"},
    {"text": "कहानी की सीख: इस कहानी से हमें यह सीख मिलती है कि आकार में छोटा होने पर भी कोई भी कभी भी काम आ सकता है। हमें किसी को छोटा नहीं समझना चाहिए।", "fallback_emoji": "🧑‍🏫✨"}
]

# --- AUDIO GENERATION ---
def generate_hindi_audio(text, scene_index):
    audio_path = f"assets/scene_{scene_index}.mp3"
    if not os.path.exists(audio_path):
        os.makedirs('assets', exist_ok=True)
        tts = gTTS(text=text, lang='hi', slow=False)
        tts.save(audio_path)
    return audio_path

# --- APPLICATION SESSION LOGIC ---
if 'scene_num' not in st.session_state:
    st.session_state.scene_num = 0

current_index = st.session_state.scene_num
scene = STORY_SCENES[current_index]

# --- DISPLAY HEADERS ---
st.title("📚 बच्चों की जादुई कहानियाँ 🌟")
st.write("---")

# Generate the audio file safely in the background
audio_file = generate_hindi_audio(scene['text'], current_index)

# --- LAYOUT CONTAINERS ---
# Using standard containers instead of column splitting guarantees 100% cloud stability
st.markdown(f'<div class="animated-character">{scene["fallback_emoji"]}</div>', unsafe_allow_html=True)

st.write("") # Blank space

st.markdown(f"""
    <div class="story-box">
        <p class="story-text">{scene['text']}</p>
    </div>
""", unsafe_allow_html=True)

st.write("") 
st.audio(audio_file, format="audio/mp3", autoplay=True)

# --- NAVIGATION CONTROLS ---
st.write("---")
nav_col1, nav_col2 = st.columns(2)

with nav_col1:
    if current_index > 0:
        if st.button("⬅️ पीछे जाएँ", use_container_width=True):
            st.session_state.scene_num -= 1
            st.rerun()

with nav_col2:
    if current_index < len(STORY_SCENES) - 1:
        if st.button("आगे बढ़ें ➡️", use_container_width=True):
            st.session_state.scene_num += 1
            st.rerun()
    else:
        if st.button("🔄 फिर से शुरू करें", use_container_width=True):
            st.session_state.scene_num = 0
            st.rerun()
