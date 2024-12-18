package db

import (
	"database/sql"
	"fmt"
	"music_service/config"
)

func Connect(cfg *config.Config) *sql.DB {
	connStr := fmt.Sprintf("user=%s password=%s dbname=%s sslmode=disable host=%s port=%s", cfg.POSTGRES_USER,
		cfg.POSTGRES_PASSWORD, cfg.POSTGRES_DB, cfg.POSTGRES_HOST, cfg.POSTGRES_PORT)
	db, err := sql.Open("postgres", connStr)
	if err != nil {
		panic("DB connection error")
	}
	
	return db
}