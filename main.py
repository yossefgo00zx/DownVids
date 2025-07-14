from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/api/download', methods=['POST'])
def download():
    data = request.json
    video_url = data.get('url')

    if not video_url:
        return jsonify({'error': 'رابط غير صالح'}), 400

    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'format': 'best',
            'forcejson': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return jsonify({
                'title': info.get('title'),
                'url': info['url'],
                'ext': info.get('ext'),
                'thumbnail': info.get('thumbnail'),
                'duration': info.get('duration'),
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return 'yt-dlp backend is running!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
