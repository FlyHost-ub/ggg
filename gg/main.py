# -*- coding: utf-8 -*-
from decimal import *
from email import message
import telebot
import datetime
from telebot import types, apihelper
import sqlite3
import random, string
import time
import os,random,shutil,subprocess
from subprocess import check_output
from telebot.apihelper import ApiTelegramException
import json
import keyboards
import requests
from datetime import datetime, timedelta
from datetime import date
from dateutil.relativedelta import relativedelta
import secrets
import hashlib
import config
from getpass import getpass
from mysql.connector import connect, Error
from time import time
from threading import Thread
import threading
from threading import Timer
import time
import os,random,shutil,subprocess
import json
import urllib.request


# Слито в end_soft
bot = telebot.TeleBot(config.bot_token)
bot_name = 'Smm_Hermes_bot'

admin2 = -1001799352145

def spam(user):
	connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
	q = connection.cursor()
	date = datetime.today()
	date = date.strftime("%H:%M")
	q.execute("INSERT INTO spam (user,data) VALUES ('%s','%s')"%(user,date))
	connection.commit()
	q.execute(f"SELECT COUNT(id) FROM spam where user = '{user}'")
	message_count = q.fetchone()[0]
	if int(message_count) == 10:
		bot.send_message(user, '<b>❗️ Зафиксирована аномальная активность, если вы не прекратите спам, вы будете заблокированы.</b>',parse_mode='HTML')
	elif int(message_count) == 30:
		q.execute(f"update ugc_users set status = 'Заблокирован' WHERE id = '{user}' and bot = '{bot_name}'")
		connection.commit()
		bot.send_message(user, '<b>❗️ Вы заблокированы, для снятия блокировки обратитесь в поддержку.</b>',parse_mode='HTML')
	else:
		q.execute(f"DELETE FROM spam where data != '{date}'")
		connection.commit()
		

# Слито в end_soft


@bot.message_handler(commands=['start'])
def start_message(message):
		if message.chat.type == 'private':
			spam(message.chat.id)
			connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
			q = connection.cursor()
			q.execute(f'SELECT * FROM ugc_users WHERE id = "{message.chat.id}" and bot = "{bot_name}"')
			row = q.fetchall()
			if str(row) == '[]':
				tomorrow = datetime.now()
				data = tomorrow.strftime('%d/%m/%Y')
				q.execute("INSERT INTO ugc_users (id,bot,data,status) VALUES ('%s','%s','%s','%s')"%(message.chat.id,bot_name,data,'Активен'))
				connection.commit()
				if message.text[7:] != '' and message.text[7:] != message.chat.id:
					q.execute(f'SELECT * FROM promo WHERE name = "{message.text[7:]}"')
					rows = q.fetchall()
					if len(rows) >= 1:
						q.execute(f"update promo set coolvo = coolvo + 1 where name = '{message.text[7:]}'")
						connection.commit()
						bot.send_message(-1001799352145,f'''@{message.from_user.username} | {message.text[7:]}''')
					else:
						try:
							q.execute(f"update ugc_users set ref = '{message.text[7:]}' where id = {message.chat.id} and bot = '{bot_name}'")
							connection.commit()
							keyboard = types.InlineKeyboardMarkup()
							keyboard.add(types.InlineKeyboardButton(text='✖️ Закрыть',callback_data=f'Закрыть '))
							bot.send_message(message.text[7:], f'➕ Новый реферал: @{message.from_user.username}',reply_markup=keyboard)	
						except:
							pass
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='↗️ Как начать зарабатывать',url=f'https://telegra.ph/XAለVA--SMM-FRANCHISE--Navigaciya-po-menyu-04-15 '))
				bot.send_message(message.chat.id,'''🔥 Хочешь выучить как запустить  пассивный заработок и выйти на фиксированную прибыль без затрат, времени и средств? 

❗️ Обязательно прочитай:''',disable_web_page_preview = True,parse_mode='HTML' ,reply_markup=keyboard)
			q.execute(f"SELECT status FROM ugc_users where id = '{message.chat.id}' and bot = '{bot_name}'")
			if message.text[7:] ==  'support':
				msg = bot.send_message(message.chat.id, f'''<b>🆘 Внимание:
├</b><i>Иногда ответ может занять до 6 часов, в зависимости от нагрузки.</i>
<b>├</b><i>С вопросом о выводе средств писать в поддержку нет смысла, так как вывод происходит автоматизировано. В случае ошибки при указании реквизитов вы получите полномерный возврат.</i>
<b>└✍️ Напишите свой вопрос для обращения к нам:</b>''',parse_mode='HTML', reply_markup=keyboards.otmena)
				bot.register_next_step_handler(msg, supportadd, msg.message_id)
			else:
				bot.send_message(message.chat.id,'''<b>👑 Добро пожаловать в лучший сервис для генерации пассивного дохода.</b>''',disable_web_page_preview = True,parse_mode='HTML' ,reply_markup=keyboards.main)

			
# Слито в end_soft

# def capcha(message,msg_id):
# 		spam(message.chat.id)
# 		if message.text.lower() == 'Simpsonfather.ru':
# 			keyboard = types.InlineKeyboardMarkup()
# 			keyboard.add(types.InlineKeyboardButton(text='↗️ Как начать зарабатывать',url=f'https://telegra.ph/XAለVA--SMM-FRANCHISE--Navigaciya-po-menyu-04-15 '))
# 			bot.send_message(message.chat.id,'''🔥 Хочешь выучить как запустить  пассивный заработок и выйти на фиксированную прибыль без затрат, времени и средств? 

# ❗️Обязательно прочитай:''',disable_web_page_preview = True,parse_mode='HTML' ,reply_markup=keyboard)
# 			bot.send_message(message.chat.id,'''<b>👑 Добро пожаловать в лучший сервис для генерации пассивного дохода.</b>''',disable_web_page_preview = True,parse_mode='HTML' ,reply_markup=keyboards.main)
# 		else:
# 			photo = 'https://i.imgur.com/AyRbtQn.jpg'
# 			msg = bot.send_photo(message.chat.id,photo, '''<b>🔰 Пройдите капчу:
# └</b><i>Введите текст:</i> <code>Simpsonfather.ru</code>''',parse_mode='HTML')
# 			bot.register_next_step_handler(msg, capcha,msg.message_id)



#def check_spam(user_id):
#    if spam[user_id][1] == 0:
#        spam[user_id] = [datetime.now(), 1]
#    elif spam[user_id][1] == 20:
#        if datetime.now() - spam[user_id][0] < datetime.minute:
#            punishing_the_spammer()
#        else:
#            spam[user_id][1] == 0
#            spam[user_id][0] = datetime.now()
#    else:
#        spam[user_id][1] = spam[user_id][1] + 1

@bot.message_handler(content_types=['text'])
def send_text(message):
	msg = message.text
	if message.chat.type == 'private':
		if message.text == '🤖 Мои боты':
			connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
			q = connection.cursor()
			keyboard = types.InlineKeyboardMarkup()
			q.execute(f"SELECT * FROM list_bot where user = '{message.chat.id}'")
			rows = q.fetchall()
			if len(rows) != 0:
				for i in rows:
					keyboard.add(types.InlineKeyboardButton(text=i[2],callback_data=f'bot_ {i[0]}'))
			else:
				keyboard.add(types.InlineKeyboardButton(text='➕ Добавить бот',callback_data=f'add_bot'))	
			bot.send_message(message.chat.id, f'''<b>🤖 Список ботов:
└Выберите нужный бот:</b>''',parse_mode='HTML', reply_markup=keyboard)


# Слито в end_soft
		elif message.text == '💼 Профиль':
			connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
			q = connection.cursor()
			q.execute(f"SELECT COUNT(id) FROM list_bot where user = '{message.chat.id}'")
			botov = q.fetchone()[0]
			q.execute(f"SELECT SUM(dohod) FROM list_bot where user = '{message.chat.id}'")
			dohod = q.fetchone()[0]
			print(dohod)
			if dohod == None:
				dohod = 0
			q.execute(f"SELECT SUM(balance) FROM list_bot where user = '{message.chat.id}'")
			balance = q.fetchone()[0]
			if balance == None:
				balance = 0
			print(balance)	
			keyboard = types.InlineKeyboardMarkup()	
			keyboard.add(types.InlineKeyboardButton(text='📤 Вывести',callback_data=f'Вывод '))	
			keyboard.add(types.InlineKeyboardButton(text='🎁 Создать промо',callback_data=f'Промо '))
			keyboard.add(types.InlineKeyboardButton(text='🫂 Реферальная программа',callback_data=f'Реферальная '))		
			bot.send_message(message.chat.id, f'''<b>🎩 Личные данные:</b>
<b>├ID:</b> <code>{message.chat.id}</code>
<b>├UN:</b> <code>{message.chat.username}</code>
<b>└Ботов:</b> <code>{botov}</code>

<b>🤖 Информация по ботам:
├Доход:</b> <code>{dohod} RUB</code>
<b>└Баланс:</b> <code>{balance} RUB</code>
''',parse_mode='HTML', reply_markup=keyboard)


# Слито в end_soft
		elif message.text == '📜 Информация':
			keyboard = types.InlineKeyboardMarkup()	
			keyboard.add(types.InlineKeyboardButton(text='💬 Админ чᴀᴛ',url=f'https://t.me/+XT1onfxdBMhkMjc6'),types.InlineKeyboardButton(text='📰 Новости',url=f'https://t.me/+Off-KW3R3gk4ZjEy'))
			keyboard.add(types.InlineKeyboardButton(text='🧞 Инструкции & Информация',url=f'https://telegra.ph/XAለVA--SMM-FRANCHISE--Navigaciya-po-menyu-04-15 '))
			keyboard.add(types.InlineKeyboardButton(text=' 🧑‍🔧 Поддержка ᴄᴇᴩʙиᴄᴀ',callback_data=f'support'))
			bot.send_message(message.chat.id, '''<b>📜 Почему именно мы?
├</b><i>Наше сообщество является самым надежным поставщиком накрутки таких соц сетей, как Instagram, Vk, TikTok и Youtube, а так же и прочих услуг. </i>
<b>└</b><i>Цены в боте будут ниже рыночных и покупатель не сможет пройти мимо покупки именно у тебя!</i>

<b>💰 Мы абсолютно бесплатно:</b>
<b>├</b><i>Поможем вам запустить свой сервис накрутки и магазин.</i>
<b>├</b><i>Научим вас зарабатывать.</i>
<b>├</b><i>Сделаем бота вашим основным источником дохода в течении недели! </i>
<b>└</b><i>Мы любим зарабатывать, ровно так же, как и ты!</i>

<b>🚀 Подключение в два клика::
└</b><i>Для подключения бота вам всего лишь надо взять токен у <a href="https://t.me/BotFather">BotFather</a> и отправить его нам!</i>

<b>⚡️ Ощутите скорость самостоятельно:
└</b><i>Весь процесс накрутки и продаж автоматизирован, не нужно ни о чём беспокоиться. Занимайтесь любимыми делами, пока ваш бот будет пассивно зарабатывать!</i>''' ,parse_mode='HTML',reply_markup=keyboard,disable_web_page_preview = True)

		else:
			bot.send_message(message.chat.id, '<b>⚠️ Внимание, вероятнее всего, была введена неверная команда!</b>',parse_mode='HTML', reply_markup=keyboards.main)
	else:
		pass	

def support_otvet(message,idsup,msg_id):
	bot.delete_message(message.chat.id,message.message_id)
	if message.text.lower() != 'отмена':
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"SELECT * FROM support where id = '{idsup}'")
		row = q.fetchone()
		q.execute(f"update support set status = '0' where id = '{idsup}'")
		connection.commit()
		texts = F'''{row[2]}
└[S]<code>{message.text}</code>'''
		q.execute(f"update support set text = '{texts}' where id = '{idsup}'")
		connection.commit()
		q.execute(f"SELECT bot_token FROM list_bot where bot = '{row[4]}' ")
		bot_token = q.fetchone()[0]
		bots = telebot.TeleBot(bot_token)
		admin = config.admin
		try:
			bots.send_message(row[1], f'<b>❗️ Ответ от поддержки:</b> <code>{message.text}</code>',parse_mode='HTML')
		except:
			pass
		bot.send_message(message.chat.id, '<b>Успешно ответили</b>',parse_mode='HTML', reply_markup=keyboards.main)
	else:
		bot.send_message(message.chat.id, '<b>Отменили</b>',parse_mode='HTML', reply_markup=keyboards.main)

def poisk_user(message,bot_id,msg_id):
	bot.delete_message(message.chat.id,message.message_id)

	if message.text.lower() != 'отмена':
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"SELECT * FROM list_bot where id = '{bot_id}'")
		rows = q.fetchone()
		bot_name = rows[6]
		q.execute(f"SELECT * FROM ugc_users where id = '{message.text}'and bot = '{bot_name}' ")
		row = q.fetchone()
		bot.send_message(message.chat.id, '<b>🔍 Ищем...</b>',parse_mode='HTML')
		if row != None:
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='🔒 Заблокировать | Раблокировать',callback_data=f'заблокировать_ {bot_name} {row[0]}'))
			keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'бот '))	
			msg = bot.send_message(message.chat.id, f'''<b>👤 Пользователь:</b>
<b>├ID:</b> <code>{row[0]}</code>
<b>├Баланс:</b> <code>{row[6]}</code>
<b>└Статус:</b> <code>{row[3]}</code>
''',parse_mode='HTML',reply_markup=keyboard)
		else:
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'бот '))	
			bot.send_message(message.chat.id, '<b>🤔 Нет такого пользователя.</b>',parse_mode='HTML', reply_markup=keyboard)
	else:
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'бот '))	
		bot.send_message(message.chat.id, '<b>🤔 Отменили.</b>',parse_mode='HTML', reply_markup=keyboard)

def generator_pw():
    pwd =  string.digits
    return "".join(random.choice(pwd) for x in range(random.randint(10, 16)))

def btc_oplata_1(message):
    try:
        if int(message.text) >= int(1):
            url = f'https://h159987.srv16.test-hf.su/merchant?amount={message.text}&shop_id=66&label=6&hash=97f7a6f60c98c3778d84a9d14b645b2891e9b747c217aafb16cc7df85669ab9d'
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text=f'''↗️ Перейти к оплате ''',url=url))
            keyboard.add(types.InlineKeyboardButton(text=f'''🦋Проверить платеж''',callback_data=f'check_opl'))
            keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'Кабинет '))
            bot.send_message(message.chat.id, '''❗️ Для пополнения баланса, перейдите по ссылке  ниже и оплатите счет удобным способом !

            💡 После оплаты, вы получите уведомление о зачисление средств на баланс.''', reply_markup=keyboard)
        else:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'профиль '))
            bot.send_message(message.chat.id, f'❗️ Минимальная сумма пополнения 10 RUB',parse_mode='HTML', reply_markup=keyboards.main)
    except Exception as e:
        print(e)
def edit_procent(message,bot_id,msg_id):
	bot.delete_message(message.chat.id,message.message_id)
	bot.delete_message(message.chat.id,msg_id)
	if message.text != 'Отмена':
		if message.text.isdigit() == True:
			connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
			q = connection.cursor()
			q.execute(f"update list_bot set prace = '{message.text}' where id = '{bot_id}'")
			connection.commit()
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'bot_ {bot_id}'))
			bot.send_message(message.chat.id, f'✔️ Наценка успешно изменена, теперь ваш доход будет составлять {message.text} % от цены услуг.', reply_markup=keyboard)
		else:
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'bot_ {bot_id}'))
			bot.send_message(message.chat.id, '✖️ Ошибка, необходимо указывать целое число.', reply_markup=keyboard)

	else:
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'bot_ {bot_id}'))
		bot.send_message(message.chat.id, '✖️ Отменяем изменения......', reply_markup=keyboards.main)


def edit_sms(message,bot_id,msg_id):
	bot.delete_message(message.chat.id,message.message_id)
	bot.delete_message(message.chat.id,msg_id)
	if message.text != 'Отмена':
		if message.text.isdigit() == True:
			connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
			q = connection.cursor()
			q.execute(f"update list_bot set sms = '{message.text}' where id = '{bot_id}'")
			connection.commit()
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'bot_ {bot_id}'))
			bot.send_message(message.chat.id, f'✔️ Наценка успешно изменена.', reply_markup=keyboard)
		else:
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'bot_ {bot_id}'))
			bot.send_message(message.chat.id, '✖️ Ошибка, необходимо указывать целое число.', reply_markup=keyboard)

	else:
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'bot_ {bot_id}'))
		bot.send_message(message.chat.id, '✖️ Отменяем изменения......', reply_markup=keyboards.main)


def add_bot(message,msg_id):
	msd = bot.send_message(message.chat.id, '⏳ Идет создание бота, пожалуйста подождите....', reply_markup=keyboards.main)
	if message.text != 'Отмена':
		try:
			bot_create = telebot.TeleBot(message.text)
			user = message.chat.id
			name = bot_create.get_me().username
			balance = 0
			info = 'Текст'
			prace = 10
			bots = bot_create.get_me().username.lower()
			bot_token = message.text
			status = 'Работает'
			tomorrow = datetime.now()
			data = tomorrow.strftime('%d/%m/%Y')
			logi = data
			current_dir = os.getcwd()
			path = f'{current_dir}/bot_list/{bots}'
			os.makedirs(path, exist_ok=True)
			
			src = f'{current_dir}/bot/main.py'
			shutil.copy(src, path ,follow_symlinks=True)
			src = f'{current_dir}/bot/keyboards.py'
			shutil.copy(src, path ,follow_symlinks=True)
			
			my_file = open(f"{bots}.service", "a+")
			my_file.write(f'''[Unit]
Description={bots}
After=syslog.target
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory={current_dir}/bot_list/{bots}
ExecStart=/usr/bin/python3 {current_dir}/bot_list/{bots}/main.py
RestartSec=10
Restart=always

[Install]
WantedBy=multi-user.target''')
			my_file.close()
			src = f'{current_dir}/{bots}.service'
			print(current_dir)
			shutil.copy(src, '/etc/systemd/system/' ,follow_symlinks=True)
			print(path)
			path = os.path.join(os.path.abspath(os.path.dirname(__file__)), f'{bots}.service')
			print(path)
			os.remove(path)
			connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
			q = connection.cursor()
			q.execute("INSERT INTO list_bot (user,name,balance,info,prace,bot,bot_token,status,logi,dohod,deposit) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(user,name,balance,info,prace,bots,bot_token,status,logi,0,0))
			connection.commit()
			cmd1 = f'systemctl start {bots}'
			print(cmd1)
			subprocess.Popen(cmd1, shell=True)
			cmd = f'systemctl enable {bots}'
			print(cmd)
			subprocess.Popen(cmd, shell=True)
			cmdss = f'systemctl daemon-reload'
			print(cmdss)
			subprocess.Popen(cmdss, shell=True)

			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='🔧 Настройка бота',callback_data=f'бот '))
			keyboard.add(types.InlineKeyboardButton(text='📝 Инструкции',url=f'https://telegra.ph/XAለVA--SMM-FRANCHISE--Navigaciya-po-menyu-04-15 '))
			bot.send_message(message.chat.id, f'''Бот @{bots}, успешно подключен к <a href="t.me/Smm_Hermes_bot">Smm_Hermes_bot</a>.''',parse_mode='HTML', reply_markup=keyboard)
			bot.send_message(-1001799352145,f'''<b>🟩 Новый бот:</b>
<b>├Бот:</b> @{name}
<b>└USER:</b> @{message.chat.username}''',parse_mode='HTML')
		except Exception as e:
			print(e)
	else:
		bot.send_message(message.chat.id, '✖️ Вернулись на главную.', reply_markup=keyboards.main)

def addkeyboards(message,idbots):
	if message.text != 'Отмена':
		txtkey = message.text
		msg = bot.send_message(message.chat.id, "<b>✍️ Укажите содержимое кнопки:</b>",parse_mode='HTML', reply_markup=keyboards.main)
		bot.register_next_step_handler(msg, addkeyboards1, idbots,txtkey)
	else:
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'bot_ {idbots}'))
		bot.send_message(message.chat.id, '✖️ Отменяем изменения......', reply_markup=keyboards.main)

def addkeyboards1(message,idbots,txtkey):
	if message.text != 'Отмена':
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute("INSERT INTO keyboards (name,text,bot) VALUES ('%s','%s','%s')"%(txtkey,message.text,idbots))
		connection.commit()
		cmd1 = f'systemctl restart {idbots}'
		subprocess.Popen(cmd1, shell=True)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'бот '))
		bot.send_message(message.chat.id, f'''✔️ Кнопка успешно добавлена.''', reply_markup=keyboard)
	else:
		bot.send_message(message.chat.id, '✖️ Вернулись на главную', reply_markup=keyboards.main)

def generator_id():
    pwd =  string.digits
    return "".join(random.choice(pwd) for x in range(random.randint(9, 29)))

def generator_id1():
    pwd =  string.digits
    return "".join(random.choice(pwd) for x in range(random.randint(9, 29)))


def is_subscribed(user_id):
	try:
		status = ['creator', 'administrator', 'member','restricted']
		for i in status:
			if i == bot.get_chat_member(-735045317, user_id).status:
				return True
	except ApiTelegramException as e:
		if e.result_json['description'] == 'Bad Request: user not found':
			return False

def add_ref_balance(user,summa):
	connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
	q = connection.cursor()
	q.execute(f'select ref from ugc_users where id = "{user}" and bot = "{bot_name}"')
	ref_user = q.fetchone()[0]
	if ref_user != None:
		add_deposit = int(summa) / 100 * 10
		q.execute(f"update ugc_users set balance = balance + '{add_deposit}' where id = '{ref_user}' and bot = '{bot_name}'")
		connection.commit()
		q.execute(f"update ugc_users set ref = '{add_deposit}' where id = '{ref_user}' and bot = '{bot_name}'")
		connection.commit()
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'''✖️ Закрыть''',callback_data=f'Закрыть '))
		try:
			bot.send_message(ref_user, f'''<b>💰 Новый вывод реферала:</b> <code>{user}</code> <b>| Доход:</b> <code>{add_deposit}</code> <b>RUB</b>''',parse_mode='HTML',reply_markup=keyboard, disable_web_page_preview=True)
		except:
			pass
	else:
		pass

def addpromo(message,metod):
	try:
		if message.text != 'Отмена':
			if message.text.isdigit() == True:
				if int(message.text) >= int(1):
					summa = message.text
					msg = bot.send_message(message.chat.id, f'''✍️ <b>Укажите количество активации:</b>''',parse_mode='HTML', reply_markup=keyboards.otmena)
					bot.register_next_step_handler(msg, addpromo1, metod, summa)
				else:
					bot.send_message(message.chat.id, '''✖️ Минимальная сумма 1 RUB.''', parse_mode='HTML',reply_markup=keyboards.main)
			else:
				bot.send_message(message.chat.id, '''✖️ Минимальная сумма 1 RUB.''', parse_mode='HTML',reply_markup=keyboards.main)
		else:
			bot.send_message(message.chat.id, '✖️ Вернулись на главную',reply_markup=keyboards.main)
	except:
		bot.send_message(message.chat.id, '''✖️ Минимальная сумма 1 RUB.''', parse_mode='HTML',reply_markup=keyboards.main)

def addpromo1(message,metod,summa):
	try:
		if message.text != 'Отмена':
			if message.text.isdigit() == True:
				if float(message.text) >= float(1):
					colvo = message.text
					print(summa)
					print(colvo)
					minusbalance = int(summa) * int(colvo)
					if metod == 'referal':
						connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
						q = connection.cursor()
						q.execute(f'SELECT * FROM ugc_users WHERE id = "{message.chat.id}" and bot = "{bot_name}"')
						rows = q.fetchone()
						if float(rows[1]) >= float(minusbalance):
							q.execute(f"update ugc_users set balance = balance - '{float(minusbalance)}' where id = '{message.chat.id}' and bot = '{bot_name}'")
							connection.commit()
							promo = secrets.token_urlsafe(7)
							q.execute("INSERT INTO cupon (name,summa,colvo,user) VALUES ('%s','%s','%s','%s')"%(promo,summa,colvo,'None'))
							connection.commit()
							bot.send_message(message.chat.id, f'''<b>🎁 Промокод успешно создан:</b>
<b>├Сумма:</b> <code>{summa}</code>
<b>├Количество:</b> <code>{colvo}</code>
<b>└Название:</b> <code>{promo}</code>''', parse_mode='HTML',reply_markup=keyboards.main)

						else:
							bot.send_message(message.chat.id, '''✖
# Слито в end_soft''', parse_mode='HTML',reply_markup=keyboards.main)

# Слито в end_soft
					else:
						connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
						q = connection.cursor()
						q.execute(f"SELECT SUM(balance) FROM list_bot where user = '{message.chat.id}'")
						balance = q.fetchone()[0]
						if float(balance) >= float(minusbalance):
							q.execute(f"update list_bot set balance = balance - '{float(minusbalance)}' where bot = '{metod}'")
							connection.commit()
							promo = secrets.token_urlsafe(7)
							q.execute("INSERT INTO cupon (name,summa,colvo,user) VALUES ('%s','%s','%s','%s')"%(promo,summa,colvo,'None'))
							connection.commit()
							bot.send_message(message.chat.id, f'''<b>🎁 Промокод 
# Слито в end_soft создан:</b>
<b>├Сумма:</b> <code>{summa}</code>
<b>├Количество:</b> <code>{colvo}</code>
<b>└Название:</b> <code>{promo}</code>''', parse_mode='HTML',reply_markup=keyboards.main)

						else:
							bot.send_message(message.chat.id, '''✖️ Недостаточно средств.''', parse_mode='HTML',reply_markup=keyboards.main)
				else:
					bot.send_message(message.chat.id, '''✖️ Минимальная количество активации 1.''', parse_mode='HTML',reply_markup=keyboards.main)
			else:
				bot.send_message(message.chat.id, '''✖️ Минимальная количество активации 1.''', parse_mode='HTML',reply_markup=keyboards.main)
		else:
			bot.send_message(message.chat.id, '✖️ Вернулись на главную',reply_markup=keyboards.main)
	except:
		bot.send_message(message.chat.id, '''✖️ Минимальная количество активации 1.''', parse_mode='HTML',reply_markup=keyboards.main)
def vivod(message,method,botsname,msg_id):
	if message.text != 'Отмена':
		if message.text.isdigit() == True:
				connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
				q = connection.cursor()
				q.execute(f"SELECT * FROM list_bot WHERE bot = '{botsname}'")
				check_balans = q.fetchone()
				if botsname != 'referal':
					if float(check_balans[3]) >= float(10):
						if str(method) == str('CARD'):
							if float(check_balans[3]) >= float(200):
								q.execute(f"update list_bot set balance ='0' where bot = '{botsname}'")
								connection.commit()
								q.execute("INSERT INTO vivod (bot,user,method,summa,rekvizit,status) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')"%(botsname,message.chat.id,method,check_balans[3],message.text,'WAIT'))
								connection.commit()
								keyboard = types.InlineKeyboardMarkup()
								q.execute(f"SELECT MAX(id) FROM vivod")
								maxid = q.fetchone()[0]
								keyboard.add(types.InlineKeyboardButton(text='🔓 Статус выплаты',callback_data=f'Узнатьстатус {maxid}'))
								bot.send_message(-1001695154512, f'''<b>✅ Новая выплата:</b>
<b>├Пользователь:</b> <code>{message.chat.id}</code>
<b>└Сумма:</b> <code>{check_balans[3]} RUB</code>
<b>бот:</b> <code>{botsname}</code>
''', parse_mode='HTML', reply_markup=keyboard)
								bot.send_message(message.chat.id, '''<b>⏳ Выплата успешно заказана, ожидайте перевод !</b>''',reply_markup=keyboards.main, parse_mode='HTML')
							else:
								bot.send_message(message.chat.id, '''<b>✖️ Минимальная сумма вывода на карту 200 RUB.</b>''',reply_markup=keyboards.main, parse_mode='HTML')	
						else:
							q.execute(f"update list_bot set balance ='0' where bot = '{botsname}'")
							connection.commit()
							q.execute("INSERT INTO vivod (bot,user,method,summa,rekvizit,status) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')"%(botsname,message.chat.id,method,check_balans[3],message.text,'WAIT'))
							connection.commit()
							add_ref_balance(message.chat.id,check_balans[3])
							keyboard = types.InlineKeyboardMarkup()
							q.execute(f"SELECT MAX(id) FROM vivod")
							maxid = q.fetchone()[0]
							keyboard.add(types.InlineKeyboardButton(text='🔓 Статус выплаты',callback_data=f'Узнатьстатус {maxid}'))
							bot.send_message(-1001695154512, f'''<b>✅ Новая выплата:</b>
<b>├Пользователь:</b> <code>{message.chat.id}</code>
<b>└Сумма:</b> <code>{check_balans[3]} RUB</code>
<b>бот:</b> <code>{botsname}</code>''', parse_mode='HTML', reply_markup=keyboard)
							bot.send_message(message.chat.id, '''<b>⏳ Выплата успешно заказана, ожидайте перевод !</b>''',reply_markup=keyboards.main, parse_mode='HTML')
					else:
						bot.send_message(message.chat.id, '''<b>✖️ Минимальная сумма вывода 10 RUB.</b>''',reply_markup=keyboards.main, parse_mode='HTML')	
				else:
					q.execute(f'SELECT * FROM ugc_users WHERE id = "{message.chat.id}" and bot = "{bot_name}"')
					balancesref = q.fetchone()
					if str(balancesref[3]) >= str(10):
						if str(method) == str('CARD'):
							if str(balancesref[3]) >= str(200):
								q.execute(f"update ugc_users set balance ='0' where id = '{message.chat.id}' and bot = '{bot_name}'")
								connection.commit()
								q.execute("INSERT INTO vivod (bot,user,method,summa,rekvizit,status) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')"%('Реферальный баланс',message.chat.id,method,balancesref[1],message.text,'WAIT'))
								connection.commit()
								keyboard = types.InlineKeyboardMarkup()
								q.execute(f"SELECT MAX(id) FROM vivod")
								maxid = q.fetchone()[0]
								keyboard.add(types.InlineKeyboardButton(text='🔓 Статус выплаты',callback_data=f'Узнатьстатус {maxid}'))
								bot.send_message(-1001695154512, f'''<b>✅ Новая выплата:</b>
<b>├Пользователь:</b> <code>{message.chat.id}</code>
<b>└Сумма:</b> <code>{balancesref[3]} RUB</code>
<b>бот:</b> <code>{botsname}</code>''', parse_mode='HTML', reply_markup=keyboard)
								bot.send_message(message.chat.id, '''<b>⏳ Выплата успешно заказана, ожидайте перевод !</b>''',reply_markup=keyboards.main, parse_mode='HTML')
							else:
								bot.send_message(message.chat.id, '''<b>✖️ Минимальная сумма вывода на карту 200 RUB.</b>''',reply_markup=keyboards.main, parse_mode='HTML')	
						else:
							q.execute(f"update ugc_users set balance ='0' where id = '{message.chat.id}' and bot = '{bot_name}'")
							connection.commit()
							q.execute("INSERT INTO vivod (bot,user,method,summa,rekvizit,status) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')"%('Реферальный баланс',message.chat.id,method,balancesref[1],message.text,'WAIT'))
							connection.commit()
							keyboard = types.InlineKeyboardMarkup()
							q.execute(f"SELECT MAX(id) FROM vivod")
							maxid = q.fetchone()[0]
							keyboard.add(types.InlineKeyboardButton(text='🔓 Статус выплаты',callback_data=f'Узнатьстатус {maxid}'))
							bot.send_message(-1001695154512, f'''<b>✅ Новая выплата:</b>
<b>├Пользователь:</b> <code>{message.chat.id}</code>
<b>└Сумма:</b> <code>{balancesref[3]} RUB</code>
<b>бот:</b> <code>{botsname}</code>''', parse_mode='HTML', reply_markup=keyboard)
							bot.send_message(message.chat.id, '''<b>⏳ Выплата успешно заказана, ожидайте перевод !</b>''',reply_markup=keyboards.main, parse_mode='HTML')
					else:
						bot.send_message(message.chat.id, '''<b>✖️ Минимальная сумма вывода 10 RUB.</b>''',reply_markup=keyboards.main, parse_mode='HTML')
		else:
			bot.send_message(message.chat.id, '<b>📛 Неверно указаны реквизиты.</b>', parse_mode='HTML',reply_markup=keyboards.main)
	else:
		bot.send_message(message.chat.id, '✖️ Вернулись на главную',reply_markup=keyboards.main)

def supportadd(message,msg_id):
	try:
		if message.text != 'Отмена':
			connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
			q = connection.cursor()
			q.execute("INSERT INTO support (user,text,status,bot) VALUES ('%s', '%s', '%s', '%s')"%(message.chat.id,message.text,'2',bot_name))
			connection.commit()
			bot.send_message(message.chat.id, '''<b>✔️ Сообщение успешно отправлено в поддержку.</b>''', parse_mode='HTML', reply_markup=keyboards.main)
		else:
			bot.send_message(message.chat.id, '<b>✖️ Вернулись на главную</b>', parse_mode='HTML',reply_markup=keyboards.main)
	except:
		bot.send_message(message.chat.id, f'''<b>✖️ Ошибка</b>''',parse_mode='HTML',reply_markup=keyboards.main)

def add_proxi(message,akkss,msg_id):
	if message.text != 'Отмена':
		try:
			proxi = message.text
			login_prox = proxi.split('@')[0].split(':')[0]
			pass_prox = proxi.split('@')[0].split(':')[1]
			ip_prox = proxi.split('@')[1].split(':')[0]
			port_prox = proxi.split('@')[1].split(':')[1]
			connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_avtopost)
			q = connection.cursor()
			q.execute(f"update akk set proxi = '{proxi}' where id = '{akkss}'")
			connection.commit()
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'список {akkss}'))
			bot.send_message(message.chat.id,F'''✔️ Успешно сменили прокси.''',parse_mode='HTML', reply_markup=keyboard)
		except Exception as e:
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'список {akkss}'))
			bot.send_message(message.chat.id,f'✖️ Ошибка формата',parse_mode='HTML', reply_markup=keyboard)
	else:
		keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'список {akkss}'))
		bot.send_message(message.chat.id, '✔️ Вернулись на главную',reply_markup=keyboard)

def addchanels(message,botsnames,msg_id):
	if message.text != 'Отмена':
		if message.forward_from_chat != None:
			try:
				connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
				q = connection.cursor()
				invite_link =  bot.create_chat_invite_link(chat_id = message.forward_from_chat.id, member_limit = 1).invite_link
				q.execute(f'SELECT chanel_id FROM chanel WHERE bot = "{botsnames}"')
				srow = q.fetchone()
				if srow != None:
					q.execute(f"update chanel set chanel_id ='{message.forward_from_chat.id}' where bot = '{botsnames}'")
					connection.commit()
				else:
					q.execute("INSERT INTO chanel (chanel_id,bot) VALUES ('%s', '%s')"%(message.forward_from_chat.id,botsnames))
					connection.commit()
				bot.send_message(message.chat.id, '''✔️ Канал успешно добавлен''',reply_markup=keyboards.main, parse_mode='HTML')
			except ApiTelegramException as e:
				bot.send_message(message.chat.id, f'''✖️ Ошибка 
# Слито в end_soft: <code>{e.result_json["description"]}</code>''',reply_markup=keyboards.main, parse_mode='HTML')	
		else:
			bot.send_message(message.chat.id, '''✖️ Ошибка 
# Слито в end_soft: <code>Вы не переслали сообщение из канала</code>''',reply_markup=keyboards.main, parse_mode='HTML')	
	else:
		bot.send_message(message.chat.id, '✖️ Вернулись на главную',reply_markup=keyboards.main)

def new_data(message,smena,idchats,idakk):
	keyboard = types.InlineKeyboardMarkup()
	keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'список {idakk}'))
	if message.text != 'Отмена':
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_avtopost)
		q = connection.cursor()
		if str(smena) == 'hold':
			try:
				if int(message.text) >= int(10):
					date = datetime.today() + timedelta(minutes=int(message.text))
					date = date.strftime("%H:%M")
					q.execute(f"update list_chat set {str(smena)} = '{message.text}' where id = '{idchats}'")
					connection.commit()
					q.execute(f"update list_chat set data = '{date}' where id = '{idchats}'")
					connection.commit()
					bot.send_message(message.chat.id, '✔️ Значение успешно изменено.',parse_mode='HTML', reply_markup=keyboard)
				else:
					bot.send_message(message.chat.id, '✖️ Ошибка, минимальное время задержки 10 минут.',parse_mode='HTML', reply_markup=keyboard)
			except:
				bot.send_message(message.chat.id, '✖️ Ошибка, минимальное время задержки 10 минут.',parse_mode='HTML', reply_markup=keyboard)
		else:
			q.execute(f"update list_chat set {str(smena)} = '{message.text}' where id = '{idchats}'")
			connection.commit()
			bot.send_message(message.chat.id, '✔️ Значение успешно изменено.',parse_mode='HTML', reply_markup=keyboard)
	else:
		bot.send_message(message.chat.id, '✖️ Отменили.',parse_mode='HTML', reply_markup=keyboard)

def addcategor(message,idbots):
	if message.text != 'Отмена':
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute("INSERT INTO categor (name,bot) VALUES ('%s','%s')"%(message.text,idbots))
		connection.commit()
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'Магазин {idbots}'))
		bot.send_message(message.chat.id, f'''✔️ Категория успешно добавлена.''', reply_markup=keyboard)
	else:
		bot.send_message(message.chat.id, '✖️ Вернулись на главную', reply_markup=keyboards.main)

def addtovar(message,categor):
	if message.text != 'Отмена':
		msg = bot.send_message(message.chat.id, '''<b>✍️ Укажите 
# Слито в end_soft товара:</b>''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, addtovar1, categor, message.text)
	else:
		bot.send_message(message.chat.id, '✖️ Вернулись на главную', reply_markup=keyboards.main)
def reviews(message):
	if message.text != 'Отмена':
		bot.send_message(-1001660417215, f'''<b>💌 Новый отзыв:</b>
<b>├Пользователь:</b> @{message.from_user.username}
<b>└Текст:</b> <code>{message.text}</code>''',parse_mode='HTML')
		bot.send_message(message.chat.id, '''<b> ❤️ Спасибо за ваш отзыв, нам очень приятно.</b>''',parse_mode='HTML', reply_markup=keyboards.main)
	else:
		bot.send_message(message.chat.id, '✖️ Вернулись на главную', reply_markup=keyboards.main)

def addtovar1(message,categor,name):
	if message.text != 'Отмена':
		msg = bot.send_message(message.chat.id, '''<b>✍️ Укажите 
# Слито в end_soft для товара (От 5р):</b>''', parse_mode='HTML', reply_markup=keyboards.main)
		bot.register_next_step_handler(msg, addtovar2, categor, name, message.text)
	else:
		bot.send_message(message.chat.id, '✖️ Вернулись на главную', reply_markup=keyboards.main)

def addtovar2(message,categor,name,info):
	if message.text != 'Отмена':
		msg = bot.send_message(message.chat.id, '''<b>✍️ Отправьте TXT файл с товарами (каждый с новой строки):</b>''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, addtovar3, categor, name, info, message.text)
	else:
		bot.send_message(message.chat.id, '✖️ Вернулись на главную', reply_markup=keyboards.main)

def addtovar3(message,categor,name,info,prace):
	if message.text != 'Отмена':
		try:
			msg = bot.send_message(message.chat.id, f'''⏳ Добавляем.......''', reply_markup=keyboards.main)
			bot.delete_message(message.from_user.id,msg.message_id)
			try:
				if int(prace) >= 5:
					connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
					q = connection.cursor()
					save_dir = os.getcwd()
					file_name = message.document.file_name
					file_id = message.document.file_name
					file_id_info = bot.get_file(message.document.file_id)
					downloaded_file = bot.download_file(file_id_info.file_path)
					src = generator_pw()
					src = f'{src}.txt'
					with open(save_dir + "/tovar/" + src, 'wb') as new_file:
						new_file.write(downloaded_file)
					q.execute("INSERT INTO tovar (name,info,prace,categor,files,status) VALUES ('%s','%s','%s','%s','%s','%s')"%(name,info,prace,categor,src,'WAIT'))
					connection.commit()	
					keyboard = types.InlineKeyboardMarkup()
					keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'бот'))
					bot.send_message(message.chat.id, f'''✔️ Товар отправлен на модерацию и будет добавлен в течений 24 часов.''', reply_markup=keyboard)
					keyboard = types.InlineKeyboardMarkup()
					keyboard.add(types.InlineKeyboardButton(text='✅ Одобрить', callback_data=f'Одобрить {src} {message.chat.id}'))
					keyboard.add(types.InlineKeyboardButton(text='❌ Отклонить', callback_data=f'Отклонить {src} {message.chat.id}'))
					doc = open(save_dir + "/tovar/" + src, 'rb')
					q.execute(f'SELECT * FROM categor WHERE id = "{categor}"')
					srow = q.fetchone()
					bot.send_document(-1001799352145, doc, caption=f''' Название: {name}
	Описание: {info}

	Категория: {srow[1]}
	Цена: {prace}
	Пользователь: {message.chat.id}
	Бот: @{srow[2]}''',reply_markup=keyboard)
					doc.close()

				else:
					keyboard = types.InlineKeyboardMarkup()
					keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'бот'))
					bot.send_message(message.chat.id, f'''✖️ Ошибка добавления, попробуйте по новой.''', reply_markup=keyboard)
			except Exception as e:
				print(e)
		except:
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'бот'))
			bot.send_message(message.chat.id, f'''✖️ Ошибка добавления, попробуйте по новой.''', reply_markup=keyboard)
	else:
		bot.send_message(message.chat.id, '✖️ Вернулись на главную', reply_markup=keyboards.main)

def btc_oplata_2(message):
		try:
			if int(message.text) >= int(1):
				connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
				q = connection.cursor()
				key_pay = '08c92cac45de169773b42104f0f69ea2'
				id_payss = '1054'
				id_pay = generator_pw()
				awfawf = f"{message.text}|{id_pay}|{id_payss}|RUB|@{bot_name}:{message.chat.id}|{key_pay}"
				hash = hashlib.md5(awfawf.encode("utf-8")).hexdigest()
				url = f'https://payok.io/pay?amount={message.text}&payment={id_pay}&shop={id_payss}&desc=@{bot_name}:{message.chat.id}&sign={hash}'
				q.execute("INSERT INTO pay_ok (user,id_pay) VALUES ('%s', '%s')"%(message.chat.id,id_pay))
				connection.commit()
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text=f'''↗️ Перейти к оплате ''',url=url))
				keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'Кабинет '))
				bot.send_message(message.chat.id, '''❗️ Для пополнения баланса, перейдите по ссылке  ниже и оплатите счет удобным способом !

💡 После оплаты, вы получите уведомление о зачисление средств на баланс.''', reply_markup=keyboard)
			else:
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'профиль '))
				bot.send_message(message.chat.id, f'❗️ Минимальная сумма пополнения 10 RUB',parse_mode='HTML', reply_markup=keyboards.main)
		except:
			bot.send_message(message.chat.id, f'❗️ Минимальная сумма пополнения 10 RUB',parse_mode='HTML', reply_markup=keyboards.main)

@bot.callback_query_handler(func=lambda call: True)
def handler_call(call):
	a = call.data.split()

	if a[0] == 'Одобрить':
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"update tovar set status = 'DONE' where files = '{a[1]}'")
		connection.commit()
		print(call.message.message_id)
		text = f'''{call.message.caption}
✅ Товар одобрен'''
		bot.edit_message_caption(chat_id=-1001799352145, message_id=call.message.message_id, caption=text, parse_mode='HTML')
		q.execute(f"SELECT name FROM tovar where files = '{a[1]}'")
		namename = q.fetchone()[0]
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='✖️ Закрыть',callback_data=f'Закрыть '))
		try:
			bot.send_message(a[2], f'''✅ {namename} успешно проверен и появился на витрине.''',parse_mode='HTML', reply_markup=keyboard)
		except Exception as e:
			pass

	if a[0] == 'check_opl':
		name = 'jopa'
		secret = '7a4ca73baf7bcb4f042d59c14e893ba158155fde'
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"SELECT id_pay FROM pay_ok where user = '{call.message.chat.id}' ORDER BY id DESC LIMIT 1")
		zalupa = q.fetchone()[0]
		url = urllib.request.urlopen(f'https://api.crystalpay.ru/v1/?s={secret}&n={name}&o=receipt-check&i={zalupa}').read()
		result = json.loads(url.decode('utf8'))
		summ = (result['state'])
		summa = (result['payamount'])
		if summ == "payed":
			q.execute(f"update ugc_users set balance = balance + '{summa}' where id = '{call.message.chat.id}'")
			connection.commit()
			q.execute(f"update pay_ok set id_pay = 'paued' where user = '{call.message.chat.id}' ORDER BY id DESC LIMIT 1")
			connection.commit()
			bot.send_message(call.message.chat.id, f'Успешное пополнение: {summa} RUB')
		else: 
			bot.send_message(call.message.chat.id, 'Вы еще не оплатили')

	if a[0] == 'check_opl2':
		api_key = 'F9F332866876657CF1CEF31E57F7E5DC-DBE2A835B23C5C1B965647C16C7DF76A-2188E143B43F3FC90765E400188BCE13'
		id_pays = '380'
		magaz = '1054'
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"SELECT id_pay FROM pay_ok where user = '{call.message.chat.id}' ORDER BY id DESC LIMIT 1")
		zalupa = q.fetchone()[0]
		try:
			url2 = requests.post(url='https://payok.io/api/transaction', data={'API_ID': id_pays, 'API_KEY': api_key, 'shop': magaz, 'payment': zalupa,})
			response_data = url2.json()
			summ = (response_data['status'])
			stat = (response_data['1'])
			result2 = stat.get('amount_profit')
			if summ == "success":
				q.execute(f"update ugc_users set balance = balance + '{result2}' where id = '{call.message.chat.id}'")
				connection.commit()
				q.execute(f"update pay_ok set id_pay = 'paued' where user = '{call.message.chat.id}' ORDER BY id DESC LIMIT 1")
				connection.commit()
				bot.send_message(call.message.chat.id, f'Успешное пополнение:  <b>{result2}</b> RUB',parse_mode='HTML')
			else: 
				bot.send_message(call.message.chat.id, '<b>Ошибка</b>',parse_mode='HTML')
		except:
			bot.send_message(call.message.chat.id, f'<b>Вы еще не оплатили</b>', parse_mode='HTML')


	if a[0] == 'Отклонить':
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='Низкий валид товара',callback_data=f'Отклон {a[1]} {a[2]} 1'))
		keyboard.add(types.InlineKeyboardButton(text='Запрещенный контент',callback_data=f'Отклон {a[1]} {a[2]} 2'))
		keyboard.add(types.InlineKeyboardButton(text='Без комментариев',callback_data=f'Отклон {a[1]} {a[2]} 3'))
		keyboard.add(types.InlineKeyboardButton(text='Съебал нахуй отсюда',callback_data=f'Отклон {a[1]} {a[2]} 4'))
		bot.edit_message_reply_markup(chat_id=-1001799352145, message_id=call.message.message_id, reply_markup=keyboard)
	
	if a[0] == 'Отклон':
		global infos
		infos = 'Без комментариев'
		if int(a[3]) == int(1):
			infos = 'Низкий валид товара'
		if int(a[3]) == int(2):
			infos = 'Запрещенный контент'
		if int(a[3]) == int(3):
			infos == 'Без комментариев'
		if int(a[3]) == int(4):
			infos = 'Съебал нахуй отсюда'
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"SELECT name FROM tovar where files = '{a[1]}'")
		namename = q.fetchone()[0]
		q.execute(f"DELETE FROM tovar where files = '{a[1]}'")
		connection.commit()
		text = f'''{call.message.caption}

✖️ Товар отклонен'''
		bot.edit_message_text(chat_id=-1001799352145, message_id=call.message.message_id, caption=text, parse_mode='HTML')
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='✖️ Закрыть',callback_data=f'Закрыть '))
		try:
			bot.send_message(a[2], f'''✖️ {namename} отклонен с пометкой: {infos}.''',parse_mode='HTML', reply_markup=keyboard)
		except Exception as e:
			pass

		
	if a[0] == 'бот':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"SELECT * FROM list_bot where user = '{call.message.chat.id}' ORDER BY id DESC LIMIT 1")
		rows = q.fetchone()
		try:
			if str(rows[8]) != str('Заблокирован'):
				tomorrow = datetime.now()
				data = tomorrow.strftime('%d/%m/%Y')
				q.execute(f"SELECT COUNT(id) FROM ugc_users where bot = '{rows[6]}'")
				user_count = q.fetchone()[0]
				q.execute(f"SELECT COUNT(id) FROM ugc_users where bot = '{rows[6]}' and data = '{data}'")
				user_count_data = q.fetchone()[0]
				q.execute(f"SELECT COUNT(id) FROM list_zakaz where bot = '{rows[6]}'")
				zakaz_count = q.fetchone()[0]
				q.execute(f"SELECT COUNT(id) FROM list_zakaz where data = '{data}' and  bot = '{rows[6]}'")
				zakaz_count_data1 = q.fetchone()[0]
				q.execute(f"SELECT data FROM list_zakaz where bot = '{rows[6]}' ORDER BY id DESC LIMIT 1")
				try:
					oldzakaz = q.fetchone()[0]
				except Exception as e:
					oldzakaz = 'Нет'
				q.execute(f"SELECT COUNT(id) FROM support where bot = '{rows[6]}' and status = '1'")
				support_count = q.fetchone()[0]
				status = "🔴 Выключить" if rows[8] == "Работает" else "🟢 Включить"
				q.execute(f"SELECT COUNT(id) FROM support where bot = '{rows[6]}' and status = '1'")
				support_count = q.fetchone()[0]
				status = "🔴 Выключить" if rows[8] == "Работает" else "🟢 Включить"
				q.execute(f'SELECT chanel_id FROM chanel WHERE bot = "{rows[6].lower()}"')
				chanel_id = q.fetchone()
				if chanel_id != None:
					chanel_id = 'Активен'
				else:
					chanel_id = 'Нет'
				q.execute(f"SELECT COUNT(id) FROM list_aktiv where bot = '{rows[6]}' and code != 'Нет'")
				sms_count = q.fetchone()[0]
				if sms_count == None:
					sms_count = 0
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='🔎 Поиск пользователя',callback_data=f'Поиск {rows[0]}'))
				#types.InlineKeyboardButton(text='💬 Рассылка',url=f'https://t.me/{rows[6]}?start=sendall'),
				keyboard.add(types.InlineKeyboardButton(text=f'📨 Поддержка ({support_count})',callback_data=f'Поддержка {rows[6]}'),types.InlineKeyboardButton(text='📈 Последние заказы',callback_data=f'заказы {rows[6]}'))
				keyboard.add(types.InlineKeyboardButton(text='💸 Сменить наценку',callback_data=f'Наценка {rows[0]}'),types.InlineKeyboardButton(text=f'🔧 Настройки',callback_data=f'Настройки {rows[6]}'))
				#keyboard.add(types.InlineKeyboardButton(text='Премиум',callback_data=f'Премиум'))
				#,types.InlineKeyboardButton(text='🛍 Магазин',callback_data=f'Магазин {rows[6]}')
				#keyboard.add(types.InlineKeyboardButton(text='🎛 Редактор меню',callback_data=f'Редакторменю {rows[6]}'))
				#keyboard.add(types.InlineKeyboardButton(text='📢 Добавить канал',callback_data=f'Добавитьканал {rows[6]}'))
				keyboard.add(types.InlineKeyboardButton(text='🛍 Магазин',callback_data=f'Магазин {rows[6]}'))
				
				bot.send_message(call.message.chat.id, f'''<b>ℹ️ Информация:</b>
<b>├Бот:</b> @{rows[6]}	
<b>├Всего пользователей:</b> <code>{user_count}</code>
<b>├Новые пользователи:</b> <code>{user_count_data}</code>
<b>└Канал для подписки:</b> <code>{chanel_id}</code>

<b>📊 Статистика накрутки:</b>
<b>├Заказов:</b> <code>{zakaz_count} шт</code>
<b>├Заказов за сегодня :</b> <code>{zakaz_count_data1} шт</code>
<b>├Последний заказ:</b> <code>{oldzakaz}</code>
<b>└Наценка:</b> <code>{rows[5]} %</code>

<b>📊 Статистика смс:</b>
<b>├Принято смс:</b> <code>{sms_count} шт</code>
<b>└Наценка:</b> <code>{rows[14]} RUB</code>

<b>🏦Доходность:</b>
<b>└Прибыль:</b> <code>{rows[10]} RUB</code>''',parse_mode='HTML', reply_markup=keyboard)
			else:
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='🔧 Разблокировать',callback_data=f'Разблокировать {rows[0]} {rows[6]}'))
				keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'бот '))	
				bot.send_message(call.message.chat.id, f'''<b>ℹ️ Информация:</b>
<b>├Бот:</b> @{rows[6]}	
<b>├Дата удаления:</b> <code>{rows[9]}</code>
<b>└Статус:</b> <code>{rows[8]}</code>
''',parse_mode='HTML', reply_markup=keyboard)

		except:
			pass

	if a[0] == 'bot_':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		try:
			connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
			q = connection.cursor()
			q.execute(f"SELECT * FROM list_bot where id = '{a[1]}'")
			rows = q.fetchone()
			if str(rows[8]) != str('Заблокирован'):
				tomorrow = datetime.now()
				data = tomorrow.strftime('%d/%m/%Y')
				q.execute(f"SELECT COUNT(id) FROM ugc_users where bot = '{rows[6]}'")
				user_count = q.fetchone()[0]
				q.execute(f"SELECT COUNT(id) FROM ugc_users where bot = '{rows[6]}' and data = '{data}'")
				user_count_data = q.fetchone()[0]
				q.execute(f"SELECT COUNT(id) FROM list_zakaz where bot = '{rows[6]}'")
				zakaz_count = q.fetchone()[0]
				q.execute(f"SELECT COUNT(id) FROM list_zakaz where data = '{data}' and  bot = '{rows[6]}'")
				zakaz_count_data1 = q.fetchone()[0]
				q.execute(f"SELECT data FROM list_zakaz where bot = '{rows[6]}' ORDER BY id DESC LIMIT 1")
				try:
					oldzakaz = q.fetchone()[0]
				except Exception as e:
					oldzakaz = 'Нет'
				q.execute(f"SELECT COUNT(id) FROM support where bot = '{rows[6]}' and status = '1'")
				support_count = q.fetchone()[0]
				status = "🔴 Выключить" if rows[8] == "Работает" else "🟢 Включить"
				q.execute(f'SELECT chanel_id FROM chanel WHERE bot = "{rows[6].lower()}"')
				chanel_id = q.fetchone()
				if chanel_id != None:
					chanel_id = 'Активен'
				else:
					chanel_id = 'Нет'

				q.execute(f"SELECT COUNT(id) FROM list_aktiv where bot = '{rows[6]}' and code != 'Нет'")
				sms_count = q.fetchone()[0]
				if sms_count == None:
					sms_count = 0
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='🔎 Поиск пользователя',callback_data=f'Поиск {rows[0]}'))
				#types.InlineKeyboardButton(text='💬 Рассылка',url=f'https://t.me/{rows[6]}?start=sendall'),
				keyboard.add(types.InlineKeyboardButton(text=f'📨 Поддержка ({support_count})',callback_data=f'Поддержка {rows[6]}'),types.InlineKeyboardButton(text='📈 Последние заказы',callback_data=f'заказы {rows[6]}'))
				keyboard.add(types.InlineKeyboardButton(text='💸 Сменить наценку',callback_data=f'Наценка {rows[0]}'),types.InlineKeyboardButton(text=f'🔧 Настройки',callback_data=f'Настройки {rows[6]}'))
				#keyboard.add(types.InlineKeyboardButton(text='Премиум',callback_data=f'Премиум'))
				#keyboard.add(types.InlineKeyboardButton(text='🎛 Редактор меню',callback_data=f'Редакторменю {rows[6]}'))
				#keyboard.add(types.InlineKeyboardButton(text='📢 Добавить канал',callback_data=f'Добавитьканал {rows[6]}'))
				keyboard.add(types.InlineKeyboardButton(text='🛍 Магазин',callback_data=f'Магазин {rows[6]}'))
				
				bot.send_message(call.message.chat.id, f'''<b>ℹ️ Информация:</b>
<b>├Бот:</b> @{rows[6]}	
<b>├Всего пользователей:</b> <code>{user_count}</code>
<b>├Новые пользователи:</b> <code>{user_count_data}</code>
<b>└Канал для подписки:</b> <code>{chanel_id}</code>

<b>📊 Статистика накрутки:</b>
<b>├Заказов:</b> <code>{zakaz_count} шт</code>
<b>├Заказов за сегодня :</b> <code>{zakaz_count_data1} шт</code>
<b>├Последний заказ:</b> <code>{oldzakaz}</code>
<b>└Наценка:</b> <code>{rows[5]} %</code>

<b>📊 Статистика смс:</b>
<b>├Принято смс:</b> <code>{sms_count} шт</code>
<b>└Наценка:</b> <code>{rows[12]} RUB</code>

<b>🏦Доходность:</b>
<b>└Прибыль:</b> <code>{rows[10]} RUB</code>''',parse_mode='HTML', reply_markup=keyboard)
			else:
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='🔧 Разблокировать',callback_data=f'Разблокировать {rows[0]} {rows[6]}'))
				keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'бот '))	
				bot.send_message(call.message.chat.id, f'''<b>ℹ️ Информация:</b>
<b>├Бот:</b> @{rows[6]}	
<b>├Дата удаления:</b> <code>{rows[9]}</code>
<b>└Статус:</b> <code>{rows[8]}</code>
''',parse_mode='HTML', reply_markup=keyboard)

		except:
			pass

	elif a[0] == 'Магазин':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f'SELECT deposit FROM list_bot WHERE bot = "{a[1].lower()}"')
		bot_deposit = q.fetchone()[0]
		if int(bot_deposit) >= 0:
			tomorrow = datetime.now()
			data = tomorrow.strftime('%d/%m/%Y')
			q.execute(f"SELECT COUNT(id) FROM list_zakaz_shop where bot = '{a[1].lower()}'")
			zakaz_count_shop = q.fetchone()[0]
			q.execute(f"SELECT COUNT(id) FROM list_zakaz_shop where data = '{data}' and  bot = '{a[1].lower()}'")
			zakaz_count_data1_shop = q.fetchone()[0]
			q.execute(f"SELECT data FROM list_zakaz_shop where bot = '{a[1].lower()}' ORDER BY id DESC LIMIT 1")
			try:
				oldzakaz_shop = q.fetchone()[0]
			except Exception as e:
				oldzakaz_shop = 'Нет'
			connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
			q = connection.cursor()
			keyboard = types.InlineKeyboardMarkup()
			q.execute(f"SELECT * FROM categor WHERE bot = '{a[1].lower()}'")
			rows = q.fetchall()
			for i in rows:
				keyboard.add(types.InlineKeyboardButton(text=i[1],callback_data=f'Товары {i[0]} {a[1]}'))
			keyboard.add(types.InlineKeyboardButton(text=f'''➕ Добавить категорию''',callback_data=F'Добавитькатегорию {a[1]}'))
			keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=F'бот'))
			bot.send_message(call.message.chat.id,f'''<b>📊 Статистика магазина:</b>
<b>├Покупок:</b> <code>{zakaz_count_shop} шт</code>
<b>├Покупок за сегодня :</b> <code>{zakaz_count_data1_shop} шт</code>
<b>└Последний заказ:</b> <code>{oldzakaz_shop}</code>''', reply_markup=keyboard, parse_mode='HTML')
		else:
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=F'бот'))
			bot.send_message(call.message.chat.id,f'''😕 К сожалению, функция будет  доступна только после внесения безвозвратного депозита в размере 1000 RUB.
Это необходимо, чтобы подтвердить серьёзность ваших намерений и избежать обмана со стороны продавцов.''', reply_markup=keyboard, parse_mode='HTML')

	
	elif a[0] == 'Товары':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		keyboard = types.InlineKeyboardMarkup()
		q.execute(f"SELECT * FROM tovar WHERE categor = '{a[1]}'")
		rows = q.fetchall()
		if len(rows) != 0:
			for i in rows:
				keyboard.add(types.InlineKeyboardButton(text=i[1],callback_data=f'Товар {i[0]} {a[2]}'))

		keyboard.add(types.InlineKeyboardButton(text=f'''➕ Добавить товар''',callback_data=F'Добавитьтовар {a[1]}'))
		keyboard.add(types.InlineKeyboardButton(text=f'''➖ Удалить категорию''',callback_data=F'Удалитькатегорию {a[1]} {a[2]}'))
		keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'Магазин {a[2]}'))
		bot.send_message(call.message.chat.id,'''📜 Выберите товар:''', reply_markup=keyboard, parse_mode='HTML')
	
	if a[0] == 'Товар':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		keyboard = types.InlineKeyboardMarkup()
		q.execute(f"SELECT * FROM tovar WHERE id = '{a[1]}'")
		rows = q.fetchone()
		colvo_rovar = 0 
		with open (f'/root/smm/tovar/{rows[5]}') as f: 
			for line in f: 
				if line != '\n': 
					colvo_rovar += 1
		keyboard.add(types.InlineKeyboardButton(text='🗑 Удалить',callback_data=f'Удалитьтовар {rows[0]} {a[2]}'))
		keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'Магазин {a[2]}'))
		bot.send_message(call.message.chat.id,f'''<b>📦 Товар:</b> {rows[1]}
➖➖➖➖➖➖
<b>📜 Описание:</b>
<code>{rows[2]}</code>
➖➖➖➖➖➖
<b>🗂 Остаток: {colvo_rovar} шт</b>
➖➖➖➖➖➖
<b>💳 Цена за единицу:</b>  <code>{rows[3]}</code> <b>RUB</b>''', reply_markup=keyboard, parse_mode='HTML')


	if a[0] == 'Удалитьтовар':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"DELETE FROM tovar where id = '{a[1]}'")
		connection.commit()
		keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'Магазин {a[2]}'))
		bot.send_message(call.message.chat.id,f'''Товар удален''', reply_markup=keyboard, parse_mode='HTML')
		
	if a[0] == 'Добавитьтовар':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'''↗️ Просмотреть''',url='https://telegra.ph/XAለVA--SMM-FRANCHISE--Navigaciya-po-menyu-04-15 '))
		bot.send_message(call.message.chat.id,'''❗️ Список запрещенных товаров:''', reply_markup=keyboard, parse_mode='HTML')
		msg = bot.send_message(call.message.chat.id, '''<b>✍️ Укажите название товара:</b>''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, addtovar, a[1])

	if a[0] == 'Добавитькатегорию':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		msg = bot.send_message(call.message.chat.id, "<b>✍️ Укажите название категории:</b>",parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, addcategor, a[1])

	if a[0] == 'Удалитькатегорию':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		keyboard = types.InlineKeyboardMarkup()
		q.execute(f"DELETE FROM categor where id = '{a[1]}'")
		connection.commit()
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'Магазин {a[2]}'))	
		bot.send_message(call.message.chat.id, f'''✔️ Готово''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'Премиум':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f'SELECT chanel_id FROM chanel WHERE bot = "{a[1].lower()}"')
		chanel_id = q.fetchone()
		if chanel_id != None:
			chanel_id = 'Активен'
		else:
			chanel_id = 'Нет'
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='🎛 Редактор меню',callback_data=f'Редакторменю {a[1]}'),types.InlineKeyboardButton(text='🛍 Магазин',callback_data=f'разработке '))
		keyboard.add(types.InlineKeyboardButton(text='📢 Добавить канал',callback_data=f'Добавитьканал {a[1]}'))
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'бот '))	
		bot.send_message(call.message.chat.id, f'''<b>ℹ️ Информация:</b>
<b>├Подписка до:</b> <code>Безлимит</code>
<b>├Режим магазина:</b> <code>В разработке</code>
<b>└Канал для подписки:</b> <code>{chanel_id}</code>''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'Редакторменю':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"SELECT * FROM keyboards where bot = '{a[1]}'")
		row = q.fetchall()
		keyboard = types.InlineKeyboardMarkup()
		for i in row:
			keyboard.add(types.InlineKeyboardButton(text=i[1],callback_data=f'кнопка {i[0]} {a[1]}'))
		keyboard.add(types.InlineKeyboardButton(text='➕ Добавить кнопку',callback_data=f'Добавитькнопку {a[1]}'))	
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'бот '))	
		bot.send_message(call.message.chat.id, f'''▪️ Выберите нужную кнопку или добавьте новую:''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'кнопка':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"SELECT * FROM keyboards where id = '{a[1]}'")
		row = q.fetchone()
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='➖ Удалить',callback_data=f'Удалитькнопку {row[0]} {a[2]}'))	
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'Редакторменю {a[2]}'))	
		bot.send_message(call.message.chat.id, row[2],parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'Удалитькнопку':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		keyboard = types.InlineKeyboardMarkup()
		q.execute(f"DELETE FROM keyboards where id = '{a[1]}'")
		connection.commit()
		cmd1 = f'systemctl restart {a[2]}'
		subprocess.Popen(cmd1, shell=True)
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'бот '))	
		bot.send_message(call.message.chat.id, f'''✔️ Готово''',parse_mode='HTML', reply_markup=keyboard)
			
	if a[0] == 'Добавитькнопку':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		msg = bot.send_message(call.message.chat.id, "<b>✍️ Укажите название кнопки:</b>",parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, addkeyboards, a[1])

	if a[0] == 'Узнатьстатус':
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"SELECT status FROM vivod where id = '{a[1]}'")
		status = q.fetchone()[0]
		bot.answer_callback_query(callback_query_id=call.id,show_alert=True, text=status)
		
	if a[0] == 'Разблокировать':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		tomorrow = datetime.now()
		data = tomorrow.strftime('%d/%m/%Y')
		q.execute(f"update list_bot set status = 'Работает' WHERE id = '{a[1]}'")
		connection.commit()
		q.execute(f"update list_bot set logi = '{data}' WHERE id = '{a[1]}'")
		connection.commit()
		cmd1d = f'systemctl enable {a[2]}'
		subprocess.Popen(cmd1d, shell=True)
		cmd = f'systemctl start {a[2]}'
		subprocess.Popen(cmd, shell=True)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'бот '))	
		bot.send_message(call.message.chat.id, f'''✔️ Готово, бот разблокирован.''',parse_mode='HTML', reply_markup=keyboard)
			
	if a[0] == 'Поиск':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		msg = bot.send_message(call.message.chat.id, "<b>✍️ Укажите id пользователя:</b>",parse_mode='HTML', reply_markup=keyboards.main)
		bot.register_next_step_handler(msg, poisk_user, a[1],msg.message_id)
		
	if a[0] == 'заблокировать_':
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()

		q.execute(f"SELECT status FROM ugc_users where id = '{a[2]}' and bot = '{a[1]}'")
		status = q.fetchone()[0]

		if status == 'Активен':
			q.execute(f"update ugc_users set status = 'Заблокирован' where id = '{a[2]}' and bot = '{a[1]}'")
			connection.commit()
			bot.answer_callback_query(callback_query_id=call.id, text="✅ Заблокирован")
		else:
			q.execute(f"update ugc_users set status = 'Активен' where id = '{a[2]}' and bot = '{a[1]}'")
			connection.commit()
			bot.answer_callback_query(callback_query_id=call.id, text="✅ Разблокирован")



	if a[0] == 'Удалитьбот':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		keyboard = types.InlineKeyboardMarkup()
		q.execute(f"DELETE FROM list_bot where id = '{a[1]}'")
		connection.commit()
		path = os.path.join('/etc/systemd/system/', f'{a[2]}.service')
		os.remove(path)
		shutil.rmtree(f'/root/smm/bot_list/{a[2]}')
		cmd = f'systemctl stop {a[2]}'
		subprocess.Popen(cmd, shell=True)
		cmd1d = f'systemctl disable {a[2]}'
		subprocess.Popen(cmd1d, shell=True)
		cmds = f'systemctl daemon-reload'
		subprocess.Popen(cmds, shell=True)
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'бот '))	
		bot.send_message(call.message.chat.id, f'''✔️ Готово''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'Настройки':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"SELECT * FROM list_bot where bot = '{a[1]}'")
		rowsa = q.fetchone()
		print(rowsa[13])
		if rowsa[13] == 1:
			statussms = 'Работает'
			knopkasms = '🔴 Выключить смс'
		else:
			knopkasms = '🟢 Включить смс'
			statussms = 'Выключен'

		try:
			q.execute(f'SELECT chanel_id FROM chanel WHERE bot = "{rowsa[6]}"')
			chanel_id = q.fetchone()
			if chanel_id != None:
				chanel_id = chanel_id[0]
			else:
				chanel_id = 'Нет'
		except Exception as e:
			chanel_id = 'Нет'
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🌀 Сменить статус' ,callback_data=f'статусбот {rowsa[0]}'),types.InlineKeyboardButton(text='🗑 Удалить бот',callback_data=f'Удалитьбот {rowsa[0]} {a[1]}'))
		#keyboard.add(types.InlineKeyboardButton(text=knopkasms,callback_data=f'статуссмс {rowsa[0]}'))
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'бот '))	
		bot.send_message(call.message.chat.id, f'''<b>📈 Информация:</b>
<b>├Режим смс:</b> <code>{statussms}</code> <b>Временно отключено</b>
<b>└Статус бота:</b> <code>{rowsa[8]}</code>''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'Добавитьканал':
		bot_name = bot.get_me().username
		bot.delete_message(call.message.chat.id,call.message.message_id)
		msg = bot.send_message(call.message.chat.id, f'''<b>📜 Инструкция по добавлению:</b>

1️⃣ Добавьте @{bot_name} в нужный канала и выдайте права:
<b>├</b> Изменение профиля канала.
<b>└</b> Добавление участников.

2️⃣ Перешлите любое сообщение с канала:''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, addchanels, a[1],msg.message_id)

	if a[0] == 'статуссмс':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"SELECT * FROM list_bot where id = '{a[1]}'")
		rows = q.fetchone()
		if rows[13] == 1:
			q.execute(f"update list_bot set sms_status = '0' where id = '{a[1]}'")
			connection.commit()

		else:
			q.execute(f"update list_bot set sms_status = '1' where id = '{a[1]}'")
			connection.commit()
		keyboard = types.InlineKeyboardMarkup()	
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'бот '))	
		bot.send_message(call.message.chat.id, f'''✔️ Готово''',parse_mode='HTML', reply_markup=keyboard)
			
	if a[0] == 'статусбот':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"SELECT * FROM list_bot where id = '{a[1]}'")
		rows = q.fetchone()
		if rows[8] == 'Работает':
			q.execute(f"update list_bot set status = 'Выключен' where id = '{a[1]}'")
			connection.commit()
			cmd = f'systemctl stop {rows[6]}'
			subprocess.Popen(cmd, shell=True)
			cmd1d = f'systemctl disable {rows[6]}'
			subprocess.Popen(cmd1d, shell=True)

		if rows[8] == 'Выключен':
			q.execute(f"update list_bot set status = 'Работает' where id = '{a[1]}'")
			connection.commit()
			cmd1d = f'systemctl enable {rows[6]}'
			subprocess.Popen(cmd1d, shell=True)
			cmd = f'systemctl start {rows[6]}'
			subprocess.Popen(cmd, shell=True)
		keyboard = types.InlineKeyboardMarkup()	
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'бот '))	
		bot.send_message(call.message.chat.id, f'''✔️ Готово''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'Наценка':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		print(a[1])
		if str(a[1]) == 'nakrutka':
			msg = bot.send_message(call.message.chat.id, "✍️<b>Напишите процент на который хотите поднять цену:</b>",parse_mode='HTML', reply_markup=keyboards.main)
			bot.register_next_step_handler(msg, edit_procent, a[2],msg.message_id)

		elif str(a[1]) == 'sms':
			msg = bot.send_message(call.message.chat.id, "✍️<b>Напишите сумму на которую хотите поднять цены на смс:</b>",parse_mode='HTML', reply_markup=keyboards.main)
			bot.register_next_step_handler(msg, edit_sms, a[2],msg.message_id)

		else:
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='📈 Накрутка',callback_data=f'Наценка nakrutka {a[1]}'),types.InlineKeyboardButton(text='📱 Смс',callback_data=f'Наценка sms {a[1]}'))
			keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'бот '))
			bot.send_message(call.message.chat.id, f'''Где будем менять наценку ?''',parse_mode='HTML', reply_markup=keyboard)
		
	if a[0] == 'add_bot':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"SELECT COUNT(id) FROM list_bot where user = '{call.message.chat.id}'")
		botovcolvo = q.fetchone()[0]
		if int(botovcolvo) == 0:
			msg = bot.send_message(call.message.chat.id, '''Чтобы подключить бот, вам нужно выполнить два действия:

1. Перейдите в @BotFather и <a href="https://telegra.ph/Sozdat-bota-01-25">создайте новый бот</a>.
2. После создания бота вы получите токен (12345:6789ABCDEF) — скопируйте и отправьте его в этот чат.

Важно: не подключайте боты, которые уже используются другими сервисами (Controller Bot, разные CRM и т.д.)''',disable_web_page_preview = True,parse_mode='HTML', reply_markup=keyboards.otmena)
			bot.register_next_step_handler(msg, add_bot,msg.message_id)
		else:
			bot.send_message(call.message.chat.id, f'''<b>✖️ Максимально число активных ботов: 1</b>''',parse_mode='HTML', reply_markup=keyboards.main)
	
	if a[0] == 'заказы':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f'SELECT * FROM list_zakaz WHERE bot = "{a[1]}" ORDER BY id DESC LIMIT 5')
		row = q.fetchall()
		text = ''
		for i in row:
			text += f'''
<b>📄 ID:</b> <code>{i[7]}</code>
<b>├Услуга:</b> <code>{i[5]}</code>
<b>├URL:</b> <code>{i[2]}</code>
<b>└Количество:</b> <code>{i[3]}</code>\n'''
		keyboard = types.InlineKeyboardMarkup()	
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'бот '))	
		bot.send_message(call.message.chat.id, f'''<b>📈 Последние заказы:</b>
{text}''',parse_mode='HTML',reply_markup=keyboard)
		
	if a[0] == 'Ответить':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		msg = bot.send_message(call.message.chat.id, f'''✍️ Укажите текст ответа на запрос:''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, support_otvet, a[1],msg.message_id)

	if a[0] == 'Передать':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"update support set status = '2' where id = '{a[1]}'")
		connection.commit()
		keyboard = types.InlineKeyboardMarkup()	
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'бот '))	
		bot.send_message(call.message.chat.id, f'''✔️ Готово, вопрос передан администрации.''',parse_mode='HTML', reply_markup=keyboard)
			

	if a[0] == 'Поддержка':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"SELECT * FROM support where bot = '{a[1]}' and status = '1' ORDER BY id DESC LIMIT 1")
		rows = q.fetchone()
		if rows != None:
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='💬 Ответить',callback_data=f'Ответить {rows[0]}'),types.InlineKeyboardButton(text='↗️ Передать админу',callback_data=f'Передать {rows[0]}'))
			keyboard.add(types.InlineKeyboardButton(text=f'📜 История запросов',callback_data=f'История {rows[1]} {a[1]}'))
			keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'бот '))
			bot.send_message(call.message.chat.id, f'''<b>ℹ️ Пользователь:</b> <code>{rows[1]}</code>
<b>└Вопрос:</b> <code>{rows[2]}</code>''',parse_mode='HTML', reply_markup=keyboard)
		else:
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'бот '))
			bot.send_message(call.message.chat.id, f'''😊 Запросы в поддержку отсутствуют.''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'История':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"SELECT * FROM support where user = '{a[1]}'")
		row = q.fetchall()
		text = ''
		for i in row:
			text += f'<b>├▪️:</b> <code>{i[2]}</code>\n'

		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Поддержка {a[2]}'))
		bot.send_message(call.message.chat.id, f'''<b>ℹ️ Последние запросы пользователя:</b>
{text}<b>└Количество:</b> <code>{len(row)}</code>''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'awhat_oplata':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'''▪️ Qiwi\CARD''',callback_data='add_depozit2'))
		keyboard.add(types.InlineKeyboardButton(text=f'''▪️ LZT market''',callback_data='add_depozit'),types.InlineKeyboardButton(text=f'''▪️ Crypto''',callback_data='add_depozit'))
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'Кабинет '))
		bot.send_message(call.message.chat.id, f'''📥 Выберите способ для пополнения баланса:''',parse_mode='HTML', reply_markup=keyboard)
	
	if a[0] == 'add_depozit':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id,'''✍️ Укажите сумму пополнения:''', parse_mode='HTML')
		bot.register_next_step_handler(msg, btc_oplata_1)

	if a[0] == 'add_depozit2':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id,'''✍️ Укажите сумму пополнения:''', parse_mode='HTML')
		bot.register_next_step_handler(msg, btc_oplata_2)
	
	if a[0] == 'Кабинет':
			bot_name = 'EasyBotsFranchise_bot'
			bot.delete_message(call.message.chat.id,call.message.message_id)
			connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
			q = connection.cursor()
			q.execute(f"SELECT COUNT(id) FROM list_bot where user = '{call.message.chat.id}'")
			botov = q.fetchone()[0]

			q.execute(f"SELECT SUM(dohod) FROM list_bot where user = '{call.message.chat.id}'")
			dohod = q.fetchone()[0]
			print(dohod)
			if dohod == None:
				dohod = 0
			q.execute(f"SELECT SUM(balance) FROM list_bot where user = '{call.message.chat.id}'")
			balance = q.fetchone()[0]
			if balance == None:
				balance = 0
			print(balance)
			q.execute(f'SELECT * FROM ugc_users WHERE id = "{call.message.chat.id}" and bot = "{bot_name}"')
			rowsss = q.fetchone()
			keyboard = types.InlineKeyboardMarkup()	
			keyboard.add(types.InlineKeyboardButton(text='📤 Вывести',callback_data=f'Вывод '),types.InlineKeyboardButton(text='📥 Пополнить',callback_data=f'awhat_oplata'))		
			keyboard.add(types.InlineKeyboardButton(text='🎁 Создать промо',callback_data=f'Промо '))
			keyboard.add(types.InlineKeyboardButton(text='🫂 Реферальная программа',callback_data=f'Реферальная '))		
			bot.send_message(call.message.chat.id, f'''<b>🎩 Личные данные:</b>
<b>├ID:</b> <code>{call.message.chat.id}</code>
<b>├UN:</b> <code>{call.message.chat.username}</code>
<b>├Баланс:</b> <code>{rowsss[6]} RUB</code>
<b>└Ботов:</b> <code>{botov}</code>

<b>🤖 Информация по ботам:
├Доход:</b> <code>{dohod} RUB</code>
<b>└Баланс:</b> <code>{balance} RUB</code>''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'Топботов':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		text = f"<b>🏆Топ партнеров по доходу:\n</b>"
		q.execute(f'SELECT * FROM list_bot ORDER BY dohod DESC')
		rows = q.fetchall()
		premium = ['🥇', '🥈', '🥉', '🏅', '🏅']
		l = len(rows)
		if l > 5:
			l = 5
		for i in range(l):
			if i <= len(premium)-1:
				userid = int(rows[i][0])
				text += f"{premium[i]}{i+1}) @{rows[i][6]} | {rows[i][10]} RUB\n"
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'Кабинет'))
		bot.send_message(call.message.chat.id, f'''{text}''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'Вывод':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"SELECT * FROM list_bot where user = '{call.message.chat.id}'")
		list_bot = q.fetchall()
		keyboard = types.InlineKeyboardMarkup()
		for i in list_bot:
			keyboard.add(types.InlineKeyboardButton(text=f'{i[2]} | {i[3]} RUB',callback_data=f'Вывести {i[6]}'))
		keyboard.add(types.InlineKeyboardButton(text=f'Внутренний баланс',callback_data=f'Вывести referal'))
		bot.send_message(call.message.chat.id, f'''<b>📤  Вывод средств:
└Выберите бот для вывода:</b>''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'Промо':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"SELECT * FROM list_bot where user = '{call.message.chat.id}'")
		list_bot = q.fetchall()
		keyboard = types.InlineKeyboardMarkup()
		for i in list_bot:
			keyboard.add(types.InlineKeyboardButton(text=f'{i[2]} | {i[3]} RUB',callback_data=f'Промокод {i[6]}'))
		keyboard.add(types.InlineKeyboardButton(text=f'Внутренний баланс',callback_data=f'Промокод referal'))	
		bot.send_message(call.message.chat.id, f'''<b>🎁 Создание промокода:
└Выберите бот для списания баланса:</b>''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'Промокод':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		msg = bot.send_message(call.message.chat.id, f'''✍️ <b>Укажите сумму промокода:</b>''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, addpromo, a[1])
			
	if a[0] == 'Вывести':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='🥝 QIWI',callback_data=f'Реквизитывывод {a[1]} QIWI'),types.InlineKeyboardButton(text='💳 CARD',callback_data=f'Реквизитывывод {a[1]} CARD'))
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'💼 Профиль'))
		bot.send_message(call.message.chat.id, '''<b>📜 Информация:
├Qiwi: <code>Моментально</code> от 10 RUB
├Card: <code>Моментально</code> от 200 RUB
├ЮMoney: <code>Моментально</code> от 50 RUB
└Выберите платежную систему:</b>''',parse_mode='HTML', reply_markup=keyboard)


	if a[0] == 'Реквизитывывод':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		msg = bot.send_message(call.message.chat.id, f'''✍️ <b>Укажите реквизиты {a[2]}:</b>''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, vivod, a[2], a[1],msg.message_id)

	if a[0] == 'support':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		msg = bot.send_message(call.message.chat.id, f'''<b>🆘 Внимание:
├</b><i>Иногда ответ может занять до 6 часов, в зависимости от нагрузки.</i>
<b>├</b><i>С вопросом о выводе средств писать в поддержку нет смысла, так как вывод происходит автоматизировано. В случае ошибки при указании реквизитов вы получите полномерный возврат.</i>
<b>└✍️ Напишите свой вопрос для обращения к нам:</b>''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, supportadd, msg.message_id)		

	if a[0] == 'Автопостинг':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_avtopost)	
		q = connection.cursor()
		q.execute(f"SELECT * FROM akk where user = '{call.message.chat.id}'")
		row = q.fetchall()
		keyboard = types.InlineKeyboardMarkup()
		for i in row:
			keyboard.add(types.InlineKeyboardButton(text=i[2],callback_data=f'список {i[0]}'))
		keyboard.add(types.InlineKeyboardButton(text='➕ Добавить аккаунт',url=f't.me/QAuth_BOT'))
		keyboard.add(types.InlineKeyboardButton(text=f'''🪧 База чатов''',callback_data=f'Базачатов'))
		keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'бот '))
		bot.send_message(call.from_user.id,  f'''ℹ️ <strong>Как это работает ?
└  Д</strong><em>обавляете аккаунт, после  ваш пост будет автоматически публиковаться <strong>в любом чате</strong> с <strong> любым интервалом времени</strong>, который вы укажете.</em>''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'список':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_avtopost)
		q = connection.cursor()
		q.execute(f'SELECT * FROM akk where id =  "{a[1]}"')
		akk_info = q.fetchone()
		keyboard = types.InlineKeyboardMarkup()
		q.execute(f"SELECT COUNT(chat) FROM list_chat where akkaunt = '{akk_info[2]}'")
		chats_count = q.fetchone()[0]
		q.execute(f"SELECT * FROM list_chat  where akkaunt = '{akk_info[2]}' ORDER BY id DESC LIMIT 30")
		rows = q.fetchall()
		btns = []
		for i in range(len(rows)):
			btns.append(types.InlineKeyboardButton(text=rows[i][3], callback_data=f'servis_ {rows[i][0]} {a[1]}'))
		while btns != []:
			try:
				keyboard.add(
					btns[0],
					btns[1]
					)
				del btns[1], btns[0]
			except:
				keyboard.add(btns[0])
				del btns[0]
		keyboard.add(types.InlineKeyboardButton(text=f'''🔄  Загрузить чаты с аккаунта''',callback_data=f'loading_akk {akk_info[2]} {a[1]}'))
		keyboard.add(types.InlineKeyboardButton(text=f'''🌏 Смена прокси''',callback_data=f'настройка proxy {a[1]}'),types.InlineKeyboardButton(text=f'''🗑 Удалить аккаунт''',callback_data=f'настройка delakk {a[1]}'))
		keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'Автопостинг '))
		bot.send_message(call.message.chat.id, f'''<b>ℹ️ Информация:</b>
<b>├Прокси:</b> <code>{akk_info[3]}</code>
<b>└Чатов:</b> <code>{chats_count}</code>''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'loading_akk':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		bot.send_message(call.message.chat.id, f'🔄 Загружаем, пожалуйста ожидайте.',reply_markup=keyboards.main)
		status = chat_list.mains(a[1])
		if status == True:
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'список {a[2]}'))
			bot.send_message(call.message.chat.id, f'''✔️ Чаты успешно загружены.''',reply_markup=keyboard)
		else:
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'список {a[2]}'))
			bot.send_message(call.message.chat.id, f'✖️ Ошибка аккаунта или прокси.',reply_markup=keyboard)	
	
	if a[0] == 'Отправить':
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_avtopost)
		q = connection.cursor()
		q.execute(f"update list_chat set status = 'Send' where id = '{a[1]}'")
		connection.commit()
		bot.answer_callback_query(callback_query_id=call.id,show_alert=True, text="⏳ Отправка поставлена в очередь и будет произведена в течений минуты !")

		
	if a[0] == 'servis_':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_avtopost)
		q = connection.cursor()
		q.execute(f"SELECT * FROM list_chat where id = '{a[1]}'")
		row = q.fetchone()
		date = datetime.today()
		date= date.strftime("%H:%M")
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='📝 Сменить текст',callback_data=f'настройка text {a[1]} {a[2]}'))
		keyboard.add(types.InlineKeyboardButton(text='🌅 Сменить фото',callback_data=f'настройка photo {a[1]} {a[2]}'),types.InlineKeyboardButton(text='⏱ Сменить задержку',callback_data=f'настройка hold {a[1]} {a[2]}'))
		keyboard.add(types.InlineKeyboardButton(text='💭 Отправить сейчас',callback_data=f'Отправить {a[1]}'))
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'список {a[2]}'),types.InlineKeyboardButton(text='🗑 Удалить',callback_data=f'настройка del {a[1]} {a[2]}'))
		bot.send_message(call.from_user.id,  f'''<b>ℹ️ Информация:</b>
<b>├Id:</b> <code>{row[2]}</code>
<b>├Название:</b> <code>{row[3]}</code>
<b>├Текст:</b> <code>{row[4]}</code>
<b>├фото:</b> <code>{row[5]}</code> (ссылка)
<b>├Задержка:</b> <code>{row[6]}</code> минут
<b>├Отправка:</b> <code>{row[7]}</code>
<b>└Текущие время сервера:</b> <code>{date}</code>''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'Базачатов':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'Автопостинг'))
		doc = open('chat.rar', 'rb')
		bot.send_document(call.message.chat.id, doc, caption='✔️ Спасибо за скачивание чатов.', reply_markup=keyboard)
		
	if a[0] == 'настройка':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_avtopost)
		q = connection.cursor()
		if str(a[1]) == 'text':
			msg= bot.send_message(call.message.chat.id, "✍️ Укажите новое значение:",parse_mode='HTML')
			bot.register_next_step_handler(msg, new_data, a[1],a[2],a[3])
		if str(a[1]) == 'hold':
			msg= bot.send_message(call.message.chat.id, "✍️ Укажите новое значение задержки:",parse_mode='HTML')
			bot.register_next_step_handler(msg, new_data, a[1],a[2],a[3])
		if str(a[1]) == 'del':
			q.execute(f"DELETE FROM list_chat where id = '{a[2]}'")
			connection.commit()
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'список {a[3]}'))
			bot.send_message(call.from_user.id,  '''✔️ Чат удален.''',parse_mode='HTML', reply_markup=keyboard)
		if str(a[1]) == 'photo':
			msg= bot.send_message(call.message.chat.id, "✍️ Укажите ссылку на фото:",parse_mode='HTML')
			bot.register_next_step_handler(msg, new_data, a[1],a[2],a[3])

		if str(a[1]) == 'proxy':
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'''📜 Инструкция''',url='https://telegra.ph/XAለVA--SMM-FRANCHISE--Navigaciya-po-menyu-04-15 '),types.InlineKeyboardButton(text=f'''➕ Купить прокси''',url='https://proxy.market/?ref=pm00038810'))
			msg = bot.send_message(call.message.chat.id,'''✍️ Введите прокси в формате:
└ <code>login:password@ip:port</code> (SOCKS)''',parse_mode='HTML', reply_markup=keyboard)
			bot.register_next_step_handler(msg, add_proxi, a[2],msg.message_id)

		if str(a[1]) == 'delakk':
			q.execute(f'SELECT name FROM akk where id = "{a[2]}"')
			akk_info = q.fetchone()[0]
			q.execute(f"DELETE FROM akk where id = '{a[2]}'")
			connection.commit()
			q.execute(f"DELETE FROM list_chat where akkaunt = '{akk_info}'")
			connection.commit()
			wwwww = f'+{akk_info}'
			q.execute(f"DELETE FROM list_chat where akkaunt = '{wwwww}'")
			connection.commit()
			try:
				path = os.path.join('/root/smm/sessions/', f'{akk_info}.session')
				os.remove(path)
				path = os.path.join('/root/smm/sessions/', f'{akk_info}.session-journal')
				os.remove(path)
			except Exception as e:
				pass
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'Автопостинг'))
			bot.send_message(call.from_user.id,  '''✔️ Аккаунт удален.''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'Закрыть':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)

	if a[0] == "Оставитьотзыв":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg= bot.send_message(call.message.chat.id, "<b>✍️ Напишите текст отзыва:</b>",parse_mode='HTML')
		bot.register_next_step_handler(msg, reviews)
			
	if a[0] == 'Реферальная':		
		bot_name = 'EasyBotsFranchise_bot'
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		bot_name = 'EasyBotsFranchise_bot'
		q.execute(f'SELECT COUNT(id) FROM ugc_users WHERE ref = "{call.message.chat.id}" and bot = "{bot_name}"')
		user_ref_count = q.fetchone()[0]
		q.execute(f'SELECT * FROM ugc_users WHERE id = "{call.message.chat.id}" and bot = "{bot_name}"')
		rowsss = q.fetchone()
		dohodref = rowsss[2]
		if rowsss[2] == None:
			dohodref = 0
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='❗️ Как заработать ?!',url='https://telegra.ph/XAለVA--SMM-FRANCHISE--Navigaciya-po-menyu-04-15 '))
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'Кабинет '))
		bot.send_message(call.message.chat.id, f'''<b>🤝 Реферальная программа</b>
<b>└Ссылка:</b> https://t.me/{bot_name}?start={call.message.chat.id}

<b>📈 Статистика</b>
<b>├Доход:</b> <code>{dohodref} RUB</code>
<b>├Рефералов:</b> <code>{user_ref_count}</code>
<b>├Процентная ставка:</b> <code>10%</code>
<b>└</b><i>Приглашайте новых пользователей и получайте пассивный доход в размере 10% от всех финансовых операций рефералов!</i>''',parse_mode='HTML',reply_markup=keyboard, disable_web_page_preview=True)

# try:
# 	bot.polling(True)
# except Exception as e:
# 	bot.send_message(1960177129, e)


bot.polling(True)