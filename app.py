from flask import Flask, render_template, request, jsonify, send_file
import instaloader

app = Flask(__name__)

def download_instagram_video(url, save_path):
    loader = instaloader.Instaloader()

    try:
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(loader.context, shortcode)

        if post.is_video:
            loader.download_post(post, target=save_path)
            return f"Video downloaded to {save_path}"
        else:
            return "The given post is not a video"
    except instaloader.exceptions.ProfileNotExistsException:
        return "Invalid profile URL"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        save_path = 'path_to_save_video.mp4'  # Set your desired save path here

        # Download the video and save it to the server
        message = download_instagram_video(url, save_path)

        # Send the video file as a response to the user
        return send_file(save_path, as_attachment=True, download_name='downloaded_video.mp4')

    return render_template('index.html', message='')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
