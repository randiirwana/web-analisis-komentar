import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np
import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))

# Set style
sns.set_theme()
sns.set_palette("husl")

# Baca data
print("Membaca data...")
csv_path = os.path.join(APP_DIR, 'komentar_dengan_sentimen_khusus.csv')
df = pd.read_csv(csv_path)
df['sentimen'] = df['sentimen'].str.strip().str.capitalize()

# Konversi kolom waktu jika ada
if 'timestamp' in df.columns:
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['tanggal'] = df['timestamp'].dt.date
    df['jam'] = df['timestamp'].dt.hour
    df['hari'] = df['timestamp'].dt.day_name()

# 1. Visualisasi Distribusi Sentimen (Pie Chart)
plt.figure(figsize=(10, 6))
sentimen_counts = df['sentimen'].value_counts()
plt.pie(sentimen_counts, labels=sentimen_counts.index, autopct='%1.1f%%', startangle=90)
plt.title('Distribusi Sentimen Komentar')
plt.axis('equal')
plt.savefig('visualisasi_pie_sentimen.png')
plt.close()

# 2. Visualisasi Distribusi Sentimen (Bar Plot)
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='sentimen')
plt.title('Distribusi Sentimen Komentar')
plt.xlabel('Sentimen')
plt.ylabel('Jumlah Komentar')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('visualisasi_bar_sentimen.png')
plt.close()

if 'timestamp' in df.columns:
    # 3. Tren Sentimen per Hari
    plt.figure(figsize=(15, 6))
    daily_sentiment = df.groupby(['tanggal', 'sentimen']).size().unstack()
    daily_sentiment.plot(kind='line', marker='o')
    plt.title('Tren Sentimen per Hari')
    plt.xlabel('Tanggal')
    plt.ylabel('Jumlah Komentar')
    plt.legend(title='Sentimen')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('visualisasi_tren_harian.png')
    plt.close()

    # 4. Distribusi Komentar per Jam
    plt.figure(figsize=(12, 6))
    sns.histplot(data=df, x='jam', hue='sentimen', multiple="stack")
    plt.title('Distribusi Komentar per Jam')
    plt.xlabel('Jam')
    plt.ylabel('Jumlah Komentar')
    plt.tight_layout()
    plt.savefig('visualisasi_distribusi_jam.png')
    plt.close()

    # 5. Distribusi Komentar per Hari dalam Seminggu
    plt.figure(figsize=(12, 6))
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    sns.countplot(data=df, x='hari', hue='sentimen', order=day_order)
    plt.title('Distribusi Komentar per Hari dalam Seminggu')
    plt.xlabel('Hari')
    plt.ylabel('Jumlah Komentar')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('visualisasi_distribusi_hari.png')
    plt.close()

# 6. Wordcloud untuk setiap sentimen
try:
    from wordcloud import WordCloud
    
    def create_wordcloud(text, title, filename):
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(title)
        plt.tight_layout(pad=0)
        plt.savefig(filename)
        plt.close()

    for sentiment in df['sentimen'].unique():
        text = ' '.join(df[df['sentimen'] == sentiment]['komentar'])
        create_wordcloud(text, f'Wordcloud untuk Sentimen {sentiment}', 
                        f'wordcloud_{sentiment.lower()}.png')
except ImportError:
    print("Wordcloud tidak dapat dibuat. Install wordcloud dengan: pip install wordcloud")

# 7. Heatmap Aktivitas (Jam vs Hari)
if 'timestamp' in df.columns:
    plt.figure(figsize=(12, 8))
    df['hari_num'] = pd.Categorical(df['hari'], categories=day_order).codes
    heatmap_data = pd.crosstab(df['hari_num'], df['jam'])
    sns.heatmap(heatmap_data, cmap='Blues', annot=True, fmt='d')
    plt.title('Heatmap Aktivitas Komentar (Jam vs Hari)')
    plt.ylabel('Hari')
    plt.xlabel('Jam')
    plt.yticks(range(7), day_order)
    plt.tight_layout()
    plt.savefig('visualisasi_heatmap_aktivitas.png')
    plt.close()

print("Visualisasi selesai! File gambar telah disimpan.")

# Tampilkan ringkasan statistik
print("\nRingkasan Statistik:")
print("\nDistribusi Sentimen:")
print(df['sentimen'].value_counts(normalize=True).round(3) * 100, "%")

if 'timestamp' in df.columns:
    print("\nWaktu Paling Aktif:")
    print(f"Jam tersibuk: {df['jam'].mode().iloc[0]}")
    print(f"Hari tersibuk: {df['hari'].mode().iloc[0]}")

print("\nTotal Komentar:", len(df)) 