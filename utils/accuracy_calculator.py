"""
Accuracy Calculator untuk evaluasi model
"""
try:
    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score, 
        f1_score, classification_report, confusion_matrix
    )
except ImportError:
    print("ERROR: Scikit-learn tidak terinstall!")
    print("Install: pip install scikit-learn")
    raise


class AccuracyCalculator:
    """Calculator untuk berbagai metrics evaluasi"""
    
    def __init__(self):
        self.y_true = None
        self.y_pred = None
        self.labels = None
    
    def calculate(self, y_true, y_pred, labels=None):
        """Hitung semua metrics"""
        self.y_true = y_true
        self.y_pred = y_pred
        self.labels = labels
        
        metrics = {
            'accuracy': self.accuracy(),
            'precision': self.precision(),
            'recall': self.recall(),
            'f1_score': self.f1(),
            'confusion_matrix': self.get_confusion_matrix()
        }
        
        return metrics
    
    def accuracy(self):
        """Hitung accuracy"""
        return accuracy_score(self.y_true, self.y_pred)
    
    def precision(self, average='weighted'):
        """Hitung precision"""
        return precision_score(self.y_true, self.y_pred, average=average, zero_division=0)
    
    def recall(self, average='weighted'):
        """Hitung recall"""
        return recall_score(self.y_true, self.y_pred, average=average, zero_division=0)
    
    def f1(self, average='weighted'):
        """Hitung F1-score"""
        return f1_score(self.y_true, self.y_pred, average=average, zero_division=0)
    
    def get_confusion_matrix(self):
        """Hitung confusion matrix"""
        return confusion_matrix(self.y_true, self.y_pred)
    
    def get_classification_report(self):
        """Dapatkan classification report lengkap"""
        return classification_report(
            self.y_true, 
            self.y_pred, 
            target_names=self.labels,
            zero_division=0
        )
    
    def print_report(self):
        """Print evaluation report"""
        print("\n" + "="*60)
        print("MODEL EVALUATION REPORT")
        print("="*60)
        
        print(f"\nAccuracy:  {self.accuracy():.4f}")
        print(f"Precision: {self.precision():.4f}")
        print(f"Recall:    {self.recall():.4f}")
        print(f"F1-Score:  {self.f1():.4f}")
        
        print("\n" + "-"*60)
        print("CLASSIFICATION REPORT")
        print("-"*60)
        print(self.get_classification_report())
        
        print("\n" + "-"*60)
        print("CONFUSION MATRIX")
        print("-"*60)
        cm = self.get_confusion_matrix()
        print(cm)
        
        print("\n" + "="*60 + "\n")


# Test
if __name__ == "__main__":
    y_true = ['happy', 'sad', 'angry', 'happy', 'sad']
    y_pred = ['happy', 'sad', 'happy', 'happy', 'sad']
    labels = ['angry', 'happy', 'sad']
    
    calculator = AccuracyCalculator()
    metrics = calculator.calculate(y_true, y_pred, labels)
    calculator.print_report()