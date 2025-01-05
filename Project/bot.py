import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
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

# Главное меню кнопок
def main_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="Найти трек", callback_data="find_track")
    builder.button(text="Найти альбом", callback_data="find_album")
    builder.button(text="Создать плейлист", callback_data="create_playlist")
    builder.button(text="Добавить в плейлист", callback_data="add_to_playlist")
    builder.button(text="Воспроизвести плейлист", callback_data="play_playlist")
    builder.adjust(2)  # Устанавливаем 2 кнопки в строке
    return builder.as_markup()

@dp.message()
async def send_welcome(message: Message):
    await message.reply(
        "Привет! Добро пожаловать в бота! Выберите действие:",
        reply_markup=main_menu()
    )

@dp.callback_query(lambda c: c.data == "find_track")
async def callback_find_track(callback: CallbackQuery):
    await callback.message.reply("Введите название или ссылку на трек:")

@dp.message(lambda message: message.reply_to_message and "Введите название или ссылку на трек:" in message.reply_to_message.text)
async def get_track(message: Message):
    arg = message.text
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

@dp.callback_query(lambda c: c.data == "find_album")
async def callback_find_album(callback: CallbackQuery):
    await callback.message.reply("Введите название или ссылку на альбом:")

@dp.message(lambda message: message.reply_to_message and "Введите название или ссылку на альбом:" in message.reply_to_message.text)
async def get_album(message: Message):
    arg = message.text
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

@dp.callback_query(lambda c: c.data == "create_playlist")
async def callback_create_playlist(callback: CallbackQuery):
    await callback.message.reply("Введите имя для нового плейлиста:")

@dp.message(lambda message: message.reply_to_message and "Введите имя для нового плейлиста:" in message.reply_to_message.text)
async def create_playlist(message: Message):
    playlist_name = message.text

    try:
        response = client.add_playlist(playlist_name)
        await message.reply(f"Плейлист '{playlist_name}' успешно создан!")
    except Exception as e:
        logging.error(f"Ошибка при создании плейлиста: {e}")
        await message.reply("Произошла ошибка при создании плейлиста. Попробуйте ещё раз позже.")

@dp.callback_query(lambda c: c.data == "add_to_playlist")
async def callback_add_to_playlist(callback: CallbackQuery):
    await callback.message.reply("Введите данные в формате: <название песни>, <название плейлиста>")

@dp.message(lambda message: message.reply_to_message and "<название песни>, <название плейлиста>" in message.reply_to_message.text)
async def add_to_playlist(message: Message):
    args = message.text

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
        await message.reply(f"Произошла ошибка при добавлении песни в плейлист. Попробуйте снова позже.")

@dp.callback_query(lambda c: c.data == "play_playlist")
async def callback_play_playlist(callback: CallbackQuery):
    await callback.message.reply("Введите имя плейлиста для воспроизведения:")

@dp.message(lambda message: message.reply_to_message and "Введите имя плейлиста для воспроизведения:" in message.reply_to_message.text)
async def play_playlist(message: Message):
    playlist_name = message.text

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

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
