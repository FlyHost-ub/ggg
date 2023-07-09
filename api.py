from flask import Flask, render_template, url_for, request, redirect
import sqlite3
import json
import telebot
import datetime
from telebot import types, apihelper
from getpass import getpass
from mysql.connector import connect, Error
import time
import config

app = Flask(__name__)



TOKEN = config.bot_token
bot = telebot.TeleBot(TOKEN)
admin = -1001663964295
admin2 = -1001663964295
@app.route('/', methods=['POST'])
def create():
	if request.method == 'POST':
		try:
			payment_id = request.form['payment_id']
			profit = request.form['profit']
			desc = request.form['desc']
			shop_id = request.form['shop']
			if int(shop_id) != int(1054):
				bot_name = desc.split("@")[1].split(":")[0]
				user_id = desc.split("@")[1].split(":")[1]
				connection = connect(host=config.bd_host,user=config.bd_login,password=config.bd_pass,database=config.bd_base)
				q = connection.cursor()
				q.execute(f'SELECT * FROM pay_ok WHERE id_pay = "{payment_id}"')
				row = q.fetchone()
				if row != None:
					q.execute(f"update ugc_users set balance = balance + '{profit}' where id = '{user_id}' and bot = '{bot_name}'")
					connection.commit()
					try:
						q.execute(f"SELECT bot_token FROM list_bot where bot = '{bot_name}'")
						bot_token = q.fetchone()[0]
						bots = telebot.TeleBot(bot_token)
						bots.send_message(user_id, f'✔️ Баланс пополнен на {profit} RUB',parse_mode='HTML')
						try:
							UsrInfo = bots.get_chat_member(user_id, user_id).user
							username = UsrInfo.username
						except:
							username = 'None'
					except:
						pass
				bot.send_message(admin, f'''<b>📝 Новый депозит:</b>
<b>├UN:</b> @{username}
<b>├ID:</b> <code>{user_id}</code>
<b>├Бот:</b> @{bot_name}
<b>└ Сумма:</b> <code>{profit}</code>''',parse_mode='HTML')	

		except Exception as e:
			print(e)
	return '200'

if __name__ == "__main__":
	app.run("31.162.4.18",9090)