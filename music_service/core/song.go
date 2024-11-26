package core

import (
	"container/list"
	"context"
	"errors"
	"fmt"
	"time"
)

type Playlist interface {
	Play()
	Pause()
	AddSong()
	Next()
	Prev()
}

type Song struct {
	Name     string
	Duration int
	Author   string
	Id       int
}

func (p *SimplePlaylist) Play() string {
	if p.isPlaying {
		return "already playing"
	}

	if p.currentSongNode == nil {
		p.currentSongNode = p.Songs.Front()
	}
	ctx, cancel := context.WithCancel(p.Ctx)
	p.stopCtx = cancel
	go func() {
		p.isPlaying = true
		for {
			currentSong := p.currentSongNode.Value.(*Song)
			fmt.Println("Now playing:", currentSong.Name)
			for p.currentSongPlayTime != currentSong.Duration {
				for i := 0; i != 5; i++ {
					select {
					case <-ctx.Done():
						return
					default:
						time.Sleep(200 * time.Millisecond)
					}
				}
				p.currentSongPlayTime++
				fmt.Printf("%s: la-la-la(%ds)\n", currentSong.Name, p.currentSongPlayTime)
			}
			p.currentSongPlayTime = 0
			if p.currentSongNode == p.Songs.Back() {
				p.currentSongNode = p.Songs.Front()
			} else {
				p.currentSongNode = p.currentSongNode.Next()
			}
		}
	}()
	currentSong := p.currentSongNode.Value.(*Song)
	return fmt.Sprintf("Playing. Song: %s. Author: %s. Duration: %d", currentSong.Name, currentSong.Author, currentSong.Duration)
}

func (p *SimplePlaylist) Pause() string {
	fmt.Println("Paused")
	if !p.isPlaying {
		return "already paused"
	}
	p.isPlaying = false
	p.stopCtx()
	return "paused"
}
func (p *SimplePlaylist) AddSong(song *Song) string {
	p.coreMtx.Lock()
	res := fmt.Sprintf("New song added. Name: %s. Author: %s. Duration: %ds.", song.Name, song.Author, song.Duration)
	fmt.Println(res)
	p.Songs.PushBack(song)
	p.coreMtx.Unlock()
	return res
}

func (p *SimplePlaylist) Next() string {
	p.coreMtx.Lock()
	p.Pause()
	p.currentSongPlayTime = 0
	if p.currentSongNode == p.Songs.Back() {
		p.currentSongNode = p.Songs.Front()
	} else {
		p.currentSongNode = p.currentSongNode.Next()
	}
	res := p.Play()
	p.coreMtx.Unlock()
	return res
}

func (p *SimplePlaylist) Prev() string {
	p.coreMtx.Lock()
	p.Pause()
	p.currentSongPlayTime = 0
	if p.currentSongNode == p.Songs.Front() {
		p.currentSongNode = p.Songs.Back()
	} else {
		p.currentSongNode = p.currentSongNode.Prev()
	}
	res := p.Play()
	p.coreMtx.Unlock()
	return res
}

func (p *SimplePlaylist) DeleteSong(name string) (string, error) {
	p.coreMtx.Lock()
	var err error

	if p.isPlaying {
		err = errors.New("song is playing, can't delete")
		p.coreMtx.Unlock()
		return "song is playing, can't delete", err
	}
	node, err := p.getNode(name)
	if err != nil {
		fmt.Println("Error:", err)
		p.coreMtx.Unlock()
		return "", err
	}
	song := node.Value.(*Song)
	res := fmt.Sprintf("Song deleted. Name: %s. Author: %s. Duration: %d.", song.Name, song.Author, song.Duration)
	p.Songs.Remove(node)
	p.coreMtx.Unlock()
	return res, err
}

func (p *SimplePlaylist) GetSongs() list.List {
	p.coreMtx.Lock()
	res := *p.Songs
	p.coreMtx.Unlock()
	return res
}

func (p *SimplePlaylist) GetSong(name string) (Song, error) {
	p.coreMtx.Lock()
	var song *Song = &Song{Author: "", Name: "", Duration: 0}

	node, err := p.getNode(name)
	if err != nil {
		fmt.Println("Error:", err)
		p.coreMtx.Unlock()
		return *song, err
	}
	song = node.Value.(*Song)
	res := *song
	p.coreMtx.Unlock()
	return res, err
}

func (p *SimplePlaylist) UpdateSong(name string, author string, duration int) (string, error) {
	p.coreMtx.Lock()
	var song *Song
	res := "song updated"
	node, err := p.getNode(name)
	if err != nil {
		fmt.Println("Error:", err)
		p.coreMtx.Unlock()
		return "error", err
	}
	song.Author = author
	song.Duration = duration
	node.Value = song
	p.coreMtx.Unlock()
	return res, err
}

func (p *SimplePlaylist) getNode(name string) (*list.Element, error) {
	var node *list.Element
	var err error = errors.New("not found")
	for e := p.Songs.Front(); e != nil; e = e.Next() {
		if e.Value.(*Song).Name == name {
			node = e
			err = nil
			break
		}
	}
	return node, err
}
