package service

import (
	"container/list"
	"context"
	"music_service/errors"
	"fmt"
	"music_service/api"
	"music_service/core"
	"music_service/db"
)

func (srv *MusicServiceServer) Play(ctx context.Context, empty *api.Empty) (*api.Response, error) {
	res := srv.curPlaylist.Play()
	return &api.Response{Response: res}, nil
}

func (srv *MusicServiceServer) Pause(ctx context.Context, empty *api.Empty) (*api.Response, error) {
	res := srv.curPlaylist.Pause()
	return &api.Response{Response: res}, nil
}

func (srv *MusicServiceServer) AddSong(ctx context.Context, song *api.Song) (*api.Response, error) {
	s := new(core.Song)
	s.Author = song.Author
	s.Duration = int(song.Duration)
	s.Name = song.Name
	res := srv.curPlaylist.AddSong(s)
	err := db.AddSong(srv.DB, s)
	if err != nil {
		panic(err)
	}
	return &api.Response{Response: res}, nil
}

func (srv *MusicServiceServer) Next(ctx context.Context, empty *api.Empty) (*api.Response, error) {
	res := srv.curPlaylist.Next()
	return &api.Response{Response: res}, nil
}

func (srv *MusicServiceServer) Prev(ctx context.Context, empty *api.Empty) (*api.Response, error) {
	res := srv.curPlaylist.Prev()
	return &api.Response{Response: res}, nil
}

func (srv *MusicServiceServer) DeleteSong(ctx context.Context, song *api.Song) (*api.Response, error) {
	res, err := srv.curPlaylist.DeleteSong(song.Name)
	if err != nil {
		fmt.Println("Error:", err)
		return &api.Response{Response: ""}, err
	}
	err = db.DeleteSong(srv.DB, song.Name)
	if err != nil {
		fmt.Println("Error:", err)
		return &api.Response{Response: ""}, err
	}
	return &api.Response{Response: res}, err
}

func (srv *MusicServiceServer) AddPlaylist(ctx context.Context, playlist *api.Playlist) (*api.Response, error) {
	s := core.CreateSimplePlaylist(playlist.Name, list.New(), nil)
	res := core.AddPlaylist(s)
	err := db.AddPlaylist(srv.DB, playlist.Name)
	if err != nil {
		panic(err)
	}
	return &api.Response{Response: res}, nil
}

func (srv *MusicServiceServer) DeletePlaylist(ctx context.Context, playlist *api.Playlist) (*api.Response, error) {
	res, err := core.DeletePlaylist(playlist.Name, srv.curPlaylist)
	if err != nil {
		fmt.Println("Error:", err)
		return &api.Response{Response: ""}, err
	}
	err = db.DeletePlaylist(srv.DB, playlist.Name)
	if err != nil {
		fmt.Println("Error:", err)
		return &api.Response{Response: ""}, err
	}
	return &api.Response{Response: res}, err
}

func (srv *MusicServiceServer) PrintPlaylist(ctx context.Context, playlist *api.Playlist) (*api.Playlist, error) {
	id, err := db.GetPlaylistID(srv.DB, playlist.Name)
	if err != nil {
		return &api.Playlist{Songs: nil}, err
	}
	songs := db.GetPlaylistSongs(srv.DB, id)
	songsSlice := make([]*api.Song, songs.Len())
	i := 0
	if songs.Len() != 0 {
		for node := songs.Front(); node != nil; node = node.Next() {
			songsSlice[i] = &api.Song{
				Author:   node.Value.(*core.Song).Author,
				Name:     node.Value.(*core.Song).Name,
				Duration: int64(node.Value.(*core.Song).Duration),
			}
			i++
		}
	} else {
		err = errors.ErrNotFound
	}

	return &api.Playlist{Songs: songsSlice}, err
}

func (srv *MusicServiceServer) GetPlaylist(ctx context.Context, playlist *api.Playlist) (*api.Response, error) {
	id_playlist, err := db.GetPlaylistID(srv.DB, playlist.Name)
	if err != nil {
		return &api.Response{Response: ""}, err
	}
	songs := db.GetPlaylistSongs(srv.DB, id_playlist)
	srv.curPlaylist.Pause()
	srv.curPlaylist = core.CreateSimplePlaylist(playlist.Name, songs, context.Background())
	res := core.GetPlaylist(playlist.Name)
	return &api.Response{Response: res}, nil
}

func (srv *MusicServiceServer) GetSong(ctx context.Context, song *api.Song) (*api.Song, error) {
	var res *api.Song = nil
	coreSong, err := srv.curPlaylist.GetSong(song.Name)

	if err == nil {
		res = &api.Song{Author: coreSong.Author, Name: coreSong.Name, Duration: int64(coreSong.Duration)}
	}
	return res, err
}

func (srv *MusicServiceServer) UpdateSong(ctx context.Context, song *api.Song) (*api.Response, error) {
	s := new(core.Song)
	s.Author = song.Author
	s.Duration = int(song.Duration)
	s.Name = song.Name
	res, err := srv.curPlaylist.UpdateSong(s)
	if err != nil {
		return &api.Response{Response: ""}, err
	}
	err = db.UpdateSong(srv.DB, s)
	if err != nil {
		fmt.Println("Error:", err)
		return &api.Response{Response: ""}, err
	}
	return &api.Response{Response: res}, err
}

func (srv *MusicServiceServer) UpdatePlaylist(ctx context.Context, playlist *api.Playlist) (*api.Response, error) {
	res, err := core.UpdatePlaylist(playlist.Name)
	if err != nil {
		return &api.Response{Response: ""}, err
	}
	err = db.UpdatePlaylist(srv.DB, playlist.Name, srv.curPlaylist.Name)
	if err != nil {
		fmt.Println("Error:", err)
		return &api.Response{Response: ""}, err
	}
	return &api.Response{Response: res}, err
}

func (srv *MusicServiceServer) AddSongToPlaylist(ctx context.Context, sp *api.SongPlaylist) (*api.Response, error) {
	var err error = nil
	var song_id, playlist_id int64
	var ok bool
	song_id, err = db.GetSongID(srv.DB, sp.Song.Name)
	if err != nil {
		return &api.Response{Response: ""}, err
	}
	playlist_id, err = db.GetPlaylistID(srv.DB, sp.Playlist.Name)
	if err != nil {
		return &api.Response{Response: ""}, err
	}
	res := core.AddSongToPlaylist(song_id, playlist_id)
	ok, err = db.ConnectExists(srv.DB, song_id, playlist_id)
	if err != nil {
		return &api.Response{Response: ""}, err
	}
	if !ok {
		err = db.AddSongToPlaylist(srv.DB, song_id, playlist_id)
		if err != nil {
			return &api.Response{Response: ""}, err
		}
	}
	return &api.Response{Response: res}, err
}

func (srv *MusicServiceServer) DeleteSongFromPlaylist(ctx context.Context, sp *api.SongPlaylist) (*api.Response, error) {
	var err error = nil
	var song_id, playlist_id int64
	var ok bool
	song_id, err = db.GetSongID(srv.DB, sp.Song.Name)
	if err != nil {
		return &api.Response{Response: ""}, err
	}
	playlist_id, err = db.GetPlaylistID(srv.DB, sp.Playlist.Name)
	if err != nil {
		return &api.Response{Response: ""}, err
	}
	res := core.DeleteSongFromPlaylist(song_id, playlist_id)
	ok, err = db.ConnectExists(srv.DB, song_id, playlist_id)
	if err != nil {
		return &api.Response{Response: ""}, err
	}
	if !ok {
		err = db.DeleteSongFromPlaylist(srv.DB, song_id, playlist_id)
		if err != nil {
			return &api.Response{Response: ""}, err
		}
	}
	return &api.Response{Response: res}, err
}
