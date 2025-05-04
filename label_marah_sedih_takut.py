import pandas as pd
from label import get_sentiment

# Baca data
df = pd.read_csv('komentar_dengan_sentimen.csv')

def emosi(text):
    text_lower = text.lower()
    
    # Kata kunci untuk setiap emosi
    marah_keywords = ['marah', 'kesal', 'geram', 'murka', 'emosi', 'jengkel', 'benci', 'gondok', 'sebel', 
                     'mangkel', 'gak suka', 'ga suka', 'tidak suka', 'kzl', 'kezel', 'anjir', 'anjg',
                     'bangsat', 'bngst', 'sialan', 'kampret', '🤬', '😠', '😡']
                     
    sedih_keywords = ['sedih', 'kecewa', 'pilu', 'duka', 'nestapa', 'merana', 'galau', 'putus asa',
                      'depresi', 'menyesal', 'kehilangan', 'ditinggal', 'baper', 'nangis', 'menangis',
                      'terluka', 'sakit hati', '😢', '😭', '😔', '😞', '😥']
                      
    takut_keywords = ['takut', 'khawatir', 'cemas', 'was-was', 'ngeri', 'panik', 'trauma', 'paranoid',
                      'gelisah', 'gemetar', 'ketakutan', 'merinding', 'horor', 'horror', 'teror',
                      'mengancam', 'bahaya', '😨', '😰', '😱', '😳']
    
    # Cek kata kunci dengan bobot
    marah_count = sum([1 for word in marah_keywords if word in text_lower])
    sedih_count = sum([1 for word in sedih_keywords if word in text_lower])
    takut_count = sum([1 for word in takut_keywords if word in text_lower])
    
    # Tentukan emosi berdasarkan jumlah kata kunci terbanyak
    counts = {
        'Marah': marah_count,
        'Sedih': sedih_count, 
        'Takut': takut_count
    }
    
    max_emotion = max(counts.items(), key=lambda x: x[1])
    
    if max_emotion[1] > 0:
        return max_emotion[0]
    else:
        return 'Lainnya' # Return Lainnya jika tidak ada emosi spesifik

# Terapkan label emosi
df['emosi'] = df['komentar'].apply(emosi)

# Simpan ke file baru
df.to_csv('komentar_dengan_sentimen_khusus.csv', index=False, encoding='utf-8')

print("Labeling emosi selesai! Cek file komentar_dengan_sentimen_khusus.csv")

# Tampilkan distribusi label emosi
print("\nDistribusi Label Emosi:")
print(df['emosi'].value_counts())