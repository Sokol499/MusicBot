from api.main_pb2 import Song, Playlist, SongPlaylist, Empty
from api.main_pb2_grpc import MusicServiceStub
from grpc import insecure_channel

def get_host_port():
    host = "0.0.0.0"
    port = "8000"
    return host, port


def add_playlist(playlist_name: str):
    host, port = get_host_port()
    target = f"{host}:{port}"

    try:
        with insecure_channel(target) as channel:
            client = MusicServiceStub(channel)

            playlist = Playlist(name=playlist_name)

            response = client.AddPlaylist(playlist)

            return response.response

    except Exception as e:
        print("Error:", e)
        raise

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


def add_song_to_playlist(song_author, song_name, playlist_name):
    host, port = get_host_port()
    target = f"{host}:{port}"

    try:
        add_song(song_author, song_name)

        with insecure_channel(target) as channel:
            client = MusicServiceStub(channel)

            song_playlist = SongPlaylist(
                song=Song(name=song_name),
                playlist=Playlist(name=playlist_name)
            )

            response = client.AddSongToPlaylist(song_playlist)

            if not response or not response.response:
                print(f"Error: не удалось добавить песню '{song_name}' в плейлист '{playlist_name}'")
                return None
            else:
                return response.response

    except Exception as e:
        print(f"Error: {e}")
        return None


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


def print_playlist(playlist_name):
    host, port = get_host_port()
    target = f"{host}:{port}"

    try:
        with insecure_channel(target) as channel:
            client = MusicServiceStub(channel)

            response = client.PrintPlaylist(Playlist(name=playlist_name))

            if response is None or not response.songs:
                return f"Плейлист '{playlist_name}' пуст или не найден."

            playlist_message = f"В плейлисте '{playlist_name}' следующие треки:\n"
            for i, song in enumerate(response.songs, start=1):
                playlist_message += f"№{i}. {song.name}\n"

            return playlist_message

    except Exception as e:
        return f"Произошла ошибка при получении плейлиста '{playlist_name}': {e}"


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
