# stegic-bot
A bot that will help encrypt and decode text in / from a photo

![Stegic](https://user-images.githubusercontent.com/102413334/229926255-ee06d423-3fa0-448c-8a4f-7af520e04a38.png)

Даний бот може вживлювати текст у фотографії та декодувати текст з них.

В бота є три кнопки :

- Про бота

- Шифрування 

При переході до шифрування користувачеві необхідно надіслати зображення як файл у форматі jpg*.
Після цього бот попросить ввести саме повідомлення**, яке потрібно буде зашифрувати.
Останній крок - надати назву файлу. 
В результаті бот надішле користувачеві фотографію з вживленним у нього повідомленням та пароль. 
(Бот після шифрування або декодування автоматично видаляє тимчасові файли, тож фотографії або текст користувача не зберігається.)

- Декодування
При переході до користувачеві необхідно надіслати фотографію з зашифрованим всередині повідомленням як файл у форматі png.
Після цього бот попросить надати йому пароль.
В результаті бот відправить вам текст, який було вживлено в це зображення.


*через особливість методу та бібліотеки, що була використана, бот сприймає на вхід зображення у форматі jpg.

** повідомлення має складатись виключно з тексту, без емодзі і так далі.

==========================================================================


This bot can encode text in photos and decode text from them.

The bot has three buttons:

- About the bot 

- Encryption

When switching to encryption, the user must send the image as a jpg* file.
After that, the bot will ask you to enter the message** that needs to be encrypted.
The last step is to provide a file name.
As a result, the bot will send the user a photo with a message and password embedded in it. 
(The bot automatically deletes temporary files after encryption or decryption, so no user photos or text are stored.)

- Decoding
When going to the user, you need to send a photo with an encrypted message inside as a png file.
After that, the bot will ask for a password.
As a result, the bot will send you the text that was embedded in this image.


*due to the feature of the method and the library that was used, the bot accepts images in jpg format as input.

** the message should consist only of text, without emojis and so on.
