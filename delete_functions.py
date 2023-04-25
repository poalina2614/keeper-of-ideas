import requests
from random import choice
from help_funcs import *
def delete_event(response, event, user_id, data, dop_par=''):
    step = data[user_id]['step']
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
                                                                'Пожалуйста, скажите название того, которое хотите удалить.'
            data[user_id]['step'] += 1
            requests.post('http://snordy.pythonanywhere.com/post',
                          json=data)

    elif step == 1:
        if dop_par:
            title = dop_par
        else:
            title = ' '.join(event['request']['original_utterance'].split())
        if title in data[user_id]['events'].keys():
            data[user_id]['events'].pop(title)
            ans = [f'Событие "{title}" удалено из вашего списка мероприятий! ✔ ',
                   f'Я удалила событие "{title}" из ваших мероприятий! ✔ ']
            response['response']['text'] = choice(ans)
            choice_func(response)
            data[user_id]['step'] = 0  # поэтому обнуляем поле "step"
            data[user_id]['func_key'] = ''  # и "func_key", как признак того, что никакая функция не выполняется
            requests.post('http://snordy.pythonanywhere.com/post',
                          json=data)
        else:
            titles_list = '\n🔹 '.join(data[user_id]['events'].keys())
            titles_list = '🔹 ' + titles_list
            ans = ['К сожалению, событие не было найдено. 😿 ', 'Увы, такого события в списке нет! 😿 ']
            response['response']['text'] = choice(ans) + 'Вот список доступных мероприятий:' + '\n' + titles_list + '\n'
    return response


def delete_note(response, event, user_id, data, dop_par=''):  # удаление заметки
    step = data[user_id]['step']
    if step == 0:
        if not (data[user_id]['notes'].keys()):
            ans = ['Очень жаль, но сейчас ваш список заметок пуст. 😿 ', 'У вас ещё нет ни одной заметки. 😿 ',
                   'В вашем списке ещё нет заметок. 😿']
            picture = ['213044/202d725e84df12d2da06', '1540737/ed20068e251d427d878f', '1656841/4788ab4350b72c9cfe31',
                       '997614/9d952f90b24459a8bfb4']
            k = choice(ans)
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
            choice_func(response)
            return response
        else:
            titles_list = '\n🔹 '.join(data[user_id]['notes'].keys())
            titles_list = '🔹 ' + titles_list
            ans = ['Какую вы хотите удалить? Укажите её заголовок. ',
                   'Напишите заголовок той заметки, которую хотите удалить. ',
                   'Пожалуйста, скажите название той, которую хотите удалить. ']
            response['response']['text'] = titles_list + '\n' + 'Вот все ваши заметки. ' + choice(ans)

            data[user_id]['step'] += 1
            requests.post('http://snordy.pythonanywhere.com/post',
                          json=data)

    elif step == 1:
        if dop_par:
            title = dop_par
        else:
            title = ' '.join(event['request']['original_utterance'].split())
        if title in data[user_id]['notes'].keys():
            data[user_id]['notes'].pop(title)
            response['response']['text'] = f'Заметка "{title}" удалена из вашего списка записей! ✔ '
            choice_func(response)
            data[user_id]['step'] = 0  # поэтому обнуляем поле "step"
            data[user_id]['func_key'] = ''  # и "func_key", как признак того, что никакая функция не выполняется
            requests.post('http://snordy.pythonanywhere.com/post',
                          json=data)
        else:
            titles_list = '\n🔹 '.join(data[user_id]['notes'].keys())
            titles_list = '🔹 ' + titles_list
            ans = ['К сожалению, я не смогла найти данную заметку. Пожалуйста, повторите ещё раз. ',
                   'Данная заметка не найдена, повторите попытку ещё раз. ',
                   'Увы, такого названия в списке нет, попробуйте снова! ']
            response['response']['text'] = choice(ans) + 'Вот список доступных заметок:' + '\n' + titles_list
    return response
