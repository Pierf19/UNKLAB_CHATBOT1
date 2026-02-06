# 📚 CHATBOT UNIVERSITAS KLABAT (UNKLAB) - PANDUAN INSTALASI & SETUP

## 🎯 Persyaratan Sistem
- **Python:** 3.11.4 (atau versi 3.8+)
- **OS:** Windows 10/11 (atau Linux/Mac dengan adjustment minor)
- **Microphone:** Untuk fitur voice input (optional)
- **Internet:** Untuk speech recognition & text-to-speech (optional)

---

## 📦 STEP 1: Instalasi Library Required

Buka **PowerShell** atau **CMD** dan jalankan command berikut:

### A. Update pip (recommended)
```powershell
python -m pip install --upgrade pip
```

### B. Install semua library sekaligus
```powershell
pip install tkinter numpy scikit-learn SpeechRecognition gtts playsound
```

### C. Atau install satu per satu (jika ada error):
```powershell
# GUI Framework (built-in dengan Python, tapi pastikan)
pip install tk

# Numerical computing
pip install numpy

# Machine Learning (KNN classifier)
pip install scikit-learn

# Speech Recognition (Google API)
pip install SpeechRecognition

# Text-to-Speech (Google TTS)
pip install gtts

# Play audio files
pip install playsound
```

### D. Verifikasi instalasi
Jalankan command untuk check apakah semua library installed:
```powershell
python -c "import tkinter; import numpy; import sklearn; import speech_recognition; import gtts; import playsound; print('✅ Semua library berhasil installed!')"
```

---

## 🗂️ STEP 2: Setup File Project

Pastikan folder structure sudah seperti ini:
```
d:\UNKLAB_CHATBOT\TUGAS_CHATBOT_KAMPUS\
├── chatbot_kampus.py
├── kampus_data.json
└── SETUP_INSTALL.md (file ini)
```

---

## 🚀 STEP 3: Cara Menjalankan Aplikasi

### A. Via PowerShell/CMD (Recommended)
```powershell
# Navigate ke folder project
cd d:\UNKLAB_CHATBOT\TUGAS_CHATBOT_KAMPUS

# Jalankan program
python chatbot_kampus.py
```

### B. Atau langsung double-click file `.py` (Windows)
- Buka File Explorer
- Navigate ke `d:\UNKLAB_CHATBOT\TUGAS_CHATBOT_KAMPUS\`
- Double-click `chatbot_kampus.py`
- (Akan membuka CMD/PowerShell otomatis)

### C. Atau dari Visual Studio Code
```powershell
# Buka folder di VS Code
code d:\UNKLAB_CHATBOT\TUGAS_CHATBOT_KAMPUS

# Click "Run" button atau tekan F5
```

---

## 🎮 CARA MENGGUNAKAN APLIKASI

### 1. **Text Input (Standar)**
   - Ketik pertanyaan di text box
   - Tekan **Enter** atau klik tombol **"📤 Kirim"**
   - Bot akan merespon dengan jawaban

### 2. **Voice Input (Fitur Mic)**
   - Klik tombol **"🎤 Dengar"**
   - Tunggu status berubah menjadi "🎤 Mendengarkan..."
   - Berbicara dengan jelas ke microphone (5 detik max)
   - Teks otomatis muncul di text box
   - Bot otomatis merespon

### 3. **Clear Chat**
   - Klik tombol **"🗑️ Hapus"** untuk menghapus riwayat chat

---

## 💡 CONTOH PERTANYAAN

### Math (Kalkulator)
- "5 tambah 3"
- "10 kali 2"
- "15 bagi 3"
- "20 kurang 7"
- "50 + 25"

### Time (Waktu Real-time)
- "Jam berapa?"
- "Tanggal berapa?"
- "Jam sekarang"

### Memory (Nama)
- "Nama saya Budi"
- "Siapa nama saya?"
- "Nama saya adalah Siti"

### UNKLAB Info (Knowledge Base)
- "Tentang Unklab"
- "Dimana lokasi Unklab?"
- "Ada fakultas apa di Unklab?"
- "Info Filkom?"
- "Portal akademik?"
- "Info asrama?"
- "Biaya kuliah?"
- "Syarat sidang?"

---

## 🔧 TROUBLESHOOTING

### Problem 1: "ModuleNotFoundError: No module named 'tkinter'"
**Solution:**
```powershell
# Install tkinter (Windows)
pip install tk

# Or reinstall Python with tcl/tk checked
```

### Problem 2: "No module named 'speech_recognition'"
**Solution:**
```powershell
pip install SpeechRecognition
```

### Problem 3: Mic tidak bekerja
**Solution:**
- Check microphone settings Windows
- Pastikan app have permission untuk akses mic
- Atau skip voice feature dan gunakan text input

### Problem 4: Voice input "Tidak bisa dengar"
**Solution:**
- Berbicara lebih dekat ke mic
- Kurangi background noise
- Check internet connection (untuk Google Speech API)

### Problem 5: Error "PermissionError" saat save temp_audio.mp3
**Solution:**
- Close aplikasi lain yang mungkin lock file
- Atau disable fitur speak (comment line `speak(response)` di kode)

### Problem 6: Slow response pada KNN prediction
**Solution:**
- Normal behavior (training KNN saat runtime)
- Atau pre-train model dan save ke file `.pkl` (optimization)

---

## 🎨 FITUR-FITUR APLIKASI

### ✅ 4 TANTANGAN DOSEN (HYBRID AI)

#### 1️⃣ **MATH** - Kalkulator dengan Regex
- Detect operasi: tambah, kurang, kali, bagi
- Support multiple format: "5+3", "5 tambah 3"
- Real-time calculation dengan `eval()`
- Error handling untuk division by zero

#### 2️⃣ **MEMORY** - Ingat Nama User
- Simpan nama user di global variable
- Deteksi input "Nama saya [nama]"
- Recall nama saat bot merespon (50% probabilitas)
- Personalized responses dengan nama user

#### 3️⃣ **CONTEXT** - KNN Algorithm (AI)
- Train KNN classifier dari dataset JSON
- K=1 untuk nearest neighbor prediction
- Count Vectorizer untuk text feature extraction
- Match user intent dengan knowledge base

#### 4️⃣ **TIME** - Real-time Date/Time
- Deteksi keyword "jam" atau "tanggal"
- Return current datetime dengan format ID
- Precision: hingga detik (HH:MM:SS)

### 🔊 Fitur Tambahan

#### Voice Input (Multi-threading)
- Gunakan Google Speech Recognition API
- Async processing tidak block GUI
- Auto-send setelah voice recognized

#### Text-to-Speech (Multi-threading)
- Convert response ke MP3 (gTTS)
- Auto-play dengan playsound
- Clean temp file setelah selesai

#### GUI Themes
- Material Design (biru UNKLAB: #2c3e50)
- Responsive layout dengan Tkinter
- Color-coded messages (User=Biru, Bot=Hijau)

---

## 📊 STRUKTUR KODE

### File: `kampus_data.json`
```json
{
  "intents": [
    {
      "tag": "category_name",
      "patterns": ["pattern1", "pattern2", ...],
      "responses": ["response1", "response2", ...]
    },
    ...
  ]
}
```
- **tag**: Intent category identifier
- **patterns**: User input examples (untuk training KNN)
- **responses**: Bot answer (random pick)

### File: `chatbot_kampus.py`
```
Main Functions:
├── load_dataset()           # Load JSON
├── check_math()             # Regex math detection
├── check_time()             # Real-time datetime
├── check_name()             # Memory logic
├── train_knn_model()        # KNN classifier training
├── get_response()           # Main hybrid AI logic
├── speak()                  # gTTS + threading
├── voice_input()            # Speech recognition + threading
├── send_message()           # GUI message handler
└── create_gui()             # Tkinter GUI setup
```

---

## 🌟 OPTIMIZATION TIPS

### 1. Faster Response (KNN Training)
- Pre-train KNN dan save ke pickle file (`.pkl`)
- Load model saat startup

### 2. Better Voice Recognition
- Use offline recognition (local speech-to-text)
- Reduce background noise preprocessing

### 3. Custom Responses
- Edit `kampus_data.json` untuk add intents
- Bot otomatis learn dari dataset baru

### 4. Database Integration
- Replace JSON dengan SQL database
- Persistent user memory across sessions

---

## 📝 NOTES

- Aplikasi ini adalah **Hybrid AI System** = Rule-Based (Prioritas 1) + ML (Prioritas 2)
- KNN ditraining setiap kali user input (real-time training)
- Dataset UNKLAB-specific dengan 11 intents
- Support bahasa: **Indonesia** (ID) dan **English** (EN via speech API)
- Tested pada: Python 3.11.4, Windows 10/11

---

## 👨‍💼 Author
Senior Python Developer  
Date: February 2026  
Project: Chatbot Universitas Klabat (UNKLAB)

---

## 📞 SUPPORT & CONTACT

Jika ada masalah atau error, pastikan:
1. ✅ Python 3.11.4 terinstall
2. ✅ Semua library terinstall (check with `pip list`)
3. ✅ Microphone permission enabled (Windows Settings)
4. ✅ Internet connection aktif (untuk voice & speech)
5. ✅ File `kampus_data.json` ada di folder yang sama

Selamat menggunakan Chatbot UNKLAB! 🎓✨
