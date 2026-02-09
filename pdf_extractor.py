"""
Extract text dari PDF Buku Panduan Kampus
"""
import os
import re
try:
    import PyPDF2
except ImportError:
    print("Install PyPDF2: pip install PyPDF2")

from config import DOCS_DIR

def extract_text_from_pdf(pdf_path):
    """
    Extract semua text dari PDF
    
    Args:
        pdf_path: Path ke file PDF
        
    Returns:
        String berisi semua text dari PDF
    """
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            text = ""
            total_pages = len(pdf_reader.pages)
            
            print(f"\nMengekstrak PDF: {os.path.basename(pdf_path)}")
            print(f"Total halaman: {total_pages}")
            
            for page_num in range(total_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
                
                if (page_num + 1) % 10 == 0:
                    print(f"  Progress: {page_num + 1}/{total_pages} halaman...")
            
            print(f"✓ Ekstraksi selesai!")
            print(f"  Total karakter: {len(text)}")
            
            return text
            
    except Exception as e:
        print(f"Error: {e}")
        return ""

def clean_text(text):
    """Bersihkan text hasil ekstraksi"""
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters
    text = re.sub(r'[^\w\s\.,!?;:()\-\n]', '', text)
    
    # Fix line breaks
    text = text.replace('\n\n\n', '\n\n')
    
    return text.strip()

def extract_sections(text):
    """
    Extract sections dari buku panduan
    Contoh: BAB 1, BAB 2, atau sections lain
    """
    sections = {}
    
    # Pattern untuk detect chapter/bab
    patterns = [
        r'BAB\s+(\d+)\s*[:\-]?\s*([^\n]+)',
        r'CHAPTER\s+(\d+)\s*[:\-]?\s*([^\n]+)',
        r'([IVX]+)\.\s+([^\n]+)',  # Roman numerals
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            section_num = match.group(1)
            section_title = match.group(2).strip()
            sections[f"{section_num}. {section_title}"] = match.start()
    
    return sections

def create_knowledge_base(pdf_path):
    """
    Buat knowledge base dari PDF buku panduan
    
    Returns:
        Dictionary berisi informasi terstruktur
    """
    print("\n" + "="*60)
    print("MEMBUAT KNOWLEDGE BASE DARI PDF")
    print("="*60)
    
    # Extract text
    raw_text = extract_text_from_pdf(pdf_path)
    
    if not raw_text:
        print("Gagal extract PDF!")
        return None
    
    # Clean text
    cleaned_text = clean_text(raw_text)
    
    # Extract sections
    sections = extract_sections(cleaned_text)
    
    print(f"\n✓ Sections ditemukan: {len(sections)}")
    for section in list(sections.keys())[:5]:
        print(f"  - {section}")
    
    # Save to text file
    output_file = os.path.join(DOCS_DIR, 'buku_panduan_extracted.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)
    
    print(f"\n✓ Text tersimpan di: {output_file}")
    
    knowledge_base = {
        'raw_text': raw_text,
        'cleaned_text': cleaned_text,
        'sections': sections,
        'total_chars': len(cleaned_text),
        'total_words': len(cleaned_text.split())
    }
    
    print("\n" + "="*60)
    print("KNOWLEDGE BASE CREATED!")
    print("="*60)
    print(f"Total Words: {knowledge_base['total_words']}")
    print(f"Total Chars: {knowledge_base['total_chars']}")
    print("="*60 + "\n")
    
    return knowledge_base

def search_in_handbook(query, knowledge_base):
    """
    Search informasi dalam buku panduan
    
    Args:
        query: Pertanyaan user
        knowledge_base: Dictionary dari create_knowledge_base()
        
    Returns:
        Relevant text snippet
    """
    if not knowledge_base:
        return None
    
    text = knowledge_base['cleaned_text'].lower()
    query_lower = query.lower()
    
    # Simple keyword search
    keywords = query_lower.split()
    
    # Find paragraphs containing keywords
    paragraphs = text.split('\n\n')
    relevant = []
    
    for para in paragraphs:
        score = sum(1 for kw in keywords if kw in para)
        if score > 0:
            relevant.append((score, para))
    
    # Sort by relevance
    relevant.sort(reverse=True, key=lambda x: x[0])
    
    # Return top 3 paragraphs
    if relevant:
        top_results = [para for _, para in relevant[:3]]
        return '\n\n'.join(top_results)
    
    return None

if __name__ == "__main__":
    # Test extraction
    pdf_file = os.path.join(DOCS_DIR, 'buku_panduan_unklab.pdf')
    
    if os.path.exists(pdf_file):
        kb = create_knowledge_base(pdf_file)
        
        # Test search
        if kb:
            print("\nTest Search:")
            result = search_in_handbook("fakultas komputer", kb)
            if result:
                print(result[:500])
    else:
        print(f"PDF tidak ditemukan: {pdf_file}")
        print("Letakkan buku panduan PDF di folder 'docs/'")