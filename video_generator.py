import os
import numpy as np
# Importing directly from clips avoids the legacy editor configuration crash
from moviepy.video.VideoClip import ImageClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

def make_animated_scene(image_path, audio_path, output_path):
    """
    Combines a 2D character image and Hindi audio into an MP4 clip.
    Bypasses legacy moviepy initialization issues.
    """
    print(f"🎬 Generating video for {image_path}...")

    # 1. Load the Hindi audio track
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration

    # 2. Create a solid background canvas (1280x720)
    # Modern moviepy allows creating a solid color image clip directly
    bg_clip = ImageClip(np.zeros((720, 1280, 3), dtype=np.uint8) + [255, 253, 240], duration=duration)

    # 3. Load the character
    character_clip = ImageClip(image_path, duration=duration)
    
    # 4. Apply a simple, clean bounce calculation
    w, h = character_clip.size
    def bounce_effect(t):
        y_offset = int(15 * np.sin(2 * np.pi * 1.5 * t))
        return (640 - w // 2, 360 - h // 2 + y_offset)

    # Position the character with the bounce
    animated_character = character_clip.with_position(bounce_effect)

    # 5. Combine and attach audio
    final_video = CompositeVideoClip([bg_clip, animated_character])
    final_video = final_video.with_audio(audio_clip)

    # 6. Export the final clip
    final_video.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        logger=None
    )

    # Close assets to free up server RAM
    audio_clip.close()
    final_video.close()
    print(f"🎯 Video successfully saved to: {output_path}")
