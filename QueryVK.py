import schedule
import time
import threading
import telebot
from telebot import types
import requests
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..')) #Данная конструкция для возможности импорта из your_dir (след. стр.) функ-и send
from your_dir  import send

#🔍
#✅
#🖊️

#https://t.me/your_BOT_FOR_BOT
#@your_BOT_FOR_BOT

TOKEN_TG = <your_TOKEN>
bot = telebot.TeleBot(TOKEN_TG)


Token_VK_DB = <your_APIvk_TOKEN> #данные по этому токену можно получить в VKdev
#Мониторится стена данной группы:   https://vk.com/its_my_basket
v = 5.131 #api vk версия
domain = 'its_my_basket' 
count = 1

def job(): #проверка по api vk новые обновления в группе баскетбольной секции
    r = requests.get('https://api.vk.com/method/wall.get',
        params={
             'access_token':Token_VK_DB,
             'v':v,
             'domain':domain,
             'count':count})
             
    with open("PATH_To_TXTFile_and_nameTXTFile")as file: 
        old_POST_number = file.read()   #чтение номера последнего (обработанного) поста
    print(old_POST_number)
    new_DATE_id = r.json()['response']['items'][0]['id']
    bot.send_message(TG_id_admin, f'This is info mess. Numbers: {new_DATE_id}, {old_POST_number}')
    c_p_i = check_POST_id(old_POST_number, new_DATE_id) #сравнение последнего (обраб-го) номера поста и пришедшего после реквеста 
    if c_p_i == True:
        new_DATE_TEXT = r.json()['response']['items'][0]['text'] 
        TEXT_For_TG_msg(new_DATE_TEXT, new_DATE_id)
    else:
        pass
       
    
def check_POST_id(old_POST_number, new_DATE_id):    
    print(new_DATE_id)
    if int(new_DATE_id) > int(old_POST_number):
        print('Новый пост!')
        return True
    else:
        pass

###---Эта секция для общего ping`а всех работающих ботов
@bot.channel_post_handler()
def hello(message):
    if message.chat.id == idTgChannel and 'TOTAL' in message.text:
        time.sleep(1.15)
        send("Бот QueryVK ✅ONLINE", TOKEN_TG)
     
###---END Эта секция для общего ping`а всех работающих ботов


def TEXT_For_TG_msg(new_DATE_TEXT, new_DATE_id):
    if "|||" in new_DATE_TEXT: #Была идея идентифицировать тему поста по символу '|||' (из текста поста в вк),
        Finding = new_DATE_TEXT.find("|||")             #но на практике оказалось проще вбивать тему рассылки 
        probel = new_DATE_TEXT.find(' ', Finding+3)                    #вручную, но код остается и он рабочий 
        if probel == -1:
            need_STR = new_DATE_TEXT[Finding+3:]
        else:
            need_STR = new_DATE_TEXT[Finding+3:probel]
        send_msg_NewPOST(new_DATE_id, need_STR)
    else:
        add_Topic_manually(new_DATE_id)

def add_Topic_manually(new_DATE_id): #Добавить тему рассылки вручную
    mess = bot.send_message(TG_id_admin, f'''⚡Новый пост в группе ВК, но БЕЗ темы!
Напиши тему прямо сейчас!⤵️''')
    bot.register_next_step_handler(mess, agree_Topic, new_DATE_id) 

def agree_Topic(mess, new_DATE_id):
    keyboard = types.InlineKeyboardMarkup() 
    button_1 = types.InlineKeyboardButton(text="✅Agree", callback_data = f'Agree-{mess.text}-{new_DATE_id}') 
    button_2 = types.InlineKeyboardButton(text="🖊️Change", callback_data = f'Change-{new_DATE_id}')
    keyboard.add(button_1,  button_2)
    bot.send_message(TG_id_admin, f"""Ты указал тему поста:

{mess.text}

Так подойдет?""", reply_markup=keyboard)


###---обработчик нажатия на inline кнопки 
@bot.callback_query_handler(func = lambda call: True)
def ans(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Done!') 
    LST_For_Topic = call.data.split('-')
    if LST_For_Topic[0] == 'Agree':
        send_msg_NewPOST(LST_For_Topic[2], LST_For_Topic[1])
    elif LST_For_Topic[0] == 'Change':
        print('This is Change', LST_For_Topic)
        add_Topic_manually(LST_For_Topic[1])
    bot.answer_callback_query(callback_query_id=call.id)
###---END обработчик нажатия на inline кнопки 

#В фун-и ниже происходит формироваие ссылки на новый пост в ВК, тема рассылки в ТГ и предлагается мне, как админу,
#скопировать сформированный текст сообщения для рассылки в ТГ и, нажва на SWITCH кнопку, переместится в чат с главным
#ботом и там уже, в свою очередь, выслать это новое сообщение, котрое распространится по всем подписчикам главного ТГ Бота
def send_msg_NewPOST(new_DATE_id, need_STR):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    url_button_To_bigBOT = types.InlineKeyboardButton(text="➡️swiTCH!", url="https://t.me/rash_test_bot")
    keyboard.add(url_button_To_bigBOT)
    STR_MESS = f'https://vk.com/its_my_basket?w=wall-19986115_{new_DATE_id}'
    bot.send_message(TG_id_admin, f'☢️Новый пост в группе ВК. Подтверди(скопировав) или проигнорь!')
    bot.send_message(TG_id_admin, f'''🏀Дорогомилово-Баскет.
Будь в курсе последних новостей!

Новый пост на тему:
{need_STR.replace('_', ' ')}

Подробнее по ссылке
➡{STR_MESS}''', reply_markup=keyboard)
    wr_new_DATE_id(new_DATE_id)
    
    
def wr_new_DATE_id(new_DATE_id): #обновления номера последнего обработанного поста из ВК
    with open('PATH_To_TXTFile_and_nameTXTFile', 'w')as File:
        File.write(str(new_DATE_id))


@bot.message_handler(commands=['check']) #Проверить новый пост ВК вручную
def check_new_POST_vk(message):
    if message.chat.id == TG_id_admin:
        msg_TG = '🔍Проверка нового поста!'
        bot.send_message(message.chat.id, msg_TG)
        job()

@bot.message_handler(content_types=['text']) #На случай, если захочится пингануть боту вручную 
def default_test(message):
    bot.send_message(message.chat.id, '⚠️Ошибка!')
    
        
# Регуляраная проверка ресурса ВК schedule пока отключена, 
# т.к. считаю, что реализовать следует через webHook. В данный момент 
# проверка ресурса ВК на наличие обновлений производится по команде /check в адрес бота 
# (см несколько строк выше)
########schedule.every(15).seconds.do(job)
########
########def go():
########    while 1:
########        schedule.run_pending()
########        time.sleep(1)
########
########t = threading.Thread(target=go, name="тест")
########t.start()


if __name__ == '__main__':
    # print('Малый бот стартанул')
    # bot.polling(none_stop=True, interval=0)
    while True:
        try:
            print('Малый бот стартанул')
            bot.polling(none_stop=True, timeout=123)
        except:
            time.sleep(5)
            continue
