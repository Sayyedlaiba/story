import os
import numpy as np
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip

def make_animated_scene(image_path, audio_path, output_path):
    """
    Combines a 2D character image and Hindi audio into a kid-friendly animated video.
    Applies a subtle bouncing effect to make the character look like they are talking.
    """
    print(f"🎬 Generating video for {image_path}...")

    # 1. Load the Hindi audio track to determine video duration
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration

    # 2. Load the 2D character image (resized to standard YouTube/Horizontal video size)
    # We set the background canvas to a soft color suitable for kids
    bg_clip = ImageClip(None, duration=duration).set_size((1280, 720))
    bg_clip = bg_clip.on_color(color=(255, 253, 240), col_opacity=1) # Soft cream background

    # 3. Load the character and position them in the center
    character_clip = ImageClip(image_path).set_duration(duration)
    
    # 4. ANIMATION: Create a jumping/bouncing effect (talking simulation)
    # The character shifts up and down slightly based on a sine wave over time
    def bounce_effect(get_frame, t):
        # Calculate a vertical offset using a sine wave
        y_offset = int(15 * np.sin(2 * np.pi * 1.5 * t)) 
        # Position: centered horizontally (640), slightly adjusted vertically
        return (640 - character_clip.w // 2, 360 - character_clip.h // 2 + y_offset)

    # Apply the position animation matrix
    animated_character = character_clip.set_position(lambda t: bounce_effect(None, t))

    # 5. Composite layers together: Background + Animated Character
    final_video = CompositeVideoClip([bg_clip, animated_character])
    final_video = final_video.set_audio(audio_clip)

    # 6. Export the final MP4 file
    final_video.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        logger=None # Suppresses messy console logs
    )

    # Close assets to free up RAM
    audio_clip.close()
    final_video.close()
    print(f"🎯 Video successfully saved to: {output_path}")

# --- Test Run ---
if __name__ == "__main__":
    # Create the assets folder if it doesn't exist for testing
    os.makedirs("assets", exist_ok=True)
    
    # Example paths (Make sure you have a real image and mp3 file here)
    # make_animated_scene("assets/lion.png", "assets/scene_0.mp3", "assets/scene_0_video.mp4")
