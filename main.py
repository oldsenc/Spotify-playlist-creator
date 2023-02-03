import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
URL = "https://www.billboard.com/charts/hot-100/"
response = requests.get(URL + date)
website_html = response.text
soup = BeautifulSoup(website_html, "html.parser")
song_list = soup.find_all(name="h3", class_="a-no-trucate")
song_names = [song.getText().strip() for song in song_list]

with open("music.txt", mode="w", encoding="utf-8") as file:
    for song in song_names:
        file.write(f"{song}\n")

# Spotify authetication.

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="1ee6bccecef846959f1f40c973e60353",
        client_secret="9df9c14ad2554131962ce9087e339841",
        show_dialog=True,
        cache_path="token.txt"

    )
)
user_id = sp.current_user()["id"]
print(user_id)

# Searching Spotify for songs by title
song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=song)
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

# Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

