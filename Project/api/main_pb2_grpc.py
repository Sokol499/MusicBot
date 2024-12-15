# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from . import main_pb2 as main__pb2

GRPC_GENERATED_VERSION = '1.64.0'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in main_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class MusicServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Play = channel.unary_unary(
                '/music_service.api.MusicService/Play',
                request_serializer=main__pb2.Empty.SerializeToString,
                response_deserializer=main__pb2.Response.FromString,
                _registered_method=True)
        self.Pause = channel.unary_unary(
                '/music_service.api.MusicService/Pause',
                request_serializer=main__pb2.Empty.SerializeToString,
                response_deserializer=main__pb2.Response.FromString,
                _registered_method=True)
        self.AddSong = channel.unary_unary(
                '/music_service.api.MusicService/AddSong',
                request_serializer=main__pb2.Song.SerializeToString,
                response_deserializer=main__pb2.Response.FromString,
                _registered_method=True)
        self.DeleteSong = channel.unary_unary(
                '/music_service.api.MusicService/DeleteSong',
                request_serializer=main__pb2.Song.SerializeToString,
                response_deserializer=main__pb2.Response.FromString,
                _registered_method=True)
        self.AddSongToPlaylist = channel.unary_unary(
                '/music_service.api.MusicService/AddSongToPlaylist',
                request_serializer=main__pb2.SongPlaylist.SerializeToString,
                response_deserializer=main__pb2.Response.FromString,
                _registered_method=True)
        self.DeleteSongFromPlaylist = channel.unary_unary(
                '/music_service.api.MusicService/DeleteSongFromPlaylist',
                request_serializer=main__pb2.SongPlaylist.SerializeToString,
                response_deserializer=main__pb2.Response.FromString,
                _registered_method=True)
        self.AddPlaylist = channel.unary_unary(
                '/music_service.api.MusicService/AddPlaylist',
                request_serializer=main__pb2.Playlist.SerializeToString,
                response_deserializer=main__pb2.Response.FromString,
                _registered_method=True)
        self.GetPlaylist = channel.unary_unary(
                '/music_service.api.MusicService/GetPlaylist',
                request_serializer=main__pb2.Playlist.SerializeToString,
                response_deserializer=main__pb2.Response.FromString,
                _registered_method=True)
        self.DeletePlaylist = channel.unary_unary(
                '/music_service.api.MusicService/DeletePlaylist',
                request_serializer=main__pb2.Playlist.SerializeToString,
                response_deserializer=main__pb2.Response.FromString,
                _registered_method=True)
        self.PrintPlaylist = channel.unary_unary(
                '/music_service.api.MusicService/PrintPlaylist',
                request_serializer=main__pb2.Playlist.SerializeToString,
                response_deserializer=main__pb2.Playlist.FromString,
                _registered_method=True)
        self.UpdatePlaylist = channel.unary_unary(
                '/music_service.api.MusicService/UpdatePlaylist',
                request_serializer=main__pb2.Playlist.SerializeToString,
                response_deserializer=main__pb2.Response.FromString,
                _registered_method=True)
        self.GetSong = channel.unary_unary(
                '/music_service.api.MusicService/GetSong',
                request_serializer=main__pb2.Song.SerializeToString,
                response_deserializer=main__pb2.Song.FromString,
                _registered_method=True)
        self.UpdateSong = channel.unary_unary(
                '/music_service.api.MusicService/UpdateSong',
                request_serializer=main__pb2.Song.SerializeToString,
                response_deserializer=main__pb2.Response.FromString,
                _registered_method=True)
        self.Next = channel.unary_unary(
                '/music_service.api.MusicService/Next',
                request_serializer=main__pb2.Empty.SerializeToString,
                response_deserializer=main__pb2.Response.FromString,
                _registered_method=True)
        self.Prev = channel.unary_unary(
                '/music_service.api.MusicService/Prev',
                request_serializer=main__pb2.Empty.SerializeToString,
                response_deserializer=main__pb2.Response.FromString,
                _registered_method=True)


class MusicServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Play(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Pause(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddSong(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteSong(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddSongToPlaylist(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteSongFromPlaylist(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddPlaylist(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPlaylist(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeletePlaylist(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PrintPlaylist(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdatePlaylist(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSong(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateSong(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Next(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Prev(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MusicServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Play': grpc.unary_unary_rpc_method_handler(
                    servicer.Play,
                    request_deserializer=main__pb2.Empty.FromString,
                    response_serializer=main__pb2.Response.SerializeToString,
            ),
            'Pause': grpc.unary_unary_rpc_method_handler(
                    servicer.Pause,
                    request_deserializer=main__pb2.Empty.FromString,
                    response_serializer=main__pb2.Response.SerializeToString,
            ),
            'AddSong': grpc.unary_unary_rpc_method_handler(
                    servicer.AddSong,
                    request_deserializer=main__pb2.Song.FromString,
                    response_serializer=main__pb2.Response.SerializeToString,
            ),
            'DeleteSong': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteSong,
                    request_deserializer=main__pb2.Song.FromString,
                    response_serializer=main__pb2.Response.SerializeToString,
            ),
            'AddSongToPlaylist': grpc.unary_unary_rpc_method_handler(
                    servicer.AddSongToPlaylist,
                    request_deserializer=main__pb2.SongPlaylist.FromString,
                    response_serializer=main__pb2.Response.SerializeToString,
            ),
            'DeleteSongFromPlaylist': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteSongFromPlaylist,
                    request_deserializer=main__pb2.SongPlaylist.FromString,
                    response_serializer=main__pb2.Response.SerializeToString,
            ),
            'AddPlaylist': grpc.unary_unary_rpc_method_handler(
                    servicer.AddPlaylist,
                    request_deserializer=main__pb2.Playlist.FromString,
                    response_serializer=main__pb2.Response.SerializeToString,
            ),
            'GetPlaylist': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPlaylist,
                    request_deserializer=main__pb2.Playlist.FromString,
                    response_serializer=main__pb2.Response.SerializeToString,
            ),
            'DeletePlaylist': grpc.unary_unary_rpc_method_handler(
                    servicer.DeletePlaylist,
                    request_deserializer=main__pb2.Playlist.FromString,
                    response_serializer=main__pb2.Response.SerializeToString,
            ),
            'PrintPlaylist': grpc.unary_unary_rpc_method_handler(
                    servicer.PrintPlaylist,
                    request_deserializer=main__pb2.Playlist.FromString,
                    response_serializer=main__pb2.Playlist.SerializeToString,
            ),
            'UpdatePlaylist': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdatePlaylist,
                    request_deserializer=main__pb2.Playlist.FromString,
                    response_serializer=main__pb2.Response.SerializeToString,
            ),
            'GetSong': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSong,
                    request_deserializer=main__pb2.Song.FromString,
                    response_serializer=main__pb2.Song.SerializeToString,
            ),
            'UpdateSong': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateSong,
                    request_deserializer=main__pb2.Song.FromString,
                    response_serializer=main__pb2.Response.SerializeToString,
            ),
            'Next': grpc.unary_unary_rpc_method_handler(
                    servicer.Next,
                    request_deserializer=main__pb2.Empty.FromString,
                    response_serializer=main__pb2.Response.SerializeToString,
            ),
            'Prev': grpc.unary_unary_rpc_method_handler(
                    servicer.Prev,
                    request_deserializer=main__pb2.Empty.FromString,
                    response_serializer=main__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'music_service.api.MusicService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('music_service.api.MusicService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class MusicService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Play(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/music_service.api.MusicService/Play',
            main__pb2.Empty.SerializeToString,
            main__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Pause(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/music_service.api.MusicService/Pause',
            main__pb2.Empty.SerializeToString,
            main__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def AddSong(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/music_service.api.MusicService/AddSong',
            main__pb2.Song.SerializeToString,
            main__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeleteSong(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/music_service.api.MusicService/DeleteSong',
            main__pb2.Song.SerializeToString,
            main__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def AddSongToPlaylist(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/music_service.api.MusicService/AddSongToPlaylist',
            main__pb2.SongPlaylist.SerializeToString,
            main__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeleteSongFromPlaylist(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/music_service.api.MusicService/DeleteSongFromPlaylist',
            main__pb2.SongPlaylist.SerializeToString,
            main__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def AddPlaylist(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/music_service.api.MusicService/AddPlaylist',
            main__pb2.Playlist.SerializeToString,
            main__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetPlaylist(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/music_service.api.MusicService/GetPlaylist',
            main__pb2.Playlist.SerializeToString,
            main__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeletePlaylist(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/music_service.api.MusicService/DeletePlaylist',
            main__pb2.Playlist.SerializeToString,
            main__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def PrintPlaylist(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/music_service.api.MusicService/PrintPlaylist',
            main__pb2.Playlist.SerializeToString,
            main__pb2.Playlist.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UpdatePlaylist(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/music_service.api.MusicService/UpdatePlaylist',
            main__pb2.Playlist.SerializeToString,
            main__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetSong(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/music_service.api.MusicService/GetSong',
            main__pb2.Song.SerializeToString,
            main__pb2.Song.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UpdateSong(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/music_service.api.MusicService/UpdateSong',
            main__pb2.Song.SerializeToString,
            main__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Next(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/music_service.api.MusicService/Next',
            main__pb2.Empty.SerializeToString,
            main__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Prev(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/music_service.api.MusicService/Prev',
            main__pb2.Empty.SerializeToString,
            main__pb2.Response.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)