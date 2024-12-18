package main

import (
	"fmt"
	"music_service/api"
	"music_service/config"
	"music_service/db"
	"music_service/service"
	"net"

	_ "github.com/lib/pq"
	"google.golang.org/grpc"
)

func main() {
	cfg := config.NewConfig()
	if !cfg.IsValid() {
		panic("incorrect config")
	}

	db := db.Connect(cfg)
	defer db.Close()

	grpcServer := grpc.NewServer()
	lis, err := net.Listen("tcp", fmt.Sprintf("%s:%s", cfg.APP_IP, cfg.APP_PORT))
	if err != nil {
		panic("listen error")
	}
	api.RegisterMusicServiceServer(grpcServer, service.NewService(db))
	if err := grpcServer.Serve(lis); err != nil {
		panic(err)
	}
}
