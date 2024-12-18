package service

import (
	"context"
	"database/sql"
	"fmt"
	"music_service/core"
	"music_service/db"
	"time"

	"music_service/api"
)

type MusicServiceServer struct {
	api.UnimplementedMusicServiceServer
	curPlaylist *core.SimplePlaylist
	DB          *sql.DB
}

func NewService(DB *sql.DB) api.MusicServiceServer {
	service := MusicServiceServer{}

	for i := 1; !db.IsAvailable(DB); i++ {
		fmt.Printf("DB is unavailable(%ds)\n", i)
		time.Sleep(5 * time.Second)
	}
	fmt.Println("DB is available")
	songs := db.GetSongs(DB)
	playlist := core.CreateSimplePlaylist("My favorite playlist", songs, context.Background())
	service.curPlaylist = playlist
	service.DB = DB
	return &service
}