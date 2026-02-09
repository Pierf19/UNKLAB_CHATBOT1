"""
Speech Recognition (STT) - Speech to Text
"""
import speech_recognition as sr

class SpeechRecognizer:
    """Speech to Text Recognizer"""
    
    def __init__(self, language='id-ID'):
        self.recognizer = sr.Recognizer()
        self.language = language
        self.microphone = sr.Microphone()
        
        with self.microphone as source:
            print("Menyesuaikan dengan suara ambient...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Siap mendengarkan!")
    
    def listen(self, timeout=5, phrase_time_limit=10):
        try:
            with self.microphone as source:
                print("Mendengarkan... (Silakan bicara)")
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                return audio
        except sr.WaitTimeoutError:
            print("⏱ Timeout - Tidak ada suara terdeteksi")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def recognize(self, audio, language=None):
        if audio is None:
            return None
        
        if language is None:
            language = self.language
        
        try:
            print("Memproses audio...")
            text = self.recognizer.recognize_google(audio, language=language)
            print(f" Terdengar: '{text}'")
            return text
        except sr.UnknownValueError:
            print("❌ Tidak dapat memahami audio")
            return None
        except sr.RequestError as e:
            print(f"❌ Error dari Google: {e}")
            return None
    
    def listen_and_recognize(self, language=None, timeout=5, phrase_time_limit=10):
        audio = self.listen(timeout=timeout, phrase_time_limit=phrase_time_limit)
        return self.recognize(audio, language=language)
    
    def set_language(self, language):
        self.language = language
        print(f"Bahasa diubah ke: {language}")