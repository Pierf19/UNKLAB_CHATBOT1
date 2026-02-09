"""
Text-to-Speech (TTS)
"""
import pyttsx3
import threading

class TextToSpeech:
    """Text to Speech Engine"""
    def __init__(self, language='id', rate=150, volume=0.9):
        self.engine = pyttsx3.init()
        self.language = language
        self.is_speaking = False
        
        self.set_rate(rate)
        self.set_volume(volume)
        self.set_language(language)
        
        print("TTS Engine initialized")
 
    
    def set_rate(self, rate):
        self.engine.setProperty('rate', rate)
    
    def set_volume(self, volume):
        self.engine.setProperty('volume', volume)
    
    def set_language(self, language):
        self.language = language
        voices = self.engine.getProperty('voices')
        
        for voice in voices:
            voice_id = voice.id.lower()
            voice_name = voice.name.lower()
            
            if language == 'id':
                if 'indonesia' in voice_name or 'id' in voice_id:
                    self.engine.setProperty('voice', voice.id)
                    print(f"Voice set to: {voice.name}")
                    return
            elif language == 'en':
                if 'english' in voice_name or 'en' in voice_id:
                    if 'us' in voice_name or 'us' in voice_id:
                        self.engine.setProperty('voice', voice.id)
                        print(f"Voice set to: {voice.name}")
                        return
        
        if voices:
            self.engine.setProperty('voice', voices[0].id)
            print(f"Using default voice: {voices[0].name}")
   
    def stop(self):
        if self.is_speaking:
            self.engine.stop()
            self.is_speaking = False