"""
KNN Classifier untuk Chatbot
"""
try:
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.preprocessing import LabelEncoder
    import joblib
    import numpy as np
except ImportError:
    print("ERROR: Scikit-learn tidak terinstall!")
    print("Install: pip install scikit-learn joblib numpy")
    raise


class KNNClassifier:
    """K-Nearest Neighbors Classifier"""
    
    def __init__(self, n_neighbors=1, metric='cosine'):
        """
        Initialize KNN Classifier
        
        Args:
            n_neighbors: Jumlah neighbors untuk KNN
            metric: Distance metric ('cosine', 'euclidean', 'manhattan')
        """
        self.n_neighbors = n_neighbors
        self.metric = metric
        self.model = KNeighborsClassifier(
            n_neighbors=n_neighbors,
            metric=metric,
            weights='distance'
        )
        self.label_encoder = LabelEncoder()
        self.is_fitted = False
    
    def fit(self, X, y):
        """Train KNN model"""
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Train model
        self.model.fit(X, y_encoded)
        self.is_fitted = True
        
        return self
    
    def predict(self, X):
        """Prediksi label untuk input"""
        if not self.is_fitted:
            raise ValueError("Model belum di-train! Jalankan fit() terlebih dahulu.")
        
        y_pred_encoded = self.model.predict(X)
        y_pred = self.label_encoder.inverse_transform(y_pred_encoded)
        
        return y_pred
    
    def predict_proba(self, X):
        """Prediksi probabilitas untuk setiap class"""
        if not self.is_fitted:
            raise ValueError("Model belum di-train! Jalankan fit() terlebih dahulu.")
        
        return self.model.predict_proba(X)
    
    def predict_with_confidence(self, X):
        """Prediksi dengan confidence score"""
        predictions = self.predict(X)
        probas = self.predict_proba(X)
        
        # Confidence = probabilitas maksimum
        confidences = np.max(probas, axis=1)
        
        return predictions, confidences
    
    def save(self, model_path, encoder_path):
        """Simpan model dan encoder"""
        joblib.dump(self.model, model_path)
        joblib.dump(self.label_encoder, encoder_path)
        print(f"Model disimpan ke {model_path}")
        print(f"Label encoder disimpan ke {encoder_path}")
    
    def load(self, model_path, encoder_path):
        """Load model dan encoder"""
        self.model = joblib.load(model_path)
        self.label_encoder = joblib.load(encoder_path)
        self.is_fitted = True
        print(f"Model loaded dari {model_path}")
        return self


# Test
if __name__ == "__main__":
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    
    # Generate sample data
    X, y = make_classification(n_samples=100, n_features=10, n_classes=3, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    # Create and train KNN
    knn = KNNClassifier(n_neighbors=5)
    knn.fit(X_train, y_train)
    
    # Predict
    predictions, confidences = knn.predict_with_confidence(X_test)
    
    print("Predictions:", predictions[:5])
    print("Confidences:", confidences[:5])