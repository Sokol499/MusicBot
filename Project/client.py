from api.main_pb2 import Song, Playlist, SongPlaylist, Empty
from api.main_pb2_grpc import MusicServiceStub
from grpc import insecure_channel

def get_host_port():
    host = "localhost"
    port = "9000"
    return host, port


def add_playlist(playlist_name):
    host, port = get_host_port()
    target = f"{host}:{port}"

    try:
        with insecure_channel(target) as channel:
            client = MusicServiceStub(channel)

            playlist = Playlist(name=playlist_name)

            response = client.AddPlaylist(playlist)
            print(response.response)

    except Exception as e:
        print("Error:", e)


def add_song(song_author, song_name):
    host, port = get_host_port()
    target = f"{host}:{port}"

    try:
        with insecure_channel(target) as channel:
            client = MusicServiceStub(channel)

            song = Song(
                author=song_author,
                name=song_name,
            )

            response = client.AddSong(song)
            print(response.response)

    except Exception as e:
        print("Error:", e)


def add_song_to_playlist(song_name, playlist_name):
    host, port = get_host_port()
    target = f"{host}:{port}"

    try:
        with insecure_channel(target) as channel:
            client = MusicServiceStub(channel)

            song_playlist = SongPlaylist(
                song=Song(name=song_name),
                playlist=Playlist(name=playlist_name)
            )

            response = client.AddSongToPlaylist(song_playlist)

            if response is None:
                print("Error:", "not found")
            else:
                print(response.response)

    except Exception as e:
        print("Error:", e)


def delete_playlist(playlist_name):
    host, port = get_host_port()
    target = f"{host}:{port}"

    try:
        with insecure_channel(target) as channel:
            client = MusicServiceStub(channel)

            response = client.DeletePlaylist(Playlist(name=playlist_name))

            if response is None:
                print("Error:", "not found")
            else:
                print(response.response)

    except Exception as e:
        print("Error:", e)


def delete_song(song_name):
    host, port = get_host_port()
    target = f"{host}:{port}"

    try:
        with insecure_channel(target) as channel:
            client = MusicServiceStub(channel)

            response = client.DeleteSong(Song(name=song_name))

            print(response.response)

    except Exception as e:
        print("Error:", e)


def delete_song_from_playlist(song_name, playlist_name):
    host, port = get_host_port()
    target = f"{host}:{port}"

    try:
        with insecure_channel(target) as channel:
            client = MusicServiceStub(channel)

            song_playlist = SongPlaylist(
                song=Song(name=song_name),
                playlist=Playlist(name=playlist_name)
            )

            response = client.DeleteSongFromPlaylist(song_playlist)

            if response is None:
                print("Error:", "not found")
            else:
                print(response.response)

    except Exception as e:
        print("Error:", e)


def get_playlist(playlist_name):
    host, port = get_host_port()
    target = f"{host}:{port}"

    try:
        with insecure_channel(target) as channel:
            client = MusicServiceStub(channel)

            response = client.GetPlaylist(Playlist(name=playlist_name))

            if response is None:
                print("Error:", "not found")
            else:
                print(response.response)

    except Exception as e:
        print("Error:", e)


def get_song(song_name):
    host, port = get_host_port()
    target = f"{host}:{port}"

    try:
        with insecure_channel(target) as channel:
            client = MusicServiceStub(channel)

            response = client.GetSong(Song(name=song_name))

            print(response)

    except Exception as e:
        print("Error:", e)


def play():
    host, port = get_host_port()
    target = f"{host}:{port}"

    try:
        with insecure_channel(target) as channel:
            client = MusicServiceStub(channel)

            response = client.Play(Empty())

            print(response.response)

    except Exception as e:
        print("Error:", e)


def print_playlist(playlist_name):
    host, port = get_host_port()
    target = f"{host}:{port}"

    try:
        with insecure_channel(target) as channel:
            client = MusicServiceStub(channel)

            response = client.PrintPlaylist(Playlist(name=playlist_name))

            if response is None:
                print("Error: not found")
            else:
                for i, song in enumerate(response.songs, start=1):
                    print(f"№{i}. Song: {song}")

    except Exception as e:
        print("Error:", e)


def update(song_name):
    host, port = get_host_port()
    target = f"{host}:{port}"

    try:
        with insecure_channel(target) as channel:
            client = MusicServiceStub(channel)

            response = client.UpdateSong(Song(name=song_name))

            print(response.response)

    except Exception as e:
        print("Error:", e)


def update_playlist(playlist_name):
    host, port = get_host_port()
    target = f"{host}:{port}"

    try:
        with insecure_channel(target) as channel:
            client = MusicServiceStub(channel)

            response = client.UpdatePlaylist(Playlist(name=playlist_name))

            print(response.response)

    except Exception as e:
        print("Error:", e)
