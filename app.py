import os
import re
from flask import Flask, render_template, request, send_file, flash, redirect
import yt_dlp

app = Flask(__name__)
app.secret_key = "chave_secreta_downfree_2026"

DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('video_url')
    if not url:
        flash("Por favor, insira um link válido.")
        return redirect('/')

    ydl_opts = {
        # Força baixar apenas arquivos mp4 nativos, evitando erros de processamento de codec na Render
        'format': 'best[ext=mp4]/mp4/best',
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': False,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
    }

    render_cookie_path = "/etc/secrets/cookies.txt"
    if os.path.exists(render_cookie_path):
        ydl_opts['cookiefile'] = render_cookie_path

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            
        return send_file(filename, as_attachment=True, download_name=os.path.basename(filename))
    except Exception as e:
        print(f"Erro: {str(e)}")
        flash("Erro ao extrair vídeo desta plataforma. Tente outra URL.")
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

ydl_opts['proxy'] = 'http://usuario:senha@ip_do_proxy:porta'
