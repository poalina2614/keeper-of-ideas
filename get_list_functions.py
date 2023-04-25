import requests
from random import choice
from help_funcs import *
def get_list_events(response, event, user_id, data):
    step = data[user_id]['step']
    if step == 0:
        if not (data[user_id]['events'].keys()):
            ans = ['Очень жаль, но сейчас ваш список событий пуст. 😿 ', 'Вы пока не добавили ни одного события. 😿 ',
                   'В вашем списке ещё нет событий. 😿']
            picture = ['213044/202d725e84df12d2da06', '1540737/ed20068e251d427d878f', '1656841/4788ab4350b72c9cfe31',
                       '997614/9d952f90b24459a8bfb4']
            k = choice(ans)
            response['response']['text'] = k
            response['response']['card'] = {}
            response['response']['card']['type'] = "BigImage"
            response['response']['card']['image_id'] = choice(picture)
            response['response']['card']['description'] = k

            data[user_id]['step'] = 0  # поэтому обнуляем поле "step"
            data[user_id]['func_key'] = ''
            requests.post('http://snordy.pythonanywhere.com/post',
                          json=data)
            choice_func(response)
            return response
        else:
            titles_list = '\n🔹 '.join(data[user_id]['events'].keys())
            titles_list = '🔹 ' + titles_list
            response['response']['text'] = 'Вот все ваши события:' + '\n' + titles_list + '\n'
            data[user_id]['step'] = 0  # поэтому обнуляем поле "step"
            data[user_id]['func_key'] = ''  # и "func_key", как признак того, что никакая функция не выполняется
            requests.post('http://snordy.pythonanywhere.com/post',
                          json=data)
            choice_func(response)
            return response

def show_al_no(response, event, user_id, data):
    if not (data[user_id]['notes'].keys()):
        ans = ['Очень жаль, но сейчас ваш список заметок пуст. 😿 ', 'У вас ещё нет ни одной заметки. 😿 ',
               'В вашем списке ещё нет заметок. 😿 ']
        k = choice(ans)
        picture = ['213044/202d725e84df12d2da06', '1540737/ed20068e251d427d878f', '1656841/4788ab4350b72c9cfe31',
                   '997614/9d952f90b24459a8bfb4']
        response['response']['text'] = k
        response['response']['card'] = {}
        response['response']['card']['type'] = "BigImage"
        response['response']['card']['image_id'] = choice(picture)
        response['response']['card']['description'] = k

        data[user_id]['step'] = 0  # поэтому обнуляем поле "step"
        data[user_id]['func_key'] = ''
        requests.post('http://snordy.pythonanywhere.com/post',
                      json=data)
        choice_func(response)
        return response
    else:
        titles_list = '\n🔹 '.join(data[user_id]['notes'].keys())
        titles_list = '🔹 ' + titles_list
        response['response']['text'] = f'Вот ваши заметки:\n {titles_list} ' + '\n'
        choice_func(response)
        return response