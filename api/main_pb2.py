from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Song(_message.Message):
    __slots__ = ("name", "duration", "author")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    name: str
    duration: int
    author: str
    def __init__(self, name: _Optional[str] = ..., duration: _Optional[int] = ..., author: _Optional[str] = ...) -> None: ...

class Playlist(_message.Message):
    __slots__ = ("name", "songs")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SONGS_FIELD_NUMBER: _ClassVar[int]
    name: str
    songs: _containers.RepeatedCompositeFieldContainer[Song]
    def __init__(self, name: _Optional[str] = ..., songs: _Optional[_Iterable[_Union[Song, _Mapping]]] = ...) -> None: ...

class SongPlaylist(_message.Message):
    __slots__ = ("song", "playlist")
    SONG_FIELD_NUMBER: _ClassVar[int]
    PLAYLIST_FIELD_NUMBER: _ClassVar[int]
    song: Song
    playlist: Playlist
    def __init__(self, song: _Optional[_Union[Song, _Mapping]] = ..., playlist: _Optional[_Union[Playlist, _Mapping]] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ("response",)
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: str
    def __init__(self, response: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
