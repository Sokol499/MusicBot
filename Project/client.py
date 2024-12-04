import grpc
from contextlib import contextmanager
from api import *
from grpc import insecure_channel

def get_host_port():
    # Заменить на свою реализацию получения host и port
    host = "localhost"
    port = "9000"
    return host, port

def add_playlist(playlist_name):
    host, port = get_host_port()
    target = f"{host}:{port}"

    try:
        with insecure_channel(target) as channel:
            client = MusicServiceStub(channel)
            playlist = Playlist(name=playlist_name)  # Предположим, playlist_name определён
            response = client.AddPlaylist(playlist)
            print(response.response)  # `response` соответствует gRPC определению
    except Exception as e:
        print("Error:", e)