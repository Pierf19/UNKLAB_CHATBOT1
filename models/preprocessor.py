"""
Text Preprocessor untuk Bahasa Indonesia dan Inggris
"""
import re
import string
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
except ImportError:
    print("ERROR: NLTK tidak terinstall!")
    print("Install: pip install nltk")
    raise

# Download NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading NLTK punkt...")
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    print("Downloading NLTK stopwords...")
    nltk.download('stopwords')

# Sastrawi (optional)
try:
    from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
    SASTRAWI_AVAILABLE = True
except ImportError:
    SASTRAWI_AVAILABLE = False
    print("Warning: Sastrawi tidak terinstall. Stemming Indonesia disabled.")
    print("Install (optional): pip install Sastrawi")


class TextPreprocessor:
    """Preprocessor untuk text Bahasa Indonesia dan Inggris"""
    
    
    def __init__(self, language='id'):
        """
        Initialize preprocessor
        
        Args:
            language: 'id' untuk Indonesia, 'en' untuk English
        """
        self.language = language
        
        # Load stopwords
        try:
            self.stopwords_id = set(stopwords.words('indonesian'))
        except:
            self.stopwords_id = set()
            print("Warning: Indonesian stopwords not available")
        
        try:
            self.stopwords_en = set(stopwords.words('english'))
        except:
            self.stopwords_en = set()
            print("Warning: English stopwords not available")
        
        # Initialize Sastrawi stemmer
        if SASTRAWI_AVAILABLE:
            factory = StemmerFactory()
            self.stemmer_id = factory.create_stemmer()
        else:
            self.stemmer_id = None
        self.slang_dict = {
        "unklap": "unklab",
        "unclab": "unklab",
        "un club": "unklab",
        "adven": "advent",
        "mks": "terima kasih",
        "makasih": "terima kasih",
        "gk": "tidak",
        "ga": "tidak",
        "asmet": "asrama",
        "chapel": "ibadah",
        "pesiar": "izin keluar"
    }

    def normalize_slang(self, text):
        words = text.split()
        return " ".join([self.slang_dict.get(w, w) for w in words])
    
    def clean_text(self, text: str) -> str:
        """
        Bersihkan text dari karakter yang tidak diinginkan
        """
        text = text.lower()
        
        # 1. Hapus URL, Email, Mentions
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        text = re.sub(r'\S+@\S+', '', text)
        text = re.sub(r'@\w+|#\w+', '', text)
        
        # 2. JANGAN HAPUS ANGKA (Penting untuk 'Pasal 49' atau fitur Kalkulator)
        # Kita hanya hapus simbol yang tidak perlu, tapi biarkan angka tetap ada
        # text = re.sub(r'\d+', '', text) <--- BARIS INI DIHAPUS/DIKOMENTAR
        
        # 3. Hapus Punctuation kecuali angka dan huruf
        # Gunakan regex agar lebih bersih
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # 4. Remove extra whitespace
        text = ' '.join(text.split())
        
        return text

    
    
    def remove_stopwords(self, text: str, language: str = None) -> str:
        """
        Hapus stopwords dari text
        """
        if language is None:
            language = self.language
        
        words = text.split()
        
        if language == 'id':
            filtered_words = [w for w in words if w not in self.stopwords_id]
        else:
            filtered_words = [w for w in words if w not in self.stopwords_en]
        
        return ' '.join(filtered_words)
    
    def stem_text(self, text: str, language: str = None) -> str:
        """
        Stemming text (hanya untuk Bahasa Indonesia)
        """
        if language is None:
            language = self.language
        
        if language == 'id' and self.stemmer_id:
            return self.stemmer_id.stem(text)
        
        return text
    
    def preprocess(self, text: str, 
                   remove_stopwords: bool = False, # UBAH JADI FALSE SECARA DEFAULT
                   apply_stemming: bool = False,   # UBAH JADI FALSE UNTUK KNN N-GRAM
                   language: str = None) -> str:
        
        # 1. Langkah Pertama: Lowercase & Clean (Hapus simbol tapi jaga angka)
        text = self.clean_text(text)
        
        # 2. Langkah Kedua: Normalisasi Slang
        # Dilakukan SETELAH clean_text supaya tanda tanya/titik sudah hilang
        text = self.normalize_slang(text)
        
        # 3. Langkah Ketiga: Deteksi bahasa
        if language is None:
            language = self.detect_language(text)
        
        # 4. Remove Stopwords (Opsional)
        # Untuk KNN, kata tanya seperti 'apa', 'dimana' sangat penting. 
        # Lebih baik biarkan saja (False) agar bot tahu beda 'apa asrama' dan 'asrama'
        if remove_stopwords:
            text = self.remove_stopwords(text, language)
        
        # 5. Stemming (Opsional)
        # Jika Anda pakai N-Gram di Vectorizer, Stemming seringkali tidak diperlukan
        # dan justru memperlambat proses training.
        if apply_stemming and language == 'id':
            text = self.stem_text(text, language)
        
        return text.strip()
    
    def detect_language(self, text: str) -> str:
        """
        Deteksi bahasa dari text (sederhana)
        """
        # Daftar kata umum Indonesia
        id_words = {'yang', 'dan', 'di', 'dari', 'ke', 'untuk', 'pada', 'dengan',
                    'adalah', 'ini', 'itu', 'saya', 'kamu', 'apa', 'tidak'}
        
        # Daftar kata umum English
        en_words = {'the', 'is', 'are', 'was', 'were', 'and', 'or', 'but',
                    'in', 'on', 'at', 'to', 'for', 'of', 'with', 'a', 'an'}
        
        words = set(text.lower().split())
        
        id_count = len(words & id_words)
        en_count = len(words & en_words)
        
        return 'id' if id_count >= en_count else 'en'


# Test
if __name__ == "__main__":
    preprocessor = TextPreprocessor()
    
    text_id = "Saya sangat senang hari ini! 😊"
    print(f"Original: {text_id}")
    print(f"Cleaned: {preprocessor.preprocess(text_id)}")