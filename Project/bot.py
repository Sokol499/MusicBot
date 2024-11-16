import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
import yandex_music
import os
import asyncio

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
        "Вводить надо в формате: /track или /album ссылка_на_альбом/трек или название_альбома/трека")

@dp.message(Command(commands=['track']))
async def get_track(message: Message):
    arg = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
    if not arg:
        await message.reply("Пожалуйста, укажите название или ссылку на трек")
        return

    await message.reply("Поиск трека, пожалуйста, подождите...")

    try:
        if "music.yandex.ru" in arg:
            track_id = arg.split("/")[-1].split("?")[0]
            track = ym_client.tracks([track_id])[0]
        else:
            search_results = ym_client.search(arg)
            if search_results.best:
                track = search_results.best.result
            else:
                await message.reply("Трек не найден. Попробуйте другое название.")
                return

        artist_names = ', '.join(artist.name for artist in track.artists)

        track_filename = f"{artist_names} - {track.title}.mp3"
        track.download(track_filename)

        audio_file = FSInputFile(track_filename)
        await message.reply_document(audio_file)

        await message.reply(
            f"Трек {artist_names} - {track.title} был отправлен!\nСпасибо за использование бота")

        await asyncio.sleep(5)
        os.remove(track_filename)
        return

    except Exception as e:
        await message.reply("Произошла ошибка при загрузке трека.")
        logging.error(f"Ошибка при загрузке трека: {e}")

@dp.message(Command(commands=['album']))
async def get_album(message: Message):
    arg = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
    if not arg:
        await message.reply("Пожалуйста, укажите название или ссылку на альбом")
        return

    await message.reply("Поиск альбома, пожалуйста, подождите...")

    try:
        if "music.yandex.ru" in arg:
            album_id = arg.split("/")[-1].split("?")[0]
            album = ym_client.albums_with_tracks(album_id)
        else:
            search_results = ym_client.search(arg)
            if search_results.albums:
                album = search_results.albums.results[0]
                album = ym_client.albums_with_tracks(album.id)
            else:
                await message.reply("Альбом не найден. Попробуйте другое название.")
                return

        album_name = album.title
        artist_names = ', '.join(artist.name for artist in album.artists)
        await message.reply(f"Начинаю отправку треков из альбома: {album_name} - {artist_names}")

        for volume in album.volumes:
            for track in volume:
                track_filename = f"{', '.join(artist.name for artist in track.artists)} - {track.title}.mp3"
                track.download(track_filename)

                audio_file = FSInputFile(track_filename)
                await message.reply_document(audio_file)
                await asyncio.sleep(2)  # Задержка между отправкой треков
                os.remove(track_filename)

        await message.reply(
            f"Альбом {artist_names} - {album_name} был отправлен полностью!\nСпасибо за использование бота")

    except Exception as e:
        await message.reply("Произошла ошибка при загрузке альбома.")
        logging.error(f"Ошибка при загрузке альбома: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
