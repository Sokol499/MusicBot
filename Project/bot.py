import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import yandex_music
import os
import asyncio
from io import BytesIO
from aiogram.types import InputFile

import client

from config import TOKEN, TOKEN_1

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN_1)
dp = Dispatcher(storage=MemoryStorage())

YANDEX_MUSIC_TOKEN = TOKEN
ym_client = yandex_music.Client(YANDEX_MUSIC_TOKEN).init()

# Создаем главное меню
main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Найти трек", callback_data="find_track"),
     InlineKeyboardButton(text="Найти альбом", callback_data="find_album")],
    [InlineKeyboardButton(text="Создать плейлист", callback_data="create_playlist"),
     InlineKeyboardButton(text="Добавить в плейлист", callback_data="add_to_playlist")],
    [InlineKeyboardButton(text="Воспроизвести плейлист", callback_data="play_playlist")]
])

class MusicStates(StatesGroup):
    FIND_TRACK = State()
    FIND_ALBUM = State()
    CREATE_PLAYLIST = State()
    ADD_TO_PLAYLIST = State()
    PLAY_PLAYLIST = State()

@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: Message):
    await message.reply(
        "Привет! Я помогу тебе с музыкой из Яндекс Музыки. Выбери действие из меню ниже:",
        reply_markup=main_menu
    )

@dp.callback_query()
async def handle_menu(callback: CallbackQuery, state: FSMContext):
    if callback.data == "find_track":
        await callback.message.reply("Введите название или ссылку на трек.")
        await state.set_state(MusicStates.FIND_TRACK)
    elif callback.data == "find_album":
        await callback.message.reply("Введите название или ссылку на альбом.")
        await state.set_state(MusicStates.FIND_ALBUM)
    elif callback.data == "create_playlist":
        await callback.message.reply("Введите имя нового плейлиста.")
        await state.set_state(MusicStates.CREATE_PLAYLIST)
    elif callback.data == "add_to_playlist":
        await callback.message.reply("Введите название трека и плейлиста в формате:\n<название трека>, <название плейлиста>")
        await state.set_state(MusicStates.ADD_TO_PLAYLIST)
    elif callback.data == "play_playlist":
        await callback.message.reply("Введите имя плейлиста для воспроизведения.")
        await state.set_state(MusicStates.PLAY_PLAYLIST)

@dp.message(F.text, MusicStates.FIND_TRACK)
async def process_find_track(message: Message, state: FSMContext):
    await state.clear()
    arg = message.text
    if not arg:
        await message.reply("Пожалуйста, укажите название или ссылку на трек.")
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
    finally:
        await message.reply("Выберите следующее действие:", reply_markup=main_menu)

@dp.message(F.text, MusicStates.FIND_ALBUM)
async def process_find_album(message: Message, state: FSMContext):
    await state.clear()
    arg = message.text
    if not arg:
        await message.reply("Пожалуйста, укажите название или ссылку на альбом.")
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
    finally:
        await message.reply("Выберите следующее действие:", reply_markup=main_menu)

@dp.message(F.text, MusicStates.CREATE_PLAYLIST)
async def process_create_playlist(message: Message, state: FSMContext):
    await state.clear()
    playlist_name = message.text
    if not playlist_name:
        await message.reply("Введите имя плейлиста.")
        return

    try:
        response = client.add_playlist(playlist_name)
        await message.reply(f"Плейлист '{playlist_name}' успешно создан!")
    except Exception as e:
        logging.error(f"Ошибка при создании плейлиста: {e}")
        await message.reply("Произошла ошибка при создании плейлиста. Попробуйте позже.")
    finally:
        await message.reply("Выберите следующее действие:", reply_markup=main_menu)

@dp.message(F.text, MusicStates.ADD_TO_PLAYLIST)
async def process_add_to_playlist(message: Message, state: FSMContext):
    await state.clear()
    args = message.text
    if not args or len(args.split(",", 1)) < 2:
        await message.reply("Использование: <название трека>, <название плейлиста>")
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
            await message.reply(f"Не удалось добавить песню '{track.title}' в плейлист '{playlist_name}'.")
    except Exception as e:
        logging.error(f"Ошибка при добавлении трека в плейлист: {e}")
        await message.reply("Произошла ошибка. Попробуйте снова позже.")
    finally:
        await message.reply("Выберите следующее действие:", reply_markup=main_menu)

@dp.message(F.text, MusicStates.PLAY_PLAYLIST)
async def process_play_playlist(message: Message, state: FSMContext):
    await state.clear()
    playlist_name = message.text
    if not playlist_name:
        await message.reply("Введите имя плейлиста.")
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
                await message.reply(f"Трек '{song_name}' не найден. Пропускаю...")
                continue

            await send_track_to_user(track, message)
    except Exception as e:
        await message.reply(f"Ошибка при воспроизведении плейлиста '{playlist_name}': {e}")
        logging.error(f"Ошибка воспроизведения плейлиста '{playlist_name}': {e}")
    finally:
        await message.reply("Выберите следующее действие:", reply_markup=main_menu)

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
        # Скачиваем трек в BytesIO
        file_buffer = BytesIO()
        track.download(file_buffer)

        # Проверка на пустой буфер
        if file_buffer.getbuffer().nbytes == 0:
            raise ValueError("Буфер пуст, трек не был загружен.")

        file_buffer.seek(0)  # Возвращаем курсор в начало буфера

        # Используем InputFile для передачи данных из BytesIO
        audio_file = InputFile(file_buffer, filename=track_filename)
        await message.reply_document(audio_file)

        if not is_album:
            await message.reply(f"Трек {artist_names} - {track.title} был отправлен!\nСпасибо за использование бота")
    except Exception as e:
        # Подробный лог ошибки для отладки
        logging.error(f"Ошибка при отправке трека '{track.title}': {type(e).__name__}: {e}")
        await message.reply(f"Ошибка при отправке трека: {track.title}. Проверьте логи для деталей.")
    finally:
        file_buffer.close()  # Закрываем поток


async def send_album_to_user(album, message: Message):
    album_name = album.title
    artist_names = ', '.join(artist.name for artist in album.artists)
    await message.reply(f"Начинаю отправку треков из альбома: {album_name} - {artist_names}")

    for volume in album.volumes:
        for track in volume:
            try:
                await send_track_to_user(track, message, is_album=True)
                await asyncio.sleep(0.5)  # Минимальная пауза для Telegram API
            except Exception as e:
                logging.error(f"Ошибка при отправке трека {track.title}: {e}")

    await message.reply(f"Альбом {artist_names} - {album_name} был отправлен полностью!\nСпасибо за использование бота")


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())