package db

import (
	"container/list"
	"database/sql"
	"music_service/errors"
	"music_service/core"
)

func GetSongs(db *sql.DB) *list.List {
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

func GetSongID(db *sql.DB, name string) (int64, error) {
	var id_temp sql.NullInt64
	var id int64 = -1
	err := db.QueryRow("select id from songs where name = $1", name).Scan(&id_temp)
	if err != nil {
		return -1, err
	}
	if id_temp.Valid {
		id = id_temp.Int64
	} else {
		return -1, errors.ErrInvalidID
	}
	return id, nil
}

func GetPlaylistID(db *sql.DB, name string) (int64, error) {
	var id_temp sql.NullInt64
	var id int64 = -1
	err := db.QueryRow("select id from playlists where name = $1", name).Scan(&id_temp)
	if err != nil {
		return -1, err
	}
	if id_temp.Valid {
		id = id_temp.Int64
	} else {
		return -1, errors.ErrInvalidID
	}
	return id, nil
}

func GetPlaylistSongs(db *sql.DB, id int64) *list.List {
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

func AddSong(db *sql.DB, song *core.Song) error {
	_, err := db.Exec("insert into songs (duration, name, author) values ($1, $2, $3)", song.Duration, song.Name, song.Author)
	return err
}

func DeleteSong(db *sql.DB, name string) error {
	_, err := db.Exec("delete from songs where name = $1", name)
	return err
}

func UpdateSong(db *sql.DB, song *core.Song) error {
	_, err := db.Exec("update songs set author = $1, duration = $2 , name = $3 where name = $3", song.Author, song.Duration, song.Name)
	return err
}

func AddPlaylist(db *sql.DB, name string) error {
	_, err := db.Exec("insert into playlists (name) values ($1)", name)
	return err
}

func DeletePlaylist(db *sql.DB, name string) error {
	_, err := db.Exec("delete from playlists where name = $1", name)
	return err
}

func UpdatePlaylist(db *sql.DB, new, old string) error {
	_, err := db.Exec("update playlists set name = $1 where name = $2", new, old)
	return err
}

func AddSongToPlaylist(db *sql.DB, song_id, playlist_id int64) error {
	_, err := db.Exec("insert into songs_playlists (id_song, id_playlist) values ($1, $2)", song_id, playlist_id)
	return err
}

func DeleteSongFromPlaylist(db *sql.DB, song_id, playlist_id int64) error {
	_, err := db.Exec("delete from songs_playlists where id_song = $1 and id_playlist = $2", song_id, playlist_id)
	return err
}

func IsAvailable(db *sql.DB) bool {
	var res bool = true

	_, err := db.Query("select 1")

	if err != nil {
		res = false
	}
	return res
}