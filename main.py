if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("playlist_id", type=str, help="Resource ID of the playlist to modify",)
    parser.add_argument("--album", nargs="?", choices=["ascending",  "random", "descending"], help="Sort by album")
    parser.add_argument("--artist", nargs="?", choices=["ascending", "random", "descending"], help="Sort by artist")
    parser.add_argument("--title", nargs="?", choices=["ascending", "random", "descending"], help="Sort by title")
    parser.add_argument("sort_order", nargs="+", choices=["album", "artist", "title"], help="Specify sort order")
    args = parser.parse_args()

    import ytmusicapi
    ytmusic = ytmusicapi.YTMusic("browser.json")
    playlist = ytmusic.get_playlist(args.playlist_id, None, False, 0)
    tracks = playlist["tracks"]

    def sort_by_album(track):
        try:
            if args.album == "random":
                return hash(track["album"]["name"] or "")
            else:
                return track["album"]["name"].lower() or ""
        except:
            return ""

    def sort_by_artist(track):
        try:
            if args.artist == "random":
                return hash(track["artists"][0]["name"] or "")
            else:
                return track["artists"][0]["name"].lower() or ""
        except:
            return ""

    def sort_by_title(track):
        try:
            if args.title == "random":
                return hash(track["title"] or "")
            else:
                return track["title"].lower() or ""
        except:
            return ""

    for sort_method in args.sort_order:
        if sort_method == "album":
            if args.album == "random":
                tracks = sorted(tracks, key=sort_by_album)
            else:
                tracks = sorted(tracks, key=sort_by_album, reverse=True if args.album == "descending" else False)
        elif sort_method == "artist":
            if args.artist == "random":
                tracks = sorted(tracks, key=sort_by_artist)
            else:
                tracks = sorted(tracks, key=sort_by_artist, reverse=True if args.artist == "descending" else False)
        elif sort_method == "title":
            if args.title == "random":
                tracks = sorted(tracks, key=sort_by_title)
            else:
                tracks = sorted(tracks, key=sort_by_title, reverse=True if args.title == "descending" else False)
    
    import random, time
    last_track = None

    while len(tracks) > 0:
        track = tracks.pop(0)

        if last_track:
            track_order = (last_track["setVideoId"], track["setVideoId"],)
            print(f"Moving '{last_track["title"]}' before '{track["title"]}'...", end="")
            ytmusic.edit_playlist(args.playlist_id, moveItem=track_order)
            print("success!")

        last_track = track
        seconds = random.randint(1,4)
        milliseconds = random.randint(0,1000)
        time.sleep(seconds + milliseconds / 1000)
        