package config

import "os"

type Config struct {
	POSTGRES_HOST     string
	POSTGRES_PORT     string
	POSTGRES_DB       string
	POSTGRES_USER     string
	POSTGRES_PASSWORD string
	APP_IP            string
	APP_PORT          string
}

func NewConfig() *Config {
	cfg := Config{
		POSTGRES_HOST:     os.Getenv("POSTGRES_HOST"),
		POSTGRES_PORT:     os.Getenv("POSTGRES_PORT"),
		POSTGRES_DB:       os.Getenv("POSTGRES_DB"),
		POSTGRES_USER:     os.Getenv("POSTGRES_USER"),
		POSTGRES_PASSWORD: os.Getenv("POSTGRES_PASSWORD"),
		APP_IP:            os.Getenv("APP_IP"),
		APP_PORT:          os.Getenv("APP_PORT"),
	}
	return &cfg
}

func (cfg *Config) IsValid() bool {
	var res bool = true
	if cfg.POSTGRES_USER == "" || cfg.POSTGRES_PASSWORD == "" ||
		cfg.POSTGRES_DB == "" || cfg.POSTGRES_HOST == "" ||
		cfg.POSTGRES_PORT == "" || cfg.APP_IP == "" ||
		cfg.APP_PORT == "" {
		res = false
	}
	return res
}