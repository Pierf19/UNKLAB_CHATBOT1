"""
Konfigurasi Chatbot UNKLAB
"""
import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
MODELS_DIR = os.path.join(DATA_DIR, 'models')
DOCS_DIR = os.path.join(BASE_DIR, 'docs')
STOP_WORDS = [
    # Kata Sambung Standar
    "yang", "di", "ke", "dari", "ini", "itu", "untuk", "pada",
    "adalah", "sebagai", "dengan", "dan", "atau", "juga", "karena",
    
    # Kata Ganti Orang
    "saya", "aku", "kami", "kita", "kamu", "anda", "dia", "mereka",
    "mu", "ku", "nya",
    
    # Kata Kerja/Bantu Umum
    "bisa", 
    "sedang", "sudah", "akan", "apakah", "bagaimana", "kenapa",
   
    
   
    "unklab", "universitas", "klabat", "kampus", "kuliah", "mahasiswa",
    "tanya", "bertanya", "info", "informasi", "tentang","unclab","asrama","fasilitas", 
]
# Files
INTENTS_FILE = os.path.join(PROCESSED_DATA_DIR, 'intents.json')
MODEL_FILE = os.path.join(MODELS_DIR, 'knn_model.pkl')
VECTORIZER_FILE = os.path.join(MODELS_DIR, 'vectorizer.pkl')
LABEL_ENCODER_FILE = os.path.join(MODELS_DIR, 'label_encoder.pkl')
HANDBOOK_FILE = os.path.join(DOCS_DIR, 'buku_panduan.txt')

# Model
KNN_NEIGHBORS = 1
KNN_METRIC = 'cosine'
VECTORIZER_MAX_FEATURES = 2500
TEST_SIZE = 0.2
RANDOM_STATE = 42

# Voice
STT_LANGUAGE_ID = 'id-ID'
STT_LANGUAGE_EN = 'en-US'
TTS_LANGUAGE_ID = 'id'
TTS_LANGUAGE_EN = 'en'
TTS_RATE = 150
TTS_VOLUME = 0.0
# UI
WINDOW_TITLE = "🎓 Chatbot UNKLAB - Voice Assistant"
WINDOW_SIZE = "900x650"
CHAT_FONT = ("Segoe UI", 10)
INPUT_FONT = ("Segoe UI", 11)
HEADER_COLOR = "#1E3A8A"  # UNKLAB Blue
ACCENT_COLOR = "#10B981"  # Green

# UNKLAB Info
KAMPUS_NAME = "Universitas Klabat (UNKLAB)"
KAMPUS_TAGLINE = "Pathway to Excellence"
KAMPUS_WEBSITE = "https://www.unklab.ac.id"
KAMPUS_EMAIL = "info@unklab.ac.id"

# Create dirs
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)