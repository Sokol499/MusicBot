import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
import yandex_music
import os
import asyncio

logging.basicConfig(level=logging.INFO)

bot = Bot(token="7726809113:AAFpJSJq90G95kRov7saYikL_LUVRoR0Y8I")
dp = Dispatcher()

YANDEX_MUSIC_TOKEN = ""

ym_client = yandex_music.Client(YANDEX_MUSIC_TOKEN).init()

@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: Message):
    await message.reply(
        "Привет! Отправь название или ссылку на трек из Яндекс Музыки, и я отправлю тебе его аудиофайл.\n"
        "Вводить надо в формате: /track ссылка_на_трек или название_трека")

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

        track_filename = f"{track.artists[0].name} - {track.title}.mp3"
        track.download(track_filename)

        audio_file = FSInputFile(track_filename)
        await message.reply_document(audio_file)

        await message.reply(
            f"Трек {track.artists[0].name} - {track.title} был отправлен!\nСпасибо за использование бота")

        await asyncio.sleep(5)
        os.remove(track_filename)
        return

    except Exception as e:
        await message.reply("Произошла ошибка при загрузке трека.")
        logging.error(f"Ошибка при загрузке трека: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

