"""
UNKLAB Chatbot - Main Entry Point
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.chatbot_ui import main

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🎓 CHATBOT UNIVERSITAS KLABAT (UNKLAB)")
    print("="*60)
    print("\n✨ Features:")
    print("  ✓ Voice Chat (STT & TTS)")
    print("  ✓ Bilingual (Indonesia & English)")
    print("  ✓ KNN Machine Learning")
    print("  ✓ 25+ Topics, 500+ Patterns")
    print("  ✓ PDF Handbook Integration")
    print("\n📚 Topics:")
    print("  • Fakultas & Program Studi")
    print("  • Pendaftaran & Biaya")
    print("  • Asrama & Fasilitas")
    print("  • Portal Akademik")
    print("  • Beasiswa & Alumni")
    print("  • Dan masih banyak lagi!")
    print("\n" + "="*60 + "\n")
    
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPastikan sudah menjalankan:")
        print("  1. pip install -r requirements.txt")
        print("  2. python data_expander.py")
        print("  3. python train.py")
        sys.exit(1)