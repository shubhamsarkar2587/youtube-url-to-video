from flask import Flask, request, send_file, jsonify
from pytube import YouTube
from io import BytesIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['POST'])
def download_video():
    try:
        # Get the YouTube video URL from the request body
        data = request.get_json()
        video_url = data.get('video_url')

        if not video_url:
            return jsonify({'error': 'Missing video_url in request body'}), 400

        # Create a YouTube object
        youtube = YouTube(video_url)

        # Get the highest resolution stream (video and audio)
        video_stream = youtube.streams.get_highest_resolution()

        # Download the video content into a BytesIO object
        video_data = BytesIO()
        video_stream.stream_to_buffer(video_data)
        video_data.seek(0)

        # Set response headers for video content
        headers = {
            'Content-Type': 'video/mp4',
            'Content-Disposition': f'attachment; filename={youtube.video_id}.mp4'
        }

        # Return the video content with headers
        return send_file(video_data, mimetype='video/mp4', as_attachment=True, download_name=f'{youtube.video_id}.mp4', max_age=0)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
