# -*- coding: utf-8 -*-

from flask import Flask,request,jsonify

import telepot
import chathelper
import dbhelper
import logging

#import dbhelper
import ast
#import texthelper#test


token="370210083:AAE5kDTVO5csSAx0jPXqk8ICX9omTPa4HeQ"
url='https://cachetest-172511.appspot.com/'

# 222

app = Flask(__name__)
bot = telepot.Bot(token=token)
ch=chathelper.ChatHelper(bot=bot) #**

db=dbhelper.HandleStatus()


@app.route('/')
def hello_world():
        #db.add_user('2','shahii','new')
        #a=db.select_value(120292417)
        #a=ast.literal_eval(a)    Convert a String representation of a Dictionary to a dictionary

        #a={0:0,1:1}

        #logging.error(len(a.keys()))
        return 'Hello World!'


@app.route('/{}'.format(token),methods=['POST'])
def updates():

    update=request.get_json(force=True)
    #logging.error(update)
    ch.handle_updates(update)
    #logging.error(str(update))

    '''
    update = telegram.Update.de_json(request.get_json(force=True))
    if update is None or update.message is None:
        return
    chat_id = update.message.chat.id
    message = update.message.text.encode('utf-8')
    first_name = last_name = username = ""
    try:
        first_name = update.message.chat.first_name.encode('utf-8')
    except:
        pass
    try:
        last_name = update.message.chat.last_name.encode('utf-8')
    except:
        pass
    try:
        username = update.message.chat.username.encode('utf-8')
    except:
        pass
    chathelper.ChatHelper.send_message(chat_id=chat_id,text='hi')
    '''
    return 'OK'
@app.route('/sethook')
def setWebhook():
    bot.setWebhook(url=url+'/'+token)
    return 'Ok hook set.'
@app.route('/delthook')
def deltWebhook():
    bot.deleteWebhook()
    return 'Webhook Deleted.'

@app.route('/api/update-authority-code',methods=['POST'])
def update_authority_code():
    try:
        if not if_valid_key(request.form.get('key')):
            return jsonify({"update": '1- error'}), 250

        chat_id=int(request.form.get('chat_id'))
        auth_code=str(request.form.get('auth_code'))
        db.add_PaymentTbl(chat_id,auth_code)

        return jsonify({"update":'ok'})
        #return jsonify({"update": 'error'})
    except Exception as ex:
        logging.error(repr(ex))
        return jsonify({"2-error": str(ex)}), 250

@app.route('/api/update-payment',methods=['POST'])
def update_payment():
    try:
        if not if_valid_key(request.form.get('key')):
            return jsonify({"update": 'error'}), 250
        refid=request.form.get('refid')
        auth_code=str(request.form.get('auth_code'))
        ch.payment_completed(auth_code,refid)

        return jsonify({"update":'match'})
    except Exception as ex:
        logging.error(repr(ex))

@app.route('/bot/send_delay_message',methods=['POST'])  #Will call after some second by Taskqueue
def send_delay_message():
    chat_id = int(request.form["chat_id"])
    ch.send_delay_message(chat_id)

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

def if_valid_key(key):
    if key == 'Sh4wTaCool4321':
        return True
    else:
        return False


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80, debug=True)
