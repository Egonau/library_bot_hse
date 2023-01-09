from pyzbar.pyzbar import decode
import logging
from PIL import Image


def photo(bot,
          message):
    # в переменной bot хранится информация о токене чат-бота, message - аргумент функции в основном файле
    if message.photo is None:
        return None
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)

    img = Image.open("image.jpg")
    all_info = decode(img)
    for i in all_info:
        return (i.data.decode("utf-8"))
