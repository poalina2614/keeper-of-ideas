import requests
from random import choice
from help_funcs import *
def change_note(response, event, user_id, data, dop_par=''):
    step = data[user_id]['step']
    act_title = data[user_id]['active_title']
    end = 0
    if step == 0:
        if not (data[user_id]['notes'].keys()):
            ans = ['Очень жаль, но сейчас ваш список заметок пуст. 😿 ', 'У вас ещё нет ни одной заметки. 😿 ',
                   'В вашем списке ещё нет заметок. 😿']
            k = choice(ans)
            picture = ['213044/202d725e84df12d2da06', '1540737/ed20068e251d427d878f', '1656841/4788ab4350b72c9cfe31',
                       '997614/9d952f90b24459a8bfb4']
            response['response']['text'] = k
            response['response']['card'] = {}
            response['response']['card']['type'] = "BigImage"
            response['response']['card']['image_id'] = choice(picture)
            response['response']['card']['description'] = k
            choice_func(response)
            data[user_id]['step'] = 0  # поэтому обнуляем поле "step"
            data[user_id]['func_key'] = ''
            requests.post('http://snordy.pythonanywhere.com/post',
                          json=data)
            return response
        else:
            titles_list = '\n🔹 '.join(data[user_id]['notes'].keys())
            titles_list = '🔹 ' + titles_list
            response['response']['text'] = titles_list + '\n' + 'Вот все ваши заметки. ' \
                                                                'Пожалуйста, скажите название той, которую хотите изменить.'
            requests.post('http://snordy.pythonanywhere.com/post',
                          json=data)
    if step == 1:
        if dop_par:
            title = dop_par
        else:
            title = ' '.join(event['request']['original_utterance'].split())
        if title in data[user_id]['notes'].keys():
            data[user_id]['active_title'] = title
            response['response']['text'] = 'Выберите то, что хотите изменить. '
            response['response']['buttons'] = [{'title': '📄 Название', 'hide': True},
                                               {'title': '📝 Текст', 'hide': True}]
            requests.post('http://snordy.pythonanywhere.com/post',
                          json=data)
        else:
            titles_list = '\n🔹 '.join(data[user_id]['notes'].keys())
            titles_list = '🔹 ' + titles_list
            ans = ['К сожалению, заметка не была найдена. 😿 ', 'Увы, такой записи в списке нет! 😿 ']
            response['response']['text'] = choice(ans) + 'Вот список доступных заметок:' + '\n' + titles_list + '\n'
            return response


    elif step == 2:
        if dop_par:
            params = dop_par
        else:
            params = ' '.join(event['request']['original_utterance'].split()).lower()
        if 'название' in params or 'заголовок' in params:
            data[user_id]['func_key'] += "_title"
            response['response']['text'] = 'Какой заголовок должен быть у этой заметки?'
        elif 'описание' in params or 'текст' in params or 'содержимое' in params or 'содержание' in params:
            data[user_id]['func_key'] += "_text"
            response['response']['text'] = 'Какое новое содержание будет у этой заметки?'
        else:
            response['response']['text'] = 'Извините, но я не поняла, что именно вы хотите изменить.' \
                                           ' Вы можете редактировать название и описание заметки. ' \
                                           'Попробуйте ещё раз.'
            response['response']['buttons'] = [{'title': '📄 Название', 'hide': True},
                                               {'title': '📝 Текст', 'hide': True}]
            return response
    elif step == 3:
        if dop_par:
            user_ans = dop_par
        else:
            user_ans = ' '.join(event['request']['original_utterance'].split())
        if 'text' in data[user_id]['func_key']:
            data[user_id]['notes'][act_title]['text'] = user_ans
        elif 'title' in data[user_id]['func_key']:
            if user_ans not in data[user_id]['notes'].keys():
                old_title_data = data[user_id]['notes'][act_title]
                data[user_id]['notes'].pop(act_title)
                data[user_id]['notes'][user_ans] = old_title_data
            else:
                ans = ['Заметка с таким названием уже существует! Пожалуйста, придумайте другое. ',
                       'Такое название уже есть в списке! Пожалуйста, напишите новое. ',
                       'Это имя уже занято, пожалуйста, придумайте новое!']
                response['response']['text'] = choice(ans)
                return response

        ans = ['Всё хорошо, я сохранила ваши изменения! ✔ ', 'Изменения были успешно внесены. ✔  ']
        response['response']['text'] = choice(ans)
        choice_func(response)
        end = 1
        data[user_id]['step'] = 0  # поэтому обнуляем поле "step"
        data[user_id]['func_key'] = ''
        requests.post('http://snordy.pythonanywhere.com/post',
                      json=data)
    if not (end):  # если функция не закончилась
        data[user_id]['step'] += 1  # переходим на следующий шаг и постим изменения
        requests.post('http://snordy.pythonanywhere.com/post',
                      json=data)
    return response

def change_event(response, event, user_id, data, dop_par=''):
    step = data[user_id]['step']
    act_title = data[user_id]['active_title']
    end = 0
    if step == 0:
        if not (data[user_id]['events'].keys()):
            ans = ['Очень жаль, но сейчас ваш список событий пуст. 😿 ', 'Вы пока не добавили ни одного события. 😿 ',
                   'В вашем списке ещё нет событий. 😿 ']
            k = choice(ans)
            picture = ['213044/202d725e84df12d2da06', '1540737/ed20068e251d427d878f', '1656841/4788ab4350b72c9cfe31',
                       '997614/9d952f90b24459a8bfb4']
            response['response']['text'] = k
            response['response']['card'] = {}
            response['response']['card']['type'] = "BigImage"
            response['response']['card']['image_id'] = choice(picture)
            response['response']['card']['description'] = k

            choice_func(response)
            data[user_id]['step'] = 0  # поэтому обнуляем поле "step"
            data[user_id]['func_key'] = ''
            requests.post('http://snordy.pythonanywhere.com/post',
                          json=data)
            return response
        else:
            titles_list = '\n🔹 '.join(data[user_id]['events'].keys())
            titles_list = '🔹 ' + titles_list
            response['response']['text'] = titles_list + '\n' + 'Вот все ваши события. ' \
                                                                'Пожалуйста, скажите название того, которое хотите изменить.'
            requests.post('http://snordy.pythonanywhere.com/post',
                          json=data)
    if step == 1:
        if dop_par:
            title = dop_par
        else:
            title = ' '.join(event['request']['original_utterance'].split())
        if title in data[user_id]['events'].keys():
            data[user_id]['active_title'] = title
            response['response']['text'] = 'Выберите то, что хотите изменить. '
            response['response']['buttons'] = [{'title': '📄 Название', 'hide': True},
                                               {'title': '📝 Описание', 'hide': True},
                                               {'title': '🕜 Время', 'hide': True}, {'title': '📆 Дата', 'hide': True}]
            requests.post('http://snordy.pythonanywhere.com/post',
                          json=data)
        else:
            titles_list = '\n🔹 '.join(data[user_id]['events'].keys())
            titles_list = '🔹 ' + titles_list
            ans = ['К сожалению, событие не было найдено. 😿 ', 'Увы, такого события в списке нет! 😿 ']
            response['response']['text'] = choice(ans) + 'Вот список доступных мероприятий:' + '\n' + titles_list + '\n'
            return response

    elif step == 2:
        if dop_par:
            params = dop_par
        else:
            params = ' '.join(event['request']['original_utterance'].split()).lower()
        if 'время' in params:
            data[user_id]['func_key'] += "_time"
            ans = ['В какое время это событие должно начаться? 🕘 ', 'Напишите время проведения этого события. 🕘 ']
            response['response']['text'] = choice(ans)
        elif 'название' in params:
            data[user_id]['func_key'] += "_title"
            response['response']['text'] = 'Какой заголовок должен быть у этого события?'
        elif 'описание' in params or 'текст' in params or 'содержимое' in params:
            data[user_id]['func_key'] += "_desc"
            response['response']['text'] = 'Что вы хотите сказать об этом событии?'
        elif 'дату' in params or 'день' in params or 'дата' in params:
            data[user_id]['func_key'] += '_date'
            response['response']['text'] = 'Какого числа должно произойти это событие?'
        else:
            response['response']['text'] = 'Извините, но я не поняла, что именно вы хотите изменить. 😔 ' \
                                           ' Вы можете редактировать название, описание, время и дату мероприятия. ' \
                                           'Попробуйте ещё раз.'

            response['response']['buttons'] = [{'title': '📄 Название', 'hide': True},
                                               {'title': '📝 Описание', 'hide': True},
                                               {'title': '🕜 Время', 'hide': True}, {'title': '📆 Дата', 'hide': True}]
            return response
    elif step == 3:
        if dop_par:
            user_ans = dop_par
        else:
            user_ans = ' '.join(event['request']['original_utterance'].split())
        if 'time' in data[user_id]['func_key']:
            data[user_id]['events'][act_title]['time'] = user_ans
        elif 'date' in data[user_id]['func_key']:
            data[user_id]['events'][act_title]['date'] = user_ans
        elif 'desc' in data[user_id]['func_key']:
            data[user_id]['events'][act_title]['description'] = user_ans
        elif 'title' in data[user_id]['func_key']:
            old_title_data = data[user_id]['events'][act_title]
            data[user_id]['events'].pop(act_title)
            data[user_id]['events'][user_ans] = old_title_data
        ans = ['Всё хорошо, я сохранила ваши изменения! ✔ ', 'Изменения были успешно внесены. ✔ ',
               f'Событие "{act_title}" было успешно изменено! ✔ ']
        response['response']['text'] = choice(ans)
        choice_func(response)
        end = 1
        data[user_id]['step'] = 0  # поэтому обнуляем поле "step"
        data[user_id]['func_key'] = ''
        requests.post('http://snordy.pythonanywhere.com/post',
                      json=data)
    if not (end):  # если функция не закончилась
        data[user_id]['step'] += 1  # переходим на следующий шаг и постим изменения
        requests.post('http://snordy.pythonanywhere.com/post',
                      json=data)
    return response