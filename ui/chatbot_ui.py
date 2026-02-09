"""
UNKLAB Chatbot GUI - Enhanced Version
"""
import tkinter as tk
from tkinter import scrolledtext, messagebox
import json
import os
import threading
from datetime import datetime

from config import (
    INTENTS_FILE, MODEL_FILE, VECTORIZER_FILE, 
    LABEL_ENCODER_FILE, WINDOW_TITLE, WINDOW_SIZE,
    CHAT_FONT, INPUT_FONT, STT_LANGUAGE_ID, STT_LANGUAGE_EN,
    TTS_LANGUAGE_ID, TTS_LANGUAGE_EN, HEADER_COLOR, ACCENT_COLOR,
    KAMPUS_NAME, KAMPUS_TAGLINE
)
from models.preprocessor import TextPreprocessor
from models.text_vectorizer import TextVectorizer
from models.knn_classifier import KNNClassifier
from utils.speech_recognition import SpeechRecognizer
from utils.text_to_speech import TextToSpeech

class UnklabChatbotGUI:
    """GUI untuk UNKLAB Chatbot"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg='#f5f5f5')
        
        self.current_language = 'id'
        self.voice_enabled = True
        self.is_listening = False
        
        self.load_models()
        self.init_voice_components()
        self.create_widgets()
        
        # Welcome message
        welcome_msg = f"""
🎓 Selamat datang di {KAMPUS_NAME}!
{KAMPUS_TAGLINE}

Saya siap membantu Anda dengan informasi tentang:
📚 Fakultas & Program Studi
💰 Biaya & Beasiswa
🏠 Asrama & Fasilitas
📝 Pendaftaran & Akademik
🎯 Dan masih banyak lagi!

Tanyakan apa saja atau klik 🎤 untuk voice input!
        """
        self.add_bot_message(welcome_msg.strip())
    
    def load_models(self):
        print("Loading UNKLAB Chatbot models...")
        
        try:
            with open(INTENTS_FILE, 'r', encoding='utf-8') as f:
                self.intents_data = json.load(f)
            
            self.vectorizer = TextVectorizer()
            self.vectorizer.load(VECTORIZER_FILE)
            
            self.knn = KNNClassifier()
            self.knn.load(MODEL_FILE, LABEL_ENCODER_FILE)
            
            self.preprocessor = TextPreprocessor()
            
            print("✓ Models loaded successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", 
                f"Gagal load model: {e}\n\n"
                "Pastikan sudah menjalankan:\n"
                "1. python data_expander.py\n"
                "2. python train.py"
            )
            raise
    
    def init_voice_components(self):
        try:
            self.stt = SpeechRecognizer(language=STT_LANGUAGE_ID)
            self.tts = TextToSpeech(language=TTS_LANGUAGE_ID)
            print("✓ Voice components initialized!")
        except Exception as e:
            print(f"Warning: Voice initialization failed: {e}")
            self.voice_enabled = False
    
    def create_widgets(self):
        # Header dengan logo UNKLAB
        header_frame = tk.Frame(self.root, bg=HEADER_COLOR, height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame, 
            text="🎓 CHATBOT UNKLAB", 
            font=("Segoe UI", 18, "bold"),
            bg=HEADER_COLOR,
            fg='white'
        )
        title_label.pack(pady=10)
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame, 
            text=KAMPUS_TAGLINE, 
            font=("Segoe UI", 9, "italic"),
            bg=HEADER_COLOR,
            fg='#E0E0E0'
        )
        subtitle_label.pack()
        
        # Info bar
        info_frame = tk.Frame(self.root, bg='#E3F2FD', height=40)
        info_frame.pack(fill=tk.X)
        info_frame.pack_propagate(False)
        
        info_label = tk.Label(
            info_frame,
            text="📍 Airmadidi, Minahasa Utara  |  🌐 www.unklab.ac.id  |  📞 (0431) 891035",
            font=("Segoe UI", 9),
            bg='#E3F2FD',
            fg='#1565C0'
        )
        info_label.pack(pady=10)
        
        # Language selection
        lang_frame = tk.Frame(self.root, bg='#f5f5f5')
        lang_frame.pack(pady=8)
        
        tk.Label(
            lang_frame, 
            text="Bot Voice Language:", 
            font=("Segoe UI", 9, "bold"),
            bg='#f5f5f5'
        ).pack(side=tk.LEFT, padx=5)
        
        self.lang_var = tk.StringVar(value='id')
        
        tk.Radiobutton(
            lang_frame,
            text="🇮🇩 Indonesia",
            variable=self.lang_var,
            value='id',
            command=self.change_language,
            font=("Segoe UI", 9),
            bg='#f5f5f5',
            activebackground='#f5f5f5'
        ).pack(side=tk.LEFT, padx=3)
        
        tk.Radiobutton(
            lang_frame,
            text="🇺🇸 English",
            variable=self.lang_var,
            value='en',
            command=self.change_language,
            font=("Segoe UI", 9),
            bg='#f5f5f5',
            activebackground='#f5f5f5'
        ).pack(side=tk.LEFT, padx=3)
        
        # Chat display
        chat_container = tk.Frame(self.root, bg='white', bd=1, relief=tk.SOLID)
        chat_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_container,
            wrap=tk.WORD,
            font=CHAT_FONT,
            bg='white',
            state=tk.DISABLED,
            padx=10,
            pady=10
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Tags untuk styling
        self.chat_display.tag_config('user', 
            foreground='#1565C0', 
            font=("Segoe UI", 10, "bold")
        )
        self.chat_display.tag_config('bot', 
            foreground=ACCENT_COLOR, 
            font=("Segoe UI", 10, "bold")
        )
        self.chat_display.tag_config('timestamp', 
            foreground='#757575', 
            font=("Segoe UI", 8)
        )
        self.chat_display.tag_config('confidence', 
            foreground='#F57C00', 
            font=("Segoe UI", 8, "italic")
        )
        self.chat_display.tag_config('info', 
            foreground='#424242', 
            font=("Segoe UI", 10)
        )
        
        # Input frame
        input_container = tk.Frame(self.root, bg='#f5f5f5')
        input_container.pack(fill=tk.X, padx=1, pady=10)
        
        # Voice button
        self.voice_btn = tk.Button(
            input_container,
            text="🎤",
            font=("Segoe UI", 16),
           
            fg='black',
            width=3,
            height=20,
            command=self.toggle_voice_input,
            cursor='hand2',
            bd=0,
            relief=tk.FLAT
        )
        self.voice_btn.pack(side=tk.LEFT, padx=5)
        
        # Text input
        self.user_input = tk.Entry(
            input_container,
            font=INPUT_FONT,
            bg='white',
            bd=1,
            relief=tk.SOLID
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.user_input.bind('<Return>', lambda e: self.send_message())
        
        # Send button
        send_btn = tk.Button(
            input_container,
            text="Kirim ➤",
            font=("Segoe UI", 10, "bold"),
            bg=ACCENT_COLOR,
            fg='white',
            command=self.send_message,
            cursor='hand2',
            padx=20,
            bd=0,
            relief=tk.FLAT
        )
        send_btn.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="✓ Ready - UNKLAB Chatbot siap membantu!")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Segoe UI", 8),
            bg='#ECEFF1',
            anchor=tk.W,
            padx=15,
            pady=5
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def change_language(self):
        self.current_language = self.lang_var.get()
        
        if self.current_language == 'id':
            self.stt.set_language(STT_LANGUAGE_ID)
            self.tts.set_language(TTS_LANGUAGE_ID)
            self.status_var.set("✓ Bahasa diubah ke: Indonesia")
        else:
            self.stt.set_language(STT_LANGUAGE_EN)
            self.tts.set_language(TTS_LANGUAGE_EN)
            self.status_var.set("✓ Language changed to: English")
    
    def toggle_voice_input(self):
        if not self.voice_enabled:
            messagebox.showwarning("Voice Unavailable", 
                "Voice features tidak tersedia!\n\n"
                "Pastikan microphone terhubung dan\n"
                "PyAudio sudah terinstall."
            )
            return
        
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()
    
    def start_listening(self):
        self.is_listening = True
        self.voice_btn.config( text='🔴')
        
        if self.current_language == 'id':
            self.status_var.set("🎤 Mendengarkan... Silakan bicara!")
        else:
            self.status_var.set("🎤 Listening... Please speak!")
        
        thread = threading.Thread(target=self.listen_to_voice, daemon=True)
        thread.start()
    
    def stop_listening(self):
        self.is_listening = False
        self.voice_btn.config(fg='black', text='🎤')
        self.status_var.set("✓ Ready")
    
    def listen_to_voice(self):
        try:
            lang = STT_LANGUAGE_ID if self.current_language == 'id' else STT_LANGUAGE_EN
            text = self.stt.listen_and_recognize(
                language=lang,
                timeout=5,
                phrase_time_limit=10
            )
            
            if text:
                self.root.after(0, lambda: self.user_input.delete(0, tk.END))
                self.root.after(0, lambda: self.user_input.insert(0, text))
                self.root.after(0, self.send_message)
            
        except Exception as e:
            print(f"Voice error: {e}")
        
        finally:
            self.root.after(0, self.stop_listening)
    
    def send_message(self):
        user_text = self.user_input.get().strip()
        
        if not user_text:
            return
        
        self.user_input.delete(0, tk.END)
        self.add_user_message(user_text)
        
        # Get response
        response, confidence = self.get_bot_response(user_text)
        self.add_bot_message(response, confidence)
        
        # Speak response
        if self.voice_enabled:
            threading.Thread(
                target=lambda: self.tts.speak(response, wait=False),
                daemon=True
            ).start()
    
    def get_bot_response(self, user_text):
        try:
            # Detect language
            detected_lang = self.preprocessor.detect_language(user_text)
            
            # Preprocess
            processed_text = self.preprocessor.preprocess(
                user_text,
                remove_stopwords=True,
                apply_stemming=(detected_lang == 'id'),
                language=detected_lang
            )
            
            # Vectorize
            X = self.vectorizer.transform([processed_text])
            
            # Predict
            predictions, confidences = self.knn.predict_with_confidence(X)
            intent = predictions[0]
            confidence = confidences[0]
            
            # Get response
            for intent_data in self.intents_data['intents']:
                if intent_data['tag'] == intent:
                    responses = intent_data['responses']
                    
                    # Pilih response sesuai bahasa
                    import random
                    response = random.choice(responses)
                    
                    return response, confidence
            
            # Fallback
            if detected_lang == 'id':
                return "Maaf, saya belum memahami pertanyaan Anda. Bisa coba dengan kata lain?", confidence
            else:
                return "Sorry, I don't quite understand. Could you rephrase?", confidence
            
        except Exception as e:
            print(f"Error: {e}")
            return "Maaf, terjadi kesalahan. Silakan coba lagi.", 0.0
    
    def add_user_message(self, message):
        timestamp = datetime.now().strftime("%H:%M")
        
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n[{timestamp}] ", 'timestamp')
        self.chat_display.insert(tk.END, "Anda: ", 'user')
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def add_bot_message(self, message, confidence=None):
        timestamp = datetime.now().strftime("%H:%M")
        
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n[{timestamp}] ", 'timestamp')
        self.chat_display.insert(tk.END, " UNKLAB Bot: ", 'bot')
        self.chat_display.insert(tk.END, f"\n{message}\n", 'info')
        
        if confidence is not None and confidence > 0:
            self.chat_display.insert(
                tk.END, 
                f"  (Confidence: {confidence:.1%})\n", 
                'confidence'
            )
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)


def main():
    root = tk.Tk()
    app = UnklabChatbotGUI(root)
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()