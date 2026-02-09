"""
Script training model UNKLAB Chatbot
"""
import json
import os
from sklearn.model_selection import train_test_split

from config import (
    INTENTS_FILE, MODEL_FILE, VECTORIZER_FILE, 
    LABEL_ENCODER_FILE, KNN_NEIGHBORS, KNN_METRIC,
    VECTORIZER_MAX_FEATURES, TEST_SIZE, RANDOM_STATE,STOP_WORDS
)
from models.preprocessor import TextPreprocessor
from models.text_vectorizer import TextVectorizer
from models.knn_classifier import KNNClassifier
from utils.accuracy_calculator import AccuracyCalculator

def load_intents(filepath):
    print(f"\nLoading intents from {filepath}...")
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File {filepath} tidak ditemukan!\nJalankan: python data_expander.py")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✓ Loaded {len(data['intents'])} intents")
    return data

def prepare_training_data(intents_data):
    X = []
    y = []
    
    for intent in intents_data['intents']:
        tag = intent['tag']
        patterns = intent['patterns']
        
        for pattern in patterns:
            X.append(pattern)
            y.append(tag)
    
    print(f"\nTotal training samples: {len(X)}")
    print(f"Total unique labels: {len(set(y))}")
    
    return X, y

def train_model():
    print("\n" + "="*60)
    print("TRAINING UNKLAB CHATBOT MODEL")
    print("="*60)
    
    # Load intents
    intents_data = load_intents(INTENTS_FILE)
    
    # Prepare data
    X_raw, y = prepare_training_data(intents_data)
    
    # Preprocess
    print("\n[1/5] Preprocessing text...")
    preprocessor = TextPreprocessor()
    X_processed = []
    
    for text in X_raw:
        lang = preprocessor.detect_language(text)
        processed = preprocessor.preprocess(
            text, 
            remove_stopwords=True,
            apply_stemming=(lang == 'id'),
            language=lang
        )
        X_processed.append(processed)
    
    print(f"✓ Preprocessed {len(X_processed)} texts")
    
    # Vectorize
    print("\n[2/5] Vectorizing text...")
    vectorizer = TextVectorizer(max_features=VECTORIZER_MAX_FEATURES,stop_words=STOP_WORDS) 
    X_vectors = vectorizer.fit_transform(X_processed)
    
    print(f"✓ Feature matrix: {X_vectors.shape}")
    
    # Split
    print("\n[3/5] Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_vectors, y, 
        test_size=TEST_SIZE, 
        random_state=RANDOM_STATE,
        stratify=y
    )
    
    print(f"✓ Train: {X_train.shape[0]} samples")
    print(f"✓ Test: {X_test.shape[0]} samples")
    
    # Train KNN
    print("\n[4/5] Training KNN...")
    knn = KNNClassifier(n_neighbors=KNN_NEIGHBORS, metric=KNN_METRIC)
    knn.fit(X_train, y_train)
    
    print("✓ Model trained!")
    
    # Evaluate
    print("\n[5/5] Evaluating...")
    
    y_pred = knn.predict(X_test)
    
    calculator = AccuracyCalculator()
    metrics = calculator.calculate(y_test, y_pred, labels=sorted(set(y)))
    
    calculator.print_report()
    
    # Save
    print("Saving model...")
    vectorizer.save(VECTORIZER_FILE)
    knn.save(MODEL_FILE, LABEL_ENCODER_FILE)
    
    print("\n" + "="*60)
    print("🎓 UNKLAB CHATBOT TRAINING COMPLETED!")
    print("="*60)
    print(f"\n📊 Accuracy: {metrics['accuracy']:.4f}")
    print(f"\n💾 Files saved:")
    print(f"  - {MODEL_FILE}")
    print(f"  - {VECTORIZER_FILE}")
    print(f"  - {LABEL_ENCODER_FILE}")
    print("\n🚀 Jalankan: python main.py")
    print("="*60 + "\n")
    
    return knn, vectorizer, metrics

if __name__ == "__main__":
    train_model()