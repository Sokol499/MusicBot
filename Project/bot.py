import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, InputFile, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import yandex_music
import os
import asyncio

from config import TOKEN, TOKEN_1
import client  # Используется для работы с плейлистами

# Логгирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN_1)
dp = Dispatcher()

# Инициализация Yandex Music клиента
YANDEX_MUSIC_TOKEN = TOKEN
ym_client = yandex_music.Client(YANDEX_MUSIC_TOKEN).init()


# Главное меню
def main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("🎵 Найти трек")],
            [KeyboardButton("📀 Найти альбом")],
            [KeyboardButton("📋 Управление плейлистами")],
        ],
        resize_keyboard=True
    )
    return keyboard


def playlist_menu():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Создать плейлист", callback_data="create_playlist")],
            [InlineKeyboardButton(text="Добавить в плейлист", callback_data="add_to_playlist")],
            [InlineKeyboardButton(text="Воспроизвести плейлист", callback_data="play_playlist")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")],
        ]
    )
    return keyboard


# Стартовое сообщение
@dp.message(Command(commands=['start']))
async def send_welcome(message: Message):
    await message.reply("Привет! Выберите действие из меню ниже:", reply_markup=main_menu())


# Обработка кнопок главного меню
@dp.message()
async def handle_main_menu(message: Message):
    if message.text == "🎵 Найти трек":
        await message.reply("Введите название или ссылку на трек:")
    elif message.text == "📀 Найти альбом":
        await message.reply("Введите название или ссылку на альбом:")
    elif message.text == "📋 Управление плейлистами":
        await message.reply("Выберите действие:", reply_markup=playlist_menu())


# Обработка кнопок подменю плейлистов
@dp.callback_query()
async def handle_playlist_menu(callback: CallbackQuery):
    if callback.data == "create_playlist":
        await callback.message.reply("Введите имя нового плейлиста:")
    elif callback.data == "add_to_playlist":
        await callback.message.reply("Введите название песни и плейлиста (через запятую):")
    elif callback.data == "play_playlist":
        await callback.message.reply("Введите название плейлиста для воспроизведения:")
    elif callback.data == "back_to_main":
        await callback.message.edit_text("Возвращение в главное меню:", reply_markup=main_menu())


# Логика работы с плейлистами через client
@dp.message()
async def handle_create_playlist(message: Message):
    playlist_name = parse_user_input(message)
    if not playlist_name:
        await message.reply("Пожалуйста, укажите имя для нового плейлиста.")
        return

    try:
        client.add_playlist(playlist_name)  # Вызов функции создания плейлиста
        await message.reply(f"Плейлист '{playlist_name}' успешно создан!")
    except Exception as e:
        logging.error(f"Ошибка при создании плейлиста: {e}")
        await message.reply("Не удалось создать плейлист. Попробуйте позже.")


@dp.message()
async def handle_add_to_playlist(message: Message):
    user_input = parse_user_input(message)
    if not user_input or ',' not in user_input:
        await message.reply("Пожалуйста, укажите название песни и плейлиста через запятую.")
        return

    track_name, playlist_name = map(str.strip, user_input.split(',', 1))
    try:
        client.add_song_to_playlist(playlist_name, track_name)  # Вызов функции добавления трека
        await message.reply(f"Трек '{track_name}' добавлен в плейлист '{playlist_name}'.")
    except Exception as e:
        logging.error(f"Ошибка при добавлении трека в плейлист: {e}")
        await message.reply("Не удалось добавить трек в плейлист. Попробуйте позже.")


@dp.message()
async def handle_play_playlist(message: Message):
    playlist_name = parse_user_input(message)
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


# Остальные вспомогательные функции остаются без изменений
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


# Основная функция
async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
