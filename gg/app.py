import hashlib
import sqlite3

from flask import Flask, request, redirect


conn = sqlite3.connect(r"/1bot/database/database.db", check_same_thread=False)
cursor = conn.cursor()
app = Flask(__name__)


MERCHANT_SERCET = "1"
MERCHANT_ID = 1
BOT_URL = "https://t.me/1"


def update_status(_id, profit):
    print(_id)
    sql = "UPDATE freekassa_wait_payment SET status = ? WHERE payment_id = ?"
    cursor.execute(sql, (profit, _id))
    conn.commit()


@app.route('/good')
def good():
    return redirect(BOT_URL, code=302)


@app.route('/bad')
def bad():
    return redirect(BOT_URL, code=302)


@app.route('/notification')
def notification():
    print(request.args)


    try:
        ip_addr = request.environ['HTTP_X_FORWARDED_FOR']
    except:
        try:
            ip_addr = request.environ['REMOTE_ADDR']
        except:
            ip_addr = request.remote_addr

    print(ip_addr)    
    
    if ip_addr not in ['168.119.157.136', '168.119.60.227', '138.201.88.124', '178.154.197.79']:
        print("hacking attempt!")
        return "hacking attempt!"

    MERCHANT_ORDER_ID = request.args.get("MERCHANT_ORDER_ID")
    AMOUNT = request.args.get("AMOUNT")
    SIGN = request.args.get("SIGN")
    
    sign = hashlib.md5(f"{MERCHANT_ID}:{AMOUNT}:{MERCHANT_SERCET}:{MERCHANT_ORDER_ID}".encode()).digest().hex()
    print(sign)
    if SIGN != sign:
        print("wrong sign!")
        return "wrong sign!"

    update_status(MERCHANT_ORDER_ID, int(float(AMOUNT)))

    return "YES"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)

