
CREATE TABLE songs(
    id SERIAL PRIMARY KEY,
    duration INT,
    name VARCHAR(30),
    author VARCHAR(50)
);

INSERT INTO songs(duration, name, author) VALUES 
(35, 'Lazy song', 'Bruno Mars'),
(45, 'Complicated', 'Avril Lavigne'),
(55, 'Kigeki', 'Gen Hoshino'),
(65, 'Drunk', 'Keshi'),
(75, 'Stay', 'The Kid LAROI and Justin Bieber');

CREATE TABLE playlists(
    id SERIAL PRIMARY KEY,
    name VARCHAR(30)
);

INSERT INTO playlists(name) VALUES 
('Pop'),
('Jazz'),
('Meloman');

CREATE TABLE songs_playlists(
    id_song SERIAL references songs(id) on delete cascade,
    id_playlist SERIAL references playlists(id) on delete cascade
);

CREATE INDEX idx_song ON songs (id);
CREATE INDEX idx_playlist ON playlists (id);


INSERT INTO songs_playlists(id_song, id_playlist) VALUES 
(1, 1),
(3, 1),
(2, 2),
(4, 2),
(1, 3),
(2, 3);