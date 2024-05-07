if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("playlist_id", type=str, help="Resource ID of the playlist to modify",)
    parser.add_argument("--album", nargs="?", choices=["ascending",  "random", "descending"], help="Sort by album")
    parser.add_argument("--artist", nargs="?", choices=["ascending", "random", "descending"], help="Sort by artist")
    parser.add_argument("--title", nargs="?", choices=["ascending", "random", "descending"], help="Sort by title")
    parser.add_argument("sort_order", nargs="+", choices=["album", "artist", "title"], help="Specify sort order")
    args = parser.parse_args()

    import copy, ytmusicapi
    ytmusic = ytmusicapi.YTMusic("browser.json")
    playlist = ytmusic.get_playlist(args.playlist_id, None, False, 0)
    tracks = copy.deepcopy(playlist["tracks"])

    album_dict = {}

    def sort_by_album(track):
        try:
            album_dict[track["album"]["name"].lower() or ""] = track

            if args.album == "random":
                return hash(track["album"]["name"] or "")
            else:
                return track["album"]["name"].lower() or ""
        except:
            return ""

    artist_dict = {}

    def sort_by_artist(track):
        try:
            artist_dict[track["artists"][0]["name"].lower() or ""] = track

            if args.artist == "random":
                return hash(track["artists"][0]["name"] or "")
            else:
                return track["artists"][0]["name"].lower() or ""
        except:
            return ""

    title_dict = {}

    def sort_by_title(track):
        try:
            title_dict[track["title"].lower() or ""] = track

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

    anchor_track = playlist["tracks"][0]

    while len(tracks) > 0:
        track = tracks.pop(0)

        # Use the first track in the playlist as an anchor point to sort the other tracks
        # Move the first track after all other tracks have been sorted

        if track["setVideoId"] != anchor_track["setVideoId"]:
            track_order = (track["setVideoId"], anchor_track["setVideoId"],)
            print(f"Moving '{track["title"]}' before '{anchor_track["title"]}'...", end="")

            if playlist["tracks"].index(track) != playlist["tracks"].index(anchor_track) - 1:
                ytmusic.edit_playlist(args.playlist_id, moveItem=track_order)
                seconds = random.randint(1,2)
                milliseconds = random.randint(0,1000)
                time.sleep(seconds + milliseconds / 1000)

            print("success!")
        else:
            bookmark_track = tracks[0]

    print(f"Moving '{anchor_track["title"]}' before '{bookmark_track["title"]}'...", end="")
    track_order = (anchor_track["setVideoId"], bookmark_track["setVideoId"])
    ytmusic.edit_playlist(args.playlist_id, moveItem=track_order)
    print("success!")
        
        