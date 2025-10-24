"""
Script to download required NLTK data
"""
import nltk
import sys
import os

def download_nltk_data():
    """Download required NLTK datasets"""
    # Required NLTK data packages
    required_data = [
        'punkt',           # Tokenizer models
        'stopwords',       # Stopword lists
        'wordnet',         # WordNet lexical database
        'omw-1.4'         # Open Multilingual Wordnet
    ]
    
    print("Downloading required NLTK data...")
    for item in required_data:
        try:
            print(f"Downloading {item}...")
            nltk.download(item, quiet=True)
            print(f"✓ Successfully downloaded {item}")
        except Exception as e:
            print(f"✗ Failed to download {item}: {e}")
            return False
    
    print("All NLTK data downloaded successfully!")
    return True

if __name__ == "__main__":
    success = download_nltk_data()
    if not success:
        sys.exit(1)