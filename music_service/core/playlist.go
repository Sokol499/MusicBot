package core

import (
	"container/list"
	"context"
	"music_service/errors"
	"fmt"
	"sync"
)

type SimplePlaylist struct {
	Name  string
	Ctx   context.Context
	Songs *list.List

	currentSongNode     *list.Element
	currentSongPlayTime int
	stopCtx             context.CancelFunc
	coreMtx             *sync.Mutex
	isPlaying           bool
}

func CreateSimplePlaylist(name string, songs *list.List, ctx context.Context) *SimplePlaylist {
	p := &SimplePlaylist{Name: name, Songs: songs, Ctx: ctx}

	p.coreMtx = new(sync.Mutex)
	p.currentSongPlayTime = 0
	p.isPlaying = false
	p.stopCtx = nil
	p.currentSongNode = p.Songs.Front()
	return p
}

func AddPlaylist(playlist *SimplePlaylist) string {
	res := fmt.Sprintf("New playlist added. Name: %s.", playlist.Name)
	fmt.Println(res)
	return res
}

func DeletePlaylist(name string, p *SimplePlaylist) (string, error) {
	var err error
	res := fmt.Sprintf("Playlist deleted. Name: %s", name)
	if p.Name != name {
		return res, err
	}
	if p.isPlaying {
		return errors.ErrPlaylistAlreadyPlaying.Error(), errors.ErrPlaylistAlreadyPlaying
	}
	return res, err
}

func GetPlaylist(playlistname string) string {
	res := fmt.Sprintf("Playlist chosen. Name: %s.", playlistname)
	fmt.Println(res)
	return res
}

func UpdatePlaylist(name string) (string, error) {
	res := "playlist updated"
	var err error = nil
	if name == "" {
		return errors.ErrIncorrectPlaylistName.Error(), errors.ErrIncorrectPlaylistName
	}
	return res, err
}

func AddSongToPlaylist(song_id, playlist_id int64) string {
	res := "Song added to playlist."
	fmt.Println(res)
	return res
}

func DeleteSongFromPlaylist(song_id, playlist_id int64) string {
	res := "Song deleted from playlist."
	fmt.Println(res)
	return res
}
