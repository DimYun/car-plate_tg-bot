import asyncio
import logging
import sys
from PIL import Image
from io import BytesIO
import requests
import numpy as np
from geopy.geocoders import Nominatim

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, BufferedInputFile

from config import BOT_TOKEN, API_URL
from keyboards import kb_location, kb_location_result, kb_payment
from states import MenuSG


storage = MemoryStorage()
dp = Dispatcher(storage=storage)


@dp.message(Command("start"))
async def handler_start(message: Message, state: FSMContext) -> None:
    start_msg = (
        'Hi! I am "remember my car" bot, ' +
        'please sent me a photo of your car. It should contain ' +
        'car plate number!'
    )
    await state.set_state(MenuSG.photo_and_location)
    await message.answer(
        text=start_msg,
    )


@dp.message(StateFilter(MenuSG.photo_and_location), F.photo)
async def handler_photo(message: Message, bot: Bot) -> None:
    binary_io = await bot.download(
        message.photo[-1],  # destination=f"{message.photo[-1].file_id}.jpg"
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
        caption="Description"
    )
    await message.answer(
        text=f"Get your car photo! Car plate number is: {plate_text[0]}. Now you can sent me the geolocation.",
        reply_markup=kb_location()
    )


def get_plate(im_bytes: bytes, im_name: str) -> tuple:
    files = {
        'image': (f'{im_name}.jpg', im_bytes),
    }
    print(API_URL)
    response = requests.post(
        API_URL,
        files=files,
        verify=False
    )

    plate_number = 'Not Process'
    crop_bbox = {
        'x_min': 0,
        'x_max': 0,
        'y_min': 0,
        'y_max': 0,
    }
    plate_data = response.json()
    try:
        plate_number = plate_data['predictions']['plates'][0]['value']
    except requests.exceptions.RequestException:
        print(response.text)

    crop_bbox = plate_data['predictions']['plates'][0]['bbox']
    image = np.array(Image.open(im_bytes))
    crop_image = image[crop_bbox['y_min']:crop_bbox['y_max'], crop_bbox['x_min']:crop_bbox['x_max'], :]

    return crop_image, plate_number


@dp.message(StateFilter(MenuSG.photo_and_location), F.text == "Change photo")
async def handler_new_photo(message: Message) -> None:
    await message.answer(text="Please sent a new photo", reply_markup=ReplyKeyboardRemove())


@dp.message(StateFilter(MenuSG.photo_and_location), F.location)
async def handler_location(message: Message, state: FSMContext) -> None:
    hr_location = get_location(
        message.location.latitude,
        message.location.longitude
    )
    await message.answer(
        text=f"""
Parking address: {hr_location}
Latitude: {message.location.latitude}
Longitude: {message.location.longitude}
Is it correct?
""",
        reply_markup=kb_location_result(),
    )


def get_location(lat: float, long: float) -> str:
    # calling the nominatim tool
    geoLoc = Nominatim(user_agent="GetLoc")

    # passing the coordinates
    locname = geoLoc.reverse(f"{lat}, {long}")

    # printing the address/location name
    print(locname.address)
    return locname.address


@dp.message(StateFilter(MenuSG.photo_and_location), F.text == "Yes")
async def handler_result(message: Message, state: FSMContext) -> None:
    await state.set_state(MenuSG.payment)
    await message.answer(text="Well done!", reply_markup=ReplyKeyboardRemove())
    await message.answer(text="Now you can pay for parking", reply_markup=kb_payment())


@dp.callback_query(StateFilter(MenuSG.payment), F.data == "pay")
async def handler_payment(cd: CallbackQuery, state: FSMContext) -> None:
    await cd.answer(text="Payment are disabled now", show_alert=True)


async def main() -> None:
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
