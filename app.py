from flask import Flask, request, render_template_string
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)

HTML = """
<!doctype html>
<html lang="sv">
<head>
    <meta charset="utf-8">
    <title>YouTube Transcript</title>
</head>
<body>
    <h1>YouTube Transcript</h1>

    <form method="post">
        <input
            type="text"
            name="url"
            placeholder="Klistra in YouTube-länk"
            size="60"
            value="{{ url }}"
            required
        >
        <button type="submit">Hämta transkript</button>
    </form>

    {% if error %}
        <p><strong>Fel:</strong> {{ error }}</p>
    {% endif %}

    {% if transcript %}
        <h2>Transkript</h2>
        <textarea rows="30" cols="100">{{ transcript }}</textarea>
    {% endif %}
</body>
</html>
"""


def get_video_id(url):
    parsed = urlparse(url)

    if parsed.hostname in ("youtu.be", "www.youtu.be"):
        return parsed.path.lstrip("/")

    if parsed.hostname in ("youtube.com", "www.youtube.com"):
        return parse_qs(parsed.query).get("v", [None])[0]

    return None


@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""
    error = ""
    url = ""

    if request.method == "POST":
        url = request.form["url"]
        video_id = get_video_id(url)

        if not video_id:
            error = "Kunde inte hitta något YouTube-video-ID."
        else:
            try:
                ytt_api = YouTubeTranscriptApi()
                result = ytt_api.fetch(video_id)
                transcript = " ".join(item.text for item in result)
            except Exception as e:
                error = str(e)

    return render_template_string(
        HTML,
        transcript=transcript,
        error=error,
        url=url
    )


if __name__ == "__main__":
    app.run()
