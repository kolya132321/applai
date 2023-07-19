import os, json
from aiohttp import request
from telegram import Bot,Update
from telegram.ext import Updater
from telegram.ext import Updater,CommandHandler, MessageHandler,Filters

from telegram.utils.request import Request

global status
status=[]


def new_vacancy(update,context):
    print(update.message.text)
    update.message.reply_text(f"Vacancy description :")
    global status
    status.append({'chat_id':update.message.chat_id, 'status':'WAITING'})
    print(status)

def vac_desc(update,context):
    global status
    for x in status:
        if x['chat_id']==update.message.chat_id:

    if status == 'WAITING':
        print('sss')
        print(update.message.text)
        vac=update.message.text

def show_vacancy(update,context):
    print(update.message.chat_id)

def main():
    request = Request(con_pool_size=8)
    bot=Bot(token="6051246626:AAGIe-mec1-uanl0MqFLDJdSBJSRuRlN_0w",request=request)
    updater=Updater(bot=bot,)
    cmd=[("new_vacancy","Create a new vacancy request"),("show_vacancy","Existing vacancies progress")]
    dp = updater.dispatcher
    bot.set_my_commands(cmd)
    dp.add_handler(CommandHandler("new_vacancy",new_vacancy))
    dp.add_handler(CommandHandler("show_vacancy",show_vacancy))
    dp.add_handler(MessageHandler(~Filters.command,vac_desc))
    updater.start_polling()
    updater.idle()

if __name__=="__main__":
    main()