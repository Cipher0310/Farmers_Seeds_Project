import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import time

# 1. Setup the "Ears" (Microphone)
recognizer = sr.Recognizer()

def speak(text):
    """This function makes the computer speak."""
    print(f"🤖 AI says: {text}")
    
    # Convert text to audio
    tts = gTTS(text=text, lang='en')
    filename = "temp_voice.mp3"
    tts.save(filename)
    
    # Play the audio using Pygame
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    
    # Wait for audio to finish
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    
    # Cleanup
    pygame.mixer.quit()
    os.remove(filename)

def listen():
    """This function listens to your microphone."""
    with sr.Microphone() as source:
        print("\n🎤 Listening... (Say something!)")
        # Adjust for background noise automatically
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            # Listen for audio
            audio = recognizer.listen(source, timeout=5)
            print("✅ Audio captured. Processing...")
            
            # Convert audio to text (using Google's free server for testing)
            text = recognizer.recognize_google(audio)
            print(f"You said: '{text}'")
            return text
        except sr.WaitTimeoutError:
            print("❌ No sound detected.")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand audio.")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

# --- Main Test Loop ---
if __name__ == "__main__":
    speak("System ready. Please say something.")
    user_text = listen()
    
    if user_text:
        speak(f"I heard you say: {user_text}")
    else:
        speak("I did not hear anything.")