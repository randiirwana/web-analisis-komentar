from flask import Flask, render_template, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import io
import base64
from label import get_sentiment
import os

app = Flask(__name__)

# Path ke file CSV
CSV_FILE = 'komentar_dengan_sentimen_khusus.csv'

def load_data():
    try:
        if os.path.exists(CSV_FILE):
            df = pd.read_csv(CSV_FILE, encoding='utf-8')
            print("DEBUG: DataFrame shape:", df.shape)
            print("DEBUG: DataFrame columns:", df.columns)
            print("DEBUG: DataFrame head:\n", df.head())
            # Pastikan kolom yang diperlukan ada
            if 'komentar' not in df.columns or 'emosi' not in df.columns or 'sentimen' not in df.columns:
                df = pd.DataFrame(columns=['komentar', 'emosi', 'sentimen'])
            return df
        else:
            # Buat DataFrame kosong jika file tidak ada
            return pd.DataFrame(columns=['komentar', 'emosi', 'sentimen'])
    except Exception as e:
        print(f"Error loading CSV: {str(e)}")
        return pd.DataFrame(columns=['komentar', 'emosi', 'sentimen'])

def create_pie_chart(df):
    # Hitung jumlah untuk setiap sentimen
    sentiment_counts = df['sentimen'].value_counts()
    labels = ['Positif', 'Netral', 'Negatif', 'Sedih', 'Marah', 'Takut']
    values = [int(sentiment_counts.get(label, 0)) for label in labels]
    
    # Tambahkan data dummy jika kosong
    if sum(values[:3]) == 0:  # Jika Positif, Netral, Negatif semua 0
        values[0] = 1  # Tambah 1 ke Positif
        values[1] = 1  # Tambah 1 ke Netral
        values[2] = 1  # Tambah 1 ke Negatif
        
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title='Distribusi Sentimen')
    return fig.to_json()

def create_bar_chart(df):
    # Hitung jumlah untuk setiap sentimen
    sentiment_counts = df['sentimen'].value_counts()
    labels = ['Positif', 'Netral', 'Negatif', 'Sedih', 'Marah', 'Takut']
    values = [int(sentiment_counts.get(label, 0)) for label in labels]
    
    # Tambahkan data dummy jika kosong
    if sum(values[:3]) == 0:  # Jika Positif, Netral, Negatif semua 0
        values[0] = 1  # Tambah 1 ke Positif
        values[1] = 1  # Tambah 1 ke Netral 
        values[2] = 1  # Tambah 1 ke Negatif
        
    fig = go.Figure(data=[go.Bar(x=labels, y=values)])
    fig.update_layout(title='Jumlah Komentar per Sentimen')
    return fig.to_json()

def create_wordcloud(df, sentiment):
    text = ' '.join(df[df['sentimen'] == sentiment]['komentar'])
    if not text.strip():
        # Tambahkan teks dummy jika kosong
        if sentiment == 'Positif':
            text = 'bagus keren mantap hebat'
        elif sentiment == 'Negatif':
            text = 'buruk jelek kurang'
        elif sentiment == 'Netral':
            text = 'biasa cukup'
            
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode()

@app.route('/')
def index():
    df = load_data()
    comments = df.to_dict('records')
    return render_template('index.html', comments=comments)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        comment = data.get('comment', '')
        
        if not comment:
            return jsonify({'error': 'Komentar tidak boleh kosong'}), 400
            
        sentiment = get_sentiment(comment)
        
        # Simpan ke CSV
        df = load_data()
        new_row = pd.DataFrame({'komentar': [comment], 'emosi': [sentiment], 'sentimen': [sentiment]})
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(CSV_FILE, index=False, encoding='utf-8')
        
        # Pastikan file tersimpan dengan benar
        if not os.path.exists(CSV_FILE):
            return jsonify({'error': 'Gagal menyimpan komentar'}), 500
            
        return jsonify({
            'sentiment': sentiment,
            'comments': df.to_dict('records')
        })
    except Exception as e:
        print(f"Error in analyze: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/visualizations')
def get_visualizations():
    try:
        df = load_data()
        if df.empty:
            return jsonify({
                'pie_chart': None,
                'bar_chart': None,
                'wordcloud_positive': None,
                'wordcloud_negative': None,
                'wordcloud_neutral': None,
                'wordcloud_sedih': None,
                'wordcloud_marah': None,
                'wordcloud_takut': None,
                'sentiment_counts': {'Positif': 1, 'Netral': 1, 'Negatif': 1, 'Sedih': 0, 'Marah': 0, 'Takut': 0},
                'pie_sedih': None,
                'pie_marah': None,
                'pie_takut': None
            })
        valid_sentiments = ['Positif', 'Negatif', 'Netral', 'Sedih', 'Marah', 'Takut']
        df['emosi'] = df['emosi'].apply(lambda x: x if x in valid_sentiments else 'Netral')
        df['sentimen'] = df['sentimen'].apply(lambda x: x if x in valid_sentiments else 'Netral')
        pie_chart = create_pie_chart(df)
        bar_chart = create_bar_chart(df)
        wordcloud_positive = create_wordcloud(df, 'Positif')
        wordcloud_negative = create_wordcloud(df, 'Negatif')
        wordcloud_neutral = create_wordcloud(df, 'Netral')
        wordcloud_sedih = create_wordcloud(df, 'Sedih')
        wordcloud_marah = create_wordcloud(df, 'Marah')
        wordcloud_takut = create_wordcloud(df, 'Takut')
        sentiment_counts = df['sentimen'].value_counts().to_dict()
        for s in ['Positif', 'Netral', 'Negatif', 'Sedih', 'Marah', 'Takut']:
            if s not in sentiment_counts:
                sentiment_counts[s] = 1 if s in ['Positif', 'Netral', 'Negatif'] else 0
                
        # Diagram pie/bar khusus untuk Sedih, Marah, Takut
        def create_single_sentiment_pie(df, sentiment):
            total = len(df)
            count = sentiment_counts.get(sentiment, 0)
            labels = [sentiment, 'Lainnya']
            values = [count, total - count]
            fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
            fig.update_layout(title=f'Distribusi Sentimen {sentiment}')
            return fig.to_json()
            
        pie_sedih = create_single_sentiment_pie(df, 'Sedih')
        pie_marah = create_single_sentiment_pie(df, 'Marah')
        pie_takut = create_single_sentiment_pie(df, 'Takut')
        return jsonify({
            'pie_chart': pie_chart,
            'bar_chart': bar_chart,
            'wordcloud_positive': wordcloud_positive,
            'wordcloud_negative': wordcloud_negative,
            'wordcloud_neutral': wordcloud_neutral,
            'wordcloud_sedih': wordcloud_sedih,
            'wordcloud_marah': wordcloud_marah,
            'wordcloud_takut': wordcloud_takut,
            'sentiment_counts': sentiment_counts,
            'pie_sedih': pie_sedih,
            'pie_marah': pie_marah,
            'pie_takut': pie_takut
        })
    except Exception as e:
        print(f"Error in get_visualizations: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/comments')
def api_comments():
    df = load_data()
    comments = []
    for _, row in df.tail(1000).iterrows():
        comments.append({
            'text': row['komentar'],
            'sentiment': row['sentimen']
        })
    return jsonify(comments)

if __name__ == '__main__':
    app.run(debug=True)