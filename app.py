from flask import Flask, request, send_file, jsonify
from pytube import YouTube
from io import BytesIO

app = Flask(__name__)

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

        # Return the video content as a file download
        return send_file(video_data, as_attachment=True, download_name=f'{youtube.video_id}.mp4')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
