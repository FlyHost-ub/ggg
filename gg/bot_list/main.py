# -*- coding: utf-8 -*-
from decimal import *
import telebot
import datetime
from telebot import types, apihelper
from telebot.apihelper import ApiTelegramException
import time
import os,random,shutil,subprocess, string
import json
import requests
from datetime import datetime, timedelta
from datetime import date
from dateutil.relativedelta import relativedelta
import hashlib
from mysql.connector import connect, Error
import re
from string import whitespace

from pycrystalpay import CrystalPay
import json
import urllib.request

from pyqiwip2p import QiwiP2P

qiwi_p2p_token = 'eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6ImtjeWF2dS0wMCIsInVzZXJfaWQiOiI3OTUyMjY5MjM4OCIsInNlY3JldCI6ImI0ZTUxNGNkZWYxY2JkOGRmYzZhNDI2YWZkYWRlM2NiYmY4NDI1ZjUyM2ZhYjkwOGY1ZWRmY2FmODcwZDdjM2EifX0='
p2p = QiwiP2P(auth_key=qiwi_p2p_token)


bd_host = '91.227.16.15'
bd_login = 'h162659_fran'
bd_pass = 'kQ0rY7fM7jnD1l'
bd_base = 'h162659_franshiza'

botnames = os.path.basename(os.path.abspath(os.path.dirname(__file__)))
connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
q = connection.cursor()
q.execute(f'SELECT bot_token FROM list_bot WHERE bot = "{botnames}"')
bot_token = q.fetchone()[0]
bot = telebot.TeleBot(bot_token)
bot_name = bot.get_me().username
q.execute(f'SELECT bot_token FROM list_bot WHERE bot = "{botnames}"')
#bot_create = q.fetchone()[0]
connection.close()
#bot_create = telebot.TeleBot(bot_create)
users_zadanie = []
bot = telebot.TeleBot(bot_token)

bot_name = bot.get_me().username

print(bot_name)

def is_subscribed(user_id):
	try:
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
		q = connection.cursor()
		q.execute(f'SELECT chanel_id FROM chanel WHERE bot = "{bot_name}"')
		row = q.fetchone()
		connection.close()
		if row != None:
			try:
				invite_link =  bot_create.create_chat_invite_link(chat_id = row[0], member_limit = 1).invite_link
			except:
				return True
			status = ['creator', 'administrator', 'member','restricted']
			for i in status:
				if i == bot_create.get_chat_member(row[0], user_id).status:
					return True
			return False
		else:
			return True

	except ApiTelegramException as e:
		print(e.result_json['description'])
		if e.result_json['description'] == 'Bad Request: user not found':
			return False
		if e.result_json['description'] == 'Bad Request: chat not found':
			return True
		if e.result_json['description'] == 'Forbidden: bot was kicked from the channel chat':
			return True
		if e.result_json['description'] == 'Bad Request: CHAT_ADMIN_REQUIRED':
			return True



@bot.message_handler(commands=['start'])
def start_message(message):
	if message.chat.type == 'private':
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
		q = connection.cursor()
		q.execute(f'SELECT * FROM ugc_users WHERE id = "{message.chat.id}" and bot = "{bot_name}"')
		row = q.fetchall()
		if len(row) == 0:
			data = datetime.now().strftime('%d/%m/%Y')
			q.execute("INSERT INTO ugc_users (id,bot,data,status) VALUES ('%s','%s','%s','%s')"%(message.chat.id,bot_name,data,'Активен'))
			connection.commit()
			if message.text[7:] != '' and message.text[7:] != message.chat.id:
				q.execute(f"update ugc_users set ref = '{message.text[7:]}' where id = {message.chat.id} and bot = '{bot_name}'")
				connection.commit()
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='↗️ Ознакомиться ',url=f'https://telegra.ph/Pravila--Usloviya-01-25'))
			keyboard.add(types.InlineKeyboardButton(text='✔️ Я ознакомился и согласен с правилами сервиса !',callback_data=f'меню '))
			bot.send_message(message.chat.id,f'''<b>❗️ Перед началом использования сервисом пожалуйста ознакомьтесь с условиями и правилами сервиса.</b>''',parse_mode='HTML',reply_markup=keyboard)
		else:
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='🎛 Открыть меню',callback_data=f'меню '))
			bot.send_message(message.chat.id, '''Привет 👋
Используй меню, чтобы со мной общаться 💬''' ,parse_mode='HTML',reply_markup=keyboard)

		if str(message.text[7:]) == str(f'sendall'):
			q.execute(f'SELECT user FROM list_bot WHERE bot = "{bot_name}"')
			bot_admin = q.fetchone()[0]
			if  message.chat.id == bot_admin:
				users_zadanie.append(message.chat.id)
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='✖️ Отмена',callback_data=f'Закрыть '))
				msg = bot.send_message(message.chat.id, "✍️<b>Напишите текст для рассылки:</b>",parse_mode='HTML')
				bot.register_next_step_handler(msg, sendall, msg.message_id)
			else:
				pass
		else:
			pass
		connection.close()

def sendall(message,idsms):
	if message.chat.id in users_zadanie:
		bot.delete_message(message.chat.id,message.message_id)
		bot.delete_message(message.chat.id,idsms)
		sends = 0
		erors = 0
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'✖️ Закрыть',callback_data=f'Закрыть '))
		msg = bot.send_message(message.chat.id, '''⏳ Идет рассылка...''', reply_markup=keyboard)
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
		q = connection.cursor()
		q.execute(f'SELECT * FROM ugc_users WHERE bot = "{bot_name}"')
		row = q.fetchall()
		for i in row:
			time.sleep(0.1)
			if message.content_type == 'text':
				try:
					bot.send_message(i[0], message.text ,entities = message.entities, reply_markup=keyboard)
					sends += 1
				except:
					erors += 1
			elif message.content_type == 'photo':
				try:
					
					bot.send_photo(i[0],message.photo[0].file_id, message.caption ,caption_entities = message.caption_entities, reply_markup=keyboard)
					sends += 1
				except:
					erors += 1
		bot.send_message(message.chat.id, f'''<b>📈 Рассылка завершена</b>:
<b>├Доставленно:</b> <code>{sends}</code>
<b>└Ошибки:</b> <code>{erors}</code>\n\n''',parse_mode='HTML', reply_markup=keyboard)
	else:
		bot.delete_message(message.chat.id,message.message_id)

@bot.message_handler(content_types=['text'])
def send_text(message):
	if message.chat.type == 'private':
		bot.delete_message(message.chat.id,message.message_id)
		try:
			bot.delete_message(message.chat.id,message.message_id - 1)
		except:
			pass
		hideBoard = types.ReplyKeyboardRemove()
		msg = bot.send_message(message.chat.id, f'''⏳ Обновляем меню.......''', reply_markup=hideBoard)
		bot.delete_message(message.chat.id,msg.message_id)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='🎛 Открыть меню',callback_data=f'меню '))
		bot.send_message(message.chat.id, '''❗️ Внимание, вероятнее всего, была введена неверная команда!''',parse_mode='HTML', reply_markup=keyboard)
	else:
		pass


def supportadd(message,msdids):
	if message.chat.id in users_zadanie:
		bot.delete_message(message.chat.id,message.message_id)
		bot.delete_message(message.chat.id, msdids)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'меню '))
		try:
			connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
			q = connection.cursor()
			q.execute("INSERT INTO support (user,text,status,bot) VALUES ('%s', '%s', '%s', '%s')"%(message.chat.id,message.text,'1',bot_name))
			connection.commit()
			connection.close()
			bot.send_message(message.chat.id, '''✔️ Сообщение успешно отправлено в поддержку и в скорем времени будет рассмотрено.''', reply_markup=keyboard)
		except:
			bot.send_message(message.chat.id, f'''❗️ Ошибка отправки запроса.''',parse_mode='HTML',reply_markup=keyboard)
	else:
		bot.delete_message(message.chat.id,message.message_id)


def order_status(order_id):
    connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
    q = connection.cursor()
    q.execute("SELECT api_partner FROM geral_config  where id = '1'")
    apinakrutka = q.fetchone()[0]
    connection.close()
    s = requests.Session()
    parameters = {
        'key': apinakrutka,
        'action': 'status',
        'order': order_id
    }
    h = s.post('https://partner.soc-proof.su/api/v2', params=parameters)
    return h.json()

def statuszakaz(message,msdids):
	if message.chat.id in users_zadanie:
		bot.delete_message(message.chat.id,message.message_id)
		bot.delete_message(message.chat.id, msdids)
		order = order_status(message.text)
		if order.get("error"):
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'заказы'))
			bot.send_message(message.chat.id,f'''<b>❗️ Заказа с данным ID не существует:
└Попробуйте еще раз.</b>''',parse_mode="HTML", reply_markup=keyboard)
		else:
			print(order['status'])
			keyboard = types.InlineKeyboardMarkup()
			try:
				if order['status'] == 'Pending':
					status = "Ожидание"

				if order['status'] == 'In progress':
					status = "В работе"

				if order['status'] == 'Processing':
					status = "В очереди"

				if order['status'] == 'Completed':
					status = "Завершён"

				if order['status'] == 'Canceled':
					keyboard.add(types.InlineKeyboardButton(text=f'''❗️ Возможные ошибки''',url=f'https://telegra.ph/Informaciya-po-zakazam-01-25'))
					status = "Завершён с ошибкой"
					
				if order['status'] == 'Partial':
					keyboard.add(types.InlineKeyboardButton(text=f'''❗️ Возможные ошибки''',url=f'https://telegra.ph/Informaciya-po-zakazam-01-25'))
					status = "Завершён с ошибкой"
			except:
				keyboard.add(types.InlineKeyboardButton(text=f'''❗️ Возможные ошибки''',url=f'https://telegra.ph/Informaciya-po-zakazam-01-25'))
				status = "Завершён с ошибкой"
			keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'меню'))
			bot.send_message(message.chat.id, f'''<b>ℹ️ Информация по заказу:</b>
├<b>ID заказа:</b> <code>{message.text}</code>
├<b>Статус заказа:</b> <code>{status}</code>
└<b>Осталось:</b> <code>{order['remains']}</code>''', parse_mode="HTML" ,reply_markup=keyboard)
	else:
		bot.delete_message(message.chat.id,message.message_id)

def generator_pw():
    pwd =  string.digits
    return "".join(random.choice(pwd) for x in range(random.randint(10, 16)))

def cupon_aktiv(message,msdids):
	if message.chat.id in users_zadanie:
		bot.delete_message(message.chat.id,message.message_id)
		bot.delete_message(message.chat.id, msdids)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'профиль '))
		try:
			connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
			q = connection.cursor()
			chat_id = f'{message.chat.id}'
			q.execute(f'SELECT * FROM cupon WHERE name = "{message.text}"')
			row = q.fetchone()
			if row != None:
				id_cupon = row[0]
				ostatok_cupon = row[3]
				summa_cupon = row[2]
				user_list = row[4].replace('\r', "").split('\n')
				if ostatok_cupon >= 1:
					if chat_id in user_list:
						bot.send_message(message.chat.id, f'🙁 Промокод был недействительным или мы не одобрили его использование.',parse_mode='HTML', reply_markup=keyboard)
					else:
						q.execute(f"update cupon set colvo = colvo - 1 where id = '{id_cupon}'")
						connection.commit()
						user_list = f'{row[4]}\n{chat_id}'
						q.execute(f"update cupon set user = '{user_list}' where id = '{id_cupon}'")
						connection.commit()
						q.execute(f"update ugc_users set balance = balance + '{summa_cupon}' where id = '{message.chat.id}' and bot = '{bot_name}'")
						connection.commit()
						connection.close()
						bot.send_message(message.chat.id, f'✔️ Баланс пополнен на {summa_cupon} RUB',parse_mode='HTML', reply_markup=keyboard)
				else:
					connection.close()
					bot.send_message(message.chat.id, f'🙁 Промокод был недействительным или мы не одобрили его использование.',parse_mode='HTML', reply_markup=keyboard)
			else:
				connection.close()
				bot.send_message(message.chat.id, f'🙁 Промокод был недействительным или мы не одобрили его использование.',parse_mode='HTML', reply_markup=keyboard)
		except:
			connection.close()
			bot.send_message(message.chat.id, f'🙁 Промокод был недействительным или мы не одобрили его использование.',parse_mode='HTML', reply_markup=keyboard)
	else:
		bot.delete_message(message.chat.id,message.message_id)

def btc_oplata_2(message):
		try:
			if int(message.text) >= int(1):
				connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
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
				keyboard.add(types.InlineKeyboardButton(text=f'''🦋Проверить платеж''',callback_data=f'check_opl2'))
				keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'профиль '))
				bot.send_message(message.chat.id, '''❗️ Для пополнения баланса, перейдите по ссылке  ниже и оплатите счет удобным способом !

💡 После оплаты, вы получите уведомление о зачисление средств на баланс.''', reply_markup=keyboard)
			else:
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'профиль '))
				bot.send_message(message.chat.id, f'❗️ Минимальная сумма пополнения 10 RUB',parse_mode='HTML')
		except:
			bot.send_message(message.chat.id, f'❗️ Минимальная сумма пополнения 10 RUB',parse_mode='HTML')

def btc_oplata_1(message):
	keyboard = types.InlineKeyboardMarkup()
	if message.text != '🎛 Меню':
		new_bill = p2p.bill(amount=int(message.text), lifetime=45)
		keyboard.add(types.InlineKeyboardButton(text='💳 Перейти к оплате',url=new_bill.pay_url))
		keyboard.add(types.InlineKeyboardButton(text='✅ Проверить',callback_data=f'Check_Depozit_qiwi_{new_bill.bill_id}'))
		bot.send_message(message.chat.id, '''▪️ Для совершения оплаты перейдите по ссылки из кнопки и совершите оплату счета !
			
⏰ Ссылка актуальна: 45 минут''',parse_mode='HTML', reply_markup=keyboard)
	else:
		bot.send_message(message.chat.id, 'Отменили',parse_mode='HTML', reply_markup=keyboard)

def newpokupka(message,msdids,tovar):
	if message.chat.id in users_zadanie:
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='✖️ Отмена',callback_data=f'Магазин '))
		bot.delete_message(message.chat.id,message.message_id)
		bot.delete_message(message.chat.id, msdids)
		try:
			connection = connect(host=bd_host,user=bd_login,password=bd_pass,database='bot_shop')
			q = connection.cursor()
			keyboard = types.InlineKeyboardMarkup()
			q.execute(f"SELECT * FROM tovar WHERE id = '{tovar}'")
			rowss = q.fetchone()
			colvo_rovar = 0 
			with open (f'/root/smm/tovar/{rowss[5]}') as f: 
				for line in f: 
					if line != '\n': 
						colvo_rovar += 1
			if int(colvo_rovar) >= int(message.text):
				prace = int(message.text) * int(rowss[3])
				connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
				q = connection.cursor()
				q.execute(f"SELECT user FROM list_bot where bot = '{bot_name}'")
				users = q.fetchone()[0]
				q.execute(f"SELECT * FROM ugc_users where id = '{message.chat.id}' and bot = '{bot_name}'")
				balance = q.fetchone()[1]
				if int(prace) <= (balance):
					if colvo_rovar == int(message.text):
						connection = connect(host=bd_host,user=bd_login,password=bd_pass,database='bot_shop')
						q = connection.cursor()
						q.execute(f"DELETE FROM tovar where id = '{tovar}'")
						connection.commit()
						connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
						q = connection.cursor()
					prace_admin = int(prace) / 100 * 80
					tomorrow = datetime.now()
					data = tomorrow.strftime('%d/%m/%Y')
					q.execute("INSERT INTO list_zakaz_shop (user,tovar,colvo,prace,data,bot) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')"%(message.chat.id,rowss[1],message.text,prace_admin,data,bot_name))
					connection.commit()
					q.execute(f"update list_bot set logi = '{data}' WHERE bot = '{bot_name}'")
					connection.commit()
					q.execute(f"update list_bot set balance = balance + '{prace_admin}' where bot = '{bot_name}'")
					connection.commit()
					q.execute(f"update list_bot set dohod = dohod + '{prace_admin}' where bot = '{bot_name}'")
					connection.commit()
					q.execute(f"update ugc_users set balance = balance - '{prace}' where id = '{message.chat.id}' and bot = '{bot_name}'")
					connection.commit()
					count = 0
					while count < int(message.text):
						f=open(f'/root/smm/tovar/{rowss[5]}',encoding='utf8').readlines()
						for i in [0]:
							tovar = f.pop(i)
							tovar = tovar.translate(dict.fromkeys(map(ord, whitespace)))
						doc = open(f'/root/smm/tovar/pokupki/{message.chat.id}_{bot_name}.txt', 'a',encoding='utf8')
						doc.write(f'{rowss[1]} -  {tovar} - {data}\n')
						doc.close()
						docs = open(f'/root/smm/tovar/pokupki/{message.chat.id}_Tovar.txt', 'a')
						docs.write(f'({count}) -  {tovar}\n')
						docs.close()
						with open(f'/root/smm/tovar/{rowss[5]}','w') as F:
							F.writelines(f)
						count += 1

					keyboard = types.InlineKeyboardMarkup()
					keyboard.add(types.InlineKeyboardButton(text='✖️ Закрыть',callback_data=f'Закрыть '))	
					doc = open(f'/root/smm/tovar/pokupki/{message.chat.id}_Tovar.txt', 'rb')
					bot.send_document(message.chat.id, doc, caption='🗂 Ваши купленные товары.',reply_markup=keyboard)
					try:
						bot.send_message(users, f'''<b>Новый покупка:</b> <code>{rowss[1]}</code> <b>| Доход:</b> <code>{prace_admin}</code> <b>RUB</b>''',parse_mode='HTML',reply_markup=keyboard)
					except:
						pass
					doc.close()
					path = os.path.join('/root/smm/tovar/pokupki/', f'{message.chat.id}_Tovar.txt')
					os.remove(path)
					keyboard = types.InlineKeyboardMarkup()
					keyboard.add(types.InlineKeyboardButton(text='💌 Оставить отзыв 💌',callback_data=f'Оставитьотзыв '))
					keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернутся в меню',callback_data=f'меню '))
					connection.close()
					bot.send_message(message.chat.id, f'''<b>❤️ Спасибо, что выбираете нас: </b>
└<i>Нам было было бы очень приятно, если бы вы оставили отзыв!</i>''',parse_mode='HTML',reply_markup=keyboard)
				else:
					connection.close()
					keyboard = types.InlineKeyboardMarkup()
					keyboard.add(types.InlineKeyboardButton(text='💰 Пополнить баланс',callback_data=f'профиль '))
					keyboard.add(types.InlineKeyboardButton(text='✖️ Отмена',callback_data=f'Магазин '))
					bot.send_message(message.chat.id, f'''<b>❗️ Ошибка: пополните баланс до {prace} RUB.</b>''' ,parse_mode='HTML',reply_markup=keyboard)
			else:
				connection.close()
				msg = bot.send_message(message.chat.id, f'''<b>❗️ Ошибка количества, остаток {colvo_rovar} шт.
└Введите количество которое хотите купить:</b>''',parse_mode='HTML',reply_markup=keyboard)
				bot.register_next_step_handler(msg, newpokupka, msg.message_id,tovar)

		except:
			msg = bot.send_message(message.chat.id, f'''<b>❗️ Ошибка количества, вводить нужно целое число.
└Введите количество которое хотите купить:</b>''',parse_mode='HTML',reply_markup=keyboard)
			bot.register_next_step_handler(msg, newpokupka, msg.message_id,tovar)
	else:
		bot.delete_message(message.chat.id,message.message_id)

def newzakaz(message,msdids):
	if message.chat.id in users_zadanie:
		try:
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='✖️ Отмена',callback_data=f'Накрутка '))
			bot.delete_message(message.chat.id,message.message_id)
			bot.delete_message(message.chat.id, msdids)
			colvozakaz = message.text
			connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
			q = connection.cursor()
			q.execute(f"update ugc_users set colvo = '{colvozakaz}' where id = '{message.chat.id}' and bot = '{bot_name}'")
			connection.commit()
			q.execute(f"SELECT * FROM ugc_users where id = '{message.chat.id}' and bot = '{bot_name}'")
			uslugaqid = q.fetchone()
			q.execute(f"SELECT * FROM item where item_id = '{uslugaqid[4]}'")
			rowsss = q.fetchone()
			if int(message.text) >= int(rowsss[4]):
				if int(message.text) <= int(rowsss[5]):
					q.execute(f"SELECT prace FROM list_bot where bot = '{bot_name}'")
					plusprace = q.fetchone()[0]
					praces = float(rowsss[3]) / 1000
					praces2 = float(praces) * float(message.text)
					praces5 = float(rowsss[3]) / 100 * float(plusprace)
					pracesspracess = float(praces2) + float(praces5)
					if float(uslugaqid[4]) >= float(pracesspracess):
						msg = bot.send_message(message.chat.id, f'''<b>📄 Вы ввели количество:</b> <code>{colvozakaz} шт</code> 
<b>├Стоимость:</b> <code>{pracesspracess}</code> <b>RUB</b>
<b>└Введите ссылку:</b>''' ,parse_mode='HTML',reply_markup=keyboard)
						bot.register_next_step_handler(msg, newzakaz1 , msg.message_id)
					else:
						connection.close()
						keyboard = types.InlineKeyboardMarkup()
						keyboard.add(types.InlineKeyboardButton(text='💰 Пополнить баланс',callback_data=f'профиль '))
						keyboard.add(types.InlineKeyboardButton(text='✖️ Отмена',callback_data=f'Накрутка '))
						bot.send_message(message.chat.id, f'''<b>❗️ Ошибка: пополните баланс до {pracesspracess} RUB.</b>''' ,parse_mode='HTML',reply_markup=keyboard)
				else:
					connection.close()
					msg = bot.send_message(message.chat.id, f'''<b>❗️ Ошибка: <code>Максимальное количество {rowsss[5]} шт</code>
└Введите количество которое хотите купить:</b>''' ,parse_mode='HTML',reply_markup=keyboard)
					bot.register_next_step_handler(msg, newzakaz, msg.message_id)
			else:
				connection.close()
				msg = bot.send_message(message.chat.id, f'''<b>❗️ Ошибка: <code>Минимальное количество {rowsss[4]} шт</code>
└Введите количество которое хотите купить:</b>''' ,parse_mode='HTML',reply_markup=keyboard)
				bot.register_next_step_handler(msg, newzakaz, msg.message_id)
		except Exception as e:
			print(e)
			msg = bot.send_message(message.chat.id, f'''<b>❗️ Ошибка количества, вводить нужно целое число.
└Введите количество которое хотите купить:</b>''',parse_mode='HTML',reply_markup=keyboard)
			bot.register_next_step_handler(msg, newzakaz, msg.message_id)
	else:
		bot.delete_message(message.chat.id,message.message_id)

def newzakaz1(message, msdids):
	if message.chat.id in users_zadanie:
		try:
			bot.delete_message(message.chat.id,message.message_id)
			bot.delete_message(message.chat.id, msdids)
			connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
			q = connection.cursor()
			q.execute(f"update ugc_users set link = '{message.text}' where id = '{message.chat.id}' and bot = '{bot_name}'")
			connection.commit()
			q.execute(f"SELECT * FROM ugc_users where id = '{message.chat.id}' and bot = '{bot_name}'")
			uslugaqid = q.fetchone()
			q.execute(f"SELECT * FROM item where item_id = '{uslugaqid[4]}'")
			rowsss = q.fetchone()
			q.execute(f"SELECT prace FROM list_bot where bot = '{bot_name}'")
			plusprace = q.fetchone()[0]
			pracess = Decimal(rowsss[5]) / 100 * Decimal(plusprace)
			praces = Decimal(rowsss[5]) + Decimal(pracess)
			pracesspracess = Decimal(praces) / 1000 * Decimal(uslugaqid[4])
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'''✅ Заказать''',callback_data='Заказать'),types.InlineKeyboardButton(text=f'''🚫 Отменить''',callback_data='меню '))
			bot.send_message(message.chat.id, f'''<b>⚠️ Проверьте введённые данные:</b>
<b>├Услуга:</b> <code>{rowsss[0]}</code> 
<b>├Ссылка:</b> <code>{message.text}</code> 
<b>└Количество:</b> <code>{uslugaqid[12]} шт</code> ''' ,parse_mode='HTML',reply_markup=keyboard)
			connection.close()
		except:
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='✖️ Отмена',callback_data=f'Накрутка '))
			bot.send_message(message.chat.id, f'''<b>✖️ Ошибка ввода ссылки, попробуйте еще раз.</b>''',parse_mode='HTML',reply_markup=keyboard)
	else:
		bot.delete_message(message.chat.id,message.message_id)		

def reviews(message, msdids):
	if message.chat.id in users_zadanie:
		bot.delete_message(message.chat.id, msdids)
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
		q = connection.cursor()
		date = datetime.today()
		q.execute("INSERT INTO reviews (user,text,data,bot) VALUES ('%s', '%s', '%s', '%s')"%(message.from_user.username,message.text,date,bot_name))
		connection.commit()
		connection.close()
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='🎛 Открыть меню',callback_data=f'меню '))
		bot.send_message(message.chat.id, '''<b> ❤️ Спасибо за ваш отзыв, нам очень приятно.</b>''',parse_mode='HTML', reply_markup=keyboard)
	else:
		bot.delete_message(message.chat.id,message.message_id)

def users_zadanie_del(user):
	if user in users_zadanie:
		users_zadanie.remove(user)
	else:
		pass


@bot.callback_query_handler(func=lambda call:True)
def podcategors(call):
	a = call.data.split()
	if a[0] == 'Check_Depozit_qiwi_':
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
		q = connection.cursor()
		try:
			if p2p.check(bill_id=call.data[19:]).status == "PAID":
				bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
				q.execute(f"update ugc_users set balance = balance + '{p2p.check(bill_id=call.data[19:]).amount}' where id = '{call.message.chat.id}' and bot = '{bot_name}'")
				connection.commit()
				bot.send_message(call.message.chat.id, f"✔️ Баланс успешно пополнен на {p2p.check(bill_id=call.data[19:]).amount} RUB!",parse_mode='HTML')
			else:
				bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="⚠ Оплата не найдена!")
		except Exception as e:
			print(e)
			pass
			
	if a[0] == 'меню':
		users_zadanie_del(call.message.chat.id)
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
		q = connection.cursor()
		q.execute(f'SELECT * FROM list_bot WHERE bot = "{bot_name}"')
		bot_deposit = q.fetchone()
		if int(bot_deposit[11]) >= 1000:
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'''📈 Накрутка''',callback_data='Накрутка'),types.InlineKeyboardButton(text=f'''📩 Приём SMS''',callback_data='Прием'))
			keyboard.add(types.InlineKeyboardButton(text=f'''👤 Мой профиль''',callback_data='профиль'),types.InlineKeyboardButton(text=f'''👨 Поддержка''',callback_data='Поддержка'))
			keyboard.add(types.InlineKeyboardButton(text=f'''⚙️ Мои заказы''',callback_data='заказы'),types.InlineKeyboardButton(text=f'''📦 Мои покупки''',callback_data='покупки'))
			connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
			q = connection.cursor()
			q.execute(f"SELECT * FROM keyboards WHERE bot = '{bot_name}'")
			rows = q.fetchall()
			connection.close()
			for i in rows:
				keyboard.add(types.InlineKeyboardButton(text=i[1],callback_data=i[0]))
			bot.send_message(call.message.chat.id, f'''Привет <a href="tg://user?id={call.message.chat.id}">{call.message.chat.first_name}</a> 👋
Используй меню, чтобы со мной общаться 💬''',parse_mode='HTML', reply_markup=keyboard)
		else:
			if int(bot_deposit[13]) != 0: 
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text=f'''📈 Накрутка''',callback_data='Накрутка'),types.InlineKeyboardButton(text=f'''📩 Приём SMS''',callback_data='Прием'))
				keyboard.add(types.InlineKeyboardButton(text=f'''👤 Мой профиль''',callback_data='профиль'),types.InlineKeyboardButton(text=f'''👨 Поддержка''',callback_data='Поддержка'))
				connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
				q = connection.cursor()
				q.execute(f"SELECT * FROM keyboards WHERE bot = '{bot_name}'")
				rows = q.fetchall()
				connection.close()
				for i in rows:
					keyboard.add(types.InlineKeyboardButton(text=i[1],callback_data=i[0]))
				bot.send_message(call.message.chat.id, f'''Привет <a href="tg://user?id={call.message.chat.id}">{call.message.chat.first_name}</a> 👋
Используй меню, чтобы со мной общаться 💬''',parse_mode='HTML', reply_markup=keyboard)
			else:
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text=f'''⚡️ Продвижение''',callback_data='Накрутка'),types.InlineKeyboardButton(text=f'''⚙️ Мои заказы''',callback_data='заказы'))
				keyboard.add(types.InlineKeyboardButton(text=f'''💳 Профиль''',callback_data='профиль'),types.InlineKeyboardButton(text=f'''👨 Поддержка''',callback_data='Поддержка'))
				connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
				q = connection.cursor()
				q.execute(f"SELECT * FROM keyboards WHERE bot = '{bot_name}'")
				rows = q.fetchall()
				connection.close()
				for i in rows:
					keyboard.add(types.InlineKeyboardButton(text=i[1],callback_data=i[0]))
				bot.send_message(call.message.chat.id, f'''Привет <a href="tg://user?id={call.message.chat.id}">{call.message.chat.first_name}</a> 👋
Используй меню, чтобы со мной общаться 💬''',parse_mode='HTML', reply_markup=keyboard)

	if a[0] == 'check_opl':
		name = 'jopa'
		secret = '7a4ca73baf7bcb4f042d59c14e893ba158155fde'
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
		q = connection.cursor()
		q.execute(f"SELECT id_pay FROM pay_ok where user = '{call.message.chat.id}' ORDER BY id DESC LIMIT 1")
		zalupa = q.fetchone()[0]
		try:
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
		except:
			bot.send_message(call.message.chat.id, f'<b>Вы еще не оплатили</b>', parse_mode='HTML')

	if a[0] == 'check_opl2':
		api_key = 'F9F332866876657CF1CEF31E57F7E5DC-DBE2A835B23C5C1B965647C16C7DF76A-2188E143B43F3FC90765E400188BCE13'
		id_pays = '380'
		magaz = '1054'
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
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
	
	elif a[0] == 'Магазин':
		users_zadanie_del(call.message.chat.id)
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database='bot_shop')
		q = connection.cursor()
		keyboard = types.InlineKeyboardMarkup()
		q.execute(f"SELECT * FROM categor WHERE bot = '{bot_name}'")
		rows = q.fetchall()
		connection.close()
		if len(rows) != 0:
			for i in rows:
				keyboard.add(types.InlineKeyboardButton(text=i[1],callback_data=f'Товары {i[0]}'))
			keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад к меню''',callback_data='меню'))
			bot.send_message(call.message.chat.id,'''<b>🛍 Выберите категорию:</b>''', reply_markup=keyboard, parse_mode='HTML')
		else:
			keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data='меню'))
			bot.send_message(call.message.chat.id,'''<b>😕 К большому сожалению, мы пока что не добавили новые товары.</b>''', reply_markup=keyboard, parse_mode='HTML')

	elif a[0] == 'Товары':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database='bot_shop')
		q = connection.cursor()
		keyboard = types.InlineKeyboardMarkup()
		q.execute(f"SELECT * FROM tovar WHERE categor = '{a[1]}' and status = 'DONE'")
		rows = q.fetchall()
		connection.close()
		if len(rows) != 0:
			for i in rows:
				keyboard.add(types.InlineKeyboardButton(text=i[1],callback_data=f'Товар {i[0]}'))
			keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data='Магазин'))
			bot.send_message(call.message.chat.id,'''<b>🛍 Выберите товар:</b>''', reply_markup=keyboard, parse_mode='HTML')
		else:
			keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data='Магазин'))
			bot.send_message(call.message.chat.id,'''<b>😕 К большому сожалению, мы пока что не добавили новые товары.</b>''', reply_markup=keyboard, parse_mode='HTML')

	elif a[0] == 'Товар':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database='bot_shop')
		q = connection.cursor()
		keyboard = types.InlineKeyboardMarkup()
		q.execute(f"SELECT * FROM tovar WHERE id = '{a[1]}'")
		rows = q.fetchone()
		connection.close()
		colvo_rovar = 0 
		with open (f'/root/smm/tovar/{rows[5]}') as f: 
			for line in f: 
				if line != '\n': 
					colvo_rovar += 1
		keyboard.add(types.InlineKeyboardButton(text='🛒 Купить',callback_data=f'Купить {rows[0]}'))
		keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data=f'Товары {rows[4]}'))
		bot.send_message(call.message.chat.id,f'''<b>📦 Товар:</b> {rows[1]}
➖➖➖➖➖➖
<b>📜 Описание:</b>
<code>{rows[2]}</code>
➖➖➖➖➖➖
<b>🗂 Остаток: {colvo_rovar} шт</b>
➖➖➖➖➖➖
<b>💳 Цена за единицу:</b>  <code>{rows[3]}</code> <b>RUB</b>''', reply_markup=keyboard, parse_mode='HTML')
		
	elif a[0] == 'Купить':
		users_zadanie.append(call.message.chat.id)
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database='bot_shop')
		q = connection.cursor()
		q.execute(f"SELECT * FROM tovar WHERE id = '{a[1]}'")
		rows = q.fetchone()
		connection.close()
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='✖️ Отмена',callback_data=f'Магазин '))
		msg = bot.send_message(call.message.chat.id, f'''<b>📄 Вы выбрали товар: <code>{rows[1]}</code>
└Введите количество которое хотите купить:</b> ''',parse_mode='HTML', reply_markup=keyboard)
		bot.register_next_step_handler(msg, newpokupka, msg.message_id,a[1])
			
	elif a[0] == 'Поддержка':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'''📝 Задать вопрос''',callback_data='Задатьвопрос'),types.InlineKeyboardButton(text=f'''🔍 Проверка заказа''',callback_data='Проверить'))
		keyboard.add(types.InlineKeyboardButton(text=f'''⬅️ Назад''',callback_data='меню'))
		bot.send_message(call.message.chat.id, f'''⚡️ Если у Вас есть вопрос по работе бота, нажмите на кнопку «Задать вопрос».

При проблеме с заказом, нажмите на кнопку «Проверка заказа» и пройдите по инструкции.''',parse_mode='HTML', reply_markup=keyboard)
	elif a[0] == 'Задатьвопрос':	
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()
		users_zadanie.append(call.message.chat.id)
		keyboard.add(types.InlineKeyboardButton(text='✖️ Отмена',callback_data=f'меню '))
		msg = bot.send_message(call.message.chat.id,'''✍️ Напишите свой вопрос:''', reply_markup=keyboard, parse_mode='HTML')
		bot.register_next_step_handler(msg, supportadd, msg.message_id)
	
	elif a[0] == 'Закрыть':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)

	elif a[0] == 'профиль':
		users_zadanie_del(call.message.chat.id)
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
		q = connection.cursor()
		q.execute(f'SELECT * FROM ugc_users WHERE id = "{call.message.chat.id}" and bot = "{bot_name}"')
		row = q.fetchone()
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='💰 Пополнить',callback_data=f'awhat_oplata'),types.InlineKeyboardButton(text='🎁 Промокод',callback_data='Промокод '))
		keyboard.add(types.InlineKeyboardButton(text='👤 Реферальная система',callback_data='ref'))
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data='меню '))
		bot.send_message(call.message.chat.id, f'''<b>👤 Профиль:
├Id:</b> <code>{call.message.chat.id}</code>
<b>└Баланс:</b> <code>{row[6]} RUB</code>

	''',parse_mode='HTML', reply_markup=keyboard)


	elif a[0] == 'Промокод':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()
		users_zadanie.append(call.message.chat.id)
		keyboard.add(types.InlineKeyboardButton(text='✖️ Отмена',callback_data=f'профиль '))
		msg = bot.send_message(call.message.chat.id,'''✍️ Укажите код купона:''', reply_markup=keyboard, parse_mode='HTML')
		bot.register_next_step_handler(msg, cupon_aktiv, msg.message_id)
	
	elif a[0] == 'Прием':
		users_zadanie_del(call.message.chat.id)
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
		q = connection.cursor()
		q.execute(f"SELECT api_sms FROM geral_config where id = '1'")
		api_sms = q.fetchone()
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		h = requests.post(f'https://smshub.org/stubs/handler_api.php?api_key={api_sms[0]}&action=getPrices&country=0', headers=headers).json()
		keyboard = types.InlineKeyboardMarkup()
		q.execute(f"SELECT * FROM service_list")
		rows = q.fetchall()
		btns = []
		for i in range(len(rows)):
			try:
				colvo = str(h['0'][rows[i][1]]).split("': ")[1].split("}")[0]
			except:
				colvo = 0
			btns.append(types.InlineKeyboardButton(text=f'[{colvo}] {rows[i][2]}', callback_data=f'vibor_sms {rows[i][0]}'))
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
		status = is_subscribed(call.message.chat.id)
		if status == True:
			connection.close()
			keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад к меню', callback_data=f'меню '))
			bot.send_message(call.message.chat.id, f'''<b>📩 Выберите сервис для аренды номера:</b>
├<i>Страна: Россия 🇷🇺</i>
└<i>Цифра перед названием сервиса означает количество онлайн номеров на данный момент!</i>
➖➖➖➖➖➖➖➖➖➖➖➖
<b>❗️ Покупая номер вы всегда сможете получить не ограниченное смс в первые 20 минут!</b>''',parse_mode='HTML', reply_markup=keyboard)
		else:
			q.execute(f'SELECT chanel_id FROM chanel WHERE bot = "{bot_name}"')
			row = q.fetchone()
			connection.close()
			invite_link =  bot_create.create_chat_invite_link(chat_id = row[0], member_limit = 1).invite_link
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='↗️ Вступить', url= invite_link))
			keyboard.add(types.InlineKeyboardButton(text='♻️ Проверить', callback_data='Накрутка '))
			bot.send_message(call.message.chat.id, f'''<b>❗️ Для использования бота необходимо вступить в наш канал:</b>
<b>└Ссылка:</b> <a href="{invite_link}">{invite_link}</a>''',parse_mode='HTML', reply_markup=keyboard,disable_web_page_preview = True)

	elif a[0] == 'vibor_sms':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
		q = connection.cursor()
		q.execute(f"SELECT api_sms FROM geral_config where id = '1'")
		api_sms = q.fetchone()

		q.execute(f"SELECT sms FROM list_bot where bot = '{bot_name}'")
		praceplus = q.fetchone()
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		h = requests.post(f'https://smshub.org/stubs/handler_api.php?api_key={api_sms[0]}&action=getPrices&country=0', headers=headers).json()
		q.execute(f'SELECT * FROM service_list WHERE id = "{a[1]}"')
		sms_info = q.fetchone()
		try:
			colvo = str(h['0'][sms_info[1]]).split("': ")[1].split("}")[0]
		except:
			colvo = 0
		praces = int(sms_info[3]) + int(praceplus[0])
		keyboard = types.InlineKeyboardMarkup()
		if int(colvo) != 0:
			keyboard.add(types.InlineKeyboardButton(text='📲 Арендовать', callback_data=f'Арендовать {a[1]}'))
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data=f'Прием '))
		bot.send_message(call.message.chat.id, f'''
<b>📩 Информация:</b>
├<b>Сервис:</b> <code>{sms_info[2]}</code>
├<b>Стоимость:</b> <code>{praces} RUB</code>
└<b>Номеров доступно:</b> <code>{colvo} шт</code>
''',parse_mode='HTML', reply_markup=keyboard)

	elif a[0] == 'Арендовать':
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
		q = connection.cursor()
		q.execute(f"SELECT sms FROM list_bot where bot = '{bot_name}'")
		praceplus = q.fetchone()
		q.execute(f"SELECT api_sms FROM geral_config where id = '1'")
		api_sms = q.fetchone()
		q.execute(f"SELECT balance FROM ugc_users where id = '{call.message.chat.id}' and bot = '{bot_name}'")
		balance = q.fetchone()
		q.execute(f'SELECT * FROM service_list WHERE id = "{a[1]}"')
		sms_info = q.fetchone()
		praces = int(sms_info[3]) + int(praceplus[0])
		if int(balance[0]) >= int(praces):
			headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
			h = requests.post(f'https://smshub.org/stubs/handler_api.php?api_key={api_sms[0]}&action=getNumber&service={sms_info[1]}', headers=headers)
			if str(h.text) != 'BAD_SERVICE' and str(h.text) != 'NO_NUMBERS' and str(h.text) != 'NO_BALANCE':
				number = h.text.split("ACCESS_NUMBER:")[1].split(":")[1]
				id_number = h.text.split("ACCESS_NUMBER:")[1].split(":")[0]
				q.execute(f"update ugc_users set balance = balance - '{praces}' where id = '{call.message.chat.id}' and bot = '{bot_name}'")
				connection.commit()
				data = datetime.now()
				q.execute("INSERT INTO list_aktiv (user,bot,number,id_number,service,data,code,status) VALUES ('%s','%s', '%s','%s', '%s', '%s', '%s', '%s')"%(call.message.chat.id,bot_name,number,id_number,sms_info[2],data,'Нет','wait'))
				connection.commit()
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='✖️ Отменить', callback_data=f'Отменитьсмс {id_number}'))
				bot.send_message(call.message.chat.id, f'''
<b>💭 Информация:</b>
├<b>Сервис:</b> <code>{sms_info[2]}</code>
├<b>Номер:</b> <code>{number}</code>
├<b>Статус:</b> <code>Ожидаем код, мы оповестим когда он придет. </code>
├<b>Дата:</b> <code>{data}</code>
└<i>В случае если код не придет в течении 20 минут, вам вернутся деньги на баланс.</i>
''',parse_mode='HTML', reply_markup=keyboard)
			else:
				bot.answer_callback_query(callback_query_id=call.id,show_alert=True, text="😔 К сожалению, номера закончились, попробуйте позже.")	
		else:
			bot.answer_callback_query(callback_query_id=call.id,show_alert=True, text="❗️ Недостаточно средств, пополните баланс.")
	
	elif a[0] == 'Повторноесмс':
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
		q = connection.cursor()
		q.execute(f"SELECT api_sms FROM geral_config where id = '1'")
		api_sms = q.fetchone()
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		h = requests.post(f'https://smshub.org/stubs/handler_api.php?api_key={api_sms[0]}&action=setStatus&status=3&id={a[1]}', headers=headers)
		if str(h.text) == 'ACCESS_RETRY_GET':
			q.execute(f"update list_aktiv set status = 'WAIT' where id_number = '{a[1]}'")
			connection.commit()
			bot.answer_callback_query(callback_query_id=call.id,show_alert=True, text="⏳ Хорошо, ожидаем новые смс.....")
			bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		else:
			q.execute(f"update list_aktiv set status = 'STATUS_CANCEL' where id_number = '{a[1]}'")
			connection.commit()
			bot.answer_callback_query(callback_query_id=call.id,show_alert=True, text="😔 К сожалению, время аренды закончилось.")	
			bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
	
	elif a[0] == 'Завершитьсмс':
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
		q = connection.cursor()
		q.execute(f"SELECT api_sms FROM geral_config where id = '1'")
		api_sms = q.fetchone()
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		h = requests.post(f'https://smshub.org/stubs/handler_api.php?api_key={api_sms[0]}&action=setStatus&status=6&id={a[1]}', headers=headers)
		print(h.text)
		if str(h.text) == 'ACCESS_ACTIVATION':
			q.execute(f"update list_aktiv set status = 'DONE' where id_number = '{a[1]}'")
			connection.commit()
			bot.answer_callback_query(callback_query_id=call.id,show_alert=True, text="✔️ Работа с номером завершена.")
			bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		else:
			q.execute(f"update list_aktiv set status = 'DONE' where id_number = '{a[1]}'")
			connection.commit()
			bot.answer_callback_query(callback_query_id=call.id,show_alert=True, text="✔️ Работа с номером завершена.")	
			bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)


	elif a[0] == 'Отменитьсмс':
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
		q = connection.cursor()
		q.execute(f"SELECT sms FROM list_bot where bot = '{bot_name}'")
		praceplus = q.fetchone()
		q.execute(f"SELECT api_sms FROM geral_config where id = '1'")
		api_sms = q.fetchone()
		q.execute(f'SELECT * FROM list_aktiv WHERE id_number = "{a[1]}"')
		info = q.fetchone()
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		h = requests.post(f'https://smshub.org/stubs/handler_api.php?api_key={api_sms[0]}&action=setStatus&status=8&id={a[1]}', headers=headers)
		if str(h.text) == 'ACCESS_CANCEL':
			q.execute(f"update list_aktiv set status = 'STATUS_CANCEL' where id_number = '{a[1]}'")
			connection.commit()
			bot.answer_callback_query(callback_query_id=call.id,show_alert=True, text="✔️ Отменили активацию, средства будет возврашены на баланс в течений минуты")
			bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		else:
			q.execute(f"update list_aktiv set status = 'DONE' where id_number = '{a[1]}'")
			connection.commit()
			bot.answer_callback_query(callback_query_id=call.id,show_alert=True, text="✖️ Ошибка, вы получили код или время активации истекло.")
			bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)

	elif a[0] == 'Накрутка':
		users_zadanie_del(call.message.chat.id)
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
		q = connection.cursor()
		keyboard = types.InlineKeyboardMarkup()
		q.execute(f"SELECT * FROM category")
		rows = q.fetchall()
		btns = []
		for i in range(len(rows)):
			btns.append(types.InlineKeyboardButton(text=rows[i][0], callback_data=f'sub_category_ {rows[i][1]}'))
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
		status = is_subscribed(call.message.chat.id)
		if status == True:
			connection.close()
			keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад к меню', callback_data=f'меню '))
			bot.send_message(call.message.chat.id, f'''<b>📈 Что будем продвигать ?</b>''',parse_mode='HTML', reply_markup=keyboard)
		else:
			q.execute(f'SELECT chanel_id FROM chanel WHERE bot = "{bot_name}"')
			row = q.fetchone()
			connection.close()
			invite_link =  bot_create.create_chat_invite_link(chat_id = row[0], member_limit = 1).invite_link
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='↗️ Вступить', url= invite_link))
			keyboard.add(types.InlineKeyboardButton(text='♻️ Проверить', callback_data='Накрутка '))
			bot.send_message(call.message.chat.id, f'''<b>❗️ Для использования бота необходимо вступить в наш канал:</b>
<b>└Ссылка:</b> <a href="{invite_link}">{invite_link}</a>''',parse_mode='HTML', reply_markup=keyboard,disable_web_page_preview = True)

	elif a[0] == 'покупки':
		users_zadanie_del(call.message.chat.id)
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
		q = connection.cursor()
		q.execute(f'SELECT * FROM list_zakaz_shop WHERE user = "{call.message.chat.id}" and bot = "{bot_name}" ORDER BY id DESC LIMIT 10')
		row = q.fetchall()
		keyboard = types.InlineKeyboardMarkup()
		if str(row) != '[]':
			keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад к меню', callback_data=f'меню '))
			status = is_subscribed(call.message.chat.id)
			if status == True:
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад к меню', callback_data=f'меню '))	
				doc = open(f'/root/smm/tovar/pokupki/{call.message.chat.id}_{bot_name}.txt', 'rb')
				bot.send_document(call.message.chat.id, doc, caption='🗂 Ваши купленные товары.',reply_markup=keyboard)
				doc.close()
				connection.close()
			else:
				q.execute(f'SELECT chanel_id FROM chanel WHERE bot = "{bot_name}"')
				row = q.fetchone()
				invite_link =  bot_create.create_chat_invite_link(chat_id = row[0], member_limit = 1).invite_link
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='↗️ Вступить', url= invite_link))
				keyboard.add(types.InlineKeyboardButton(text='♻️ Проверить', callback_data='заказы '))
				bot.send_message(call.message.chat.id, f'''<b>❗️ Для использования бота необходимо вступить в наш канал:</b>
<b>└Ссылка:</b> <a href="{invite_link}">{invite_link}</a>''',parse_mode='HTML', reply_markup=keyboard,disable_web_page_preview = True)
				connection.close()
		else:
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад к меню', callback_data=f'меню '))
			bot.send_message(call.message.chat.id, f'''<b>😔 К сожалению, у вас пока что нет покупок, но в будущем они обязательно будут тут.</b>''' ,parse_mode='HTML',reply_markup=keyboard)		
	elif a[0] == 'заказы':
		users_zadanie_del(call.message.chat.id)
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
		q = connection.cursor()
		q.execute(f'SELECT * FROM list_zakaz WHERE user = "{call.message.chat.id}" and bot = "{bot_name}" ORDER BY id DESC LIMIT 10')
		row = q.fetchall()
		if str(row) != '[]':
			text = ''
			for i in row:
				text += f'''ℹ️ ID: <code>{i[7]}</code>
<b>├Услуга:</b> <code>{i[5]}</code>
<b>├Количество:</b> <code>{i[3]}</code>
<b>└Ссылка:</b> <code>{i[2]}</code>\n\n'''
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='🔎 Проверить заказ',callback_data='Проверить '))
			keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data=f'Накрутка '))
			status = is_subscribed(call.message.chat.id)
			if status == True:
				connection.close()
				bot.send_message(call.message.chat.id, f'''<b>ℹ️ Последние заказы:</b>

{text}''' ,parse_mode='HTML',reply_markup=keyboard)
			else:
				q.execute(f'SELECT chanel_id FROM chanel WHERE bot = "{bot_name}"')
				row = q.fetchone()
				invite_link =  bot_create.create_chat_invite_link(chat_id = row[0], member_limit = 1).invite_link
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='↗️ Вступить', url= invite_link))
				keyboard.add(types.InlineKeyboardButton(text='♻️ Проверить', callback_data='заказы '))
				bot.send_message(call.message.chat.id, f'''<b>❗️ Для использования бота необходимо вступить в наш канал:</b>
<b>└Ссылка:</b> <a href="{invite_link}">{invite_link}</a>''',parse_mode='HTML', reply_markup=keyboard,disable_web_page_preview = True)
				connection.close()
		else:
			connection.close()
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data=f'Накрутка '))
			bot.send_message(call.message.chat.id, f'''<b>😔 К сожалению, у вас пока что нет заказов, но в будущем они обязательно будут тут.</b>''' ,parse_mode='HTML',reply_markup=keyboard)
	
	elif call.data == 'awhat_oplata':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'''▪️ Qiwi\CARD''',callback_data='add_depozit'))
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'профиль '))
		bot.send_message(call.message.chat.id, f'''📥 Выберите способ для пополнения баланса:''',parse_mode='HTML', reply_markup=keyboard)
	
	elif a[0] == 'add_depozit':
		keyboard = types.InlineKeyboardMarkup()
		users_zadanie.append(call.message.chat.id)
		keyboard.add(types.InlineKeyboardButton(text='✖️ Отмена',callback_data=f'профиль '))
		msg = bot.send_message(call.message.chat.id,'''✍️ Укажите сумму пополнения:''', reply_markup=keyboard, parse_mode='HTML')
		bot.register_next_step_handler(msg, btc_oplata_1)

	elif a[0] == 'add_depozit2':
		keyboard = types.InlineKeyboardMarkup()
		users_zadanie.append(call.message.chat.id)
		keyboard.add(types.InlineKeyboardButton(text='✖️ Отмена',callback_data=f'профиль '))
		msg = bot.send_message(call.message.chat.id,'''✍️ Укажите сумму пополнения:''', reply_markup=keyboard, parse_mode='HTML')
		bot.register_next_step_handler(msg, btc_oplata_2)

	elif a[0] == 'назад':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
		q = connection.cursor()
		keyboard = types.InlineKeyboardMarkup()
		q.execute(f"SELECT * FROM category")
		rows = q.fetchall()
		btns = []
		for i in range(len(rows)):
			btns.append(types.InlineKeyboardButton(text=rows[i][0], callback_data=f'sub_category_ {rows[i][1]}'))
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
		connection.close()
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data='Накрутка '))
		bot.send_message(call.message.chat.id, f'''◾️ Выберите нужный пункт меню:''',parse_mode='HTML', reply_markup=keyboard)
		
	elif a[0] == 'sub_category_':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		sub_category_id = a[1]
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
		q = connection.cursor()
		q.execute(f"update ugc_users set categ = '{sub_category_id}' where id = '{call.message.chat.id}' and bot = '{bot_name}'")
		connection.commit()
		keyboard = types.InlineKeyboardMarkup()
		q.execute(f"SELECT * FROM sub_category where category = '{sub_category_id}'")
		rows = q.fetchall()
		connection.close()
		for i in rows:
			keyboard.add(types.InlineKeyboardButton(text=i[0],callback_data=f'item_ {i[2]}'))
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'Накрутка '))
		bot.send_message(call.message.chat.id, f'''<b>📈 Какая услуга вас интересует ?</b>''',parse_mode='HTML', reply_markup=keyboard)

	elif a[0] == 'item_':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		item_id = a[1]
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
		q = connection.cursor()
		keyboard = types.InlineKeyboardMarkup()
		q.execute(f"SELECT categ FROM ugc_users where id = '{call.message.chat.id}' and bot = '{bot_name}'")
		categ = q.fetchone()[0]
		q.execute(f"update ugc_users set categ1 = '{item_id}' where id = '{call.message.chat.id}' and bot = '{bot_name}'")
		connection.commit()
		q.execute(f"SELECT * FROM item where sub_category = '{item_id}'")
		rows = q.fetchall()
		for i in rows:
			q.execute(f"SELECT * FROM item where item_id = '{i[8]}'")
			rowss = q.fetchone()
			q.execute(f"SELECT prace FROM list_bot where bot = '{bot_name}'")
			plusprace = q.fetchone()[0]

			praces121 = float(rowss[3]) / 100 * float(plusprace)
			praces = float(rowss[3]) + float(praces121)
			keyboard.add(types.InlineKeyboardButton(text=f'{i[0]} | {praces} RUB',callback_data=f'usluga_ {i[8]}'))
		connection.close()
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'sub_category_ {categ}'))
		bot.send_message(call.message.chat.id, f'''<b>📈 Выберите нужную услугу:</b>
└ Цена за 1000 шт.''',parse_mode='HTML', reply_markup=keyboard)

	elif a[0] == 'usluga_':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		usluga__id = a[1]
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
		q = connection.cursor()
		q.execute(f"SELECT categ1 FROM ugc_users where id = '{call.message.chat.id}' and bot = '{bot_name}'")
		categ1 = q.fetchone()[0]
		q.execute(f"update ugc_users set usluga = '{usluga__id}' where id = '{call.message.chat.id}' and bot = '{bot_name}'")
		connection.commit()
		keyboard = types.InlineKeyboardMarkup()
		q.execute(f"SELECT * FROM ugc_users where id = '{call.message.chat.id}' and bot = '{bot_name}'")
		rowss = q.fetchone()
		q.execute(f"SELECT * FROM item where item_id = '{usluga__id}'")
		rows = q.fetchone()
		q.execute(f"SELECT prace FROM list_bot where bot = '{bot_name}'")
		plusprace = q.fetchone()[0]
		praces1212 = float(rows[3]) / 100 * float(plusprace)
		praces = float(rows[3]) + float(praces1212)
		print(praces1212)
		print(praces)

		connection.close()
		keyboard.add(types.InlineKeyboardButton(text='🛒 Заказать',callback_data=f'zakazat'))
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'item_ {categ1}'))
		bot.send_message(call.message.chat.id, f'''📦 <b>Услуга:</b> <code>{rows[0]}</code> 
➖➖➖➖➖➖
📜 <b>Описание:</b> 
<code>{rows[7]}</code>
➖➖➖➖➖➖
📥 <b>Минимальное количество заказа: {rows[4]}</b> 
📤 <b>Максимальное количество: {rows[5]}</b> 
➖➖➖➖➖➖
💳 <b>Цена за 1000: </b> <b>{praces} RUB</b>''',parse_mode='HTML', reply_markup=keyboard)

	elif a[0] == 'zakazat':
		users_zadanie.append(call.message.chat.id)
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
		q = connection.cursor()
		

		q.execute(f"SELECT usluga FROM ugc_users where id = '{call.message.chat.id}' and bot = '{bot_name}'")

		usluga__id = q.fetchone()[0]

		q.execute(f"SELECT * FROM item where item_id = '{usluga__id}'")
		rows = q.fetchone()
		connection.close()
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='✖️ Отмена',callback_data=f'Накрутка '))
		msg = bot.send_message(call.message.chat.id, f'''<b>📄 Вы выбрали услугу: <code>{rows[0]}</code>
└Введите количество которое хотите купить:</b> ''',parse_mode='HTML', reply_markup=keyboard)
		bot.register_next_step_handler(msg, newzakaz, msg.message_id)
	
	elif a[0] == "Проверить":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		users_zadanie.append(call.message.chat.id)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='✖️ Отмена',callback_data=f'меню '))
		msg= bot.send_message(call.message.chat.id, "✍️<b>Напишите ID заказа (ID можно узнать во вкладке «Мои заказы»):</b>",parse_mode='HTML', reply_markup=keyboard)
		bot.register_next_step_handler(msg, statuszakaz, msg.message_id)
	
	elif a[0] == 'ref':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
		q = connection.cursor()
		q.execute(f'SELECT COUNT(id) FROM ugc_users WHERE ref = "{call.message.chat.id}" and bot = "{bot_name}"')
		user_ref_count = q.fetchone()[0]
		connection.close()
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data=f'профиль '))
		bot.send_message(call.message.chat.id, f'''<b>🤝 Реферальная программа</b>
<b>└Ссылка:</b> https://t.me/{bot_name}?start={call.message.chat.id}

<b>📈 Статистика</b>
<b>├Рефералов:</b> <code>{user_ref_count}</code>
<b>├Процент:</b> <code>5%</code>
<b>└Если вы пригласите человека который пополнит баланс в боте, вам дадут 5% от пополнения на ваш баланс!</b>''',parse_mode='HTML',reply_markup=keyboard, disable_web_page_preview=True)	

	elif a[0] == 'Заказать':
		try:
			bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
			connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
			q = connection.cursor()
			q.execute(f"SELECT * FROM ugc_users where id = '{call.message.chat.id}' and bot = '{bot_name}'")
			confzakaz = q.fetchone()
			q.execute(f"SELECT * FROM item where item_id = '{confzakaz[4]}'")
			rowsss = q.fetchone()
			q.execute(f"SELECT user FROM list_bot where bot = '{bot_name}'")
			users = q.fetchone()[0]
			q.execute(f"SELECT prace FROM list_bot where bot = '{bot_name}'")
			plusprace = q.fetchone()[0]

			prace_admin = float(rowsss[3]) / 100 * float(plusprace)
			praces_usluga = float(rowsss[3]) + float(prace_admin)
			prace = float(praces_usluga) / 1000 * float(confzakaz[12])
			pracess = float(rowsss[3]) / 1000 * float(confzakaz[12]) # Цена без накрутки
			prace_admin = float(prace) - float(pracess)
			if int(confzakaz[6]) >= int(prace):
				tomorrow = datetime.now()
				data = tomorrow.strftime('%d/%m/%Y')
				apinakrutka  = 'ef43cb03bd410b3d6fa1622b00756ced'
				idnakrutka  = rowsss[6]
				link  = confzakaz[13]
				colvo  = confzakaz[12]
				zakazid = urllib.request.urlopen(f'https://partner.soc-proof.su/api/v2/?key={apinakrutka}&action=add&service={idnakrutka}&link={link}&quantity={colvo}').read()
				result = json.loads(zakazid.decode('utf8'))
				zakazid2 = (result['order'])
				print(zakazid2)
				q.execute(f"update ugc_users set balance = balance - '{prace}' where id = '{call.message.chat.id}' and bot = '{bot_name}'")
				connection.commit()
				q.execute("INSERT INTO list_zakaz (user,link,colvo,data,usluga,bot,id_nakzakaz) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')"%(call.message.chat.id,confzakaz[13],confzakaz[12],data,str(rowsss[0]),bot_name,zakazid2))
				connection.commit()
				q.execute(f"update list_bot set logi = '{data}' WHERE bot = '{bot_name}'")
				connection.commit()
				q.execute(f"update list_bot set balance = balance + '{prace_admin}' where bot = '{bot_name}'")
				connection.commit()
				q.execute(f"update list_bot set dohod = dohod + '{prace_admin}' where bot = '{bot_name}'")
				connection.commit()
				connection.close()
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='💌 Оставить отзыв 💌',callback_data=f'Оставитьотзыв '))
				keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернутся в меню',callback_data=f'меню '))
				bot.send_message(call.message.chat.id, f'''<b>✅ Ваш заказ успешно принят в работу:</b>
└<i>Номер вашего заказа</i> - <code>{zakazid2}</code>
➖➖➖➖➖➖➖➖➖
<b>❤️ Спасибо, что выбираете нас: </b>
└<i>Нам было было бы очень приятно, если бы вы оставили отзыв!</i>''',parse_mode='HTML',reply_markup=keyboard, disable_web_page_preview=True)
				try:
					connection.close()
					keyboard = types.InlineKeyboardMarkup()
					keyboard.add(types.InlineKeyboardButton(text='✖️ Закрыть',callback_data=f'Закрыть '))
					bot.send_message(users, f'''<b>Новый заказ:</b> <code>{rowsss[0]}</code> <b>| Доход:</b> <code>{prace_admin}</code> <b>RUB</b>''',parse_mode='HTML',reply_markup=keyboard, disable_web_page_preview=True)
				except:
					pass
			else:
				connection.close()
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='💰 Пополнить баланс',callback_data=f'профиль '))
				keyboard.add(types.InlineKeyboardButton(text='✖️ Отмена',callback_data=f'Накрутка '))
				bot.send_message(call.message.chat.id, f'''<b>❗️ Ошибка: пополните баланс до {prace} RUB.</b>''' ,parse_mode='HTML',reply_markup=keyboard)
		except Exception as e:
			print(e)
			connection.close()
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернутся в меню',callback_data=f'меню '))
			bot.send_message(call.message.chat.id, f'''<b>❗️ Ошибка оформления заказа</b>''',parse_mode='HTML',reply_markup=keyboard)


	elif a[0] == "Оставитьотзыв":
		users_zadanie.append(call.message.chat.id)
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='✖️ Отмена',callback_data=f'меню '))
		msg= bot.send_message(call.message.chat.id, "<b>✍️ Напишите текст отзыва:</b>",parse_mode='HTML', reply_markup=keyboard)
		bot.register_next_step_handler(msg, reviews, msg.message_id)
	else:
		connection = connect(host=bd_host,user=bd_login,password=bd_pass,database=bd_base)
		q = connection.cursor()	
		q.execute(f"SELECT * FROM keyboards WHERE bot = '{bot_name}' and id = '{a[0]}'")
		rows = q.fetchone()
		connection.close()
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Вернутся в меню',callback_data=f'меню '))
		if rows != None:
			try:
				bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
				bot.send_message(call.message.chat.id, rows[2], parse_mode='HTML' ,reply_markup=keyboard)
			except:
				bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
				bot.send_message(call.message.chat.id, '''✖️ Ошибка.''' ,parse_mode='HTML',reply_markup=keyboard)
	

bot.polling(True)

