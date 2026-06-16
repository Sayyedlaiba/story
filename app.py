import streamlit as st
from gtts import gTTS
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="बालकहानियाँ - Kids Story World",
    page_icon="📚",
    layout="centered"
)

# --- CUSTOM CSS FOR KIDS THEME ---
st.markdown("""
    <style>
    .main { background-color: #FFFDF0; }
    h1 { color: #FF4B4B; text-align: center; font-family: 'Comic Sans MS', sans-serif; }
    .story-box { background-color: #FFFFFF; padding: 20px; border-radius: 15px; 
                 border: 3px solid #FFD700; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    .story-text { font-size: 24px; color: #333333; line-height: 1.6; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- STORY DATA ---
# Using a classic Panchatantra story: The Lion and the Mouse
STORY_SCENES = [
    {
        "text": "एक समय की बात है, एक घने जंगल में एक बड़ा ही पराक्रमी शेर रहता था। वह दोपहर में पेड़ की छांव में सो रहा था।",
        "character": "lion",
        "fallback_emoji": "🦁💤"
    },
    {
        "text": "तभी वहाँ एक छोटा सा चूहा आया और शेर की पीठ पर चढ़कर कूदने लगा। शेर की नींद टूट गई और उसने गुस्से में चूहे को पकड़ लिया।",
        "character": "mouse",
        "fallback_emoji": "🐭🐾"
    },
    {
        "text": "चूहा रोने लगा और बोला, 'हे राजा! मुझे माफ कर दीजिए, मैं भविष्य में आपकी मदद करूँगा।' शेर हँसा और उसने चूहे को छोड़ दिया।",
        "character": "mouse",
        "fallback_emoji": "🐭🙏"
    },
    {
        "text": "कुछ दिनों बाद, शिकारियों ने शेर को एक मजबूत जाल में पकड़ लिया। शेर जोर-जोर से दहाड़ने लगा।",
        "character": "lion",
        "fallback_emoji": "🦁🕸️"
    },
    {
        "text": "शेर की आवाज सुनकर छोटा चूहा वहाँ आया। उसने अपने नुकीले दांतों से जाल को काट दिया और शेर को आजाद कर दिया।",
        "character": "mouse",
        "fallback_emoji": "🐭✂️"
    },
    {
        "text": "कहानी की सीख: इस कहानी से हमें यह सीख मिलती है कि आकार में छोटा होने पर भी कोई भी कभी भी काम आ सकता है। हमें किसी को छोटा नहीं समझना चाहिए।",
        "character": "narrator",
        "fallback_emoji": "🧑‍🏫✨"
    }
]

# --- AUDIO GENERATION FUNCTION ---
def generate_hindi_audio(text, scene_index):
    audio_path = f"assets/scene_{scene_index}.mp3"
    # Only generate if it doesn't exist to save loading time
    if not os.path.exists(audio_path):
        os.makedirs('assets', exist_ok=True)
        tts = gTTS(text=text, lang='hi', slow=False)
        tts.save(audio_path)
    return audio_path

# --- APP UI ---
st.title("📚 बच्चों की जादुई कहानियाँ 🌟")
st.write("---")

# Initialize session state to track the current scene
if 'scene_num' not in st.session_state:
    st.session_state.scene_num = 0

current_index = st.session_state.scene_num
scene = STORY_SCENES[current_index]

# Layout: 2 Columns (Left for 2D Character, Right for Story Text & Audio)
col1, col2 = st.columns([1, 2])

with col1:
    # Attempt to load local 2D character images, fallback to emojis if missing
    image_path = f"assets/{scene['character']}.png"
    if os.path.exists(image_path):
        st.image(image_path, use_column_width=True)
    else:
        # Fun fallback large emoji for kids if images aren't uploaded yet
        st.markdown(f"<h1 style='font-size: 100px; margin: 0;'>{scene['fallback_emoji']}</h1>", unsafe_allow_html=True)

with col2:
    # Display the story text inside a styled box
    st.markdown(f"""
        <div class="story-box">
            <p class="story-text">{scene['text']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("") # Spacing
    
    # Generate and render real voice audio
    with st.spinner("आवाज़ तैयार हो रही है..."):
        audio_file = generate_hindi_audio(scene['text'], current_index)
        st.audio(audio_file, format="audio/mp3", autoplay=True)

# --- NAVIGATION BUTTONS ---
st.write("---")
nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])

with nav_col1:
    if current_index > 0:
        if st.button("⬅️ पीछे जाएँ"):
            st.session_state.scene_num -= 1
            st.rerun()

with nav_col3:
    if current_index < len(STORY_SCENES) - 1:
        if st.button("आगे बढ़ें ➡️"):
            st.session_state.scene_num += 1
            st.rerun()
    else:
        if st.button("🔄 फिर से शुरू करें"):
            st.session_state.scene_num = 0
            st.rerun()

# Progress bar for kids to see how far they've come
progress_percentage = int((current_index + 1) / len(STORY_SCENES) * 100)
st.progress(progress_percentage / 100)
st.caption(f"पन्ना {current_index + 1} / {len(STORY_SCENES)}")
