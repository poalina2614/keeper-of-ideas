import requests
from random import choice
from deep_translator import GoogleTranslator

def advice(response):
    adv = requests.get('https://api.adviceslip.com/advice')
    adv = adv.json()
    adv = adv['slip']['advice']
    adv = GoogleTranslator(source='english', target='russian').translate(adv)
    picture = ['213044/202d725e84df12d2da06', '1540737/ed20068e251d427d878f', '1656841/4788ab4350b72c9cfe31',
               '997614/9d952f90b24459a8bfb4']
    response['response']['text'] = adv
    response['response']['card'] = {}
    response['response']['card']['type'] = "BigImage"
    response['response']['card']['image_id'] = choice(picture)
    response['response']['card']['description'] = adv
    response['response']['card']['description'] = adv
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
