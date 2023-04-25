import requests
from random import choice
from help_funcs import *


def add_event(response, event, user_id, data, dop_par=''):
    step = data[user_id]['step']
    act_title = data[user_id]['active_title']
    end = 0  # 0, если функция еще выполняется
    if step == 0:  # шаг прибавляется после каждого отправленного сообщения от навыка
        ans = ['Скажите название мероприятия.', 'Какое название будет у этого события?']
        response['response']['text'] = choice(ans)

    elif step == 1:
        if not (dop_par):
            title = ' '.join(event['request']['original_utterance'].split())  # получаем текст сообщения от пользователя
        else:
            title = dop_par
        if title not in data[user_id]['events']:
            data[user_id]['events'][title] = {'date': '', 'time': '', 'description': ''}
            data[user_id]['active_title'] = title  # запоминание названия события, с которым мы работаем
            ans = ['Теперь описание события.', 'Теперь, скажите пару слов об этом событии. ',
                   'Что вы можете сказать об этом событии?']
            response['response']['text'] = choice(ans)  # отправляем ответ с запросом данных
        else:
            response['response']['text'] = 'Событие с таким названием уже существует! Пожалуйста, придумайте другое. '
            return response
    elif step == 2:
        if dop_par:
            desc = dop_par
        else:
            desc = event['request']['original_utterance']
        data[user_id]['events'][act_title]['description'] = desc
        ans = ['Почти всё! Добавьте время начала события. ', 'Отлично! Сейчас скажите время проведения мероприятия. ']
        response['response']['text'] = choice(ans)

    elif step == 3:
        if dop_par:
            time = dop_par
        else:
            time = event['request']['original_utterance']
        data[user_id]['events'][act_title]['time'] = time
        ans = ['И последнее! Напишите дату мероприятия в любом удобном для Вас виде. ',
               'И наконец, введите дату вашего события. ']
        response['response']['text'] = choice(ans)

    elif step == 4:  # этот шаг последний
        if dop_par:
            date = dop_par
        else:
            date = event['request']['original_utterance']
        data[user_id]['events'][act_title]['date'] = date
        response['response']['text'] = f'Я запомнила ваше событие "{act_title}". ✔ ' \
                                       f'Теперь вы сможете получить к нему доступ в любое время, ' \
                                       f'сказав мне "{act_title}" или получить список всех событий. '
        data[user_id]['step'] = 0  # поэтому обнуляем поле "step"
        data[user_id]['func_key'] = ''  # и "func_key", как признак того, что никакая функция не выполняется
        requests.post('http://snordy.pythonanywhere.com/post',
                      json=data)
        end = 1
        choice_func(response)  # лепим к ответу стандартную фразу
    if not (end):  # если функция не закончилась
        data[user_id]['step'] += 1  # переходим на следующий шаг и постим изменения
        requests.post('http://snordy.pythonanywhere.com/post',
                      json=data)
    return response


def add_note(response, event, user_id, data, dop_par=''):  # добавление заметки
    step = data[user_id]['step']
    act_title = data[user_id]['active_title']
    end = 0  # 0, если функция еще выполняется
    if step == 0:  # шаг прибавляется после каждого отправленного сообщения от навыка
        ans = ['Скажите название заметки.', 'Напишите заголовок для заметки. ', 'Как будет называться ваша заметка?']
        response['response']['text'] = choice(ans)
    elif step == 1:
        if dop_par:
            title = dop_par
        else:
            title = ' '.join(event['request']['original_utterance'].split())
        if title not in data[user_id]['notes']:
            data[user_id]['notes'][title] = {'text': ''}
            data[user_id]['active_title'] = title
            ans = ['Теперь описание заметки. ', 'Сейчас скажите содержание заметки. ', 'Добавьте описание заметки. ']
            response['response']['text'] = choice(ans)
        else:
            ans = ['Заметка с таким названием уже существует! Пожалуйста, придумайте другое. ',
                   'Такое название уже есть в списке! Пожалуйста, напишите новое. ',
                   'Это имя уже занято, пожалуйста, придумайте новое!']
            response['response']['text'] = choice(ans)
            return response

    elif step == 2:
        if dop_par:
            text = dop_par
        else:
            text = ' '.join(event['request']['original_utterance'].split())
        data[user_id]['notes'][act_title]['text'] = text
        ans = [f'Всё прошло успешно! Я запомнила вашу заметку "{act_title}". ✔ ',
               f'Ваша заметка "{act_title}" добавлена! ✔ ',
               f'Отлично! Ваша заметка "{act_title}" создана. ✔ ']
        response['response']['text'] = choice(ans)
        data[user_id]['step'] = 0
        data[user_id]['func_key'] = ''  # и "func_key", как признак того, что никакая функция не выполняется
        requests.post('http://snordy.pythonanywhere.com/post',
                      json=data)
        end = 1
        choice_func(response)
    if not (end):  # если функция не закончилась
        data[user_id]['step'] += 1  # переходим на следующий шаг и постим изменения
        requests.post('http://snordy.pythonanywhere.com/post',
                      json=data)
    return response
