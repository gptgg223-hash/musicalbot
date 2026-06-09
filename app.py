from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.route('/search', methods=['POST'])
def search():
    song = request.form.get("song")
    response = requests.get(
    "https://jiosavanapiryden.vercel.app/api/search/songs",
    params={"query": song}
    )

    data = response.json()

    results = data["data"]["results"][:20]

    songs_html = ""

    for result in results:
        title = result["name"]
        artist = result["artists"]["primary"][0]["name"]
        duration = result["duration"]
        album = result["album"]["name"]
        image = result["image"][-1]["url"]

        songs_html += f"""
        <a href="{result['url']}" target="_blank">
<button style="padding:10px 20px;background:#1DB954;color:white;border:none;border-radius:8px">
🎵 Open Song
</button>
</a>

    <div style="background:#1e1e1e;padding:20px;border-radius:15px;width:90%;
max-width:300px;margin:15px auto;">
        <img src="{image}" width="180">
        <h2>
<a href="#" style="color:white;text-decoration:none;">
{title}
</a>
</h2>
        <p>🎤 Artist: {artist}</p>
        <p>💿 Album: {album}</p>
        <p>⏱️ Duration: {duration} sec</p>
    </div>
    """

    return f"""
    <html>
    <body style='background:#121212;color:white;font-family:Arial;text-align:center'>
        <h1>🎵 Search Results</h1>

        <div style='background:#222;padding:20px;border-radius:10px;width:80%;margin:auto'>
             <div style="background:#1e1e1e;padding:20px;border-radius:15px;width:300px;margin:auto">

{songs_html}

<button style="padding:10px 20px;background:#1DB954;color:white;border:none;border-radius:8px">
▶ Play
</button>

</div>

        </div>

        <br>
        <a href='/'>
            <button>⬅ Back</button>
        </a>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

