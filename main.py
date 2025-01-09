import asyncio
import logging
import sys
import typing

from PIL import Image
from io import BytesIO
import requests
import base64
import numpy as np
from geopy.geocoders import Nominatim

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, BufferedInputFile

from config import BOT_TOKEN

from keyboards import kb_location, kb_location_result, kb_payment

from states import MenuSG


storage = MemoryStorage()
dp = Dispatcher(storage=storage)


@dp.message(Command("start"))
async def handler_start(message: Message, state: FSMContext) -> None:
    await state.set_state(MenuSG.photo_and_location)
    await message.answer(text="Привет, пришли фото)")

@dp.message(StateFilter(MenuSG.photo_and_location), F.photo)
async def handler_photo(message: Message, bot: Bot) -> None:
    binary_io = await bot.download(
        message.photo[-1],
        # destination=f"{message.photo[-1].file_id}.jpg"
    )
    crop_image, plate_text = get_plate(
        BytesIO(binary_io.read()),
        message.photo[-1].file_id
    )
    crop_image = Image.fromarray(crop_image)

    img_bytesio = BytesIO()
    img_bytesio.name = 'image.jpeg'
    crop_image.save(img_bytesio, 'JPEG')
    img_bytesio.seek(0)

    await message.answer_photo(
        BufferedInputFile(
            img_bytesio.read(),
            filename="buffer_img.jpg"
        ),
        caption="Opisanie"
    )
    await message.answer(text=f"Получил! Номер: {plate_text[0]}, Теперь пришли геолокацию", reply_markup=kb_location())


def get_plate(im_bytes: bytes, im_name: str) -> tuple:
    url = 'https://logicyield.org/plates/plates/process_content'

    files = {
        'image': (f'{im_name}.jpg', im_bytes),
    }
    response = requests.post(
        url,
        # headers=headers,
        files=files
    )

    plate_number = 'Not Process'
    crop_bbox = {
        'x_min': 0,
        'x_max': 0,
        'y_min': 0,
        'y_max': 0,
    }
    try:
        data = response.json()
        plate_number = data['predictions']['plates'][0]['value']
        crop_bbox = data['predictions']['plates'][0]['bbox']
        # print(data)
    except requests.exceptions.RequestException:
        print(response.text)

    image = np.array(Image.open(im_bytes))
    crop_image = image[crop_bbox['y_min']:crop_bbox['y_max'], crop_bbox['x_min']:crop_bbox['x_max'], :]

    return crop_image, plate_number


@dp.message(StateFilter(MenuSG.photo_and_location), F.text == "Изменить фото")
async def handler_new_photo(message: Message) -> None:
    """
    надо придумать как удалить старое фото.
    у меня есть решение, но мне нужно время на её реализацию
    """
    await message.answer(text="Пришли новое фото)", reply_markup=ReplyKeyboardRemove())


@dp.message(StateFilter(MenuSG.photo_and_location), F.location)
async def handler_location(message: Message, state: FSMContext) -> None:
    hr_location = get_location(
        message.location.latitude,
        message.location.longitude
    )
    await message.answer(text=f"""
Адрес парковки: {hr_location}
Широта: {message.location.latitude}
Долгота: {message.location.longitude}
Правильно?
""", reply_markup=kb_location_result())


def get_location(lat: float, long: float) -> str:
    # calling the nominatim tool
    geoLoc = Nominatim(user_agent="GetLoc")

    # passing the coordinates
    locname = geoLoc.reverse(f"{lat}, {long}")

    # printing the address/location name
    print(locname.address)
    return locname.address



@dp.message(StateFilter(MenuSG.photo_and_location), F.text == "Да")
async def handler_result(message: Message, state: FSMContext) -> None:
    await state.set_state(MenuSG.payment)
    await message.answer(text="Все готово!", reply_markup=ReplyKeyboardRemove())
    await message.answer(text="Осталось оплатить", reply_markup=kb_payment())

@dp.callback_query(StateFilter(MenuSG.payment), F.data == "pay")
async def handler_payment(cd: CallbackQuery, state: FSMContext) -> None:
    await cd.answer(text="Оплата временно не работает", show_alert=True)


async def main() -> None:
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())