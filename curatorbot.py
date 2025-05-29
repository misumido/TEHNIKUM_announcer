import time
import telebot
from datetime import date
import threading
import schedule
import curatorbase
from calendar_client import ggl

bot = telebot.TeleBot("")

calendar_actual = []
calendar_status0 = []
calendar_status1 = []


def get_actual_calendars():
    all_from_api = ggl.evenets_list()
    actual_date = str(date.today())
    for a in all_from_api:
        if a.get("Дата события") == actual_date:
            calendar_actual.append(a)


def announcement(calendar_actual):
    db_groups = curatorbase.get_groups()
    for a in calendar_actual:
        for b in db_groups:
            try:
                api_name_index = a.get("Название").index(",")
                api_name = a.get("Название")[0:api_name_index]
                if api_name == b[0]:
                    group_id = b[1]
                    lesson_num = a.get("Название")[api_name_index+1:]
                    speaker_and_lesson_name = a.get("Описание")
                    lesson_time = a.get("Время события")

                    bot.send_message(group_id, f"Ребят, всем привет👋\n\n"
                                               f"📚Блок {api_name}\n"
                                               f"{lesson_num} в {lesson_time}\n"
                                               f"{speaker_and_lesson_name}\n\n"
                                               f"Полетели🚀 ждём всех без опозданий")
                    calendar_status1.append([api_name, group_id])
            except:
                if a not in calendar_status0:
                    calendar_status0.append(a)
                    bot.send_message(305896408, f"Анонс не выполнен: {calendar_status0}")


def feedback(calendar_status1):
    for groups in calendar_status1:
        try:
            group_id = groups[1]
            bot.send_message(group_id, "Добрый вечер ребят 👋\n"
                                       "Уделите 2 минуты для обратной связи🤍 \n\n"
                                       "https://forms.gle/Z45pmgdUFmdWdPbY9")
        except:
            bot.send_message(305896408, f"Обратная связь не отправлена: {groups}")
    calendar_status1.clear()
    calendar_status0.clear()


schedule.every().day.at("18:26").do(get_actual_calendars)
schedule.every().day.at("18:27").do(announcement, calendar_actual=calendar_actual)
schedule.every().day.at("18:28").do(feedback, calendar_status1=calendar_status1)


def all_schedules():
    while True:
        schedule.run_pending()
        time.sleep(1)



@bot.channel_post_handler()
def channel(message):
    channel_id = message.chat.id
    channel_name = message.chat.title
    add_to_base = curatorbase.add_group(channel_name, channel_id)
    if add_to_base == True:
        bot.send_message(305896408, f'{channel_name} добавлен в базу')


schedules_treading = threading.Thread(target=all_schedules)

schedules_treading.start()

bot.polling()

# если нужно будет отправлять сообщения в группу
# @bot.message_handler(content_types=['new_chat_members'])
# def add_group_to_base(message):
#     new_member_id = message.json.get("new_chat_participant").get("id")
#     if new_member_id == 6605946285:
#         group_id = message.chat.id
#         group_name = message.chat.title
#         add_to_base = curatorbase.add_group(group_name, group_id)
#         bot.send_message(message.chat.id, f'{add_to_base}')
