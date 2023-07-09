import telebot
from telebot import types
from mysql.connector import connect, Error


main = telebot.types.ReplyKeyboardMarkup(True)
main.row('⚡️ Продвижение','⚙️ Мои заказы')
main.row('💳 Профиль','👨 Поддержка')

otmena = telebot.types.ReplyKeyboardMarkup(True)
otmena.row('Отмена')
