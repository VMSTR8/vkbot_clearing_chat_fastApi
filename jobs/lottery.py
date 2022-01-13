from random import sample
from time import sleep

from vkapi import get_conversation_members, users_get, send_message


async def lottery(lottery_id):
    """
    Присваивает каждому участнику чата номера от 1 до 1000
    :param lottery_id: Сюда передается peer_id
    :return: Отправляет по одному сообщению на каждого участника чата с присвоенным номером
    """
    # список нужен для работы с id'шниками
    list_of_ids = []

    user_ids = await get_conversation_members(lottery_id)  # смотрим, кто сидит в чате
    for vk_id in user_ids['items']:  # циклом складываем в список только id пользователей
        if vk_id['member_id'] > 0:
            list_of_ids.append(vk_id['member_id'])
    lottery_numbers = (sample(range(1, 1000), len(user_ids)))
    dictionary = dict(zip(list_of_ids, lottery_numbers))

    for number in dictionary.items():
        for data in await users_get(number[0]):
            await send_message(lottery_id, message=f"Пользователю @id{number[0]}({data['first_name']} "
                                                   f"{data['last_name']}) присвоен номер {number[1]}")
            sleep(0.3)
