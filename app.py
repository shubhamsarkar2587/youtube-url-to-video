from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from pytube import YouTube
from io import BytesIO

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['POST'])
def download_video():
    try:
        data = request.get_json()
        video_url = data.get('video_url')

        if not video_url:
            return jsonify({'error': 'Missing video_url in the request body'}), 400

        youtube = YouTube(video_url)
        video_stream = youtube.streams.get_highest_resolution()

        video_data = BytesIO()
        video_stream.stream_to_buffer(video_data)
        video_data.seek(0)

        return send_file(video_data,
                         mimetype='video/mp4',
                         as_attachment=True,
                         download_name=f'{youtube.video_id}.mp4',
                         max_age=0)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
