import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")
URL = f"https://www.billboard.com/charts/hot-100/{date}/"
ID = "your client id"
SECRET = "your client secret"
response = requests.get(URL)
website_html = response.text
soup = BeautifulSoup(website_html, "html.parser")
all_songs = soup.select(selector="li ul li h3")
song_list = [song.getText().strip() for song in all_songs]
with open("songs.txt", mode="w", encoding="utf-8") as file:
    for song in song_list:
        file.write(f"{song}\n")

#spoptipy
spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=ID,
                              client_secret=SECRET,
                              redirect_uri="http://example.com",
                              scope="playlist-modify-private",
                              cache_path="token.txt",
                              show_dialog=True))
user_id = spotify.current_user()["id"]
song_uris = []
year = date.split("-")[0]
for song in song_list:
    result = spotify.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
        print(song_uris)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
playlist = spotify.user_playlist_create(user=user_id,name=f"{date} Billboard 100",public=False)
spotify.playlist_add_items(playlist_id=playlist['id'], items=song_uris)