package main

import (
	"database/sql"
	"fmt"
	"github.com/gremislaw/music_service/api"
	_ "github.com/lib/pq"
	"google.golang.org/grpc"
	"music_service/service"
	"net"
)

func main() {
	cfg := service.NewConfig()
	if !cfg.IsValid() {
		panic("incorrect config")
	}

	connStr := fmt.Sprintf("user=%s password=%s dbname=%s sslmode=disable host=%s port=%s", cfg.POSTGRES_USER,
		cfg.POSTGRES_PASSWORD, cfg.POSTGRES_DB, cfg.POSTGRES_HOST, cfg.POSTGRES_PORT)
	db, err := sql.Open("postgres", connStr)
	if err != nil {
		panic("DB connection error")
	}
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
