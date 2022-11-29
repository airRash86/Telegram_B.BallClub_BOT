import sqlite3 as sq 
import telebot
from telebot import types
import os
import sys
import time

sys.path.insert(1, os.path.join(sys.path[0], '..')) #Данная конструкция для возможности импорта из your_dir (след. стр.) функ-ю send
from your_dir import send

TOKEN = <your_TOKEN>

bot = telebot.TeleBot(TOKEN)
 
###https://t.me/rash_test_bot
###@Dorogomil-BASKET_BOT

#✅
#🤝
#⚠️
#🏀
#⚡
#➡️
#ℹ️
#⤵️
#⛔
#❓
#↪️
#⭕
#🔍  



###---------Unsubscribe
@bot.message_handler(commands=['OTPISKA'])
def OTPISKA(message):
    with sq.connect('PATH_To_DB_and_nameDB')as con:
        cur = con.cursor()
        cur.execute(f"""SELECT id_TG, spec FROM Descrip_THEMSELF WHERE id_TG = {message.chat.id}""")
        check = cur.fetchone()
        print(check)
        if len(check[0]) == 2 and check[0][1] == 'allowed':
            BUTT_OTPISKA = types.InlineKeyboardMarkup()
            agree_OTPISKA = types.InlineKeyboardButton(text = "Да", callback_data = f'AgreeNewUserOrDel-{message.chat.id}-OTPISKA')
            STAY_HERE_BUTT = types.InlineKeyboardButton(text = "Нет", callback_data = 'back')
            BUTT_OTPISKA.add(agree_OTPISKA, STAY_HERE_BUTT)
            bot.send_message(message.chat.id, f'''❓Отказаться от получения уведомлений о новостях в Дорогомилово-баскет?
''', reply_markup=BUTT_OTPISKA)
### --------END Unsubscribe

###---Взятие номера
@bot.message_handler(commands=['number'])
def phone(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text='📞Поделиться номером',request_contact=True)
    keyboard.add(button_phone)
    msg_phone = bot.send_message(message.chat.id, '''Чтобы поделиться номером телефона просто нажмите на кнопку
"📞Поделиться номером" ниже ⤵️

❗Вручную с клавиатуры номер вводить НЕ нужно!''', reply_markup=keyboard)
    bot.register_next_step_handler(msg_phone, contact) 
##---перехват и вывод номера телефона 
@bot.message_handler(content_types=['contact'])
def contact(message):
    keyboard = types.ReplyKeyboardRemove()
    if message.contact is not None:
        mess = message.contact.phone_number
        T_mess = f'Номер:  {mess}  - сохранен в базу'
        bot.send_message(message.chat.id, T_mess, reply_markup=keyboard)
        print(message.contact.phone_number) 
        add_Phone_Num(message, mess)
    elif message.text == '/menu':
        geophone(message)
    else:
        bot.send_message(message.chat.id, '''⚠️Некорректная команда! Для передачи номера следуйте инструкции ниже
или нажмите ➡️/menu для перехода в главное меню,
но тогда регистрация не будет завершена!''', reply_markup=keyboard)
        phone(message)
        

@bot.message_handler(commands=['menu', 'start'])
def geophone(message):
    # Эти параметры для клавиатуры необязательны, просто для удобства
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_1 = types.KeyboardButton(text= "🏀Написать боту Дорогомилово-Баскет") 
    button_2 = types.KeyboardButton(text="📸Фото тренировочного зала") 
    button_3 = types.KeyboardButton(text="⚙️Запрос в поддержку")
    keyboard.add(button_1,  button_2, button_3)
    msg_For_START_chaT=bot.send_message(message.chat.id, """🤝Привет! Это бот Баскетбольной секции

➡️Если вы еще не занимались в Дорогомилово-Баскет (ДБ), то
нажмите "Написать боту Дорогомилово-Баскет"

➡Если же вы уже тренируетесь в ДБ, то все равно нажмите на "Написать боту Дорогомилово-Баскет",
так ваши занятия в секции станут еще удобнее!""", reply_markup=keyboard)
##    bot.register_next_step_handler(msg_For_START_chaT, ansWRE_To_START_chaT, keyboard) # возможно имеет смысл действовать через NEXT_STEP


##---обработка текстовых
@bot.message_handler(content_types=['text']) 
def default_test(message):
    if message.text == "🏀Написать боту Дорогомилово-Баскет":
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Отлично!', reply_markup=keyboard)
        CHECK_id_TG = check_id_TG(message.chat.id)
        if CHECK_id_TG == None:
            Hi_To_new_member(message) 
        elif CHECK_id_TG == False:    
            G_C_Mes = Global_Check(message)
            if G_C_Mes == 2:
                bot.send_message(message.chat.id, 'ℹ️Для завершения регистрации вам нужно поделиться номером телефона!', reply_markup=keyboard)
                phone(message)
            elif G_C_Mes == 3:
                priVET_non_STOP(message)
    elif message.text == "⚙️Запрос в поддержку":
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Чтобы написать в поддержку - выберите один из способов ниже!', reply_markup=keyboard)
        suppORT(message)
    elif message.text == "📸Фото тренировочного зала":
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Готово!', reply_markup=keyboard)
        BUTT = types.InlineKeyboardMarkup()
        FOTO_gym = types.InlineKeyboardButton(text = "📸Зал-1", callback_data = 'FOTO_gym')
        FOTO_gym_2 = types.InlineKeyboardButton(text = "📸Зал-2", callback_data = 'FOTO_gym_2')
        FOTO_balls = types.InlineKeyboardButton(text = "📸Мячи", callback_data = 'FOTO_balls')
        FOTO_shower = types.InlineKeyboardButton(text = "📸Душ", callback_data = 'FOTO_shower')
        FOTO_TOILET = types.InlineKeyboardButton(text = "📸Туалет", callback_data = 'FOTO_TOILET')
        FOTO_dress_room = types.InlineKeyboardButton(text = "📸Раздевалка", callback_data = 'FOTO_dress_room')
        FOTO_Table_Tennis = types.InlineKeyboardButton(text = "📸Наст. Теннис", callback_data = 'FOTO_Table_Tennis')
        BACK = types.InlineKeyboardButton(text ="↩️Назад в меню", callback_data = 'back') 
        BUTT.add(FOTO_gym, FOTO_gym_2, FOTO_balls, FOTO_shower, FOTO_TOILET, FOTO_dress_room, FOTO_Table_Tennis, BACK)
        bot.send_message(message.chat.id, 'Выберите фото', reply_markup=BUTT)
###---взаимодействие с другим ботом (новый пост вк)
    elif message.chat.id == TG_id_admin and '''🏀Дорогомилово-Баскет.
Будь в курсе последних новостей!

Новый пост на тему:''' in message.text:
        rassilka(message.text)
###---END взаимодействие с другим ботом (новый пост вк)
    else:
        abc=types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Ошибка!', reply_markup=abc)
        bot.send_message(message.from_user.id, f'''⚠️"{message.text}" - некорректная команда
Нажмите /menu и выбирете один из пунктов главного меню''')
        try:
            bot.edit_message_reply_markup(message.chat.id, message_id = message.message_id-1, reply_markup = '')
        except:
            print('Зато без ошибки)))')
####---END обработка текстовых 


def suppORT(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    url_button = types.InlineKeyboardButton(text="🟦Написать в VK!", url="https://vk.com/admin")
    url_button_1 = types.InlineKeyboardButton(text="🟢Написать в WHATS App!", url="https://api.whatsapp.com/send?phone=adminPHONEnum")
    url_button_2 = types.InlineKeyboardButton(text="🔵Написать в TG!", url="https://t.me/adminNICKname")
    url_button_3 = types.InlineKeyboardButton(text="↩️Назад в меню", callback_data = 'back')
    keyboard.add(url_button, url_button_1, url_button_2, url_button_3)
    bot.send_message(message.chat.id, "📡Способы связи:", reply_markup=keyboard)


###---FOTO
def FOTO_1_2_3_4_5(call, arg):
    ###циклом фор --- BUTT.add из передавать вторым аргументом строку call.data   
    BUTT = types.InlineKeyboardMarkup(row_width=3)
    FOTO_gym = types.InlineKeyboardButton(text = "📸Зал-I", callback_data = 'FOTO_gym')
    FOTO_gym_2 = types.InlineKeyboardButton(text = "📸Зал-2", callback_data = 'FOTO_gym_2')
    FOTO_balls = types.InlineKeyboardButton(text = "📸Мячи", callback_data = 'FOTO_balls')
    FOTO_shower = types.InlineKeyboardButton(text = "📸Душ", callback_data = 'FOTO_shower')
    FOTO_TOILET = types.InlineKeyboardButton(text = "📸Туалет", callback_data = 'FOTO_TOILET')
    FOTO_dress_room = types.InlineKeyboardButton(text = "📸Раздевалка", callback_data = 'FOTO_dress_room')
    FOTO_Table_Tennis = types.InlineKeyboardButton(text = "📸Наст.Теннис", callback_data = 'FOTO_Table_Tennis')
    BACK = types.InlineKeyboardButton(text ="↩️Назад в меню", callback_data = 'back')
    supply = [FOTO_gym, FOTO_gym_2, FOTO_balls, FOTO_shower, FOTO_TOILET, FOTO_dress_room, FOTO_Table_Tennis, BACK]
    For_save = []
    for i in supply:
        if i.callback_data != arg:
            For_save.append(i)
    saved = tuple(For_save)
    BUTT.add(*saved)
    bot.send_message(call.message.chat.id, 'Вы также можете просмотреть и другие фото⤵', reply_markup=BUTT)
###---END FOTO

###---Эта секция для общего ping`а всех работающих ботов
@bot.channel_post_handler()
def hello(message):
    if message.chat.id == -1001856957974  and 'TOTAL' in message.text:
        send("Первый (Dorogomil-Bas) 1960073417 ✅ONLINE", TOKEN)
        # bot.reply_to(message, "✅ВторойAFTERdel_5288033405_ONLINE")
###---END Эта секция для общего ping`а всех работающих ботов
    
###---Проверка на наличие id_TG в БД
def check_id_TG(b):
    with sq.connect('PATH_To_DB_and_nameDB')as con:
            cur = con.cursor()
            cur.execute(f"""SELECT id_TG FROM Descrip_THEMSELF WHERE Descrip_THEMSELF.id_TG = {b}""")
            check = cur.fetchone()
            if check == None:
                return None
            else:
                return False
###---END Проверка на наличие id_TG в БД

###---Начальный глобальный обработчик Global_Check(message)
def Global_Check(message):
    with sq.connect('PATH_To_DB_and_nameDB')as con:
        cur = con.cursor()
        cur.execute(f"""SELECT Name_secName, Temporary_descrip, phone_number FROM Descrip_THEMSELF WHERE Descrip_THEMSELF.id_TG = {message.chat.id}""")
        check_Global = cur.fetchone()
    if len(check_Global[0])!=0 and len(check_Global[1])==0 and len(str(check_Global[2]))==0:
        print(check_Global[0], 'это 1 (Name_secName, т.е. введи описание)')
        add_discr(message)
    elif len(check_Global[0])!=0 and len(check_Global[1])!=0 and len(str(check_Global[2]))==0:
        print(check_Global[1], 'это 2 (TempDiscr, т.е. введи телеофн)')
        return 2
    elif len(check_Global[0])!=0 and len(check_Global[1])!=0 and len(str(check_Global[2]))!=0:
        print(f'Привет, {check_Global[0]}! Не бросай баскетбол!')
        return 3
###---END Начальный глобальный обработчик Global_Check(message)

### --- приветствие для новых участников
def Hi_To_new_member(message): 
    msg_name = bot.send_message(message.chat.id, f'''☝️Бот работает в тестовом режиме и, возможно, ваших данных еще нет в системе)

💡Есть предложение познакомиться!
Как вас зовут?

ℹИдентификация безопасна и нужна для получения вами в числе первых информации об интересных
мероприятиях в Дорогомилово-Баскет.

➡️Напишите пожалуйста ваши имя и фамилию в одном сообщении.''') 
    bot.register_next_step_handler(msg_name,FIKS_name)  
### --- END приветствие для новых участников


###---Рассылка по клиентам
def rassilka(TEXT):
    with sq.connect('PATH_To_DB_and_nameDB')as con:
        cur = con.cursor()
        cur.execute(f"""SELECT id_TG FROM Descrip_THEMSELF WHERE spec = 'allowed'""")
        ids = cur.fetchall()
    TEXT+= """

Отписаться от рассылки: нажмите /OTPISKA"""
    rassilka_GO(TEXT, ids)
    
def rassilka_GO(TEXT, ids):
    print('rassilka_GO')
    try:
        for i in ids:
            try:
                print(i[0])                    
                bot.send_message(i[0], TEXT)
            except:
                pass
                print('error: ', i)
    except:
        pass            
###---END Рассылка по клиентам
    
######------IF DESCR IS FULL
def priVET_non_STOP(message):
    with sq.connect('PATH_To_DB_and_nameDB')as con:
        cur = con.cursor()
        cur.execute(f"""SELECT Name_secName FROM Descrip_THEMSELF WHERE Descrip_THEMSELF.id_TG = {message.chat.id}""")
        check = cur.fetchone()
        
        bot.send_message(message.chat.id, f'''ℹ️Исходя из данных бота, вас зовут:    {check[0]},
Если это верная информация, то продолжайте играть в баскетбол🏀! 

Если же нужны коррективы, то нажмите на ➡️/menu,
а затем нажмите на кнопку
⚙Запрос в поддержку  ''')
######------END IF DESCR IS FULL

###---- Подтверждение имени при регистрации 
def FIKS_name(message):
    BUTT_hi = types.InlineKeyboardMarkup()
    y_name = types.InlineKeyboardButton(text = "✅Да", callback_data = 'yes_name')
    n_name = types.InlineKeyboardButton(text = "🖊️Изменить", callback_data = 'change')
    buT_back = types.InlineKeyboardButton(text = "↩️Глав. меню", callback_data = 'back')
    BUTT_hi.add(y_name, n_name, buT_back)
    bot.send_message(message.chat.id, f'''Вас зовут:   {message.text}
Верно?''', reply_markup=BUTT_hi)
#----- END Подтверждение имени при регистрации

##---Обработчик нажатий на inline кнопки 
@bot.callback_query_handler(func = lambda call: True)
def ans(call):
    if call.data == 'FOTO_gym':
        img = open('/PATH/зал1.jpg', 'rb')
        bot.send_photo(call.message.chat.id,  img)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Фото игрового зала') #удаление инлайн клавы
        FOTO_1_2_3_4_5(call, call.data)
    elif call.data == 'FOTO_gym_2':
        img_2 = open('/PATH/зал2.jpg', 'rb')
        bot.send_photo(call.message.chat.id,  img_2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Фото')
        FOTO_1_2_3_4_5(call, call.data)
    elif call.data == 'FOTO_balls':
        img_3 = open('/PATH/мячи.jpg', 'rb')
        bot.send_photo(call.message.chat.id,  img_3)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Снаряды')
        FOTO_1_2_3_4_5(call, call.data)
    elif call.data == 'FOTO_shower':
        img_4 = open('/PATH/душ.jpg', 'rb')
        bot.send_photo(call.message.chat.id,  img_4)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Фото душевой')
        FOTO_1_2_3_4_5(call, call.data)
    elif call.data == 'FOTO_TOILET':
        img_5 = open('/PATH/туалет.jpg', 'rb')
        bot.send_photo(call.message.chat.id,  img_5)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Фото туалета')
        FOTO_1_2_3_4_5(call, call.data)
    elif call.data == 'FOTO_dress_room':
        img_6 = open('/PATH/раздевалка.jpg', 'rb')
        bot.send_photo(call.message.chat.id,  img_6)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Фото раздевалки')
        FOTO_1_2_3_4_5(call, call.data)
    elif call.data == 'FOTO_Table_Tennis':
        img_7 = open('/PATH/теннис.jpg', 'rb')
        bot.send_photo(call.message.chat.id,  img_7)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='В перерыве можно поиграть и в настольный Теннис!')
        FOTO_1_2_3_4_5(call, call.data) 
    elif call.data == 'back':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='↩️Возврат в главное меню!')
        geophone(call.message)
    elif call.data == 'yes_name':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='✅Супер!')
        c_m_id = call.message.chat.id
        T_m = call.message.text
        if 'Вас зовут: ' in T_m:
            T_m = T_m.replace('Вас зовут: ', '')
            if 'Верно?' in T_m:
                T_m = T_m.replace('Верно?', '')
                T_m = T_m.strip()
        with sq.connect('PATH_To_DB_and_nameDB')as con:
            cur = con.cursor()
            cur.execute(f"INSERT INTO Descrip_THEMSELF VALUES (?, ?, ?, ?, ?, ?)", (c_m_id, T_m, '', '', '', ''))
            print('Зарегано!')
            add_discr(call.message)
    elif call.data == 'change':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='ок!')
        Hi_To_new_member(call.message)
    elif call.data == 'no chang':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='⏳Секундочку...', reply_markup=None)      
        if '➡Вы описали себя так:' in call.message.text:
            call.message.text = call.message.text.replace('➡Вы описали себя так:', '')
            if 'Вас устраивает или необходимо внести коррективы?' in call.message.text:
                call.message.text = call.message.text.replace('Вас устраивает или необходимо внести коррективы?', '')
                if 'Выберите один из двух вариантов ниже!' in call.message.text: 
                    call.message.text = call.message.text.replace('Выберите один из двух вариантов ниже!', '') 
        else:
            pass
        V_V = check_id_TG(call.message.chat.id) #---отсбда блок по добавлению описания в БД
        if V_V == False:
            C_D_T = check_Temporary_descrip(call.message.chat.id)
            if C_D_T == None:
                with sq.connect('PATH_To_DB_and_nameDB')as con:
                    cur = con.cursor()
                    cur.execute(f"""UPDATE Descrip_THEMSELF SET Temporary_descrip = '{call.message.text.strip()}' WHERE
id_TG = {call.message.chat.id}""")
                bot.send_message(call.message.chat.id, '''💥Отлично! Почти готово)

Следуйте инструкции далее.
☎️Осталось только ввести номер телефона
Это безопасно и никакого спама)''')
                phone(call.message)
            else:
                print(f'Ваша характеристика: {C_D_T}')
        elif V_V == None:
            print('HE IS NOT IN DATE BASE!') #---END отсбда блок по добавлению описания в БД
    elif call.data == 'pravka':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Ща!')
        add_discr(call.message)
    elif 'AgreeNewUserOrDel' in call.data:
        LST_in_add_or_del = call.data.split('-')
        with sq.connect('PATH_To_DB_and_nameDB')as con:
            cur = con.cursor()
            if len(LST_in_add_or_del) == 2:
                cur.execute(f"""UPDATE Descrip_THEMSELF SET spec = 'allowed' WHERE
id_TG = {LST_in_add_or_del[1]}""")
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='✅Новый юзер добавлен в рассылку')
            elif len(LST_in_add_or_del) == 3:
                cur.execute(f"""UPDATE Descrip_THEMSELF SET spec = ' ' WHERE
id_TG = {LST_in_add_or_del[1]}""")
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='⭕Уведомления прекращены')
    elif call.data == 'FAULT_NewUser_In_mailing':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='⛔Отказ в добавлении нового юзера в рассылку')
        
    bot.answer_callback_query(callback_query_id=call.id) #это чтобы иконка часов не висела на кнопке 
###---END Обработчик нажатий на inline кнопки

###---Занесение телефона в базу
def add_Phone_Num(message, arg):
    with sq.connect('PATH_To_DB_and_nameDB')as con:
        cur = con.cursor()
        cur.execute(f"""UPDATE Descrip_THEMSELF SET phone_number = '{arg}' WHERE
id_TG = {message.chat.id}""")
    Finishing(message)
    
def Finishing(message):
    BUTT_Fin = types.InlineKeyboardMarkup()
    m_BUTT = types.InlineKeyboardButton(text = "Главное меню", callback_data = 'back')
    BUTT_Fin.add(m_BUTT)
    bot.send_message(message.chat.id, '''✅На этом всё!
Теперь клуб 🏀Дорогомилово-Баскет стал еще ближе
Продолжайте играть в Баскетбол, а от этого бота иногда будут приходить уведомления
об интересных событиях Клуба!
Если они покажутся вам навязчивыми, то от рассылки всегда можно отписаться)

А сейчас вы можете перейти в главное меню и глянуть, например, там фотки,
для этого просто нажмите на кнопку "Главное меню"⤵️
  
🤝Спасибо, что выбрали Дорогомилово-Баскет!''', reply_markup=BUTT_Fin)
    print(message.chat.id)
    alarm_New_Member(message)

####----- Обработка add New user
def alarm_New_Member(message):
    with sq.connect('PATH_To_DB_and_nameDB')as con:
        cur = con.cursor()
        cur.execute(f"""SELECT * FROM Descrip_THEMSELF WHERE id_TG = {message.chat.id}""")
        check = cur.fetchone()
    BUTT_alarm = types.InlineKeyboardMarkup()
    agree_BUTT = types.InlineKeyboardButton(text = "✅Add", callback_data = f'AgreeNewUserOrDel-{message.chat.id}')
    FAULT_BUTT = types.InlineKeyboardButton(text = "⛔FAULT", callback_data = 'FAULT_NewUser_In_mailing')
    url_WApp_BUTT = types.InlineKeyboardButton(text="↪️W.App NewUser !", url=f"https://api.whatsapp.com/send?phone={check[3]}")
    BUTT_alarm.add(agree_BUTT, FAULT_BUTT, url_WApp_BUTT)
    bot.send_message(416735064, f'''✅Added new user
➡️TG id: {check[0]}
➡️name: {check[1]}
➡️desck: {check[2]}
➡️phone: {check[3]}

❓Добавить его в рассылку из ВК?
''', reply_markup=BUTT_alarm)
####-----END Обработка add New user
    
    
###---Блок запроса и внесения в БД описания нового юзера 
@bot.message_handler(commands=['add_discr']) 
def add_discr(message):
    knop = types.ReplyKeyboardMarkup(resize_keyboard=True)
    knop.add(types.KeyboardButton('✅Да'), types.KeyboardButton('⛔Нет')) 
    msg_For_chaT = bot.send_message(message.chat.id, """➡️Чтобы начать тренировки в Дорогомилово-Баскет
вам нужно немного рассказать о себе. Совсем не сложно. Сделаете это на следующем шаге?""", reply_markup=knop)
    bot.register_next_step_handler(msg_For_chaT, ansWRE_To_TG)

def ansWRE_To_TG(message):   #внимание к bot.send_message, а не хендлер
    knop = types.ReplyKeyboardRemove()
    if message.text == '✅Да':
        msg = bot.send_message(message.chat.id, '''✏️Напишите о себе:
- ❓Ваш рост, возраст
- ❓Занимались ли баскетболом? Если да, то где (клуб, секция, улица) и как долго?
- ❓Какой сейчас род деятельности (учеба/работа)? Какое направление учебного заведения или работы?
ℹ️Пишите пожалуйств в свободной форме, но важно указать данные о себе в одном сообщении,
а не разбивать рассказ о себе на несколько отдельных сообшений.
⚡Приступайте прямо сейчас!''', reply_markup=knop)
        bot.register_next_step_handler(msg, add_To_DB)
    elif message.text == '⛔Нет':
        bot.send_message(message.chat.id, '''Нет, так нет...''', reply_markup=knop)
        bot.send_message(message.chat.id, '↩️Возврат в главное меню')        
        geophone(message)
    elif message.text == '/menu':
        bot.send_message(message.from_user.id, f'''↩️Возврат в главное меню''', reply_markup=knop)
        geophone(message)
    else:
        knop = types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, f'''⚠️"{message.text}" - некорректная команда
Попробуйте еще раз или нажмите на /menu для возврата в главное меню''', reply_markup=knop)
        beTWEEn(message)
        
def beTWEEn(message):
    bot.send_message(message.from_user.id, '⏳Секундочку...')
    add_discr(message)
    

def add_To_DB(message):
    a = message.text
    b = message.chat.id
    markup = types.InlineKeyboardMarkup() 
    switch_button = types.InlineKeyboardButton(text='🖊️Изменить',   callback_data = 'pravka')
    switch_button_1 = types.InlineKeyboardButton(text='✅Без изменений', callback_data = 'no chang')
    markup.add(switch_button_1, switch_button)
    bot.send_message(message.chat.id, f"""➡Вы описали себя так:

{a}

Вас устраивает или необходимо внести коррективы?
Выберите один из двух вариантов ниже!""", reply_markup = markup)
###---END Блок запроса и внесения в БД описания нового юзера 


###---Проверка на наличие Temporary_descrip, найденного по id_TG в БД
def check_Temporary_descrip(b):
    with sq.connect('PATH_To_DB_and_nameDB')as con:
            cur = con.cursor()
            cur.execute(f"""SELECT Temporary_descrip FROM Descrip_THEMSELF WHERE id_TG = {b}""")
            check = cur.fetchone()
            if len(check[0]) == 0:
                return None
            else:
                return len(check[0])
###---END Проверка на наличие Temporary_descrip, найденного по id_TG в БД

# print('БОТ СТАРТАНУЛ')
# bot.polling()

while True:
    try:
        print('БОТ Дорогомилово-Баскет СТАРТАНУЛ')
        bot.polling(none_stop=True, timeout=123)
    except:
        time.sleep(5)
        continue









