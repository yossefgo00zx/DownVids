from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import tempfile

app = Flask(__name__)
CORS(app)  # ✅ أضف هذا السطر بعد إنشاء Flask app

@app.route('/api/download', methods=['POST'])
def download():
    data = request.json
    video_url = data.get('url')

    if not video_url:
        return jsonify({'error': 'رابط غير صالح'}), 400

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            ydl_opts = {
                'outtmpl': f'{tmpdir}/%(title)s.%(ext)s',
                'format': 'best',
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                filename = ydl.prepare_filename(info)

            return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return 'yt-dlp backend is running!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
