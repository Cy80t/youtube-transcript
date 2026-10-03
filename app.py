from youtube_transcript_api import YouTubeTranscriptApi


video_id = "V6UiEXrVrvg"

ytt_api = YouTubeTranscriptApi()
transcript = ytt_api.fetch(video_id)

text = " ".join(snippet.text for snippet in transcript)

print(text)
