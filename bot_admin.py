# -*- coding: utf-8 -*-
from decimal import *
import telebot
import datetime
from telebot import types, apihelper
import sqlite3
import random, string
import time
import os,random,shutil,subprocess
from subprocess import check_output
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
import pytz
import itertools 
import json
import urllib.request

bot = telebot.TeleBot('5721496808:AAH-rI8XBupvKjO1IfQ_MZL51vkBzBFyz98')
@bot.message_handler(content_types=['text','photo','document'])
def send_text(message):
	if message.chat.type == 'private':
		if message.text == '/admin':
			admin = config.admin
			for i in admin:
				if message.chat.id == i:
					keyboard = types.InlineKeyboardMarkup()
					keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
					bot.send_message(message.chat.id, f''' 🖐 Привет администратор !''',parse_mode='HTML', reply_markup=keyboard)
					

def obnovabot(message,idsms):
	bot.delete_message(message.chat.id,message.message_id)
	bot.delete_message(message.chat.id,idsms)
	if message.text != 'Отмена':
		try:
			save_dir = os.getcwd()
			file_name = message.document.file_name
			file_id = message.document.file_name
			file_id_info = bot.get_file(message.document.file_id)
			downloaded_file = bot.download_file(file_id_info.file_path)
			src = file_name
			with open(save_dir + "/bot/" + src, 'wb') as new_file:
				new_file.write(downloaded_file)
			connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
			q = connection.cursor()
			q.execute(f"SELECT * FROM list_bot")
			rows = q.fetchall()
			for i in rows:
				name = i[6]
				try:
					path = os.path.join(f'/root/smm/bot_list/{name}/', f'main.py')
					os.remove(path)
				except:
					pass
				current_dir = os.getcwd()
				path = f'{current_dir}/bot_list/{name}'
				src = f'{current_dir}/bot/main.py'
				shutil.copy(src, path ,follow_symlinks=True)
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Меню'))
			bot.send_message(message.chat.id, "[*] File added:\nFile name - {}\nFile directory - {}".format(str(file_name), str(save_dir)), reply_markup=keyboard)
		except Exception as ex:
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
			bot.send_message(message.chat.id, "[!] error - {}".format(str(ex)), reply_markup=keyboard)

	else:
		user = message.chat.id
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
		hideBoard = types.ReplyKeyboardRemove()
		msg = bot.send_message(message.chat.id, f'''⏳ Отменяем.......''', reply_markup=hideBoard)
		bot.delete_message(message.from_user.id,msg.message_id)
		bot.send_message(message.chat.id, f'''✖️ Отменили.''',parse_mode='HTML', reply_markup=keyboard)

def support_otvet(message,idsms,idsup):
	bot.delete_message(message.chat.id,message.message_id)
	bot.delete_message(message.chat.id,idsms)
	try:
		if message.text.lower() != 'отмена':
			connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
			q = connection.cursor()
			q.execute(f"SELECT * FROM support where id = '{idsup}'")
			row = q.fetchone()
			q.execute(f"update support set status = '0' where id = '{idsup}'")
			connection.commit()
			texts = F'''{row[2]}
	└[Adm]<code>{message.text}</code>'''
			q.execute(f"update support set text = '{texts}' where id = '{idsup}'")
			connection.commit()
			q.execute(f"SELECT bot_token FROM list_bot where bot = '{row[4]}' ")
			bot_token = q.fetchone()[0]
			bots = telebot.TeleBot(bot_token)
			admin = config.admin
			try:
				bots.send_message(row[1], f'<b>❗️ Ответ от администрации:</b> <code>{message.text}</code>',parse_mode='HTML')
			except:
				pass
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Поддержка'))
			bot.send_message(message.chat.id, '✔️  Успешно ответили на запрос.',parse_mode='HTML', reply_markup=keyboard)
		else:
			user = message.chat.id
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
			hideBoard = types.ReplyKeyboardRemove()
			msg = bot.send_message(message.chat.id, f'''⏳ Отменяем.......''', reply_markup=hideBoard)
			bot.delete_message(message.from_user.id,msg.message_id)
			bot.send_message(message.chat.id, f'''✖️ Отменили.''',parse_mode='HTML', reply_markup=keyboard)
	except Exception as e:
		print(e)
		bot.send_message(-1001695154512, f'Жопа ЭТО ПИЗДЕЦ \n\n\n{e}')
		pass

def editdohod(message,idsms,ssss):
	bot.delete_message(message.chat.id,message.message_id)
	bot.delete_message(message.chat.id,idsms)
	if message.text != 'Отмена':
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		print(ssss)
		q.execute(f"update dohod set {str(ssss)} = {str(ssss)} + '{message.text}' WHERE id = '1'")
		connection.commit()
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Доход'))
		bot.send_message(message.chat.id, f'''Готово.''',parse_mode='HTML', reply_markup=keyboard)
	else:
		user = message.chat.id
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
		hideBoard = types.ReplyKeyboardRemove()
		msg = bot.send_message(message.chat.id, f'''⏳ Отменяем.......''', reply_markup=hideBoard)
		bot.delete_message(message.from_user.id,msg.message_id)
		bot.send_message(message.chat.id, f'''✖️ Отменили.''',parse_mode='HTML', reply_markup=keyboard)


def sendall(message,idsms):
	bot.delete_message(message.chat.id,message.message_id)
	bot.delete_message(message.chat.id,idsms)
	global botsname
	botsname = message.text
	if message.text != 'Отмена':
		msg = bot.send_message(message.chat.id, f'''✍️ Отправьте сообщение для рассылки:''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, sendallgo ,msg.message_id)
	else:
		user = message.chat.id
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
		hideBoard = types.ReplyKeyboardRemove()
		msg = bot.send_message(message.chat.id, f'''⏳ Отменяем.......''', reply_markup=hideBoard)
		bot.delete_message(message.from_user.id,msg.message_id)
		bot.send_message(message.chat.id, f'''✖️ Отменили рассылку.''',parse_mode='HTML', reply_markup=keyboard)


def sendgoallbase(message,idsms):
	bot.delete_message(message.chat.id,message.message_id)
	bot.delete_message(message.chat.id,idsms)
	sends = 0
	erors = 0
	if message.text != 'Отмена':
		keyboa = types.InlineKeyboardMarkup()
		keyboa.add(types.InlineKeyboardButton(text='✖️ Закрыть',callback_data=f'Закрыть'))
		msg = bot.send_message(message.chat.id, '''⏳ Идет рассылка...''')
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f'SELECT * FROM list_bot WHERE bot != "SimpsonSmm_bot"')
		token = q.fetchall()
		for i in token:
			bot_send = telebot.TeleBot(i[7])
			q.execute(f'SELECT * FROM ugc_users WHERE bot = "{i[6]}"')
			row = q.fetchall()
			for i in row:
				time.sleep(0.03)
				if message.content_type == 'text':
					try:
						bot_send.send_message(i[0], message.text ,entities = message.entities, reply_markup=keyboa)
						sends += 1
					except:
						erors += 1
				elif message.content_type == 'photo':
					try:
						bot_send.send_photo(i[0],message.photo[0].file_id, message.caption ,caption_entities = message.caption_entities)
						sends += 1
					except:
						erors += 1
		bot.delete_message(message.from_user.id,msg.message_id)
		bot.send_message(message.chat.id, f'''<b>📈 Рассылка завершена</b>:
<b>├Доставленно:</b> <code>{sends}</code>
<b>└Ошибки:</b> <code>{erors}</code>\n\n''',parse_mode='HTML', reply_markup=keyboard)

	else:
		user = message.chat.id
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
		hideBoard = types.ReplyKeyboardRemove()
		msg = bot.send_message(message.chat.id, f'''⏳ Отменяем.......''', reply_markup=hideBoard)
		bot.delete_message(message.from_user.id,msg.message_id)
		bot.send_message(message.chat.id, f'''✖️ Отменили рассылку.''',parse_mode='HTML', reply_markup=keyboard)


def add_categor(message,idsms):
	bot.delete_message(message.chat.id,message.message_id)
	bot.delete_message(message.chat.id,idsms)
	if message.text != 'Отмена':
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute("INSERT INTO category (name) VALUES ('%s')"%(message.text))
		connection.commit()
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
		bot.send_message(message.chat.id, f'''✔️  Категория успешно добавлена''', reply_markup=keyboard)
	else:
		user = message.chat.id
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
		hideBoard = types.ReplyKeyboardRemove()
		msg = bot.send_message(message.chat.id, f'''⏳ Отменяем.......''', reply_markup=hideBoard)
		bot.delete_message(message.from_user.id,msg.message_id)
		bot.send_message(message.chat.id, f'''✖️ Отменили добавление.''',parse_mode='HTML', reply_markup=keyboard)

def add_razdel(message,idsms,idcategor):
	bot.delete_message(message.chat.id,message.message_id)
	bot.delete_message(message.chat.id,idsms)
	if message.text != 'Отмена':
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute("INSERT INTO sub_category (name,category) VALUES ('%s','%s')"%(message.text,idcategor))
		connection.commit()
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
		bot.send_message(message.chat.id, f'''✔️  Раздел успешно добавлен''', reply_markup=keyboard)
	else:
		user = message.chat.id
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
		hideBoard = types.ReplyKeyboardRemove()
		msg = bot.send_message(message.chat.id, f'''⏳ Отменяем.......''', reply_markup=hideBoard)
		bot.delete_message(message.from_user.id,msg.message_id)
		bot.send_message(message.chat.id, f'''✖️ Отменили добавление.''',parse_mode='HTML', reply_markup=keyboard)


def add_usluga_1(message,idsms,idrazdel):
	bot.delete_message(message.chat.id,message.message_id)
	bot.delete_message(message.chat.id,idsms)
	if message.text != 'Отмена':
		global name_usluga
		name_usluga = message.text
		msg = bot.send_message(message.chat.id, f'''✍️ Укажите описание услуги для добавления:''',parse_mode='HTML', reply_markup=keyboards.otmena)
		idsms = msg.message_id
		bot.register_next_step_handler(msg, add_usluga_2,idsms,idrazdel)
	else:
		user = message.chat.id
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
		bot.delete_message(message.from_user.id,msg.message_id)
		bot.send_message(message.chat.id, f'''✖️ Отменили добавление.''',parse_mode='HTML', reply_markup=keyboard)

def add_usluga_2(message,idsms,idrazdel):
	bot.delete_message(message.chat.id,message.message_id)
	bot.delete_message(message.chat.id,idsms)
	if message.text != 'Отмена':
		global info_usluga
		info_usluga = message.text
		msg = bot.send_message(message.chat.id, f'''✍️ Укажите цену за 1000 единиц:''',parse_mode='HTML', reply_markup=keyboards.otmena)
		idsms = msg.message_id
		bot.register_next_step_handler(msg, add_usluga_3,idsms,idrazdel)
	else:
		user = message.chat.id
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
		bot.delete_message(message.from_user.id,msg.message_id)
		bot.send_message(message.chat.id, f'''✖️ Отменили добавление.''',parse_mode='HTML', reply_markup=keyboard)

def add_usluga_3(message,idsms,idrazdel):
	bot.delete_message(message.chat.id,message.message_id)
	bot.delete_message(message.chat.id,idsms)
	if message.text != 'Отмена':
		global prace_usluga
		prace_usluga = message.text
		msg = bot.send_message(message.chat.id, f'''✍️ Укажите мин единиц услуги:''',parse_mode='HTML', reply_markup=keyboards.otmena)
		idsms = msg.message_id
		bot.register_next_step_handler(msg, add_usluga_4,idsms,idrazdel)
	else:
		user = message.chat.id
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
		bot.delete_message(message.from_user.id,msg.message_id)
		bot.send_message(message.chat.id, f'''✖️ Отменили добавление.''',parse_mode='HTML', reply_markup=keyboard)

def add_usluga_4(message,idsms,idrazdel):
	bot.delete_message(message.chat.id,message.message_id)
	bot.delete_message(message.chat.id,idsms)
	if message.text != 'Отмена':
		global min_usluga
		min_usluga = message.text
		msg = bot.send_message(message.chat.id, f'''✍️ Укажите макс единиц услуги:''',parse_mode='HTML', reply_markup=keyboards.otmena)
		idsms = msg.message_id
		bot.register_next_step_handler(msg, add_usluga_5,idsms,idrazdel)
	else:
		user = message.chat.id
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
		bot.delete_message(message.from_user.id,msg.message_id)
		bot.send_message(message.chat.id, f'''✖️ Отменили добавление.''',parse_mode='HTML', reply_markup=keyboard)

def add_usluga_5(message,idsms,idrazdel):
	bot.delete_message(message.chat.id,message.message_id)
	bot.delete_message(message.chat.id,idsms)
	if message.text != 'Отмена':
		global max_usluga
		max_usluga = message.text
		msg = bot.send_message(message.chat.id, f'''✍️ Укажите ID SERVICE с партнера:''',parse_mode='HTML', reply_markup=keyboards.otmena)
		idsms = msg.message_id
		bot.register_next_step_handler(msg, add_usluga_6,idsms,idrazdel)
	else:
		user = message.chat.id
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
		bot.delete_message(message.from_user.id,msg.message_id)
		bot.send_message(message.chat.id, f'''✖️ Отменили добавление.''',parse_mode='HTML', reply_markup=keyboard)

def add_usluga_6(message,idsms,idrazdel):
	bot.delete_message(message.chat.id,message.message_id)
	bot.delete_message(message.chat.id,idsms)
	if message.text != 'Отмена':
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute("INSERT INTO item (name,sub_category,category,cost,min,max,service_id,item_desc) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(name_usluga,idrazdel,idrazdel,prace_usluga,min_usluga,max_usluga,message.text,info_usluga))
		connection.commit()
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
		bot.send_message(message.chat.id, f'''✔️  Услуга успешно добавлена''', reply_markup=keyboard)
	else:
		user = message.chat.id
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
		bot.delete_message(message.from_user.id,msg.message_id)
		bot.send_message(message.chat.id, f'''✖️ Отменили добавление.''',parse_mode='HTML', reply_markup=keyboard)


def sendallgo(message,idsms):
	bot.delete_message(message.chat.id,message.message_id)
	bot.delete_message(message.chat.id,idsms)
	if message.text != 'Отмена':
		msg = bot.send_message(message.chat.id, '''⏳ Идет рассылка...''')
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f'SELECT bot_token FROM list_bot WHERE bot = "{botsname}"')
		token = q.fetchone()[0]
		bot_send = telebot.TeleBot(token)
		if botsname == 'JopaPosting':
			connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database='bomber')
			q = connection.cursor()
			q.execute(f'SELECT * FROM ugc_users')
			row = q.fetchall()
		elif botsname == 'JopaPosting':
			connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database='avtopost_new')
			q = connection.cursor()
			q.execute(f'SELECT * FROM ugc_users')
			row = q.fetchall()
		else:
			q.execute(f'SELECT * FROM ugc_users WHERE bot = "{botsname}"')
			row = q.fetchall()
		sends = 0
		erors = 0
		keyboa = types.InlineKeyboardMarkup()
		keyboa.add(types.InlineKeyboardButton(text='✖️ Закрыть',callback_data=f'Закрыть'))
		for i in row:
			if botsname == 'JopaPosting':
				user = i[1]
			elif botsname == 'JopaPosting':
				user = i[1]
			else:
				user = i[0]
			time.sleep(0.03)
			if message.content_type == 'text':
				try:
					bot_send.send_message(user, message.text ,entities = message.entities, reply_markup=keyboa)
					sends += 1
				except:
					erors += 1
			elif message.content_type == 'photo':
				try:
					bot_send.send_photo(user,message.photo[0].file_id, message.caption ,caption_entities = message.caption_entities, reply_markup=keyboa)
					sends += 1
				except:
					erors += 1
		bot.delete_message(message.from_user.id,msg.message_id)
		bot.send_message(message.chat.id, f'''<b>📈 Рассылка завершена</b>:
<b>├Бот:</b> @{botsname}
<b>├Доставленно:</b> <code>{sends}</code>
<b>└Ошибки:</b> <code>{erors}</code>\n\n''',parse_mode='HTML', reply_markup=keyboard)

	else:
		user = message.chat.id
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
		hideBoard = types.ReplyKeyboardRemove()
		msg = bot.send_message(message.chat.id, f'''⏳ Отменяем.......''', reply_markup=hideBoard)
		bot.delete_message(message.from_user.id,msg.message_id)
		bot.send_message(message.chat.id, f'''✖️ Отменили рассылку.''',parse_mode='HTML', reply_markup=keyboard)

def addbalance(message,users,bots,idsms):
	bot.delete_message(message.chat.id,message.message_id)
	bot.delete_message(message.chat.id,idsms)
	if message.text != 'Отмена':
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"update ugc_users set balance = '{message.text}' WHERE id = '{users}' and bot = '{bots}'")
		connection.commit()
		keyboard = types.InlineKeyboardMarkup()	
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'Меню'))	
		bot.send_message(message.chat.id, '✔️ Успешно сменили баланс.',parse_mode='HTML', reply_markup=keyboard)
	else:
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
		hideBoard = types.ReplyKeyboardRemove()
		msg = bot.send_message(message.chat.id, f'''⏳ Отменяем.......''', reply_markup=hideBoard)
		bot.delete_message(message.from_user.id,msg.message_id)
		bot.send_message(message.chat.id, f'''✖️ Отменили пополнение баланса.''',parse_mode='HTML', reply_markup=keyboard)

def addbalancebot(message,users,idsms):
	bot.delete_message(message.chat.id,message.message_id)
	bot.delete_message(message.chat.id,idsms)
	if message.text != 'Отмена':
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"update list_bot set balance = '{message.text}' WHERE id = '{users}'")
		connection.commit()
		keyboard = types.InlineKeyboardMarkup()	
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'Меню'))	
		bot.send_message(message.chat.id, '✔️ Успешно сменили баланс.',parse_mode='HTML', reply_markup=keyboard)
	else:
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
		hideBoard = types.ReplyKeyboardRemove()
		msg = bot.send_message(message.chat.id, f'''⏳ Отменяем.......''', reply_markup=hideBoard)
		bot.delete_message(message.from_user.id,msg.message_id)
		bot.send_message(message.chat.id, f'''✖️ Отменили пополнение баланса.''',parse_mode='HTML', reply_markup=keyboard)


def dell_akk(message,idsms):
	bot.delete_message(message.chat.id,message.message_id)
	bot.delete_message(message.chat.id,idsms)
	if message.text != 'Отмена':
			connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_avtopost)
			q = connection.cursor()
			q.execute(f"DELETE FROM akk where name = '{message.text}'")
			connection.commit()
			q.execute(f"DELETE FROM list_chat where akkaunt = '{message.text}'")
			connection.commit()
			try:
				path = os.path.join('/root/JopaPosting/Avtopostbot/sessions/', f'{message.text}.session')
				os.remove(path)
				path = os.path.join('/root/JopaPosting/Avtopostbot/sessions/', f'{message.text}.session-journal')
				os.remove(path)
			except Exception as e:
				pass
			keyboard = types.InlineKeyboardMarkup()	
			keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'Меню'))	
			bot.send_message(message.chat.id, '✔️ Успешно удалили акк.',parse_mode='HTML', reply_markup=keyboard)
	else:
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
		hideBoard = types.ReplyKeyboardRemove()
		msg = bot.send_message(message.chat.id, f'''⏳ Отменяем.......''', reply_markup=hideBoard)
		bot.delete_message(message.from_user.id,msg.message_id)
		bot.send_message(message.chat.id, f'''✖️ Отменили.''',parse_mode='HTML', reply_markup=keyboard)

def add_promo(message,idsms):
	bot.delete_message(message.chat.id,message.message_id)
	bot.delete_message(message.chat.id,idsms)
	if message.text != 'Отмена':
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute("INSERT INTO promo (name,coolvo) VALUES ('%s','%s')"%(message.text,0))
		connection.commit()
		keyboard = types.InlineKeyboardMarkup()	
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'Меню'))	
		bot.send_message(message.chat.id, f'✔️ Успешно добавили ссылку: <a href="https://t.me/Smm_Hermes_bot?start={message.text}">{message.text}</a>',parse_mode='HTML', reply_markup=keyboard)
	else:
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
		hideBoard = types.ReplyKeyboardRemove()
		msg = bot.send_message(message.chat.id, f'''⏳ Отменяем.......''', reply_markup=hideBoard)
		bot.delete_message(message.from_user.id,msg.message_id)
		bot.send_message(message.chat.id, f'''✖️ Отменили пополнение баланса.''',parse_mode='HTML', reply_markup=keyboard)

def editusluga(message,idsms,idusluga,whatsmena):
	bot.delete_message(message.chat.id,message.message_id)
	bot.delete_message(message.chat.id,idsms)
	if message.text != 'Отмена':
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"update item set {str(whatsmena)} = '{message.text}' WHERE item_id = '{idusluga}'")
		connection.commit()
		keyboard = types.InlineKeyboardMarkup()	
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'Меню'))	
		bot.send_message(message.chat.id, '✔️ Успешно изменили.',parse_mode='HTML', reply_markup=keyboard)
	else:
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
		hideBoard = types.ReplyKeyboardRemove()
		msg = bot.send_message(message.chat.id, f'''⏳ Отменяем.......''', reply_markup=hideBoard)
		bot.delete_message(message.from_user.id,msg.message_id)
		bot.send_message(message.chat.id, f'''✖️ Отменили пополнение баланса.''',parse_mode='HTML', reply_markup=keyboard)

def poisk_user_admin(message,idsms):
	bot.delete_message(message.chat.id,message.message_id)
	bot.delete_message(message.chat.id,idsms)
	if message.text.lower() != 'отмена':
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		idusers = message.text.split('\n')[0]
		bot_names = message.text.split('\n')[1]
		q.execute(f"SELECT * FROM ugc_users where id = '{idusers}'and bot = '{bot_names}' ")
		row = q.fetchone()
		if row != None:
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='🔒 Заблокировать | Раблокировать',callback_data=f'заблокировать_ {row[0]} {bot_names}'))
			keyboard.add(types.InlineKeyboardButton(text='➕ Добавить баланс',callback_data=f'Добавитьбаланс {idusers} {bot_names}'))	
			keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'Меню'))	
			msg = bot.send_message(message.chat.id, f'''👤 Пользователь: 
🆔 ID: <code>{row[0]}</code>
💰 Баланс: <code>{row[6]}</code>
🔐 Статус: <code>{row[3]}</code>
''',parse_mode='HTML',reply_markup=keyboard)
		else:
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
			hideBoard = types.ReplyKeyboardRemove()
			msg = bot.send_message(message.chat.id, f'''⏳ Отменяем.......''', reply_markup=hideBoard)
			bot.delete_message(message.from_user.id,msg.message_id)
			bot.send_message(message.chat.id, f'''✖️ Нет такого пользователя.''',parse_mode='HTML', reply_markup=keyboard)
	else:
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
		hideBoard = types.ReplyKeyboardRemove()
		msg = bot.send_message(message.chat.id, f'''⏳ Отменяем.......''', reply_markup=hideBoard)
		bot.delete_message(message.from_user.id,msg.message_id)
		bot.send_message(message.chat.id, f'''✖️ Отменили.''',parse_mode='HTML', reply_markup=keyboard)

def poisk_bot(message,idsms):
	bot.delete_message(message.chat.id,message.message_id)
	bot.delete_message(message.chat.id,idsms)
	if message.text.lower() != 'отмена':
		# try:
			connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
			q = connection.cursor()
			q.execute(f"SELECT * FROM list_bot where name = '{message.text}'")
			rows = q.fetchone()
			if rows != None:
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
				status = "🔴 Выключить" if rows[8] == "Работает" else "🟢 Включить"
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text=f'🚫 Заблокировать',callback_data=f'Заблокировать {rows[6]} block'),types.InlineKeyboardButton(text='🗑 Удалить',callback_data=f'Заблокировать {rows[6]} dell'))
				keyboard.add(types.InlineKeyboardButton(text='💰 Обновить баланс',callback_data=f'Обновитьбаланс {rows[0]}'))	
				keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'Меню'))	
				bot.send_message(message.chat.id, f'''<b>ℹ️ Информация:</b>
<b>├Бот:</b> @{rows[6]}	
<b>├Всего пользователей:</b> <code>{user_count}</code>
<b>└Новые пользователи:</b> <code>{user_count_data}</code>

<b>📊 Статистика:</b>
<b>├Заказов:</b> <code>{zakaz_count} шт</code>
<b>├Заказов за сегодня :</b> <code>{zakaz_count_data1} шт</code>
<b>└Последний заказ:</b> <code>{oldzakaz}</code>

<b>🏦Доходность:</b>
<b>├Наценка:</b> <code>{rows[5]} %</code>
<b>├Баланс:</b> <code>{rows[3]} RUB</code>
<b>└Прибыль:</b> <code>{rows[10]} RUB</code>''',parse_mode='HTML', reply_markup=keyboard)
			else:
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
				bot.send_message(message.chat.id, f'''✖️ Нет такого бота.''',parse_mode='HTML', reply_markup=keyboard)
		# except:
		# 	pass
	else:
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
		hideBoard = types.ReplyKeyboardRemove()
		msg = bot.send_message(message.chat.id, f'''⏳ Отменяем.......''', reply_markup=hideBoard)
		bot.delete_message(message.from_user.id,msg.message_id)
		bot.send_message(message.chat.id, f'''✖️ Отменили.''',parse_mode='HTML', reply_markup=keyboard)

def minus_money(message,idsms):
	bot.delete_message(message.chat.id,message.message_id)
	bot.delete_message(message.chat.id,idsms)
	if message.text.lower() != 'отмена':
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute("SELECT my_id_pay FROM geral_config  where id = "+str(1))
		my_id_pay = q.fetchone()[0]
		q.execute("SELECT my_key_pay FROM geral_config  where id = "+str(1))
		my_key_pay = q.fetchone()[0]
		summa = message.text.split('\n')[0]
		rekvizit = message.text.split('\n')[1]
		minus_money = requests.post(url='https://payok.io/api/payout_create',data={'API ID': my_id_pay, 'API KEY': str(my_key_pay), 'amount': float(summa), 'method': str(tip_vivod), 'reciever': str(rekvizit), 'comission_type': str('payment')})
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'Меню'))	
		bot.send_message(message.chat.id, minus_money.text ,parse_mode='HTML', reply_markup=keyboard)
	else:
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🎛 Меню',callback_data=f'Меню'))
		hideBoard = types.ReplyKeyboardRemove()
		msg = bot.send_message(message.chat.id, f'''⏳ Отменяем.......''', reply_markup=hideBoard)
		bot.delete_message(message.from_user.id,msg.message_id)
		bot.send_message(message.chat.id, f'''✖️ Отменили.''',parse_mode='HTML', reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call: True)
def handler_call(call):
	a = call.data.split()
	if a[0] == 'Меню':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		msg = bot.send_message(call.message.chat.id, f'''⏳ Идет загрузка.......''',parse_mode='HTML')
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		tomorrow = datetime.now()
		data = tomorrow.strftime('%d/%m/%Y')
		q.execute(f"SELECT COUNT(id) FROM ugc_users where bot = 'fast_smm'")
		user_count = q.fetchone()[0]
		q.execute(f"SELECT COUNT(id) FROM ugc_users where bot = 'fast_smm' and ref >= 1")
		user_count_ref = q.fetchone()[0]
		q.execute(f"SELECT DISTINCT id FROM ugc_users where bot != 'fast_smm'")
		user_unik = q.fetchall()
		q.execute(f"SELECT DISTINCT id FROM ugc_users where data = '{data}' and bot != 'fast_smm'")
		user_data = q.fetchall()
		q.execute(f"SELECT COUNT(id) FROM ugc_users where bot = 'fast_smm' and data = '{data}'")
		user_count_data = q.fetchone()[0]
		q.execute(f"SELECT COUNT(id) FROM list_bot")
		bot_count = q.fetchone()[0]
		q.execute(f"SELECT SUM(balance) FROM ugc_users")
		users_balance = q.fetchone()[0]
		q.execute(f"SELECT SUM(balance) FROM list_bot where balance >= '10'")
		bot_balance = q.fetchone()[0]
		q.execute(f"SELECT SUM(dohod) FROM list_bot")
		bot_dohod = q.fetchone()[0]
		q.execute(f"SELECT COUNT(id) FROM list_zakaz where data = '{data}'")
		zakaz_count_data = q.fetchone()[0]
		q.execute(f"SELECT COUNT(id) FROM list_zakaz")
		zakaz_count = q.fetchone()[0]
		date = datetime.today() - timedelta(days=1)
		date_minus = date.strftime("%d/%m/%Y")
		q.execute(f"SELECT COUNT(id) FROM list_zakaz where data = '{date_minus}'")
		zakaz_old_data = q.fetchone()[0]
		q.execute(f"SELECT COUNT(id) FROM list_bot where status = 'Работает'")
		bot_on = q.fetchone()[0]
		q.execute(f"SELECT COUNT(id) FROM list_bot where status = 'Заблокирован'")
		bot_block = q.fetchone()[0]
		q.execute(f"SELECT COUNT(id) FROM list_bot where status = 'Выключен'")
		bot_off = q.fetchone()[0]
		q.execute("SELECT my_id_pay FROM geral_config  where id = "+str(1))
		my_id_pay = q.fetchone()[0]
		q.execute("SELECT my_key_pay FROM geral_config  where id = "+str(1))
		my_key_pay = q.fetchone()[0]
		q.execute(f"SELECT api_sms FROM geral_config where id = '1'")
		api_sms = q.fetchone()
		try:
			headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
			h = requests.post(f'https://smshub.org/stubs/handler_api.php?api_key={api_sms[0]}&action=getBalance', headers=headers)
			balancesms = str(h.text.split(":")[1])
		except:
			balancesms = 'Ошибка ключа'
		try:
			balancepayok = requests.post(url='https://payok.io/api/balance',data={'API ID': my_id_pay, 'API KEY': str(my_key_pay)}).json()['balance']
		except:
			balancepayok = 'Ошибка ключа'
		try:
			name = 'jopa'
			secret = '7a4ca73baf7bcb4f042d59c14e893ba158155fde'
			balancecase = requests.post(f'https://api.crystalpay.ru/v1/?s={secret}&n={name}&o=balance').json()['balance']
		except:
			balancecase = 'Ошибка ключа'
		try:
			apinakrutka2 = '8ee0e78bc65cd55fd117d9a37ef32932'
			zakazid = urllib.request.urlopen(f'https://partner.soc-proof.su/api/v2/?key={apinakrutka2}&action=balance').read()
			result = json.loads(zakazid.decode('utf8'))
			balanceservice = (result['balance'])
		except:
			balanceservice = 'Ошибка ключа'
		q.execute(f"SELECT COUNT(id) FROM support where status = '2'")
		support_count = q.fetchone()[0]
		q.execute(f"SELECT COUNT(id) FROM vivod where status = 'WAIT'")
		viplata_count = q.fetchone()[0]
		q.execute(f"SELECT COUNT(id) FROM reviews")
		reviews_count = q.fetchone()[0]
		q.execute(f"SELECT COUNT(id) FROM list_zakaz_shop")
		tovar_count_count = q.fetchone()[0]
		q.execute(f"SELECT SUM(prace) FROM list_zakaz_shop")
		sum_count_count = q.fetchone()[0]
		q.execute(f"SELECT SUM(summa) FROM vivod where status = 'DONE'")
		sumviplata = q.fetchone()[0]
		q.execute(f"SELECT COUNT(id) FROM list_aktiv where code != 'Нет'")
		sms_count = q.fetchone()[0]
		if sms_count == None:
			sms_count = 0
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database='h159987_bbb1')
		q = connection.cursor()
		q.execute(f"SELECT COUNT(id) FROM tovar where status = 'DONE'")
		tovar_count = q.fetchone()[0]
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='👤 Пользователи',callback_data=f'Пользователи'),types.InlineKeyboardButton(text='🤖 Боты',callback_data=f'Боты'),types.InlineKeyboardButton(text='🛍 Услуги',callback_data=f'Добавление'))
		keyboard.add(types.InlineKeyboardButton(text=f'📢 Промо',callback_data=f'Промостатистика'),types.InlineKeyboardButton(text='💬 Рассылка',callback_data=f'Рассылка'))
		keyboard.add(types.InlineKeyboardButton(text=f'⁉️ Поддержка ({support_count})',callback_data=f'Поддержка'),types.InlineKeyboardButton(text=f'🔧 Настройки',callback_data=f'Настройки'))
		keyboard.add(types.InlineKeyboardButton(text=f'Доход ботов', callback_data=f'Доход'))
		keyboard.add(types.InlineKeyboardButton(text=f'♻️ Обновить данные',callback_data=f'Меню'))
		text = f'''<b>ℹ️ Информация по сервису:</b>
<b>├Всего клиентов сервиса:</b> <code>{user_count} / {user_count_ref}</code>
<b>├Новые клиенты сервиса:</b> <code>{user_count_data}</code>
<b>├Ботов:</b> <code>{bot_count} шт</code> 
<b>├Ботов активно:</b> <code>{bot_on} шт</code>
<b>├Ботов заблокировано:</b> <code>{bot_block} шт</code>
<b>├Ботов выключено:</b> <code>{bot_off} шт</code>
<b>├Уникальных пользователей:</b> <code>{len(user_unik)}</code>
<b>├Новых пользователей:</b> <code>{len(user_data)}</code>

<b>ℹ️ Финансы ботов:</b>
<b>├Доход ботов:</b> <code>{bot_dohod} RUB</code>
<b>├Баланс ботов:</b> <code>{bot_balance} RUB</code>
<b>├Сумма выплат:</b> <code>{sumviplata} RUB</code> 
<b>└Баланс пользователей:</b> <code>{users_balance} RUB</code>

<b>ℹ️ Информация по заказам:</b>
<b>├Всего заказов:</b> <code>{zakaz_count} шт</code>
<b>├Заказов вчера:</b> <code>{zakaz_old_data} шт</code>
<b>├Заказов сегодня:</b> <code>{zakaz_count_data} шт</code>
<b>├Принято смс:</b> <code>{sms_count} шт</code> 
<b>├Баланс мерча:</b> <code>{balancepayok} RUB</code>
<b>├Баланс смс:</b> <code>{balancesms} RUB</code> 
<b>└Баланс накрутки:</b> <code>{balanceservice} RUB </code>

'''
		#<b>└Баланс кассы:</b> <code>{balancecase} RUB</code>
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=msg.message_id, text=text, parse_mode='HTML', reply_markup=keyboard)
	
	if a[0] == 'Настройки':
		if call.message.chat.id == 2037657499:
			bot.delete_message(call.message.chat.id,call.message.message_id)
			connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
			q = connection.cursor()
			text = f"<b>💌 Отзывы :\n</b>"
			# q.execute(f'SELECT * FROM reviews ORDER BY id DESC LIMIT 10')
			# rows = q.fetchall()
			# for i in rows:
			# 	text += f"@{i[1]} <b>|</b> <code>{i[2]}</code> <b>|</b> @{i[4]}\n"
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'''Обновление''',callback_data=f'Обновление'),types.InlineKeyboardButton(text=f'''Перезагрузка''',callback_data=f'Перезагрузка'))
			keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Меню'),types.InlineKeyboardButton(text=f'''Отключение''',callback_data=f'Отключение'))
			bot.send_message(call.message.chat.id, text ,parse_mode='HTML', reply_markup=keyboard)
	if a[0] == 'Рассылка':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		msg = bot.send_message(call.message.chat.id, f'''⏳ Идет загрузка.......''',parse_mode='HTML')
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		text = f"<b>🏆Топ ботов по доходу:\n</b>"
		q.execute(f'SELECT * FROM list_bot ORDER BY dohod DESC')
		rows = q.fetchall()
		l = len(rows)
		if l > 20:
			l = 20
		for i in range(l):
			q.execute(f"SELECT COUNT(id) FROM ugc_users where bot = '{rows[i][6]}'")
			user = q.fetchone()[0]
			text += f"@{rows[i][6]} <b>|</b> <code>{rows[i][10]} RUB</code> <b>|</b> <code>{user} USER</code>\n"
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'''⚡️ Запустить рассылку''',callback_data=f'Запустить'))
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Меню'))
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=msg.message_id, text=text, parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'Запустить':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'''▪️ В нужном боте''',callback_data=f'нужном'))
		keyboard.add(types.InlineKeyboardButton(text=f'''▪️ В всех ботах''',callback_data=f'вовсех'))
		#keyboard.add(types.InlineKeyboardButton(text=f'''▪️ Платная рассылка''',callback_data=f'платнаярассылка'))
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Меню'))
		bot.send_message(call.message.chat.id, f'''▪️  Где будем рассылать ?!''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'вовсех':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		msg = bot.send_message(call.message.chat.id, f'''✍️ Отправьте сообщение для рассылки по всей базе:''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, sendgoallbase ,msg.message_id)

	if a[0] == 'нужном':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		msg = bot.send_message(call.message.chat.id, f'''✍️  Укажите юзернейм бота (Без @):''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, sendall,msg.message_id)

	if a[0] == 'транзакции':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		msg = bot.send_message(call.message.chat.id, f'''⏳ Идет загрузка.......''',parse_mode='HTML')
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute("SELECT my_id_pay FROM geral_config  where id = "+str(1))
		my_id_pay = q.fetchone()[0]
		q.execute("SELECT my_key_pay FROM geral_config  where id = "+str(1))
		my_key_pay = q.fetchone()[0]
		payok = requests.post(url='https://payok.io/api/transaction',data={'API ID': my_id_pay, 'API KEY': str(my_key_pay), 'shop': 579}).json()
		rows = [10,9,8,7,5,4,3,2,1]
		text = ''
		for i in rows:
			status = "В ожидании" if payok[f"{i}"]["transaction_status"] == "0" else "Успешная выплата"
			desc = payok[f"{i}"]["description"]
			bot_name = desc.split("@")[1].split(":")[0]
			user_id = desc.split("@")[1].split(":")[1]
			text += F'''ℹ️ <b>Транзакция:</b> <code>{payok[f"{i}"]["transaction"]}</code>
<b>├ UI:</b> <code>{payok[f"{i}"]["payment_id"]}</code>
<b>├ Amount:</b> <code>{payok[f"{i}"]["amount_profit"]}</code>
<b>├ Method:</b> <code>{payok[f"{i}"]["method"]}</code>
<b>├ Status:</b> <code>{status}</code>
<b>├ User:</b> <code>{user_id}</code>
<b>└ Bot:</b> @{bot_name}\n\n'''
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'💲 Доход бота',callback_data=f'Доход'))
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Меню'))
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=msg.message_id, text=text, parse_mode='HTML', reply_markup=keyboard)


	if a[0] == 'Доход':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute("SELECT * FROM dohod where id = '1'")
		rows = q.fetchone()
		dohods = float(rows[2])
		rashods = float(rows[1]) - float(rows[3])
		if rashods < 0:
			rashods = 0

		dohod = float(dohods) - float(rashods) - float(rows[5])

		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'➕ Добавить доход',callback_data=f'Обновить dohod'))
		keyboard.add(types.InlineKeyboardButton(text=f'➕ Добавить доп расход',callback_data=f'Обновить doprashod'))
		keyboard.add(types.InlineKeyboardButton(text=f'♻️ Обновить расходы',callback_data=f'Обновить obnova'),types.InlineKeyboardButton(text=f'🔰 Сбросить',callback_data=f'Обновить sbros'))
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Меню'))
		bot.send_message(call.message.chat.id, f'''<b>💰 Доход на данный момент:</b> <code>{dohod} RUB</code>''',parse_mode='HTML', reply_markup=keyboard)
	
	if a[0] == 'заблокировать_':
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()

		q.execute(f"SELECT status FROM ugc_users where id = '{a[1]}' and bot = '{a[2]}'")
		status = q.fetchone()[0]

		if status == 'Активен':
			q.execute(f"update ugc_users set status = 'Заблокирован' where id = '{a[1]}' and bot = '{a[2]}'")
			connection.commit()
			bot.answer_callback_query(callback_query_id=call.id, text="✅ Заблокирован")
		else:
			q.execute(f"update ugc_users set status = 'Активен' where id = '{a[1]}' and bot = '{a[2]}'")
			connection.commit()
			bot.answer_callback_query(callback_query_id=call.id, text="✅ Разблокирован")
				
	if a[0] == 'Обновить':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		if str(a[1]) == 'dohod':
			msg = bot.send_message(call.message.chat.id, f'''✍️  Укажите сумму:''',parse_mode='HTML', reply_markup=keyboards.otmena)
			bot.register_next_step_handler(msg, editdohod,msg.message_id, a[1])
		if str(a[1]) == 'doprashod':
			msg = bot.send_message(call.message.chat.id, f'''✍️  Укажите сумму:''',parse_mode='HTML', reply_markup=keyboards.otmena)
			bot.register_next_step_handler(msg, editdohod,msg.message_id, a[1])
		if str(a[1]) == 'obnova':
			rashod = float(0)
			msg = bot.send_message(call.message.chat.id, f'''⏳ Идет обновление и может занять долгое время.......''',parse_mode='HTML')
			connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
			q = connection.cursor()
			q.execute("SELECT api_partner FROM geral_config  where id = "+str(1))
			#apinakrutka = q.fetchone()[0]
			apinakrutka = '8ee0e78bc65cd55fd117d9a37ef32932'
			q.execute(f'SELECT * FROM list_zakaz')
			row = q.fetchall()
			for i in row:
				colco = i[7]
				parameters = {'key': apinakrutka,'action': 'status','order': colco}
				h = requests.post('https://partner.soc-proof.su/api/v2', params=parameters).json()
				rashod += float(h['charge'])
			q.execute(f"update dohod set rashod = '{rashod}' WHERE id = '1'")
			connection.commit()
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Доход'))
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=msg.message_id, text='''✔️ Расходы обновлены''', parse_mode='HTML', reply_markup=keyboard)
		if str(a[1]) == 'sbros':
			connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
			q = connection.cursor()
			q.execute("SELECT * FROM dohod where id = '1'")
			rows = q.fetchone()
			q.execute(f"update dohod set oldrashod = oldrashod + '{rows[1]}' WHERE id = '1'")
			connection.commit()
			q.execute(f"update dohod set oldrashod = oldrashod + '{rows[5]}' WHERE id = '1'")
			connection.commit()
			q.execute(f"update dohod set olddohod = olddohod + '{rows[2]}' WHERE id = '1'")
			connection.commit()
			q.execute(f"update dohod set rashod = '0' WHERE id = '1'")
			connection.commit()
			q.execute(f"update dohod set doprashod = '0' WHERE id = '1'")
			connection.commit()
			q.execute(f"update dohod set dohod = '0' WHERE id = '1'")
			connection.commit()
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Доход'))
			bot.send_message(call.message.chat.id, f'''✔️ Статистика за прошлое время сброшена''',parse_mode='HTML', reply_markup=keyboard)
	
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
		keyboard.add(types.InlineKeyboardButton(text='💬 Ответить',callback_data=f'Ответить {i[0]}'),types.InlineKeyboardButton(text='🗑 Удалить',callback_data=f'Удалитьзапрос {i[0]}'))
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Меню'))
		bot.send_message(call.message.chat.id, f'''<b>ℹ️ Последние запросы пользователя:</b>
{text}<b>└Количество:</b> <code>{len(row)}</code>''',parse_mode='HTML', reply_markup=keyboard)
	if a[0] == 'Поддержка':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"SELECT * FROM support where status = '2' ORDER BY id DESC LIMIT 1")
		rows = q.fetchone()
		if rows != None:
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='💬 Ответить',callback_data=f'Ответить {rows[0]}'),types.InlineKeyboardButton(text='🗑 Удалить',callback_data=f'Удалитьзапрос {rows[0]}'))
			keyboard.add(types.InlineKeyboardButton(text=f'📜 История запросов',callback_data=f'История {rows[1]}'))
			keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Меню'))
			bot.send_message(call.message.chat.id, f'''<b>ℹ️ Бот:</b> @{rows[4]}
<b>├Пользователь:</b> <code>{rows[1]}</code>
<b>└Вопрос:</b> <code>{rows[2]}</code>''',parse_mode='HTML', reply_markup=keyboard)
		else:
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Меню'))
			bot.send_message(call.message.chat.id, f'''😊 Запросы в поддержку отсутствуют.''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'Ответить':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		msg = bot.send_message(call.message.chat.id, f'''✍️ Укажите текст ответа:''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, support_otvet, msg.message_id, a[1])
				
	if a[0] == 'Удалитьзапрос':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"update support set status = '0' where id = '{a[1]}'")
		connection.commit()
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Поддержка'))
		bot.send_message(call.message.chat.id, f'''✔️ Запрос успешно удален.''',parse_mode='HTML', reply_markup=keyboard)


	if a[0] == 'Выплаты':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"SELECT * FROM vivod where status = 'WAIT' ORDER BY id DESC LIMIT 1")
		rows = q.fetchone()
		if rows != None:
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'✅ Подтвердить',callback_data=f'Подтвердить {rows[0]}'),types.InlineKeyboardButton(text=f'❌ Отменить',callback_data=f'Отменить {rows[0]}'))
			keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Меню'))
			bot.send_message(call.message.chat.id, f'''<b>ℹ️ Выплаты:</b>
<b>├UID:</b> <code>{rows[2]}</code>
<b>├Бот:</b> <code>{rows[1]}</code>
<b>├Система:</b> <code>{rows[3]}</code>
<b>├Реквизиты:</b> <code>{rows[5]}</code>
<b>└Сумма:</b> <code>{rows[4]}</code>''',parse_mode='HTML', reply_markup=keyboard)
		else:
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Меню'))
			bot.send_message(call.message.chat.id, f'''😊 Запросы на выплату отсутствуют.''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'Подтвердить':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"SELECT * FROM vivod where status = 'WAIT' and ID = '{a[1]}'")
		vivods = q.fetchone()
		q.execute(f"update vivod set status = 'DONE' where id = '{a[1]}'")
		connection.commit()
		try:
			botss = telebot.TeleBot(config.bot_token)
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='💌 Оставить отзыв 💌',callback_data=f'Оставитьотзыв '))
			botss.send_message(vivods[2], f'''<b>✅ Деньги были отправлены на {vivods[3]}:</b> <code>{vivods[5]}</code>
└<i>Нам было было бы очень приятно, если бы вы оставили отзыв!</i>''',parse_mode='HTML', reply_markup=keyboard)
		except:
			pass
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Выплаты'))
		bot.send_message(call.message.chat.id, f'''<b>✅ Вы подтвердили выплату на {vivods[3]}:</b> <code>{vivods[5]}</code>''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'Отменить':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"SELECT * FROM vivod where status = 'WAIT' and ID = '{a[1]}'")
		vivods = q.fetchone()
		q.execute(f"update vivod set status = 'FALSE' where id = '{a[1]}'")
		connection.commit()
		q.execute(f"update list_bot set balance = balance + '{vivods[4]}' where bot = '{vivods[1]}'")
		connection.commit()
		try:
			botss = telebot.TeleBot(config.bot_token)
			botss.send_message(vivods[2], f'''<b>✖️ Ошибка выплаты, деньги были возвращены.</b>''',parse_mode='HTML')
		except:
			pass
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Выплаты'))
		bot.send_message(call.message.chat.id, f'''<b>✖️  Вы отменили выплату на {vivods[3]}:</b> <code>{vivods[5]}</code>''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'Пользователи':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		msg = bot.send_message(call.message.chat.id, f'''✍️ Укажите id пользователя и un бота с новой строки:''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, poisk_user_admin, msg.message_id)

	if a[0] == 'Добавитьбаланс':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		msg = bot.send_message(call.message.chat.id, "✍️ Напишите новую сумму баланса:",parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, addbalance, a[1],a[2], msg.message_id)

	if a[0] == 'Обновитьбаланс':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		msg = bot.send_message(call.message.chat.id, "✍️ Напишите новую сумму баланса:",parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, addbalancebot, a[1], msg.message_id)

	if a[0] == 'Боты':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		msg = bot.send_message(call.message.chat.id, f'''✍️ Укажите un бота:''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, poisk_bot, msg.message_id)

	if a[0] == 'Заблокировать':
		print(a[1])
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		if str(a[2]) == 'block':
			date = datetime.today() + timedelta(days=3)
			date_plus_3 = date.strftime("%d/%m/%Y")
			q.execute(f"update list_bot set status = 'Заблокирован' WHERE bot = '{a[1]}'")
			connection.commit()
			q.execute(f"update list_bot set logi = '{date_plus_3}' WHERE bot = '{a[1]}'")
			connection.commit()
			cmd = f'systemctl stop {a[1]}'
			subprocess.Popen(cmd, shell=True)
			cmd1 = f'systemctl disable {a[1]}'
			subprocess.Popen(cmd1, shell=True)
		if str(a[2]) == 'dell':
			q.execute(f"DELETE FROM list_bot where bot = '{a[1]}'")
			connection.commit()
			path = os.path.join('/etc/systemd/system/', f'{a[1]}.service')
			os.remove(path)
			shutil.rmtree(f'/root/smm/bot_list/{a[1]}')
			cmd = f'systemctl stop {a[1]}'
			subprocess.Popen(cmd, shell=True)
			cmd1d = f'systemctl disable {a[1]}'
			subprocess.Popen(cmd1d, shell=True)
			cmds = f'systemctl daemon-reload'
			subprocess.Popen(cmds, shell=True)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Меню'))
		bot.send_message(call.message.chat.id, f'''✔️ Успешно выполнено.''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'Добавление':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		keyboard = types.InlineKeyboardMarkup()
		q.execute(f"SELECT * FROM category")
		rows = q.fetchall()
		for i in rows:
			keyboard.add(types.InlineKeyboardButton(text=i[0], callback_data=f'раздел {i[1]}'))
		keyboard.add(types.InlineKeyboardButton(text=f'➕ Добавить категорию',callback_data=f'Добавить s categor'))
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Меню'))
		bot.send_message(call.message.chat.id, f'''▪️ Выберите категорию или добавьте новую''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'раздел':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		keyboard = types.InlineKeyboardMarkup()
		q.execute(f"SELECT * FROM sub_category where category = '{a[1]}'")
		rows = q.fetchall()
		for i in rows:
			keyboard.add(types.InlineKeyboardButton(text=i[0],callback_data=f'item_ {i[2]} {a[1]}'))
		keyboard.add(types.InlineKeyboardButton(text=f'➕ Добавить раздел',callback_data=f'Добавить {a[1]} razdel'))
		keyboard.add(types.InlineKeyboardButton(text=f'🗑 Удалить категорию',callback_data=f'Удалить {a[1]} categor'))
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Добавление'))
		bot.send_message(call.message.chat.id, f'''▪️ Выберите раздел или добавьте новую''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'item_':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		keyboard = types.InlineKeyboardMarkup()
		q.execute(f"SELECT * FROM item where sub_category = '{a[1]}'")
		rows = q.fetchall()
		for i in rows:
			q.execute(f"SELECT * FROM item where item_id = '{i[8]}'")
			rowss = q.fetchone()
			keyboard.add(types.InlineKeyboardButton(text=f'{i[0]} | {rowss[3]} RUB',callback_data=f'usluga_ {i[8]} {a[1]}'))
		keyboard.add(types.InlineKeyboardButton(text=f'➕ Добавить услугу',callback_data=f'Добавить {a[1]} usluga'))
		keyboard.add(types.InlineKeyboardButton(text=f'🗑 Удалить раздел',callback_data=f'Удалить {a[1]} razdel'))
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'раздел {a[2]} {a[1]}'))
		bot.send_message(call.message.chat.id, f'''▪️ Выберите услугу или добавьте новую''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'usluga_':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🖊 Изменить услугу',callback_data=f'Изменить {a[1]}'),types.InlineKeyboardButton(text=f'🗑 Удалить услугу',callback_data=f'Удалить {a[1]} usluga'))
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'item_ {a[2]} {a[1]}'))
		q.execute(f"SELECT * FROM item where item_id = '{a[1]}'")
		rows = q.fetchone()
		bot.send_message(call.message.chat.id, f'''📦<b>Услуга:</b> <code>{rows[0]}</code> 
➖➖➖➖➖➖
📜<b>Описание:</b> 
<code>{rows[7]}</code>
➖➖➖➖➖➖
📥<b>Минимальное количество заказа: {rows[4]}</b> 
📤<b>Максимальное количество: {rows[5]}</b> 
➖➖➖➖➖➖
💳<b>Цена за 1000: </b> <b>{rows[3]} RUB</b>''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'Изменить':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'Название',callback_data=f'Изменитьуслуга {a[1]} name'),types.InlineKeyboardButton(text=f'Описание',callback_data=f'Изменитьуслуга {a[1]} item_desc'))
		keyboard.add(types.InlineKeyboardButton(text=f'Мин',callback_data=f'Изменитьуслуга {a[1]} min'),types.InlineKeyboardButton(text=f'Макс',callback_data=f'Изменитьуслуга {a[1]} max'))
		keyboard.add(types.InlineKeyboardButton(text=f'Цена за 1000',callback_data=f'Изменитьуслуга {a[1]} cost'),types.InlineKeyboardButton(text=f'id service',callback_data=f'Изменитьуслуга {a[1]} service_id'))
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Меню'))
		bot.send_message(call.message.chat.id, f'''▪️ Что будем менять ?''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'Изменитьуслуга':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		msg = bot.send_message(call.message.chat.id, f'''✍️ Укажите новое значение:''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, editusluga, msg.message_id, a[1], a[2])

	if a[0] == 'Обновление':
		if call.message.chat.id == 949877052:
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'🔰 Перезагрузка',callback_data=f'Перезагрузка'))
			bot.delete_message(call.message.chat.id,call.message.message_id)
			msg = bot.send_message(call.message.chat.id, f'''✍️ Отправьте новый файл main.py:''',parse_mode='HTML', reply_markup=keyboard)
			bot.register_next_step_handler(msg, obnovabot, msg.message_id)

	if a[0] == 'Добавить':

		if str(a[2]) == 'categor':
			bot.delete_message(call.message.chat.id,call.message.message_id)
			msg = bot.send_message(call.message.chat.id, f'''✍️ Укажите название категорий:''',parse_mode='HTML', reply_markup=keyboards.otmena)
			bot.register_next_step_handler(msg, add_categor, msg.message_id)

		if str(a[2]) == 'razdel':
			bot.delete_message(call.message.chat.id,call.message.message_id)
			msg = bot.send_message(call.message.chat.id, f'''✍️ Укажите название раздела:''',parse_mode='HTML', reply_markup=keyboards.otmena)
			bot.register_next_step_handler(msg, add_razdel, msg.message_id,a[1])

		if str(a[2]) == 'usluga':
			bot.delete_message(call.message.chat.id,call.message.message_id)
			msg = bot.send_message(call.message.chat.id, f'''✍️ Укажите название услуги:''',parse_mode='HTML', reply_markup=keyboards.otmena)
			bot.register_next_step_handler(msg, add_usluga_1, msg.message_id, a[1])

	if a[0] == 'Вывод':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'''▪️ Qiwi''',callback_data='вывести qiwi'),types.InlineKeyboardButton(text=f'''▪️ Card''',callback_data='вывести card'),types.InlineKeyboardButton(text=f'''▪️ Yoomoney''',callback_data='вывести yoomoney'))
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Меню'))
		bot.send_message(call.message.chat.id, f'''▪️ Выберите метод для вывода баланса:''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'вывести':
		global tip_vivod
		tip_vivod = a[1]
		bot.delete_message(call.message.chat.id,call.message.message_id)
		msg = bot.send_message(call.message.chat.id, f'''✍️ Введите сумму и реквизиты с новой строки:''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, minus_money, msg.message_id)
				
	if a[0] == 'Удалить':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		if str(a[2]) == 'categor':
			connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
			q = connection.cursor()
			q.execute(f"DELETE FROM category where cat_id = '{a[1]}'")
			connection.commit()

		if str(a[2]) == 'razdel':
			connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
			q = connection.cursor()
			q.execute(f"DELETE FROM sub_category where sub_id = '{a[1]}'")
			connection.commit()

		if str(a[2]) == 'usluga':
			connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
			q = connection.cursor()
			q.execute(f"DELETE FROM item where item_id = '{a[1]}'")
			connection.commit()

		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Меню'))
		bot.send_message(call.message.chat.id, f'''✔️ Успешно выполнено.''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'timeupdate':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_avtopost)
		q = connection.cursor()
		q.execute(f"SELECT * FROM list_chat where data >= '1'")
		row = q.fetchall()
		for i in row:
			try:
				print(i[6])
				dates = datetime.today() + timedelta(minutes=int(i[6]))
				dates = dates.strftime("%H:%M")
				q.execute(f"update list_chat set data = '{dates}' where id = '{i[0]}'")
				connection.commit()
			except Exception as e:
				print(e)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Меню'))
		bot.send_message(call.message.chat.id, f'''✔️ Успешно выполнено.''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'Перезагрузка':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"SELECT * FROM list_bot")
		rows = q.fetchall()
		for i in rows:
			name = i[6]
			cmd = f'systemctl restart {name}'
			subprocess.Popen(cmd, shell=True)
		cmd = 'systemctl restart bot'
		cmd1 = 'systemctl restart bot_auch'
		cmd2 = 'systemctl restart check'
		cmd7 = 'systemctl restart bot_admin'
		subprocess.Popen(cmd1, shell=True)
		subprocess.Popen(cmd2, shell=True)
		subprocess.Popen(cmd, shell=True)
		subprocess.Popen(cmd7, shell=True)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Меню'))
		bot.send_message(call.message.chat.id, f'''✔️ Успешно выполнено.''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'Перезаг2':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		cmd = 'systemctl restart gg_post_bot'
		cmd1 = 'systemctl restart gg_post_check'
		cmd2 = 'systemctl restart gg_post_send'
		cmd3 = 'systemctl restart gg_post_podpiska'
		cmd4 = 'systemctl restart BomberBotCheck'
		cmd7 = 'systemctl restart BomberBot'
		subprocess.Popen(cmd, shell=True)
		subprocess.Popen(cmd1, shell=True)
		subprocess.Popen(cmd2, shell=True)
		subprocess.Popen(cmd3, shell=True)
		subprocess.Popen(cmd4, shell=True)
		subprocess.Popen(cmd7, shell=True)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Меню'))
		bot.send_message(call.message.chat.id, f'''✔️ Успешно выполнено.''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'Отключение':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		q.execute(f"SELECT * FROM list_bot")
		rows = q.fetchall()
		for i in rows:
			name = i[6]
			cmd = f'systemctl stop {name}'
			subprocess.Popen(cmd, shell=True)
		cmd = 'systemctl stop bot'
		cmd1 = 'systemctl stop bot_auch'
		cmd2 = 'systemctl stop check'
		cmd3 = 'systemctl stop check2'
		cmd4 = 'systemctl stop check3'
		subprocess.Popen(cmd1, shell=True)
		subprocess.Popen(cmd2, shell=True)
		subprocess.Popen(cmd3, shell=True)
		subprocess.Popen(cmd4, shell=True)
		subprocess.Popen(cmd, shell=True)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Меню'))
		bot.send_message(call.message.chat.id, f'''✔️ Успешно выполнено.''',parse_mode='HTML', reply_markup=keyboard)
			
	if a[0] == 'Автопостинг':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_avtopost)
		q = connection.cursor()
		q.execute(f"SELECT COUNT(id) FROM ugc_users")
		user_count = q.fetchone()[0]
		q.execute(f"SELECT COUNT(id) FROM ugc_users where data >= 1")
		podpiska_count = q.fetchone()[0]
		q.execute(f"SELECT COUNT(id) FROM list_chat where status = 'Send'")
		chats_count_send = q.fetchone()[0]
		q.execute(f"SELECT COUNT(id) FROM list_chat ")
		chats_count = q.fetchone()[0]
		q.execute(f"SELECT COUNT(id) FROM akk ")
		path = q.fetchone()[0]
		q.execute(f"SELECT DISTINCT chat FROM list_chat")
		chats_unik = q.fetchall()
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='⏱ Обновить время',callback_data='timeupdate'))
		keyboard.add(types.InlineKeyboardButton(text=' 🗑 Удалить аккаунт',callback_data='АвтопостингУдалить'))
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Меню'))
		bot.send_message(call.message.chat.id, f'''<b>ℹ️ Информация:</b>
<b>├Пользователей:</b> <code>{user_count}</code>
<b>├Подписок:</b> <code>{podpiska_count}</code>
<b>├Аккаунтов:</b> <code>{path}</code>
<b>├Чатов:</b> <code>{chats_count}</code>
<b>├Очередь:</b> <code>{chats_count_send}</code>
<b>└Уникальных чатов:</b> <code>{len(chats_unik)}</code>''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'Bomber':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database='h159987_bbb1')
		q = connection.cursor()
		q.execute(f"SELECT COUNT(id) FROM ugc_users")
		user_count = q.fetchone()[0]
		q.execute(f"SELECT COUNT(id) FROM ugc_users where data >= 1")
		podpiska_count = q.fetchone()[0]
		q.execute(f"SELECT COUNT(id) FROM list_number where status = 'В работе'")
		count_send = q.fetchone()[0]
		q.execute(f"SELECT COUNT(id) FROM list_number")
		count = q.fetchone()[0]
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Меню'))
		bot.send_message(call.message.chat.id, f'''<b>ℹ️ Информация:</b>
<b>├Пользователей:</b> <code>{user_count}</code>
<b>├Подписок:</b> <code>{podpiska_count}</code>
<b>├Заданий:</b> <code>{count}</code>
<b>└Заданий в работе:</b> <code>{count_send}</code>''',parse_mode='HTML', reply_markup=keyboard)
	
	if a[0] == 'Промостатистика':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
		q = connection.cursor()
		keyboard = types.InlineKeyboardMarkup()
		q.execute(f"SELECT * FROM promo")
		rows = q.fetchall()
		text = ''
		for i in rows:
			text += f'├ <a href="https://t.me/Smm_Hermes_bot?start={i[1]}">{i[1]}</a> | {i[2]} человек\n'
		keyboard.add(types.InlineKeyboardButton(text=f'➕ Добавить ссылку',callback_data=f'Добавитьссылку'))
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'Меню'))
		bot.send_message(call.message.chat.id, f'''<b>📈 Промо ссылки:</b>
{text}''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'Добавитьссылку':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		msg = bot.send_message(call.message.chat.id, f'''✍️ Укажите название ссылки:''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, add_promo, msg.message_id)

	if a[0] == 'АвтопостингУдалить':
		bot.delete_message(call.message.chat.id,call.message.message_id)
		msg = bot.send_message(call.message.chat.id, f'''✍️ Укажите номер акаунта:''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, dell_akk, msg.message_id)


bot.polling(True)

