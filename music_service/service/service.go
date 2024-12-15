package service

import (
	"container/list"
	"context"
	"database/sql"
	"errors"
	"fmt"
	"music_service/core"
	"os"
	"time"

	"music_service/api"
)

type MusicServiceServer struct {
	api.UnimplementedMusicServiceServer
	curPlaylist *core.SimplePlaylist
	db          *sql.DB
}

type config struct {
	POSTGRES_HOST     string
	POSTGRES_PORT     string
	POSTGRES_DB       string
	POSTGRES_USER     string
	POSTGRES_PASSWORD string
	APP_IP            string
	APP_PORT          string
}

func getSongsFromDb(db *sql.DB) *list.List {
	songs := list.New()
	rows, err := db.Query("select * from songs")
	if err != nil {
		panic(err)
	}
	defer rows.Close()
	for rows.Next() {
		song := new(core.Song)
		err = rows.Scan(&song.Id, &song.Duration, &song.Name, &song.Author)
		if err != nil {
			panic(err)
		}
		songs.PushBack(song)
	}
	return songs
}

func ConnectExists(db *sql.DB, id_song, id_playlist int64) (bool, error) {
	sqlStmt := "select * from songs_playlists where id_song = $1 and id_playlist = $2"
	err := db.QueryRow(sqlStmt, id_song, id_playlist).Scan(&id_song, &id_playlist)
	if err != nil {
		if err != sql.ErrNoRows {
			return false, err
		}
		return false, nil
	}
	return true, nil
}

func getSongID(db *sql.DB, name string) (int64, error) {
	var id_temp sql.NullInt64
	var id int64 = -1
	err := db.QueryRow("select id from songs where name = $1", name).Scan(&id_temp)
	if err != nil {
		fmt.Println("Error:", err)
		return -1, err
	}
	if id_temp.Valid {
		id = id_temp.Int64
	} else {
		err = errors.New("invalid id in getPlatlistID")
		fmt.Println("Error:", err)
		return -1, err
	}
	return id, nil
}

func getPlaylistID(db *sql.DB, name string) (int64, error) {
	var id_temp sql.NullInt64
	var id int64 = -1
	err := db.QueryRow("select id from playlists where name = $1", name).Scan(&id_temp)
	if err != nil {
		fmt.Println("Error:", err)
		return -1, err
	}
	if id_temp.Valid {
		id = id_temp.Int64
	} else {
		err = errors.New("invalid id in getPlatlistID")
		fmt.Println("Error:", err)
		return -1, err
	}
	return id, nil
}

func getPlaylistSongs(db *sql.DB, id int64) *list.List {
	rows, err := db.Query("select id_song from songs_playlists where id_playlist = $1", id)
	if err != nil {
		panic(err)
	}
	defer rows.Close()
	songs := list.New()
	for rows.Next() {
		song := new(core.Song)
		id_song := 0
		err := rows.Scan(&id_song)
		if err != nil {
			panic(err)
		}
		row := db.QueryRow("select * from songs where id = $1", id_song)
		err = row.Scan(&song.Id, &song.Duration, &song.Name, &song.Author)
		if err != nil {
			panic(err)
		}
		songs.PushBack(song)
	}
	if err = rows.Err(); err != nil {
		panic(err)
	}
	return songs
}

func isDBAvailable(db *sql.DB) bool {
	var res bool = true

	_, err := db.Query("select 1")

	if err != nil {
		res = false
	}
	return res
}

func NewConfig() config {
	cfg := config{
		POSTGRES_HOST:     os.Getenv("POSTGRES_HOST"),
		POSTGRES_PORT:     os.Getenv("POSTGRES_PORT"),
		POSTGRES_DB:       os.Getenv("POSTGRES_DB"),
		POSTGRES_USER:     os.Getenv("POSTGRES_USER"),
		POSTGRES_PASSWORD: os.Getenv("POSTGRES_PASSWORD"),
		APP_IP:            os.Getenv("APP_IP"),
		APP_PORT:          os.Getenv("APP_PORT"),
	}
	return cfg
}

func (cfg config) IsValid() bool {
	var res bool = true
	if cfg.POSTGRES_USER == "" || cfg.POSTGRES_PASSWORD == "" ||
		cfg.POSTGRES_DB == "" || cfg.POSTGRES_HOST == "" ||
		cfg.POSTGRES_PORT == "" || cfg.APP_IP == "" ||
		cfg.APP_PORT == "" {
		res = false
	}
	return res
}

func NewService(db *sql.DB) api.MusicServiceServer {
	service := MusicServiceServer{}

	for i := 1; !isDBAvailable(db); i++ {
		fmt.Printf("Db is unavailable(%ds)\n", i)
		time.Sleep(5 * time.Second)
	}
	fmt.Println("Db is available")
	songs := getSongsFromDb(db)
	playlist := core.CreateSimplePlaylist("My favorite playlist", songs, context.Background())
	service.curPlaylist = playlist
	service.db = db
	return &service
}

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
	_, err := srv.db.Exec("insert into songs (duration, name, author) values ($1, $2, $3)", song.Duration, song.Name, song.Author)
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
	_, err = srv.db.Exec("delete from songs where name = $1", song.Name)
	if err != nil {
		fmt.Println("Error:", err)
		return &api.Response{Response: ""}, err
	}
	return &api.Response{Response: res}, err
}

func (srv *MusicServiceServer) AddPlaylist(ctx context.Context, playlist *api.Playlist) (*api.Response, error) {
	s := core.CreateSimplePlaylist(playlist.Name, list.New(), nil)
	res := core.AddPlaylist(s)
	_, err := srv.db.Exec("insert into playlists (name) values ($1)", playlist.Name)
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
	_, err = srv.db.Exec("delete from playlists where name = $1", playlist.Name)
	if err != nil {
		fmt.Println("Error:", err)
		return &api.Response{Response: ""}, err
	}
	return &api.Response{Response: res}, err
}

func (srv *MusicServiceServer) PrintPlaylist(ctx context.Context, playlist *api.Playlist) (*api.Playlist, error) {
	id, err := getPlaylistID(srv.db, playlist.Name)
	if err != nil {
		return &api.Playlist{Songs: nil}, err
	}
	songs := getPlaylistSongs(srv.db, id)
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
		err = errors.New("not found")
	}

	return &api.Playlist{Songs: songsSlice}, err
}

func (srv *MusicServiceServer) GetPlaylist(ctx context.Context, playlist *api.Playlist) (*api.Response, error) {
	id_playlist, err := getPlaylistID(srv.db, playlist.Name)
	if err != nil {
		return &api.Response{Response: ""}, err
	}
	songs := getPlaylistSongs(srv.db, id_playlist)
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
	res, err := srv.curPlaylist.UpdateSong(song.Name, song.Author, int(song.Duration))
	if err != nil {
		return &api.Response{Response: ""}, err
	}
	_, err = srv.db.Exec("update songs set author = $1, duration = $2 where name = $3", song.Author, song.Duration, song.Name)
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
	_, err = srv.db.Exec("update playlists set name = $1 where name = $2", playlist.Name, srv.curPlaylist.Name)
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
	song_id, err = getSongID(srv.db, sp.Song.Name)
	if err != nil {
		return &api.Response{Response: ""}, err
	}
	playlist_id, err = getPlaylistID(srv.db, sp.Playlist.Name)
	if err != nil {
		return &api.Response{Response: ""}, err
	}
	res := core.AddSongToPlaylist(song_id, playlist_id)
	ok, err = ConnectExists(srv.db, song_id, playlist_id)
	if err != nil {
		return &api.Response{Response: ""}, err
	}
	if !ok {
		_, err = srv.db.Exec("insert into songs_playlists (id_song, id_playlist) values ($1, $2)", song_id, playlist_id)
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
	song_id, err = getSongID(srv.db, sp.Song.Name)
	if err != nil {
		return &api.Response{Response: ""}, err
	}
	playlist_id, err = getPlaylistID(srv.db, sp.Playlist.Name)
	if err != nil {
		return &api.Response{Response: ""}, err
	}
	res := core.DeleteSongFromPlaylist(song_id, playlist_id)
	ok, err = ConnectExists(srv.db, song_id, playlist_id)
	if err != nil {
		return &api.Response{Response: ""}, err
	}
	if !ok {
		_, err = srv.db.Exec("delete from songs_playlists where id_song = $1 and id_playlist = $2", song_id, playlist_id)
		if err != nil {
			return &api.Response{Response: ""}, err
		}
	}
	return &api.Response{Response: res}, err
}
