from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InputFile
from aiogram.filters import Command, Text
import yandex_music
import os
import asyncio

from config import TOKEN, TOKEN_1
import client  # Используется для работы с плейлистами

# Логгирование
import logging
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN_1)
dp = Dispatcher()

# Инициализация Yandex Music клиента
YANDEX_MUSIC_TOKEN = TOKEN
ym_client = yandex_music.Client(YANDEX_MUSIC_TOKEN).init()


# Главное меню
def main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    # Добавление кнопок
    button1 = KeyboardButton("🎵 Найти трек")
    button2 = KeyboardButton("📀 Найти альбом")
    button3 = KeyboardButton("📋 Управление плейлистами")
    keyboard.add(button1, button2, button3)
    return keyboard


# Меню для управления плейлистами
def playlist_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton("Создать плейлист")
    button2 = KeyboardButton("Добавить в плейлист")
    button3 = KeyboardButton("Воспроизвести плейлист")
    button4 = KeyboardButton("Назад")
    keyboard.add(button1, button2, button3, button4)
    return keyboard


# Стартовое сообщение
@dp.message(Command(commands=['start']))
async def send_welcome(message: Message):
    await message.reply("Привет! Выберите действие из меню ниже:", reply_markup=main_menu())


# Обработка главного меню
@dp.message(Text("🎵 Найти трек"))
async def find_track_prompt(message: Message):
    await message.reply("Введите название или ссылку на трек:")


@dp.message(Text("📀 Найти альбом"))
async def find_album_prompt(message: Message):
    await message.reply("Введите название или ссылку на альбом:")


@dp.message(Text("📋 Управление плейлистами"))
async def manage_playlists(message: Message):
    await message.reply("Выберите действие:", reply_markup=playlist_menu())


# Обработка кнопок управления плейлистами
@dp.message(Text("Создать плейлист"))
async def create_playlist(message: Message):
    await message.reply("Введите имя нового плейлиста:")


@dp.message(Text("Добавить в плейлист"))
async def add_to_playlist(message: Message):
    await message.reply("Введите название песни и плейлиста (через запятую):")


@dp.message(Text("Воспроизвести плейлист"))
async def play_playlist(message: Message):
    await message.reply("Введите название плейлиста для воспроизведения:")


@dp.message(Text("Назад"))
async def back_to_main_menu(message: Message):
    await message.reply("Возвращение в главное меню:", reply_markup=main_menu())


# Обработка создания плейлиста
@dp.message()
async def handle_create_playlist(message: Message):
    playlist_name = message.text.strip()
    if not playlist_name:
        await message.reply("Пожалуйста, укажите имя для нового плейлиста.")
        return

    try:
        client.add_playlist(playlist_name)  # Вызов функции создания плейлиста
        await message.reply(f"Плейлист '{playlist_name}' успешно создан!")
    except Exception as e:
        logging.error(f"Ошибка при создании плейлиста: {e}")
        await message.reply("Не удалось создать плейлист. Попробуйте позже.")


# Обработка добавления трека в плейлист
@dp.message()
async def handle_add_to_playlist(message: Message):
    user_input = message.text.strip()
    if ',' not in user_input:
        await message.reply("Пожалуйста, укажите название песни и плейлиста через запятую.")
        return

    track_name, playlist_name = map(str.strip, user_input.split(',', 1))
    try:
        client.add_song_to_playlist(playlist_name, track_name)  # Вызов функции добавления трека
        await message.reply(f"Трек '{track_name}' добавлен в плейлист '{playlist_name}'.")
    except Exception as e:
        logging.error(f"Ошибка при добавлении трека в плейлист: {e}")
        await message.reply("Не удалось добавить трек в плейлист. Попробуйте позже.")


# Обработка воспроизведения плейлиста
@dp.message()
async def handle_play_playlist(message: Message):
    playlist_name = message.text.strip()
    if not playlist_name:
        await message.reply("Пожалуйста, укажите имя плейлиста для воспроизведения.")
        return

    try:
        tracks = client.print_playlist(playlist_name)  # Вызов функции получения треков
        if not tracks:
            await message.reply(f"Плейлист '{playlist_name}' пуст или не найден.")
            return

        await message.reply(f"Начинаю воспроизведение плейлиста '{playlist_name}':")
        for track in tracks:
            await send_track_to_user(track, message, is_album=True)
            await asyncio.sleep(1)

    except Exception as e:
        logging.error(f"Ошибка при воспроизведении плейлиста: {e}")
        await message.reply("Не удалось воспроизвести плейлист. Попробуйте позже.")


# Логика работы с Yandex Music
async def send_track_to_user(track, message: Message, is_album=False):
    artist_names = ', '.join(artist.name for artist in track.artists)
    track_filename = f"{artist_names} - {track.title}.mp3"

    try:
        track.download(track_filename)
        audio_file = InputFile(track_filename)
        await message.reply_document(audio_file)

        if not is_album:
            await message.reply(
                f"Трек {artist_names} - {track.title} был отправлен!\nСпасибо за использование бота"
            )
    finally:
        await asyncio.sleep(5)
        if os.path.exists(track_filename):
            os.remove(track_filename)


# Основная функция
async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
