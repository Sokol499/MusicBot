import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
import yandex_music
import os
import asyncio

import client

from config import TOKEN, TOKEN_1

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN_1)
dp = Dispatcher()

YANDEX_MUSIC_TOKEN = TOKEN

ym_client = yandex_music.Client(YANDEX_MUSIC_TOKEN).init()

@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: Message):
    await message.reply(
        "Привет! Отправь название или ссылку на трек/альбом, и я отправлю тебе аудиоформат.\n"
        "Вводить надо в формате: /track или /album ссылка_на_альбом/трек или название_альбома/трека"
    )

@dp.message(Command(commands=['track']))
async def get_track(message: Message):
    arg = parse_user_input(message)
    if not arg:
        await message.reply("Пожалуйста, укажите название или ссылку на трек")
        return

    await message.reply("Поиск трека, пожалуйста, подождите...")

    try:
        track = await find_track(arg)
        if not track:
            await message.reply("Трек не найден. Попробуйте другое название.")
            return

        await send_track_to_user(track, message)

    except Exception as e:
        await message.reply("Произошла ошибка при загрузке трека.")
        logging.error(f"Ошибка при загрузке трека: {e}")

@dp.message(Command(commands=['album']))
async def get_album(message: Message):
    arg = parse_user_input(message)
    if not arg:
        await message.reply("Пожалуйста, укажите название или ссылку на альбом")
        return

    await message.reply("Поиск альбома, пожалуйста, подождите...")

    try:
        album = await find_album(arg)
        if not album:
            await message.reply("Альбом не найден. Попробуйте другое название.")
            return

        await send_album_to_user(album, message)

    except Exception as e:
        await message.reply("Произошла ошибка при загрузке альбома.")
        logging.error(f"Ошибка при загрузке альбома: {e}")

def parse_user_input(message: Message) -> str:
    return message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""

async def find_track(arg: str):
    if "music.yandex.ru" in arg:
        track_id = arg.split("/")[-1].split("?")[0]
        return ym_client.tracks([track_id])[0]
    else:
        search_results = ym_client.search(arg)
        return search_results.best.result if search_results.best else None

async def find_album(arg: str):
    if "music.yandex.ru" in arg:
        album_id = arg.split("/")[-1].split("?")[0]
        return ym_client.albums_with_tracks(album_id)
    else:
        search_results = ym_client.search(arg)
        if search_results.albums:
            album = search_results.albums.results[0]
            return ym_client.albums_with_tracks(album.id)
        return None

async def send_track_to_user(track, message: Message, is_album=False):
    artist_names = ', '.join(artist.name for artist in track.artists)
    track_filename = f"{artist_names} - {track.title}.mp3"

    try:
        track.download(track_filename)
        audio_file = FSInputFile(track_filename)
        await message.reply_document(audio_file)

        if not is_album:
            await message.reply(
                f"Трек {artist_names} - {track.title} был отправлен!\nСпасибо за использование бота"
            )
    finally:
        await asyncio.sleep(5)
        if os.path.exists(track_filename):
            os.remove(track_filename)

async def send_album_to_user(album, message: Message):
    album_name = album.title
    artist_names = ', '.join(artist.name for artist in album.artists)
    await message.reply(f"Начинаю отправку треков из альбома: {album_name} - {artist_names}")

    for volume in album.volumes:
        for track in volume:
            await send_track_to_user(track, message, is_album=True)
            await asyncio.sleep(2)

    await message.reply(
        f"Альбом {artist_names} - {album_name} был отправлен полностью!\nСпасибо за использование бота"
    )


@dp.message(Command(commands=['create_playlist']))
async def create_playlist(message: Message):
    playlist_name = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
    if not playlist_name:
        await message.reply("Введите имя плейлиста после команды.")
        return

    try:
        response = client.add_playlist(playlist_name)
        await message.reply(f"Плейлист '{playlist_name}' успешно создан!")
    except Exception as e:
        logging.error(f"Ошибка при создании плейлиста: {e}")
        await message.reply("Произошла ошибка при создании плейлиста. Попробуйте ещё раз позже.")


@dp.message(Command(commands=['add_to_playlist']))
async def add_to_playlist(message: Message):
    args = parse_user_input(message)
    if not args or len(args.split(",", 1)) < 2:
        await message.reply("Использование: /add_to_playlist <название песни>, <название плейлиста>")
        return

    try:
        song_name, playlist_name = map(str.strip, args.split(",", maxsplit=1))

        track = await find_track(song_name)
        if not track:
            await message.reply(f"Трек '{song_name}' не найден в Яндекс Музыке.")
            return

        song_author = ', '.join(artist.name for artist in track.artists)

        response = client.add_song_to_playlist(song_author, track.title, playlist_name)

        if response:
            await message.reply(f"Песня '{track.title}' от '{song_author}' добавлена в плейлист '{playlist_name}'!")
        else:
            await message.reply(f"Не удалось добавить песню '{track.title}' от '{song_author}' в плейлист '{playlist_name}'.")
    except Exception as e:
        logging.error(f"Ошибка при добавлении трека в плейлист: {e}")
        await message.reply(f"Произошла ошибка при добавлении песни '{song_name}' в плейлист '{playlist_name}'. Попробуйте снова позже.")


@dp.message(Command(commands=['remove_from_playlist']))
async def remove_from_playlist(message: Message):
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.reply("Использование: /remove_from_playlist <название_песни> <название_плейлиста>")
        return

    song_name, playlist_name = args[1], args[2]

    try:
        response = client.delete_song_from_playlist(song_name, playlist_name)

        if response:
            await message.reply(f"Песня '{song_name}' была удалена из плейлиста '{playlist_name}'!")
        else:
            await message.reply(f"Не удалось удалить песню '{song_name}' из плейлиста '{playlist_name}'.")
    except Exception as e:
        await message.reply(f"Произошла ошибка при удалении песни из плейлиста '{playlist_name}'. Попробуйте снова позже.")
        logging.error(f"Ошибка при удалении песни из плейлиста: {e}")


@dp.message(Command(commands=['play_playlist']))
async def play_playlist(message: Message):
    playlist_name = parse_user_input(message)
    if not playlist_name:
        await message.reply("Введите имя плейлиста после команды.")
        return

    try:
        response = client.print_playlist(playlist_name)

        if "не найден" in response or "пуст" in response:
            await message.reply(response)
            return

        await message.reply(f"Начинаю воспроизведение плейлиста '{playlist_name}'...")

        song_lines = response.split("\n")[1:]
        for i, song_line in enumerate(song_lines, start=1):
            song_name = song_line.split(". ")[-1]
            await message.reply(f"Обработка трека №{i}: {song_name}")

            track = await find_track(song_name)
            if not track:
                await message.reply(f"Трек '{song_name}' не найден в Яндекс.Музыке. Пропускаю...")
                continue

            await send_track_to_user(track, message)

    except Exception as e:
        await message.reply(f"Ошибка при воспроизведении плейлиста '{playlist_name}': {e}")
        logging.error(f"Ошибка воспроизведения плейлиста '{playlist_name}': {e}")


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())