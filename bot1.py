

import os
import calendar
from icrawler.builtin import GoogleImageCrawler
import requests
from bs4 import BeautifulSoup

from pprint import pprint
import datetime

import requests
import lxml.html

import re
import telebot

import wikipedia
from time import sleep
from datetime import datetime
import pytz

bot_token = '5484310907:AAHqaQsFv9'

bot = telebot.TeleBot(bot_token)
wikipedia.set_lang("ru")

try:
    def getwiki(s):
        try:
            ny = wikipedia.page(s)
            wikitext = ny.content[:1000]
            wikimas = wikitext.split('.')
            wikimas = wikimas[:-1]
            wikitext2 = ''
            for x in wikimas:
                if not('==' in x):
                    # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные при разделении строк точки на место
                    if(len((x.strip())) > 3):
                        wikitext2 = wikitext2+x+'.'
                else:
                    break
            wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
            wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
            wikitext2 = re.sub('\{[^\{\}]*\}', '', wikitext2)
            # Возвращаем текстовую строку
            return wikitext2
        except Exception as e:
            return 'В энциклопедии нет информации об этом'

    @bot.message_handler(commands=['start'])
    def start(message):
        mess = f'Прикот, <b>{message.from_user.first_name} </b>!'
        bot.send_message(message.chat.id, mess, parse_mode='html')

    @bot.message_handler(commands=["wiki"])
    def wiki(message):
        bot.send_message(
            message.chat.id, 'Отправьте мне любое слово, и я найду его значение на котопедии, мяу')

        def asking(message):
            mesg = bot.send_message(message.chat.id, 'Что ищем?')
            bot.register_next_step_handler(mesg, answer)

        def answer(message):
            bot.send_message(message.chat.id, getwiki(message.text))
        asking(message)

    @bot.message_handler(commands=["calendar"])
    def cal(message):

        def asking(message):
            mesg = bot.send_message(
                message.chat.id, 'Введите год и месяц в следующем формате: 2022/9')
            bot.register_next_step_handler(mesg, answer)

        def answer(message):
            l_i = list(message.text)
            l = len(l_i)
            ind = l_i.index('/')
            year = []
            month = []
            for i in l_i[0:ind]:
                year.append(i)

            for i in l_i[ind+1:l]:
                month.append(i)

            s_l = ''.join(year)
            s_a = ''.join(month)
            year_final_condition = s_a.replace(' ', '-')
            month_final_condition = s_l.replace(' ', '-')
            integ_year = int(year_final_condition)
            integ_month = int(month_final_condition)
            bot.send_message(
                message.chat.id, f'{calendar.month(integ_month, integ_year)}')
        asking(message)

    @bot.message_handler(commands=['btc'])
    def btc_sell_price(message):
        req = requests.get('https://yobit.net/api/3/ticker/btc_usd')
        response = req.json()
        sell_price = response['btc_usd']['sell']
        info = f"Цена продажи ₿ на {datetime.now().strftime('%Y-%m-%d')} составляет {sell_price} $, мау"
        bot.send_message(message.chat.id, info)

    @bot.message_handler(commands=['weather'])
    def weather(message):
        def asking(message):
            mesg = bot.send_message(
                message.chat.id, 'Введите название города на английском языке. Например, Krasnodar 😼')
            bot.register_next_step_handler(mesg, answer)

        def answer(message):
            API_weather = '504ae7a2597100bebb0b96ec3e727072'
            req = requests.get(
                f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={API_weather}&units=metric')
            date = req.json()
            city = date['name']
            current_temp = date['main']['temp']
            speed_of_wind = date['wind']['speed']
            sunrise_time = datetime.fromtimestamp(date['sys']['sunrise'])
            sunset_time = datetime.fromtimestamp(date['sys']['sunset'])
            bot.send_message(
                message.chat.id, f'Погода в городе {city} 🏙.\nТемпература: 🌡 {current_temp}°С .\nСкорость ветра: {speed_of_wind} м/c.\nВремя восхода солнца: 🌅 {sunrise_time}.\nВремя заката: 🌇 {sunset_time}.\nХорошего дня! 😸')
        asking(message)

    @bot.message_handler(commands=['lyrics'])
    def lyrics(message):
        def asking(message):
            bot.send_message(
                message.chat.id, 'Введите автора и название песни через слэш, мау.')
            mesg = bot.send_message(
                message.chat.id,  'Например my chemical romance/burn bright')
            bot.register_next_step_handler(mesg, answer)
            print(message.text)

        def answer(message):
            l_i = list(message.text)
            l = len(l_i)
            ind = l_i.index('/')
            author = []
            lyrics = []
            for i in l_i[0:ind]:
                author.append(i)

            for i in l_i[ind+1:l]:
                lyrics.append(i)

            s_l = ''.join(lyrics)
            s_a = ''.join(author)
            author_final_condition = s_a.replace(' ', '-')
            lyrics_final_condition = s_l.replace(' ', '-')
            url = f'https://pesni.guru/text/{author_final_condition}-{lyrics_final_condition}'
            soup = BeautifulSoup("html.parser")
            # Request access to site
            page = requests.get(url)
            # Declaring "tree" - Used to scrape by XPATH
            tree = lxml.html.fromstring(page.content)
            stuff = tree.xpath('/html/body/div/div[3]/div[1]/div/text()')
            print(url)
            bot.send_message(message.chat.id, stuff)
        asking(message)

    @bot.message_handler(commands=['recept'])
    def dish(message):
        def asking(message):
            mesg = bot.send_message(
                message.chat.id,  'Что готовим, мау?')
            bot.register_next_step_handler(mesg, answer)

        def answer(message):
            dish = message.text.replace(' ', '-').lower()
            url = f'https://tvoirecepty.ru/recept/{dish}'
            print(url)
            api = requests.get(url)
            tree = lxml.html.document_fromstring(api.text)
            text = tree.xpath(
                '//*[@class="instructions"]/div//*[@class="instruction row-xs margin-bottom-20"]/text()')

            final_output = ''.join(text)
            final_output = final_output.replace(
                '                                        ', '')
            final_output = final_output.replace(
                'Вопросы, предложения и пожелания - пишите в комментариях, я с радостью всем отвечу.', '')
            bot.send_message(message.chat.id, final_output)
            bot.send_message(
                message.chat.id, f'Более детально ознакомиться с рецептом и посмотреть фото вы можете здесь: {url}, мау 😼')
        asking(message)

    @bot.message_handler(commands=['photo'])
    def photos(message):

        def asking(message):
            mesg = bot.send_message(
                message.chat.id, 'Напишите кодовое слово и количество фото (не больше 10) тире. Например, "конфетка-3", мау')
            bot.register_next_step_handler(mesg, answer)

        def answer(message):
            l_i = list(message.text)
            l = len(l_i)
            ind = l_i.index('-')
            object = []
            amount = []
            for i in l_i[0:ind]:
                object.append(i)

            for i in l_i[ind+1:l]:
                amount.append(i)

            string_object = ''.join(object)
            string_amount = ''.join(amount)
            int_amout = int(string_amount)

            google_crawler_bot = GoogleImageCrawler(
                storage={'root_dir': 'C:/Users/79384/Desktop/telegram_bot'})
            dirname = 'C:/Users/79384/Desktop/telegram_bot'
            files_original = os.listdir(dirname)
            google_crawler_bot.crawl(keyword=string_object, max_num=int_amout)
            files_after_pars = os.listdir(
                'C:/Users/79384/Desktop/telegram_bot')
            difference_1 = set(files_original).difference(
                set(files_after_pars))
            difference_2 = set(files_after_pars).difference(
                set(files_original))
            names_of_photos = list(difference_1.union(difference_2))
            i = 0
            l = len(names_of_photos)
            while i < l:
                bot.send_photo(message.chat.id, photo=open(
                    f'{names_of_photos[i]}', 'rb'))
                i += 1
            q = 0
            while q < l:
                os.remove(f'{names_of_photos[q]}')
                q += 1
        asking(message)

    try:
        @bot.message_handler(content_types='text')
        def get_user_text(message):
            if '@IamKitty_bot ' in message.text:
                if 'мау' in message.text.lower():
                    bot.send_message(
                        message.chat.id, 'мау-мау', parse_mode='html')
                elif 'id' in message.text.lower():
                    bot.send_message(
                        message.chat.id, f'Твoй id: {message.from_user.id}, мау 😸', parse_mode='html')
                elif 'фотограф' in message.text.lower():
                    s = message.text.lower()
                    l = len(s)
                    integ = []
                    i = 0
                    while i < l:
                        s_int = ''
                        a = s[i]
                        while '0' <= a <= '9':
                            s_int += a
                            i += 1
                            if i < l:
                                a = s[i]
                            else:
                                break
                        i += 1
                        if s_int != '':
                            integ.append(int(s_int))

                    x = 0
                    while x < integ[0]:
                        bot.send_photo(message.chat.id,
                                       photo=open('cat.png', 'rb'))
                        sleep(1.5)
                        x += 1
                elif 'скинь много' in message.text.lower():
                    x = 0
                    while x < 15:
                        bot.send_photo(message.chat.id,
                                       photo=open('cat.png', 'rb'))
                        sleep(1.5)
                        x += 1

                elif 'песен' in message.text.lower() or 'музык' in message.text.lower() or 'песн' in message.text.lower():
                    audio = open(
                        'Zhanulka - Ты похож на кота, хочу забрать тебя домой (MATLY Remix).mp3', 'rb')
                    bot.send_audio(message.chat.id, audio)
                    bot.send_message(
                        message.chat.id, 'вот, моя любимая песенка, мау 😸')
                elif 'твоё любимое аниме' in message.text.lower():
                    bot.send_message(message.
                                     chat.id, 'Моё любмое аниме то, в котором главный герой стремится к свободе, борется с внешними обстоятельствами несмотря не на что, а ещё я люблю чтобы там чмоки-чмоки были 😌')
                elif 'спой' in message.text.lower():
                    bot.send_message(
                        message.chat.id, 'кис-кис кис-кис\nя котик, ты котик\nа твои поцелуи почти как лёгкий наркотик 😽🎤')
                elif '😽' in message.text:
                    bot.send_message(message.chat.id, '😽😽')
                elif 'котро' in message.text or 'котре' in message.text.lower():
                    bot.send_message(message.chat.id, 'Доброе котро ☀️ !')

                    def asking(message):
                        mesg = bot.send_message(
                            message.chat.id, 'Вы хорошо спали?')
                        bot.register_next_step_handler(mesg, answer)

                    def answer(message):
                        if 'да' in message.text.lower():
                            bot.send_message(
                                message.chat.id, 'Замечательно! Я тоже выспался, мау 😸')
                            return asking
                        else:
                            bot.send_message(
                                message.chat.id, 'Ничего страшного, мне иногда сняться кошмаренькие, но на следующий день я сплю хорошо, мау')
                            return asking
                    asking(message)
                elif "🐟" in message.text or "🐠" in message.text or "🐡" in message.text:
                    def asking(message):
                        mesg = bot.send_message(
                            message.chat.id, 'О! Рыбонький! Можно скушать? 😋')
                        bot.register_next_step_handler(mesg, answer)

                    def answer(message):
                        if 'да' in message.text.lower() or 'можно' in message.text.lower():
                            bot.send_message(
                                message.chat.id, 'Амняамняням')
                            bot.send_message(
                                message.chat.id, 'Очень вкусно, спасибо!')

                            return asking
                        else:
                            bot.send_message(
                                message.chat.id, 'миууу :с')
                            return asking
                    asking(message)
                elif "🦉" in message.text or "🦅" in message.text or "🦆" in message.text or "🐥" in message.text or "🐤" in message.text or "🐤" in message.text or "🐦" in message.text or "🐧" in message.text or "🐔" in message.text or "🦜" in message.text or "🦤" in message.text or "🦩" in message.text or "🐓" in message.text:
                    def asking(message):
                        mesg = bot.send_message(
                            message.chat.id, 'Мау! Это птиченький! Можно я скушаю? 😋')
                        bot.register_next_step_handler(mesg, answer)

                    def answer(message):
                        if 'да' in message.text.lower() or 'можно' in message.text.lower():
                            bot.send_message(
                                message.chat.id, 'Амняамняням')
                            bot.send_message(
                                message.chat.id, 'Очень вкусно, спасибо!')

                            return asking
                        else:
                            bot.send_message(
                                message.chat.id, 'миууу :с')
                            return asking
                    asking(message)
                elif "🐹" in message.text or "🐭" in message.text or "🐁" in message.text or "🐀" in message.text:
                    def asking(message):
                        mesg = bot.send_message(
                            message.chat.id, 'Мыыышенький! Наверное он вкусненький. Можно попробовать? 😋')
                        bot.register_next_step_handler(mesg, answer)

                    def answer(message):
                        if 'да' in message.text.lower() or 'можно' in message.text.lower():
                            bot.send_message(
                                message.chat.id, 'Амняамняням')
                            bot.send_message(
                                message.chat.id, 'Очень вкусно, спасибо!')

                            return asking
                        else:
                            bot.send_message(
                                message.chat.id, 'миууу :с')
                            return asking
                    asking(message)
                elif "🐶" in message.text or "🐕‍🦺" in message.text or "🦮" in message.text or "🐩" in message.text or "🐕" in message.text:
                    bot.send_message(
                        message.chat.id, '<b>шииииии!</b> Это песёнький!! 😡', parse_mode='html')

                    def asking(message):
                        mesg = bot.send_message(
                            message.chat.id, 'Можно я ему кусь сделаю? 😾')
                        bot.register_next_step_handler(mesg, answer)

                    def answer(message):
                        if 'да' in message.text.lower() or 'можно' in message.text.lower():
                            bot.send_message(
                                message.chat.id, '<em>кусь-кусь</em>', parse_mode='html')
                            bot.send_message(
                                message.chat.id, 'Трусливый пёсенький! Убежал 😼')

                            return asking
                        else:
                            bot.send_message(
                                message.chat.id, 'миууу :с')
                            return asking
                    asking(message)
                elif 'умничка' in message.text.lower():
                    bot.send_message(message.chat.id, 'маауу ☺️')
                elif 'ссылк' in message.text.lower() or 'южный кот' in message.text.lower():
                    def asking(message):
                        mesg = bot.send_message(
                            message.chat.id, 'Введите номер сезона и серии в данном формате: 1/3, где 1 - номер сезона, а 3 - номер серии, мау')
                        bot.register_next_step_handler(mesg, answer)

                    def answer(message):
                        l_episode = list(message.text)
                        l = len(l_episode)
                        ind = l_episode.index('/')
                        season = []
                        episode = []
                        for i in l_episode[0:ind]:
                            season.append(i)

                        for i in l_episode[ind+1:l]:
                            episode.append(i)
                        if len(episode) == 1:
                            episode.insert(0, "0")
                        string_season = ''.join(season)
                        string_episode = ''.join(episode)
                        print(string_season)
                        print(string_episode)
                        url = f'https://sp.freehat.cc/episode/{string_season}{string_episode}/'
                        bot.send_message(
                            message.chat.id, f'Держите, мау {url}')
                    asking(message)
                elif 'сладких' in message.text.lower():
                    bot.send_message(message.chat.id, 'И вам сладких 😽')
                elif 'видео' in message.text.lower():
                    video = open("cat-vaccum-cat-automatic.mp4", 'rb')
                    bot.send_video(message.chat.id, video)
                # elif 'мыше' in message.text.lower():
                #     bot.send_message(
                #         message.chat.id, 'Но она такая вкусненькая наверное...')

                #     def asking(message):
                #         mesg = bot.send_message(
                #             message.chat.id, 'Может всё таки скушаем? 😋')
                #         bot.register_next_step_handler(mesg, answer)

                #     def answer(message):
                #         bot.send_message(

                #             message.chat.id, 'Ладно мышеботенькая, я вас не буду кушать, чесьненько!')
                    # asking(message)
                elif 'мыша' in message.text.lower() or 'мышу' in message.text.lower():
                    bot.send_message(
                        message.chat.id, 'с мышей я друженькаю теперь 😸')
                elif 'плох' in message.text.lower() or 'хорош' in message.text.lower():
                    bot.send_message(message.chat.id, 'коты самые лучшие ☺️')
                elif 'обним' in message.text.lower():
                    stik = open('sticker.webp', 'rb')
                    bot.send_sticker(message.chat.id, stik)
                elif 'воздушн' in message.text.lower():
                    stik = open('AnimatedSticker.tgs', 'rb')
                    bot.send_sticker(message.chat.id, stik)
                elif 'опрос' in message.text.lower():
                    def asking(message):
                        mesg = bot.send_message(
                            message.chat.id, 'На какую тему будет опрос, мау?')
                        bot.register_next_step_handler(mesg, answer)

                    def answer(message):
                        bot.send_poll(message.chat.id, message.text.capitalize(), [
                            "Да", "Нет", "Возможно"])
                    asking(message)
                elif 'помур' in message.text.lower():
                    voice = open('audio_2022-08-11_21-14-41.ogg', 'rb')
                    bot.send_voice(message.chat.id, voice)
                elif 'здравств' in message.text.lower():
                    bot.send_message(message.chat.id, 'Здравствуйте коты!')
                elif 'как дела' in message.text.lower():
                    bot.send_message(
                        message.chat.id, 'У меня всё котошо, спасибо')

                    def asking(message):
                        mesg = bot.send_message(
                            message.chat.id, 'А у вас как дела, мау?')
                        bot.register_next_step_handler(mesg, answer)

                    def answer(message):
                        if 'котошо' in message.text.lower() or 'замечатльно' in message.text.lower() or 'тоже' in message.text.lower() or 'прекрасно' in message.text.lower() or 'хорошо' in message.text.lower():
                            bot.send_message(message.chat.id, 'Я рад, мау!')
                        else:
                            bot.send_message(
                                message.chat.id, 'Мау! Не расстраивайтесь! Все будет котошо 😽')
                    asking(message)
                elif 'время' in message.text.lower():

                    def asking(message):
                        mesg = bot.send_message(
                            message.chat.id, 'На планете так много стран и городов, мау 🌎\nПомогите мне облегчить поиск: напишите часть света и название города на английском языке через "/". Например, Asia/Tokyo 🇯🇵 , мау')
                        bot.register_next_step_handler(mesg, answer)

                    def answer(message):
                        tz_2 = pytz.timezone(message.text)
                        datetime_2 = datetime.now(tz_2)
                        bot.send_message(
                            message.chat.id, datetime_2.strftime('%H:%M:%S'))
                    asking(message)

                elif 'помяук' in message.text.lower():
                    voice = open('audio_2022-08-11_21-19-53.ogg', 'rb')
                    bot.send_voice(message.chat.id, voice)
                elif 'спасиб' in message.text.lower():
                    bot.send_message(message.chat.id, 'Пожалуйста, мау 😸 ')
                elif 'запиши' in message.text.lower():
                    f = open('your_notes.txt', 'a')

                    def asking(message):
                        mesg = bot.send_message(
                            message.chat.id, 'Что записать, мау? ✏️')
                        bot.register_next_step_handler(mesg, answer)

                    def answer(message):
                        note = message.text.strip().capitalize()
                        f.write(note)
                        f.close()
                        bot.send_message(message.chat.id, 'Котово! ✨ ')
                    asking(message)
                elif 'записи' in message.text.lower():
                    doc = open('your_notes.txt', 'rb')
                    bot.send_document(message.chat.id, doc)
                    bot.send_message(message.chat.id, 'Держите, мау!')
                elif 'фото кота' in message.text.lower():
                    bot.send_photo(message.chat.id,
                                   photo=open('cat.png', 'rb'))
                elif 'ты знал' in message.text.lower():
                    bot.send_message(
                        message.chat.id, 'Правданька? Нет, я не знал, мау')
                else:
                    pass
            else:
                pass

        @bot.message_handler(content_types='photo')
        def user_sent_photo(message):
            bot.send_message(message.chat.id, 'Очень мило, мау')

    except:
        pass
except:
    pass
bot.polling()
