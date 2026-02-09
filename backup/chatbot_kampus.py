#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chatbot Universitas Klabat (UNKLAB) - GUI Tkinter dengan Hybrid AI
Features: Math, Memory, Context (KNN), Time, Voice Input/Output
Author: Senior Python Developer
Date: 2026
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import json
import re
import os
import threading
import time
from datetime import datetime
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

# ======================== GLOBAL VARIABLES ========================
user_name = ""  # Menyimpan nama user
recognizer = sr.Recognizer()
dataset = {}

# ======================== LOAD DATA JSON ========================
def load_dataset():
    """Load dataset dari kampus_data.json"""
    global dataset
    try:
        with open('kampus_data.json', 'r', encoding='utf-8') as f:
            dataset = json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", "File kampus_data.json tidak ditemukan!")
        dataset = {"intents": []}

# ======================== MATH LOGIC (PRIORITAS 1a) ========================
def check_math(user_input):
    """
    Deteksi dan hitung operasi matematika menggunakan Regex
    Pattern: [angka] [operasi] [angka]
    Operasi: tambah, kurang, kali, bagi
    """
    # Normalize input
    text = user_input.lower()
    
    # Pattern untuk berbagai format: "5 tambah 3", "5+3", "lima ditambah tiga"
    # Convert kata ke simbol
    text = text.replace('tambah', '+').replace('ditambah', '+').replace('plus', '+')
    text = text.replace('kurang', '-').replace('dikurang', '-').replace('minus', '-')
    text = text.replace('kali', '*').replace('dikali', '*').replace('kali', '*')
    text = text.replace('bagi', '/').replace('dibagi', '/').replace('per', '/')
    
    # Regex pattern untuk deteksi angka operasi angka
    pattern = r'(\d+(?:[.,]\d+)?)\s*([+\-*/])\s*(\d+(?:[.,]\d+)?)'
    match = re.search(pattern, text)
    
    if match:
        num1 = float(match.group(1).replace(',', '.'))
        operator = match.group(2)
        num2 = float(match.group(3).replace(',', '.'))
        
        try:
            if operator == '+':
                result = num1 + num2
                return f"{num1} + {num2} = {result}"
            elif operator == '-':
                result = num1 - num2
                return f"{num1} - {num2} = {result}"
            elif operator == '*':
                result = num1 * num2
                return f"{num1} × {num2} = {result}"
            elif operator == '/':
                if num2 == 0:
                    return "Tidak bisa dibagi dengan nol!"
                result = num1 / num2
                return f"{num1} ÷ {num2} = {result:.2f}"
        except:
            return None
    
    return None

# ======================== TIME LOGIC (PRIORITAS 1b) ========================
def check_time(user_input):
    """
    Deteksi kata 'jam' atau 'tanggal' dan return waktu real-time
    """
    text = user_input.lower()
    now = datetime.now()
    
    if 'jam' in text:
        jam_str = now.strftime("%H:%M:%S")
        tanggal_str = now.strftime("%d-%m-%Y")
        return f"Jam sekarang adalah {jam_str}, tanggal {tanggal_str}"
    
    if 'tanggal' in text:
        tanggal_str = now.strftime("%A, %d %B %Y")
        jam_str = now.strftime("%H:%M")
        return f"Tanggal hari ini adalah {tanggal_str}, pukul {jam_str}"
    
    if 'berapa jam' in text or 'jam berapa' in text:
        jam_str = now.strftime("%H:%M:%S")
        return f"Jam sekarang {jam_str}"
    
    return None

# ======================== MEMORY LOGIC (PRIORITAS 1c) ========================
def check_name(user_input):
    """
    Deteksi input nama dan tanyaan nama
    Pattern: "Nama saya [nama]", "Siapa nama saya", "Nama saya adalah"
    """
    global user_name
    text = user_input.lower()
    
    # Cek apakah user memberitahu nama
    nama_pattern = r'nama\s+saya\s+(?:adalah\s+)?([a-zñáéíóúü\s]+)'
    nama_match = re.search(nama_pattern, text, re.IGNORECASE)
    
    if nama_match:
        user_name = nama_match.group(1).strip().title()
        return f"Nama yang bagus! Saya akan memanggil kamu {user_name} dari sekarang."
    
    # Cek apakah user bertanya tentang namanya
    if 'siapa nama saya' in text or 'nama saya siapa' in text:
        if user_name:
            return f"Nama kamu adalah {user_name}."
        else:
            return "Kamu belum memberitahu nama kamu. Coba katakan 'Nama saya [nama]'."
    
    return None

# ======================== KNN CONTEXT LOGIC (PRIORITAS 2) ========================
def train_knn_model():
    """
    Train KNN model dari dataset JSON untuk context understanding
    """
    intents = dataset.get("intents", [])
    
    patterns = []
    labels = []
    
    for intent in intents:
        for pattern in intent.get("patterns", []):
            patterns.append(pattern.lower())
            labels.append(intent.get("tag", ""))
    
    if not patterns:
        return None, None, None
    
    # Vectorize patterns
    vectorizer = CountVectorizer(lowercase=True, analyzer='char', ngram_range=(1, 2))
    X = vectorizer.fit_transform(patterns)
    
    # Train KNN (k=1 untuk nearest neighbor terdekat)
    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(X, labels)
    
    return knn, vectorizer, labels

# ======================== MAIN RESPONSE FUNCTION ========================
def get_response(user_input):
    """
    HYBRID AI LOGIC dengan prioritas:
    PRIORITAS 1 (Rule-Based):
      a. Math
      b. Time
      c. Name/Memory
    PRIORITAS 2 (AI KNN):
      Context understanding menggunakan KNN
    """
    
    # PRIORITAS 1a: Check Math
    math_result = check_math(user_input)
    if math_result:
        return math_result
    
    # PRIORITAS 1b: Check Time
    time_result = check_time(user_input)
    if time_result:
        return time_result
    
    # PRIORITAS 1c: Check Name/Memory
    name_result = check_name(user_input)
    if name_result:
        return name_result
    
    # PRIORITAS 2: KNN Context Understanding
    knn, vectorizer, labels = train_knn_model()
    
    if knn is None:
        return "Maaf, saya tidak bisa memproses pertanyaan Anda saat ini."
    
    try:
        # Vectorize user input
        user_vector = vectorizer.transform([user_input.lower()])
        
        # Predict intent
        predicted_tag = knn.predict(user_vector)[0]
        
        # Find matching response dari dataset
        for intent in dataset.get("intents", []):
            if intent.get("tag") == predicted_tag:
                responses = intent.get("responses", [])
                if responses:
                    response = responses[0]  # Ambil response pertama
                    
                    # Fitur: Sebut nama user sesekali di awal kalimat
                    if user_name and np.random.rand() > 0.5:
                        response = f"{user_name}, {response[0].lower()}{response[1:]}"
                    
                    return response
        
        return "Maaf, saya tidak mengerti pertanyaan Anda. Bisa rephrase?"
    
    except Exception as e:
        return f"Terjadi kesalahan: {str(e)}"

# ======================== VOICE FUNCTIONS (MULTITHREADING) ========================
def speak(text):
    """
    Convert text ke MP3 menggunakan gTTS dan play dengan playsound
    Menggunakan threading untuk tidak memblock GUI
    """
    def _speak_thread():
        try:
            temp_file = "temp_audio.mp3"
            
            # Generate MP3
            tts = gTTS(text=text, lang='id', slow=False)
            tts.save(temp_file)
            
            # Play audio
            playsound(temp_file)
            
            # Delete temp file
            if os.path.exists(temp_file):
                os.remove(temp_file)
        except Exception as e:
            print(f"Error speaking: {e}")
    
    # Run di thread terpisah
    thread = threading.Thread(target=_speak_thread, daemon=True)
    thread.start()

def voice_input():
    """
    Dengarkan input dari microphone dan convert ke teks
    Auto-send ke chatbot setelah voice input selesai
    Menggunakan threading untuk tidak memblock GUI
    """
    def _voice_input_thread():
        try:
            status_label.config(text="🎤 Mendengarkan...", fg="#f39c12")
            root.update()
            
            with sr.Microphone() as source:
                # Adjust untuk ambient noise
                recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Record dengan timeout
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            # Recognize speech
            text = recognizer.recognize_google(audio, language='id-ID')
            
            # Set ke entry box
            user_entry.delete(0, tk.END)
            user_entry.insert(0, text)
            
            status_label.config(text="✅ Terima kasih", fg="#27ae60")
            root.update()
            
            # Auto-send setelah 1 detik
            time.sleep(1)
            send_message()
            
        except sr.RequestError:
            status_label.config(text="❌ Kesalahan koneksi internet", fg="#e74c3c")
            messagebox.showerror("Error", "Tidak ada koneksi internet untuk speech recognition.")
        except sr.UnknownValueError:
            status_label.config(text="❌ Tidak bisa dengar suara", fg="#e74c3c")
            messagebox.showwarning("Warning", "Maaf, saya tidak bisa mengerti suara Anda.")
        except Exception as e:
            status_label.config(text="❌ Error", fg="#e74c3c")
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    # Run di thread terpisah
    thread = threading.Thread(target=_voice_input_thread, daemon=True)
    thread.start()

# ======================== GUI FUNCTIONS ========================
def send_message():
    """
    Kirim pesan dari user ke chatbot dan tampilkan response
    """
    user_input = user_entry.get()
    
    if not user_input.strip():
        messagebox.showwarning("Warning", "Silakan masukkan teks atau gunakan mic!")
        return
    
    # Tampilkan user message di chat log
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, f"\n👤 Kamu: {user_input}\n", "user")
    chat_log.see(tk.END)
    chat_log.config(state=tk.DISABLED)
    
    # Clear entry
    user_entry.delete(0, tk.END)
    
    # Get response from chatbot
    response = get_response(user_input)
    
    # Tampilkan bot response di chat log
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, f"🤖 UNKLAB Bot: {response}\n", "bot")
    chat_log.see(tk.END)
    chat_log.config(state=tk.DISABLED)
    
    # Speak the response (optional - uncomment untuk aktifkan)
    # speak(response)
    
    # Log untuk debug (optional)
    print(f"[USER] {user_input}")
    print(f"[BOT] {response}\n")

def on_enter_key(event):
    """
    Send message saat user tekan Enter
    """
    send_message()

# ======================== GUI SETUP ========================
def create_gui():
    """
    Setup GUI menggunakan Tkinter dengan tema biru UNKLAB
    """
    global root, chat_log, user_entry, status_label
    
    root = tk.Tk()
    root.title("Chatbot Universitas Klabat (UNKLAB)")
    root.geometry("700x650")
    
    # Color theme - Biru UNKLAB
    bg_color = "#2c3e50"
    fg_color = "#ecf0f1"
    accent_color = "#3498db"
    
    root.configure(bg=bg_color)
    
    # ===== HEADER FRAME =====
    header_frame = tk.Frame(root, bg=accent_color, height=60)
    header_frame.pack(fill=tk.X)
    
    title_label = tk.Label(
        header_frame,
        text="🎓 UNKLAB AI Assistant",
        font=("Helvetica", 18, "bold"),
        bg=accent_color,
        fg="white"
    )
    title_label.pack(pady=10)
    
    # ===== STATUS LABEL =====
    status_label = tk.Label(
        root,
        text="✅ Siap",
        font=("Helvetica", 9),
        bg=bg_color,
        fg="#27ae60"
    )
    status_label.pack(pady=5)
    
    # ===== CHAT LOG (SCROLLED TEXT) =====
    chat_frame = tk.Frame(root, bg=bg_color)
    chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    chat_log = scrolledtext.ScrolledText(
        chat_frame,
        wrap=tk.WORD,
        font=("Courier", 10),
        bg="#34495e",
        fg=fg_color,
        state=tk.DISABLED,
        relief=tk.FLAT,
        highlightthickness=0
    )
    chat_log.pack(fill=tk.BOTH, expand=True)
    
    # Configure tags untuk styling
    chat_log.tag_config("user", foreground="#3498db", font=("Courier", 10, "bold"))
    chat_log.tag_config("bot", foreground="#2ecc71", font=("Courier", 10, "bold"))
    
    # ===== INPUT FRAME =====
    input_frame = tk.Frame(root, bg=bg_color)
    input_frame.pack(fill=tk.X, padx=10, pady=10)
    
    user_entry = tk.Entry(
        input_frame,
        font=("Courier", 11),
        bg="#34495e",
        fg=fg_color,
        insertbackground=fg_color,
        relief=tk.FLAT,
        highlightthickness=0
    )
    user_entry.pack(fill=tk.X, side=tk.LEFT, expand=True, ipady=8)
    user_entry.bind('<Return>', on_enter_key)  # Enter key to send
    
    # ===== BUTTONS FRAME =====
    button_frame = tk.Frame(root, bg=bg_color)
    button_frame.pack(fill=tk.X, padx=10, pady=5)
    
    send_btn = tk.Button(
        button_frame,
        text="📤 Kirim",
        command=send_message,
        bg=accent_color,
        fg="white",
        font=("Helvetica", 10, "bold"),
        relief=tk.FLAT,
        cursor="hand2",
        padx=15,
        pady=8
    )
    send_btn.pack(side=tk.LEFT, padx=5)
    
    mic_btn = tk.Button(
        button_frame,
        text="🎤 Dengar",
        command=voice_input,
        bg="#e74c3c",
        fg="white",
        font=("Helvetica", 10, "bold"),
        relief=tk.FLAT,
        cursor="hand2",
        padx=15,
        pady=8
    )
    mic_btn.pack(side=tk.LEFT, padx=5)
    
    clear_btn = tk.Button(
        button_frame,
        text="🗑️  Hapus",
        command=lambda: chat_log.config(state=tk.NORMAL) or chat_log.delete(1.0, tk.END) or chat_log.config(state=tk.DISABLED),
        bg="#95a5a6",
        fg="white",
        font=("Helvetica", 10, "bold"),
        relief=tk.FLAT,
        cursor="hand2",
        padx=15,
        pady=8
    )
    clear_btn.pack(side=tk.LEFT, padx=5)
    
    # Welcome message
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, "🤖 UNKLAB Bot: Assalamualaikum! Selamat datang di Chatbot Universitas Klabat.\n", "bot")
    chat_log.insert(tk.END, "🤖 UNKLAB Bot: Tanya saya tentang UNKLAB, atau gunakan fitur kalkulator & waktu real-time!\n\n", "bot")
    chat_log.config(state=tk.DISABLED)
    
    return root

# ======================== MAIN PROGRAM ========================
if __name__ == "__main__":
    print("=" * 60)
    print("Chatbot Universitas Klabat (UNKLAB) - Hybrid AI")
    print("=" * 60)
    
    # Load dataset
    load_dataset()
    print(f"✅ Dataset loaded: {len(dataset.get('intents', []))} intents")
    
    # Create and run GUI
    root = create_gui()
    print("✅ GUI started")
    print("\n💡 Tips:")
    print("  - Tanya tentang UNKLAB (Salam, Lokasi, Fakultas, dll)")
    print("  - Lakukan operasi math: '5 tambah 3', '10 kali 2', etc")
    print("  - Tanya waktu: 'Jam berapa?', 'Tanggal berapa?'")
    print("  - Beritahu nama: 'Nama saya [nama]'")
    print("  - Gunakan tombol Dengar untuk voice input")
    print("=" * 60)
    
    root.mainloop()
