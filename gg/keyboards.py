import telebot
from telebot import types
from mysql.connector import connect, Error


main = telebot.types.ReplyKeyboardMarkup(True)
main.row('🤖 Мои боты')
main.row('💼 Профиль','📜 Информация')

otmena = telebot.types.ReplyKeyboardMarkup(True)
otmena.row('Отмена')


admin = telebot.types.ReplyKeyboardMarkup(True)
admin.row('Статистика','Рассылка')
admin.row('Добавление','Удаление','Изменить')
admin.row('Пользователи','Боты')
admin.row('Поддержка','Выплаты')