import os
import re
from flask import Flask, render_template_string, request, send_file, flash, redirect
import yt_dlp

app = Flask(__name__)
app.secret_key = "chave_secreta_downfree_2026"

# Pasta temporária para salvar os downloads
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Interface DOWNFREE com Tailwind CSS v3 (Estável via CDN)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DOWNFREE - Download de Vídeos Grátis e Sem Limites</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- Tailwind CSS v3 (Script CDN Tradicional) -->
    <script src="https://tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Plus Jakarta Sans', 'sans-serif'],
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col justify-between antialiased relative overflow-x-hidden">

    <!-- Fundo Decorativo com Gradiente Sutil -->
    <div class="absolute inset-0 bg-gradient-to-b from-indigo-950/30 via-slate-950 to-slate-950 -z-10"></div>

    <!-- Header / Navbar -->
    <header class="w-full max-w-6xl mx-auto px-6 py-6 flex justify-between items-center">
        <div>
            <span class="text-2xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400">
                DOWNFREE<span class="text-indigo-500">.</span>
            </span>
        </div>
        <span class="text-xs font-semibold px-3 py-1 bg-indigo-500/10 border border-indigo-500/20 rounded-full text-indigo-400">
            v1.0 • Sem Limites
        </span>
    </header>

    <!-- Conteúdo Principal -->
    <main class="w-full max-w-2xl mx-auto px-6 py-12 flex-grow flex flex-col justify-center">
        
        <div class="text-center mb-8">
            <h1 class="text-4xl sm:text-5xl font-extrabold tracking-tight text-white mb-3">
                Baixe vídeos de <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">qualquer lugar</span>
            </h1>
            <p class="text-slate-400 text-base sm:text-lg max-w-md mx-auto">
                Cole o link abaixo para fazer o download instantâneo, sem marcas d'água e totalmente gratuito.
            </p>
        </div>

        <!-- Caixa de Alertas do Flask -->
        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            {% for category, message in messages %}
              <div class="mb-6 p-4 rounded-xl text-sm {% if category == 'error' %}bg-red-500/10 text-red-300 border border-red-500/20{% else %}bg-emerald-500/10 text-emerald-300 border border-emerald-500/20{% endif %}">
                {{ message }}
              </div>
            {% endfor %}
          {% endif %}
        {% endwith %}

        <!-- Formulário de Download -->
        <div class="bg-slate-900/60 border border-slate-800 p-6 sm:p-8 rounded-2xl shadow-2xl">
            <form action="/download" method="POST" class="space-y-4" onsubmit="showLoading()">
                <div class="relative">
                    <input 
                        type="url" 
                        name="video_url" 
                        id="video_url"
                        required 
                        placeholder="Cole a URL do TikTok, Instagram, YouTube..." 
                        class="w-full pl-4 pr-20 py-4 bg-slate-950 border border-slate-800 rounded-xl focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 text-white placeholder-slate-600 transition-all font-medium"
                    >
                    <button type="button" onclick="clearInput()" class="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300 text-xs font-semibold transition-colors">
                        LIMPAR
                    </button>
                </div>
                
                <button 
                    type="submit" 
                    id="btn-submit"
                    class="w-full py-4 bg-indigo-600 hover:bg-indigo-500 font-semibold rounded-xl transition-all shadow-lg shadow-indigo-600/20 text-white cursor-pointer"
                >
                    Download Automático
                </button>
            </form>

            <!-- Estado de Carregamento (Loading) -->
            <div id="loading" class="hidden mt-8 pt-6 border-t border-slate-800/60 flex flex-col items-center justify-center space-y-3">
                <div class="animate-spin rounded-full h-8 w-8 border-4 border-indigo-500 border-t-transparent"></div>
                <div class="text-center">
                    <p class="text-sm font-medium text-slate-200">Processando e extraindo a mídia...</p>
                    <p class="text-xs text-slate-500 mt-1">Isso pode levar alguns segundos dependendo da plataforma.</p>
                </div>
            </div>
        </div>

        <!-- Plataformas Suportadas (Apenas Visual) -->
        <div class="mt-12 flex flex-wrap justify-center gap-6 text-xs font-semibold text-slate-600 tracking-wider uppercase">
            <span>✦ TikTok</span>
            <span>✦ Instagram</span>
            <span>✦ YouTube</span>
            <span>✦ Twitter / X</span>
            <span>✦ Facebook</span>
        </div>

    </main>

    <!-- Footer -->
    <footer class="w-full text-center py-6 border-t border-slate-900 text-xs text-slate-600">
        <p>&copy; 2026 DOWNFREE. Todos os direitos reservados.</p>
    </footer>

    <script>
        function showLoading() {
            document.getElementById('loading').classList.remove('hidden');
            document.getElementById('btn-submit').disabled = true;
            document.getElementById('btn-submit').classList.add('opacity-40');
            document.getElementById('btn-submit').innerText = "Buscando vídeo...";
        }

        function clearInput() {
            document.getElementById('video_url').value = '';
            document.getElementById('video_url').focus();
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('video_url')
    
    if not url:
        flash("Por favor, insira um link válido.", "error")
        return redirect('/')

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            
        return send_file(
            filename,
            as_attachment=True,
            download_name=os.path.basename(filename)
        )

    except Exception as e:
        print(f"Erro: {str(e)}")
        flash("Erro ao processar este link. Verifique se ele está correto e tente novamente.", "error")
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
