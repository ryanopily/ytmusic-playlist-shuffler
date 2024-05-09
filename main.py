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

    # anchor_track is a track in the playlist that is in the wrong spot and needs to be moved ahead of its current position
    # instead of moving anchor_track directly, we move the correct tracks into anchor_track's current position, which pushes anchor_track forward
    # at some point, anchor_track will reach it's correct position, and a new anchor_track will be chosen
    anchor_track = playlist["tracks"].pop(0)

    while len(tracks) > 0:
        track = tracks.pop(0)

        #anchor_track is in the wrong position; move the correct track in its current position
        if track != anchor_track:
            track_order = (track["setVideoId"], anchor_track["setVideoId"],)
            print(f"Moving '{track["title"]}' before '{anchor_track["title"]}'")
            ytmusic.edit_playlist(args.playlist_id, moveItem=track_order)
            # avoid rate limit
            seconds = random.randint(1,3)
            milliseconds = random.randint(0,1000)
            time.sleep(seconds + milliseconds / 1000)
            # since track is in the correct position it cannot function as an anchor_track, so it must be removed
            if len(playlist["tracks"]) > 0:
                playlist["tracks"].remove(track)
        # anchor_track is in the correct position; choose a new anchor_track
        else:
            if len(playlist["tracks"]) > 0:
                anchor_track = playlist["tracks"].pop(0)
            print(f"Skipping {track["title"]}")