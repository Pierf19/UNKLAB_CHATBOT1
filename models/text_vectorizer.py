"""
Text Vectorizer menggunakan TF-IDF
"""
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    import joblib
except ImportError:
    print("ERROR: Scikit-learn tidak terinstall!")
    print("Install: pip install scikit-learn joblib")
    raise


class TextVectorizer:
    """Vectorizer untuk convert text ke numerical features"""
    
    def __init__(self, max_features=2500, ngram_range=(1, 7),stop_words=None ):
        """
        Initialize vectorizer
        
        Args:
            max_features: Maksimal jumlah features
            ngram_range: Range untuk n-grams
        """
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            min_df=1,
            max_df=0.8,
            stop_words=stop_words, 
            lowercase=True,
            analyzer='char_wb',
            sublinear_tf=True
        )
        self.is_fitted = False
    
    def fit(self, texts):
        """Fit vectorizer pada texts"""
        self.vectorizer.fit(texts)
        self.is_fitted = True
        return self
    
    def transform(self, texts):
        """Transform texts ke numerical features"""
        if not self.is_fitted:
            raise ValueError("Vectorizer belum di-fit! Jalankan fit() terlebih dahulu.")
        
        return self.vectorizer.transform(texts)
    
    def fit_transform(self, texts):
        """Fit dan transform sekaligus"""
        self.fit(texts)
        return self.transform(texts)
    
    def save(self, filepath):
        """Simpan vectorizer ke file"""
        joblib.dump(self.vectorizer, filepath)
        print(f"Vectorizer disimpan ke {filepath}")
    
    def load(self, filepath):
        """Load vectorizer dari file"""
        self.vectorizer = joblib.load(filepath)
        self.is_fitted = True
        print(f"Vectorizer loaded dari {filepath}")
        return self


# Test
if __name__ == "__main__":
    texts = [
        "saya senang hari ini",
        "saya sedih sekali",
        "hari ini menyenangkan"
    ]
    
    vectorizer = TextVectorizer(max_features=10)
    X = vectorizer.fit_transform(texts)
    
    print("Feature matrix shape:", X.shape)
    print("Feature matrix:\n", X.toarray())