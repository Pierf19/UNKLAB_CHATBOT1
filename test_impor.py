"""
Test semua imports
"""
import sys
import os

print("Testing imports...")
print("="*60)

try:
    print("\n1. Testing config...")
    import config
    print("   ✓ config OK")
except Exception as e:
    print(f"   ✗ config ERROR: {e}")

try:
    print("\n2. Testing models.preprocessor...")
    from models.preprocessor import TextPreprocessor
    print("   ✓ TextPreprocessor OK")
except Exception as e:
    print(f"   ✗ TextPreprocessor ERROR: {e}")

try:
    print("\n3. Testing models.text_vectorizer...")
    from models.text_vectorizer import TextVectorizer
    print("   ✓ TextVectorizer OK")
except Exception as e:
    print(f"   ✗ TextVectorizer ERROR: {e}")

try:
    print("\n4. Testing models.knn_classifier...")
    from models.knn_classifier import KNNClassifier
    print("   ✓ KNNClassifier OK")
except Exception as e:
    print(f"   ✗ KNNClassifier ERROR: {e}")

try:
    print("\n5. Testing utils.accuracy_calculator...")
    from utils.accuracy_calculator import AccuracyCalculator
    print("   ✓ AccuracyCalculator OK")
except Exception as e:
    print(f"   ✗ AccuracyCalculator ERROR: {e}")

print("\n" + "="*60)
print("Import test completed!")
print("="*60)