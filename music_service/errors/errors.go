package errors

import "errors"

var (
	ErrNotFound = errors.New("not found")
	ErrPlaylistAlreadyPlaying = errors.New("playlist is playing, can't delete")
	ErrInvalidID = errors.New("invalid id in getPlatlistID")
	ErrSongAlreadyPlaying = errors.New("song is playing, can't delete")
	ErrIncorrectPlaylistName = errors.New("incorrect name for playlist")
)
