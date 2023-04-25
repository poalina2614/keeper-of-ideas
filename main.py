from random import choice
import logging
import pymorphy2

import requests
from give_advice import advice
from help_funcs import choice_func,what_can,help,card_helper
from delete_functions import *
from add_functions import *
from change_functions import *
from get_one_functions import *
from get_list_functions import *


# Устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO)

sessionStorage = {}

step = 0
func_key = ''
act_title = ''


def main(event, context):
    global step, func_key, act_title
    logging.info(f'Request: {event!r}')  # логирование

    response = {
        'session': event['session'],
        'version': event['version'],
        'response': {
            'end_session': False

        }
    }
    new_user = None  # флаг,отвечающий за то, пользовался юзер этим навыком раньше или нет
    if new_user is None:
        data = requests.get('http://snordy.pythonanywhere.com')
        data = dict(data.json())
        if 'user' in event['session']:
            user_id = event['session']['user']['user_id']
        else:
            response['response']['text'] = 'Чтобы пользоваться этим навыком, вы должны войти в свой яндекс-аккаунт.' \
                                           ' Авторизуйтесь и возвращайтесь!'
            response['response']['end_session'] = True
            return response
        if not (user_id in data):
            data[user_id] = {'events': {}, "notes": {}, 'step': 0, 'func_key': '', 'active_title': ''}
            new_user = True
            requests.post('http://snordy.pythonanywhere.com/post',
                          json=data)  # обновленные данные отправляются на мой сервер

        else:
            new_user = False

    if event['session']['new'] and new_user:  # если сессия новая, то выводим приветственное сообщение
        response['response']['text'] = 'Добро пожаловать, я "Хранитель идей"! 😺  ' \
                                       'Я помогу вам сохранять ваши записи и события, чтобы вы о них не забыли.' \
                                       'Что вы хотите сделать сейчас?'
        response['response']['card'] = {}
        response['response']['card']['type'] = "BigImage"
        response['response']['card']['image_id'] = "1540737/ea7e7e75ed78536cfdbb"
        response['response']['card']['title'] = 'Добро пожаловать в навык "Умные заметки"!'
        response['response']['card'][
            'description'] = "Я помогу вам сохранять ваши записи и события, чтобы вы о них не забыли. Чем я могу помочь?"

        response['response']['buttons'] = [{'title': '💭 Хочу совет!', 'hide': True},
                                           {'title': '📝 Добавить заметку', 'hide': True},
                                           {'title': '❌ Выход', 'hide': False},
                                           {'title': '✏ Редактировать заметку', 'hide': True},
                                           {'title': '⛔ Удалить заметку', 'hide': True},
                                           {'title': '📄 Показать информацию об одной заметке', 'hide': True},
                                           {'title': '📋 Показать список всех заметок', 'hide': True},
                                           {'title': '📆 Добавить событие', 'hide': True},
                                           {'title': '✏ Редактировать событие', 'hide': True},
                                           {'title': '⛔ Удалить событие', 'hide': True},
                                           {'title': '📆 Показать информацию об одном событии', 'hide': True},
                                           {'title': '📅 Показать список всех событий', 'hide': True}]
    elif event['session']['new'] and not (new_user):
        f1 = ['Приветствую!', 'С возвращением!', 'И снова здравствуйте!']
        f2 = ['Что вы хотите сделать сейчас?', 'Чем я могу помочь?', 'Что я могу сделать для вас?']
        w1 = choice(f1)
        w2 = choice(f2)
        response['response']['text'] = w1 + w2
        response['response']['card'] = {}
        response['response']['card']['type'] = "BigImage"
        response['response']['card']['image_id'] = "1540737/ea7e7e75ed78536cfdbb"
        response['response']['card']['title'] = w1
        response['response']['card']['description'] = w2

        response['response']['buttons'] = [{'title': '💭 Хочу совет!', 'hide': True},
                                           {'title': '📝 Добавить заметку', 'hide': True},
                                           {'title': '❌ Выход', 'hide': False},
                                           {'title': '✏ Редактировать заметку', 'hide': True},
                                           {'title': '⛔ Удалить заметку', 'hide': True},
                                           {'title': '📄 Показать информацию об одной заметке', 'hide': True},
                                           {'title': '📋 Показать список всех заметок', 'hide': True},
                                           {'title': '📆 Добавить событие', 'hide': True},
                                           {'title': '✏ Редактировать событие', 'hide': True},
                                           {'title': '⛔ Удалить событие', 'hide': True},
                                           {'title': '📆 Показать информацию об одном событии', 'hide': True},
                                           {'title': '📅 Показать список всех событий', 'hide': True}]
        user_id = event['session']['user']['user_id']
        # обнуляем значения полей "step" и "func_key" при начале диалога
        data = requests.get('http://snordy.pythonanywhere.com').json()
        data[user_id]['step'] = 0
        data[user_id]['func_key'] = ''
        data[user_id]['active_title'] = ''
        requests.post('http://snordy.pythonanywhere.com/post',
                      json=data)

    else:  # если нет, то проверяем ключевые слова в сообщении
        req = ' '.join(event['request']['original_utterance'].lower().split())
        for z in [',', '.', '?', ':', ';', '!']:
            req = ''.join(req.split(z))
        morph = pymorphy2.MorphAnalyzer()
        words_sp = list(map(lambda el: morph.parse(el)[0].normal_form, req.split()))
        user_id = event['session']['user']['user_id']
        data = requests.get('http://snordy.pythonanywhere.com').json()  # получаем инфу с сервера
        step = data[user_id]['step']  # этап выполнения функции
        func_key = data[user_id]['func_key']  # ключ, для определения с какой именно функцией мы работаем
        if event['state']['session']:
            if 'help' in event['state']['session'] and event['state'][
                'session']['help']:  # если есть флаг активной команды помощи
                if 'да' in req:  # если чел подтверждает, что хотел использовать в заметках или события
                    dop_par = event['state']['session'][
                        'help']  # вводим новый аргумент, у которого есть дефолтное значение
                    if 'change_ev' in func_key:  # в этой функции подразделение по названию, а в словаре только общая форма
                        change_event(response, event, user_id, data, dop_par)
                    elif 'change_note' in func_key:
                        change_note(response, event, user_id, data, dop_par)
                    else:
                        sl[func_key](response, event, user_id, data,
                                     dop_par)  # просто вызывем ту функцию, которая была активна, продолжая ее  использование
                elif 'нет' in req:  # если юзер хотел получить помощь
                    if 'ev' in data[user_id]['func_key'] and data[user_id]['active_title'] in data[user_id]['events']:
                        data[user_id]['events'].pop(data[user_id]['active_title'])
                    elif 'no' in data[user_id]['func_key'] and data[user_id]['active_title'] in data[user_id]['notes']:
                        data[user_id]['notes'].pop(data[user_id]['active_title'])
                    ans = ['Я рассказала вам о своих возможностях. 🤖 ', 'Это мои возможности. 🤖 ',
                           'Это всё, что я умею. 🤖 ']
                    response['response']['text'] = choice(ans)

                    choice_func(response)
                    data[user_id]['step'] = 0  # чистим следы ранее активной функции
                    data[user_id]['func_key'] = ''
                    requests.post('http://snordy.pythonanywhere.com/post',
                                  json=data)
                else:
                    response['session_state'] = {'help': event['state']['session']['help'],'func_key':'','step':0}
                    response['response'][
                        'text'] = 'Извините, я вас не поняла, поэтому повторю вопрос. Вы хотели бы использовать фразу,' \
                                  ' в которой упоминается просьба о помощи в своей заметке/событии? ' \
                                  ' Пожалуйста, ответьте да или нет.'
                    response['response']['buttons'] = [{'title': 'Да ✔', 'hide': True},
                                                       {'title': 'Нет ❌', 'hide': True}]

                return response
            elif 'what_can' in event['state']['session'] and event['state'][
                'session']['what_can']:
                if 'да' in req:  # если чел подтверждает, что хотел использовать в заметках или события
                    dop_par = event['state']['session']['what_can']
                    if 'change_ev' in func_key:
                        change_event(response, event, user_id, data, dop_par)
                    elif 'change_note' in func_key:
                        change_note(response, event, user_id, data, dop_par)
                    else:
                        sl[func_key](response, event, user_id, data, dop_par)
                elif 'нет' in req:  # если юзер хотел получить помощь
                    ans = ['Я рассказала вам о своих возможностях. 🤖 ', 'Это мои возможности. 🤖 ',
                           'Это всё, что я умею. 🤖 ']

                    response['response']['text'] = choice(ans)
                    if 'ev' in data[user_id]['func_key'] and data[user_id]['active_title'] in data[user_id]['events']:
                        data[user_id]['events'].pop(data[user_id]['active_title'])
                    elif 'no' in data[user_id]['func_key'] and data[user_id]['active_title'] in data[user_id]['notes']:
                        data[user_id]['notes'].pop(data[user_id]['active_title'])
                    choice_func(response)
                    data[user_id]['step'] = 0
                    data[user_id]['func_key'] = ''
                    requests.post('http://snordy.pythonanywhere.com/post',
                                  json=data)
                else:
                    response['session_state'] = {'what_can': event['state']['session']['what_can'],'func_key':'','step':0}
                    response['response'][
                        'text'] = 'Извините, я вас не поняла, поэтому повторю вопрос. 😨 Вы хотели бы использовать фразу,' \
                                  ' в которой упоминается вопрос о моих возможностях в своей заметке/событии? ' \
                                  ' Пожалуйста, ответьте да или нет.'
                    response['response']['buttons'] = [{'title': 'Да ✔', 'hide': True},
                                                       {'title': 'Нет ❌', 'hide': True}]

                return response


        elif 'помощь' in words_sp or 'помочь' in words_sp or 'помогать' in words_sp or 'хелп' in words_sp:
            if not (func_key):  # если нет активных функций
                help(response)  # просто вызываем функцию хелп
                response['response']['text'] += 'Чем я могу сейчас помочь?'
                response['response']['buttons'] = [{'title': '💭 Хочу совет!', 'hide': True},
                                                   {'title': '📝 Добавить заметку', 'hide': True},
                                                   {'title': '❌ Выход', 'hide': False},
                                                   {'title': '✏ Редактировать заметку', 'hide': True},
                                                   {'title': '⛔ Удалить заметку', 'hide': True},
                                                   {'title': '📄 Показать информацию об одной заметке', 'hide': True},
                                                   {'title': '📋 Показать список всех заметок', 'hide': True},
                                                   {'title': '📆 Добавить событие', 'hide': True},
                                                   {'title': '✏ Редактировать событие', 'hide': True},
                                                   {'title': '⛔ Удалить событие', 'hide': True},
                                                   {'title': '📆 Показать информацию об одном событии', 'hide': True},
                                                   {'title': '📅 Показать список всех событий', 'hide': True}]

            else:
                response['session_state'] = {'help': event['request'][
                    'original_utterance'],'func_key':'','step':0}  # сохраняем ответ юзера, который явялется командой помощь и сохраняем состояние до следующего ответа
                help(response)  # все таки вызываем эту функцию, на всякий случай, чтобы не делать еще больше веток
                # потом уточняем у юзера, хотел ли он увидеть сообщение о помощи или хотел использовать это
                response['response']['card'][
                    'description'] += '\n⚠ Я вывела вам подсказку. Возможно вы хотели использовать его в заметке/событии? ' \
                                      'Если вы ответите да, я использую это. ✔ \n' \
                                      'Если же нет, то Ваши изменения не сохранятся. ❌'
                response['response'][
                    'text'] += '\n⚠ Я вывела вам подсказку. Возможно вы хотели использовать его в заметке/событии? ' \
                               'Если вы ответите да, я использую это. ✔ \n' \
                               'Если же нет, то Ваши изменения не сохранятся. ❌'
                response['response']['buttons'] = [{'title': 'Да ✔', 'hide': True},
                                                   {'title': 'Нет ❌', 'hide': True}]

        elif ('что' in words_sp and 'уметь' in words_sp) or ('что' in words_sp and 'мочь' in words_sp) or (
                'какой' in words_sp and 'возможности' in words_sp):
            if not (func_key):
                what_can(response)
                response['response']['text'] += 'Чем я могу сейчас помочь?'
                response['response']['buttons'] = [{'title': '💭 Хочу совет!', 'hide': True},
                                                   {'title': '📝 Добавить заметку', 'hide': True},
                                                   {'title': '❌ Выход', 'hide': False},
                                                   {'title': '✏ Редактировать заметку', 'hide': True},
                                                   {'title': '⛔ Удалить заметку', 'hide': True},
                                                   {'title': '📄 Показать информацию об одной заметке', 'hide': True},
                                                   {'title': '📋 Показать список всех заметок', 'hide': True},
                                                   {'title': '📆 Добавить событие', 'hide': True},
                                                   {'title': '✏ Редактировать событие', 'hide': True},
                                                   {'title': '⛔ Удалить событие', 'hide': True},
                                                   {'title': '📆 Показать информацию об одном событии', 'hide': True},
                                                   {'title': '📅 Показать список всех событий', 'hide': True}]

            else:
                response['session_state'] = {'what_can': event['request']['original_utterance']}
                what_can(response)
                response['response']['card'][
                    'description'] += '\n⚠ Я вывела вам подсказку. Возможно вы хотели использовать его в заметке/событии? ' \
                                      'Если вы ответите да, я использую это. ✔ \n' \
                                      'Если же нет, то Ваши изменения не сохранятся. ❌'
                response['response'][
                    'text'] += '\n⚠ Я вывела вам подсказку. Возможно вы хотели использовать его в заметке/событии? ' \
                               'Если вы ответите да, я использую это. ✔ \n' \
                               'Если же нет, то Ваши изменения не сохранятся. ❌'
                response['response']['buttons'] = [{'title': 'Да ✔', 'hide': True},
                                                   {'title': 'Нет ❌', 'hide': True}]
        elif ('хотеть' in words_sp or 'дать' in words_sp) and ('совет' in words_sp):
            return advice(response)

        elif func_key == 'add_ev' and step != 0:
            return add_event(response, event, user_id, data)
        elif func_key == 'add_note' and step != 0:
            return add_note(response, event, user_id, data)
        elif func_key == 'del_ev' and step != 0:
            return delete_event(response, event, user_id, data)
        elif 'change_ev' in data[user_id]['func_key'] and step != 0:
            return change_event(response, event, user_id, data)
        elif func_key == 'get_ev':
            return get_event(response, event, user_id, data)
        elif (('событие' in words_sp or 'мероприятие' in words_sp) and (
                'добавить' in words_sp or 'создать' in words_sp)):  # функция вызывается в первый раз
            # в func_key добавляем ее название, как признак активности
            data[user_id]['func_key'] = 'add_ev'
            return add_event(response, event, user_id, data)
        elif (('заметка' in words_sp or 'запись' in words_sp) and ('добавить' in words_sp or 'создать' in words_sp)):
            data[user_id]['func_key'] = 'add_note'
            return add_note(response, event, user_id, data)

        elif (('событие' in words_sp or 'мероприятие' in words_sp) and (
                'удалить' in words_sp or 'убрать' in words_sp or 'удаль' in words_sp or 'стереть' in words_sp)):
            data[user_id]['func_key'] = 'del_ev'
            return delete_event(response, event, user_id, data)

        elif (((('событие' in words_sp or 'мероприятие' in words_sp) and (
                'один' in words_sp)) or 'событие' in req or 'мероприятие' in req) and (
                      'показать' in words_sp or 'вывести' in words_sp)):
            data[user_id]['func_key'] = 'get_ev'
            return get_event(response, event, user_id, data)

        elif (('событие' in words_sp or 'мероприятие' in words_sp) and (
                'изменить' in words_sp or 'редактировать' in words_sp)):
            data[user_id]['func_key'] = 'change_ev'
            return change_event(response, event, user_id, data)

        elif ((('событие' in words_sp or 'мероприятие' in words_sp) and (
                'список' in words_sp or 'весь' in words_sp or 'всё' in words_sp) or 'мероприятия' in req or 'события' in req) and (
                      'получить' in words_sp or 'вывести' in words_sp or 'показать' in words_sp)):
            return get_list_events(response, event, user_id, data)

        elif func_key == 'del_note' and step != 0:  # условие удаление заметки
            return delete_note(response, event, user_id, data)

        elif (('заметка' in words_sp or 'запись' in words_sp) and (
                'удалить' in words_sp or 'удаль' in words_sp or 'убрать' in words_sp or 'стереть' in words_sp)):  # начальное условие удаления заметки
            data[user_id]['func_key'] = 'del_note'
            return delete_note(response, event, user_id, data)

        elif 'change_note' in func_key and step != 0:
            return change_note(response, event, user_id, data)

        elif (('запись' in words_sp or 'заметка' in words_sp) and (
                'изменить' in words_sp or 'редактировать' in words_sp)):
            data[user_id]['func_key'] = 'change_note'
            return change_note(response, event, user_id, data)

        elif ((('заметка' in words_sp or 'запись' in words_sp) and (
                'список' in words_sp or 'весь' in words_sp or 'всё' in words_sp) or 'записи' in req or 'заметки' in req) and (
                      'получить' in words_sp or 'вывести' in words_sp or 'показать' in words_sp)):
            return show_al_no(response, event, user_id, data)
        elif (((('заметка' in words_sp or 'запись' in words_sp) and (
                'один' in words_sp)) or 'заметку' in req or 'запись' in req) and (
                      'показать' in words_sp or 'вывести' in words_sp)):
            data[user_id]['func_key'] = 'get_note'
            return get_note(response, event, user_id, data)
        elif func_key == 'get_note' and step != 0:
            return get_note(response, event, user_id, data)

        elif req in ['выйти', 'выход', 'пока', 'до свидания', 'прощай',
                     'закончить', 'стоп', '❌ выход']:
            farewells = ['До новых встреч! 👋', 'Пока! 👋', 'До свидания! 👋']
            response['response']['text'] = choice(farewells)
            response['response']['end_session'] = True

        else:
            if ' '.join(event['request']['original_utterance'].split()) in data[user_id]['events'].keys():
                data[user_id]['func_key'] = 'get_ev'
                data[user_id]['step'] = 1
                step = 1
                return get_event(response, event, user_id, data)
            response['response']['text'] = 'Извините, я вас не понимаю!'
            response['response']['buttons'] = [{'title': '💭 Хочу совет!', 'hide': True},
                                               {'title': '📝 Добавить заметку', 'hide': True},
                                               {'title': '❌ Выход', 'hide': False},
                                               {'title': '✏ Редактировать заметку', 'hide': True},
                                               {'title': '⛔ Удалить заметку', 'hide': True},
                                               {'title': '📄 Показать информацию об одной заметке', 'hide': True},
                                               {'title': '📋 Показать список всех заметок', 'hide': True},
                                               {'title': '📆 Добавить событие', 'hide': True},
                                               {'title': '✏ Редактировать событие', 'hide': True},
                                               {'title': '⛔ Удалить событие', 'hide': True},
                                               {'title': '📆 Показать информацию об одном событии', 'hide': True},
                                               {'title': '📅 Показать список всех событий', 'hide': True}]
    return response

sl = {'add_note': add_note, 'add_ev': add_event, 'del_note': delete_note,
      'del_ev': delete_event, 'get_ev': get_event, 'get_note': get_note, 'change_note': change_note,
      'change_ev': change_event}