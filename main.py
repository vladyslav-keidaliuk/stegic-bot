import telebot
import os
from PIL import Image
from telebot import types
from transliterator import get_ready, fix
from steganocryptopy.steganography import Steganography


bot = telebot.TeleBot(token='YOUR_TOKEN')


def convert_to_code(personal_password):  # подовжує пароль, якщо він менше 44 символів

    while len(personal_password) != 43:
        personal_password = personal_password + "0"
    personal_password = personal_password + "="
    return personal_password

def menubar(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    about_btn = types.KeyboardButton('/Про_бота')
    encode_btn = types.KeyboardButton('/Шифрування')
    decode_btn = types.KeyboardButton('/Декодування')
    markup.add(about_btn, encode_btn, decode_btn)

    bot.send_message(message.chat.id, "Головне меню", reply_markup=markup)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    about_btn = types.KeyboardButton('/Про_бота')
    encode_btn = types.KeyboardButton('/Шифрування')
    decode_btn = types.KeyboardButton('/Декодування')
    markup.add(about_btn, encode_btn, decode_btn)

    bot.send_message(message.chat.id, "Привіт, "
                     + message.from_user.first_name
                     + ", я Stegic, допоможу тобі сховати таємне повідомлення у зображення, "
                       "або навпаки витягнути повідомлення з зображення.\n"
                       "1. Щоб сховати повідомлення у зображення, натисніть <Шифрування>\n"
                       "2. Щоб побачити сховане повідомлення у зображення, натисніть <Декодування>\n"
                       "3. Щоб дізнатись більш детальну інформацію про бота, натисніть <Про_бота>", reply_markup=markup)


@bot.message_handler(commands=['Про_бота'])
def send_about(message):
    bot.send_message(
        message.chat.id,
        "Stegic\n\n"
        "Цей бот створено для вживлення повідомлень в зображення.\n\n"
        "Важлива інформація\n\n"
        "1) Бот після вживлення повідомлень в зображення видаляє Ваше зображення та повідомлення.\n"
        "2) Бажано надсилати зображення у форматі jpg.\n"
        "3) Бажано надсилати зображення у портретній орієнтації, в іншому випадку бот поверне зображення на 90°\n"
        "4) Пароль має бути завдовжки не більше 43 символів!!!!!\n"
        "5) Приклад паролю:\n"
        "   1. QWERTYUIOPasdfghjklzxcvbnm12345678912345674\n"
        "   2. PasswordExample\n"
        "6) Не можна у повідомленні використовувати стікери, емодзі і т.д.\n"
        "7) Зображення відправляємо боту як файл, а не фото.")


@bot.message_handler(commands=['Шифрування'])
def _start_(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(chat_id, 'Надішли мені зображення', reply_markup=markup)
    bot.register_next_step_handler(msg, get_photo)


def get_photo(message):
    try:
        downloaded_file = bot.download_file(bot.get_file(message.document.file_id).file_path)
        src = 'img/' + str(message.chat.id) + 'original.jpg'
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        Image.open('img/' + str(message.chat.id) + 'original.jpg').save('img/' + str(message.chat.id) + 'original.png')
        bot.reply_to(message, "Я збережу це.")
        msg = bot.send_message(message.chat.id, 'Увага! Наразі підтримується текст англійською та українською.\n'
                                                'Заборонено використовувати емодзі та усе інше, що не є текстом.\n\n'
                                                'Надішліть текст, який буде зашифровано в зображенні: ')
        bot.register_next_step_handler(msg, get_secret_text_and_encryption)

    except:
        bot.send_message(message.chat.id, 'Виникла помилка!! Можливо Ви надіслали фото не як файл.\n'
                                          'Наступного разу спробуйте надіслати фото як файл.\n'
                                          'Вас буде повернено до головного меню.')
        menubar(message)


def get_secret_text_and_encryption(message):
    chat_id = message.chat.id

    try:
        open('text/' + str(message.chat.id) + 'message.txt', 'w', encoding='UTF-8').write(get_ready(message.text))

        msg = bot.send_message(chat_id, 'Увага! Пароль має бути лише з англійських букв, '
                                        'без пробілів та не більше 43 символів у довжину.\n'
                                        'Дозволяються нижні підкреслення\n'
                                        'Напиши пароль, який знадобиться при декодуванні: ')
        bot.register_next_step_handler(msg, get_password_for_image)

    except:
        bot.send_message(chat_id, 'Виникла помилка!! Можливо Ви надіслали не текст.\n'
                                  'Вас буде повернено до головного меню.')
        menubar(message)


def get_password_for_image(message):
    try:
        password = message.text

        if (len(password) < 44) & (password[-1] != "="):
            password = convert_to_code(password)

        open('text/' + str(message.chat.id) + 'personal.key', 'w', encoding='UTF-8').write(password)
        open('text/' + str(message.chat.id) + 'personal_to_user.key', 'w', encoding='UTF-8').write(message.text)

        msg = bot.send_message(message.chat.id, 'Напишіть яку назву повинен мати Ваш файл'
                                                ' зі схованим повідомленням всередині зображення: ')
        bot.register_next_step_handler(msg, named_and_create_secret_image)
    except:
        bot.send_message(message.chat.id,
                         'Виникла помилка!! Можливо Ви надіслали не сукупність літер та знаків,'
                         'або не англійскою, або з пробілами.\n'
                         'Вас буде повернено до головного меню.')
        menubar(message)


def named_and_create_secret_image(message):
    try:

        chat_id = message.chat.id
        secret = Steganography.encrypt("text/" + str(message.chat.id) + "personal.key",
                                       "img/" + str(message.chat.id) + "original.png",
                                       "text/" + str(message.chat.id) + "message.txt")
        secret.save('img/' + str(message.text) + '.png')
        open('text/' + str(message.chat.id) + 'personal.key', 'r', encoding='UTF-8').read()

        key_to_user = open('text/' + str(message.chat.id) + 'personal_to_user.key', 'r', encoding='UTF-8')
        key_to_user_read = key_to_user.read()
        key_to_user.close()

        key_to_user_read = "Ваш пароль : " + key_to_user_read
        reply_file = open('img/' + str(message.text) + '.png', 'rb')

        bot.send_document(chat_id, reply_file)
        bot.send_message(chat_id, key_to_user_read)

        reply_file.close()

        os.remove('img/' + str(message.text) + '.png')
        os.remove('img/' + str(message.chat.id) + 'original.png')
        os.remove('img/' + str(message.chat.id) + 'original.jpg')
        os.remove('text/' + str(message.chat.id) + 'message.txt')
        os.remove('text/' + str(message.chat.id) + 'personal.key')
        os.remove('text/' + str(message.chat.id) + 'personal_to_user.key')

        bot.send_message(chat_id, 'Усе готово ))')
        menubar(message)
    except:
        bot.send_message(message.chat.id,
                         'Виникла помилка!!\n'
                         'Спробуйте ще раз.\n'
                         'Вас буде повернено до головного меню.')
        menubar(message)


@bot.message_handler(commands=['Декодування'])
def start_decrypt(message):
    markup = types.ReplyKeyboardRemove(selective=False)

    msg = bot.send_message(message.chat.id, 'Надішли мені зображення яке всередині містить секретне повідомлення',
                           reply_markup=markup)
    bot.register_next_step_handler(msg, get_photo_decrypt)


def get_photo_decrypt(message):
    try:

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = 'img/' + str(message.chat.id) + 'secret_to_decode.png'
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        open('img/' + str(message.chat.id) + 'secret_to_decode.png', 'rb').close()
        bot.reply_to(message, "Я збережу це.")
        msg = bot.send_message(message.chat.id, 'Напиши мені пароль : ')
        bot.register_next_step_handler(msg, decode_secret)

    except:
        bot.send_message(message.chat.id,
                         'Виникла помилка!! Можливо Ви надіслали фото з секретним повідомленням не як файл.\n'
                         'Наступного разу спробуйте надіслати фото як файл.\n'
                         'Вас буде повернено до головного меню.')
        menubar(message)


def decode_secret(message):
    try:

        chat_id = message.chat.id
        key_for_decode = message.text

        if len(str(key_for_decode)) < 44:
            key_for_decode = convert_to_code(str(key_for_decode))
        else:
            key_for_decode = str(key_for_decode)

        message_secret = open('text/' + str(message.chat.id) + 'key_for_decode.key', 'w', encoding='UTF-8')
        message_secret.write(key_for_decode)
        before_translit = Steganography.decrypt("text/" + str(message.chat.id) + "key_for_decode.key",
                                                "img/" + str(message.chat.id) + "secret_to_decode.png")

        text = fix(before_translit)
        bot.send_message(chat_id, "Ось що було сховано в цьому зображенні :\n")
        bot.send_message(chat_id, text)

        os.remove('img/' + str(message.chat.id) + 'secret_to_decode.png')
        os.remove('text/' + str(message.chat.id) + 'key_for_decode.key')
        menubar(message)

    except Exception:
        bot.send_message(message.chat.id,
                         'Виникла помилка!!\n'
                         'Спробуйте ще раз.\n'
                         'Вас буде повернено до головного меню.')
        menubar(message)


updates = bot.get_updates()
last_update_id = updates[-1].update_id if updates else None

bot.get_updates(offset=last_update_id)
bot.polling(none_stop=True)
