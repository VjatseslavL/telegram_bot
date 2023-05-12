import requests
import telebot
from bs4 import BeautifulSoup
import string
import re

bot = telebot.TeleBot("6101624288:AAG9lUqHj5_EHFxVdTF1bRc6rXcVKl1Dnec")

def add_user(user_id):
    data_user = {
        "user_id": user_id,
        "user_group": "None"
    }
    with open("users.json", "r") as file_read:
        data_users = json.load(file_read)
        if {"user_id": user_id, "user_group": "None"} in data_users:
            pass
        else:
            with open("users.json", "w") as file_write:
                data_users.append({"user_id": user_id, "user_group": "None"})
                json.dump(data_users, file_write, indent=2)
                file_read.close()
                file_write.close()


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id,
                     "Привет, вот тебе список команд, что могут тебе помочь: \n"
                     "/start - посмотреть все возможные команды\n"
                     "/schedule - изменнёное расписание\n"
                     "/teachers - список учителей"
                     "/groups - список групп\n"
                     "/search - поиск группы")

@bot.message_handler(commands=['schedule'])
def send_schedule(message):

    tthk_url = "https://www.tthk.ee/tunni_muudatus/"  # сайт из которого берётся код
    response = requests.get(tthk_url)
    soup = BeautifulSoup(response.content, "html.parser")  # копирования кода с сайта

    soup_table = soup.find_all('table')  #
    # формируем текст для отправки пользователю
    data = []  #
    text = 'Вот изменения в расписании:\n'  # начальное сообщение
    schedule = ""  # строка в которую будет вноситься из таблицы tr td
    for i in range(len(soup_table) - 1):  # количество таблиц
        schedule += "\n"  # добавить в начале строки, чтобы была прорущенная строка в начале перед каждой таблицей
        if i == 0:  # пропустить лишний специальный символ
            schedule = ""
        for j in range(len(soup_table[i].find_all("tr"))):  # количество tr в таблице в которых содержится данные из расписпи
            schedule += "\n"  # перенёс на новую строку ряда
            for k in soup_table[i].find_all("tr")[j]:  # перебор элементов из таблицы
                if k == "\n":  # убрать лишние специальные символы
                    continue
                if len(schedule) >= 4050:  # у сообщения в телеграме есть ограничение по длинне в 4096 байт
                    bot.send_message(message.chat.id, schedule)
                    schedule = ""  # очистка для продолжения сообщения
                    continue
                schedule += f" | {k.text}"  # внесение элементов в сообщение
    bot.send_message(message.chat.id, schedule)  # отправить пользователю сообщение

@bot.message_handler(commands=['teachers'])
def send_search(message):
    url = "https://www.tthk.ee/tunni_muudatus/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    table_soup = soup.find_all("table")
    results_teacher = []
    for table in range(len(table_soup) - 1):
        for tr in range(len(table_soup[table].find_all("tr"))):
            results_teacher.append("\n")
            for td in table_soup[table].find_all("tr")[tr]:
                results_teacher.append(td.text)
    teachers = []
    count = 0
    teachers_copy = results_teacher[::]
    teachers_copy = teachers_copy[1:]
    for table in range(len(teachers_copy)):
        if '\n' in teachers_copy:
            index = teachers_copy.index("\n")
        if len(teachers_copy[:index]) == 6:
            teachers.append(teachers_copy[4])
            teachers_copy = teachers_copy[index:]
            teachers_copy = teachers_copy[1:]
        if len(teachers_copy[:index]) == 5:
            teachers.append(teachers_copy[3])
            teachers_copy = teachers_copy[index:]
            teachers_copy = teachers_copy[1:]
    teachers_message = "Тут список всех групп, что есть в изменённом расписании\n"
    all_teachers = []
    for teachers_element in teachers:
        if teachers_element not in all_teachers:
            all_teachers.append(teachers_element)
            teachers_message += f"{teachers_element}\n"

    teachers_message += "\n /search - поиск в расписании по группе"
    bot.send_message(message.chat.id, teachers_message)


@bot.message_handler(commands=['groups'])
def send_search(message):
    url = "https://www.tthk.ee/tunni_muudatus/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    table_seacrh = soup.find_all("table")
    search_results = []
    for i in range(len(table_seacrh) - 1):
        for j in range(len(table_seacrh[i].find_all("tr"))):
            search_results.append("\n")
            for k in table_seacrh[i].find_all("tr")[j]:
                search_results.append(k.text)
    groups_search = []
    count = 0
    groups_copy = search_results[::]
    groups_copy = groups_copy[1:]
    for i in range(len(groups_copy)):
        if '\n' in groups_copy:
            index = groups_copy.index("\n")
        if len(groups_copy[:index]) == 6:
            groups_search.append(groups_copy[2])
            groups_copy = groups_copy[index:]
            groups_copy = groups_copy[1:]
        if len(groups_copy[:index]) == 5:
            groups_search.append(groups_copy[1])
            groups_copy = groups_copy[index:]
            groups_copy = groups_copy[1:]
    group_message = "Тут список всех групп, что есть в изменённом расписании\n"
    all_groups = []
    for group in groups_search:
        if group not in all_groups:
            all_groups.append(group)
            group_message += f"{group}\n"

    group_message += "\n /search - поиск в расписании по группе"
    bot.send_message(message.chat.id, group_message)
    copylist = search_results[::]

@bot.message_handler(commands=['search'])
def send_search(message):
    bot.send_message(message.chat.id, "Введите группу для поиска:\n")
    @bot.message_handler(content_types=['text'])
    def send_search(message):
        listgroup = []
        url = "https://www.tthk.ee/tunni_muudatus/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        table = soup.find_all('table')  #

        list_seacrh = []
        for i in range(len(table) - 1):
            for j in range(len(table[i].find_all("tr"))):
                list_seacrh.append("\n")
                for k in table[i].find_all("tr")[j]:
                    list_seacrh.append(k.text)
        list_group_search = []
        count = 0
        list_seacrh_copy = list_seacrh[::]
        list_seacrh_copy = list_seacrh_copy[1:]
        for i in range(len(list_seacrh_copy)):
            if '\n' in list_seacrh_copy:
                index = list_seacrh_copy.index("\n")
            if len(list_seacrh_copy[:index]) == 6:
                list_group_search.append(list_seacrh_copy[2])
                list_seacrh_copy = list_seacrh_copy[index:]
                list_seacrh_copy = list_seacrh_copy[1:]
            if len(list_seacrh_copy[:index]) == 5:
                list_group_search.append(list_seacrh_copy[1])
                list_seacrh_copy = list_seacrh_copy[index:]
                list_seacrh_copy = list_seacrh_copy[1:]

        messagegroup = "Тут список всех групп, что есть в изменённом расписании\n"
        listgroup = []
        for i in list_group_search:
            if i not in listgroup:
                listgroup.append(i)
                messagegroup += f"{i}\n"

        # формируем текст для отправки пользователю
        data = []  #
        text1 = 'Вот изменения в расписании:\n'  # начальное сообщение
        schedule = " "
        for i in range(len(table) - 1):  # количество таблиц
            if message.text not in listgroup:
                bot.send_message(message.chat.id, "Такой группы не сущетсвует!")
                text1 = ""
                break
            for j in range(len(table[i].find_all("tr"))):  # количество tr в таблице в которых содержится данные из расписпи
                text = " | ".join(data) + "\n"
                if message.text in text and message.text in listgroup:
                    text1 += "| "
                    text1 = "".join(f"{text1}{text}")
                data.clear()
                for k in table[i].find_all("tr")[j]:  # перебор элементов из таблицы
                    if k == "\n":  # убрать лишние специальные символы
                        continue
                    if k.text not in data:
                        data.append(k.text)
        if len(text1) != 0:
            bot.send_message(message.chat.id, text1)

bot.polling()
