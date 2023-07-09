# -*- coding: utf-8 -*-
from decimal import *
import telebot
from telebot import types, apihelper
import random, string
import time
import os,random,shutil,subprocess
import json
import keyboards
import requests
from datetime import datetime, timedelta,date
import config
from mysql.connector import connect, Error

bot = telebot.TeleBot(config.bot_token)

# Слито в end_soft

def proverkatoken():
	connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
	q = connection.cursor()
	q.execute(f"SELECT COUNT(id) FROM vivod where status = 'WAIT'")
	sut_count = q.fetchone()[0]
	if sut_count >= 1:
# Слито в end_soft
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='✖️ Закрыть',callback_data=f'Закрыть '))
		bot.send_message(5887700524,f'''❗️ У вас {sut_count} новых выплат.''',parse_mode='HTML', reply_markup=keyboard)

	q.execute(f"SELECT * FROM list_bot")
	rows = q.fetchall()
	for i in rows:
		try:
# Слито в end_soft
			q.execute(f"SELECT COUNT(id) FROM support where bot = '{i[6]}' and status = '1'")
			support_count = q.fetchone()[0]
			if support_count >= 1:
				try:
					keyboard = types.InlineKeyboardMarkup()
					keyboard.add(types.InlineKeyboardButton(text='✖️ Закрыть',callback_data=f'Закрыть '))
					bot.send_message(i[1],f'''❗️ У вас {support_count} новых обращений в поддержку.''',parse_mode='HTML', reply_markup=keyboard)
				except:
					pass
		except:
			pass

def check_bot():
	date = datetime.today() - timedelta(days=3)
	date_minus_3 = date.strftime("%d/%m/%Y")
	date = datetime.today() + timedelta(days=7)
	date_plus_3 = date.strftime("%d/%m/%Y")
	date = datetime.today()
	date_today = date.strftime("%d/%m/%Y")
	connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
	q = connection.cursor()
	q.execute(f"SELECT * FROM list_bot")
	rows = q.fetchall()
	for i in rows:
		try:
			name = i[6]
			user = i[1]
			status = i[8]
			date_create = i[9]
			if status == 'Работает':
				if str(date_create) == str(date_minus_3):
					q.execute(f"update list_bot set status = 'Заблокирован' WHERE bot = '{name}'")
					connection.commit()
					q.execute(f"update list_bot set logi = '{date_plus_3}' WHERE bot = '{name}'")
					connection.commit()
					cmd = f'systemctl stop {name}'
					subprocess.Popen(cmd, shell=True)
					cmd1d = f'systemctl disable {name}'
					subprocess.Popen(cmd1d, shell=True)
					bot.send_message(-1001799352145,f'''<b>🟧 Блокировка:</b>
<b>├Бот:</b> @{name}
<b>└Причина:</b> <code>Нет заказов более 3х дней</code>''',parse_mode='HTML')

					bot.send_message(user,f'''<b>🟧 Блокировка:</b>
<b>├Бот:</b> @{name}
<b>└Причина:</b> <code>Нет заказов более 3х дней</code>''',parse_mode='HTML')
				else:
					pass	
			else:
				pass
		except:
			pass



while True:
	try:
		proverkatoken()
	except:
		pass
	try:
		check_bot()
	except:
		pass
	cmd = f'systemctl restart check3'
	subprocess.Popen(cmd, shell=True)
	time.sleep(700)