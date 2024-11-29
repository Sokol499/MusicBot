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

# -------------------- Команды бота --------------------

@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: Message):
    """Обработка команд /start и /help."""
    await message.reply(
        "Привет! Отправь название или ссылку на трек/альбом, и я отправлю тебе аудиоформат.\n"
        "Вводить надо в формате: /track или /album ссылка_на_альбом/трек или название_альбома/трека"
    )

@dp.message(Command(commands=['track']))
async def get_track(message: Message):
    """Обработка команды /track для поиска и отправки трека."""
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
    """Обработка команды /album для поиска и отправки альбома."""
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

# -------------------- Вспомогательные функции --------------------

def parse_user_input(message: Message) -> str:
    """Извлекает аргумент команды из текста сообщения."""
    return message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""

async def find_track(arg: str):
    """Ищет трек по ссылке или названию."""
    if "music.yandex.ru" in arg:
        track_id = arg.split("/")[-1].split("?")[0]
        return ym_client.tracks([track_id])[0]
    else:
        search_results = ym_client.search(arg)
        return search_results.best.result if search_results.best else None

async def find_album(arg: str):
    """Ищет альбом по ссылке или названию."""
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
    """Скачивает и отправляет трек пользователю.

    :param track: Объект трека.
    :param message: Сообщение пользователя.
    :param is_album: Если True, сообщение об отправке трека не отправляется.
    """
    artist_names = ', '.join(artist.name for artist in track.artists)
    track_filename = f"{artist_names} - {track.title}.mp3"

    try:
        track.download(track_filename)
        audio_file = FSInputFile(track_filename)
        await message.reply_document(audio_file)

        if not is_album:  # Сообщение отправляется только для одиночных треков
            await message.reply(
                f"Трек {artist_names} - {track.title} был отправлен!\nСпасибо за использование бота"
            )
    finally:
        await asyncio.sleep(5)
        if os.path.exists(track_filename):
            os.remove(track_filename)

async def send_album_to_user(album, message: Message):
    """Скачивает и отправляет все треки альбома пользователю."""
    album_name = album.title
    artist_names = ', '.join(artist.name for artist in album.artists)
    await message.reply(f"Начинаю отправку треков из альбома: {album_name} - {artist_names}")

    for volume in album.volumes:
        for track in volume:
            await send_track_to_user(track, message, is_album=True)  # Передаем is_album=True
            await asyncio.sleep(2)  # Задержка между отправкой треков

    await message.reply(
        f"Альбом {artist_names} - {album_name} был отправлен полностью!\nСпасибо за использование бота"
    )

@dp.message(Command(commands=['create_playlist']))
async def create_playlist(message: Message):
    await message.reply("Функция создания плейлистов находится в разработке.")

@dp.message(Command(commands=['add_to_playlist']))
async def add_to_playlist(message: Message):
    await message.reply("Функция добавления треков в плейлист находится в разработке.")

@dp.message(Command(commands=['remove_from_playlist']))
async def remove_from_playlist(message: Message):
    await message.reply("Функция удаления треков из плейлиста находится в разработке.")

@dp.message(Command(commands=['play_playlist']))
async def play_playlist(message: Message):
    await message.reply("Функция воспроизведения плейлиста находится в разработке.")


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())