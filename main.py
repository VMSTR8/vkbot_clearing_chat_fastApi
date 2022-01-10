from random import randint, sample
from time import sleep

from fastapi import FastAPI, Request

from starlette.responses import Response

from vk.exceptions import VkAPIError

from settings import CONFIRMATION_TOKEN, ADMIN_ID, GROUP_ID

from vkapi import is_member, remove_chat_user, get_conversation_members, send_message, users_get

app = FastAPI()


@app.post('/')
async def processing(vk: Request):
    data = await vk.json()

    if 'type' not in data.keys():
        return Response(content='not vk')
    if data['type'] == 'confirmation':
        return Response(content=CONFIRMATION_TOKEN)
    elif data['type'] == 'message_new':

        text = data['object']['message']['text']  # отлавливаем текст сообщения
        user_id = data['object']['message']['from_id']  # отлавливаем id пользователя
        peer_id = data['object']['message']['peer_id']  # отлавливаем id беседы

        list_of_ids = []  # список нужен для работы с id'шниками

        # две переменные, для того чтобы считать сколько было пользователей и сколько удалено
        to_stay = 0
        to_delete = 0

        # проверка на то, что текст прислал нужный пользователь и на то, что сообщение отправлено в чате
        if user_id != peer_id:
            if text.lower() in ['помощь', 'help', 'h']:
                help_id = peer_id
                await send_message(help_id, message='Есть следующие команды:\n'
                                                    'roll - бросает кубик от 1 до 1000\n\n'
                                                    'Админские команды:\n'
                                                    'clean - проверяет членство в закрытой группе, и удаляет тех, '
                                                    'кто в закрытой группе не состоит\n'
                                                    'del - удаляет всех пользователей чата, кроме админов\n'
                                                    'lottery - присваивает всем участникам номера от 1 до 1000')

            # бросание кубика от 1 до 1000, потом доделаю, чтобы пользователь сам выбирал максимальное число
            elif text.lower() == 'roll':
                roll_id = peer_id
                for data in await users_get(user_id):
                    await send_message(roll_id, message=f"Команду запустил @id{user_id}({data['first_name']} "
                                                        f"{data['last_name']}). Выпало {randint(1, 1000)}")

            elif user_id == int(ADMIN_ID):

                # инициализирует команду очистки чата
                if text.lower() == 'clean':
                    clean_id = peer_id

                    print('Команда принята.')

                    try:
                        user_ids = await get_conversation_members(clean_id)  # смотрим, кто сидит в чате
                        for vk_id in user_ids['items']:  # циклом складываем в список только id пользователей
                            if vk_id['member_id'] > 0:
                                list_of_ids.append(vk_id['member_id'])

                        for vk_id in list_of_ids:  # запуск цикла удаления тех, кого нет в закрытой группе
                            try:
                                # проверяем, есть ли человек в закрытой группе
                                if await is_member(int(GROUP_ID), vk_id) or vk_id == 6887358:
                                    print(f'{vk_id} прошел проверку')
                                    to_stay += 1
                                else:
                                    await remove_chat_user(clean_id, vk_id)  # удаляем пользователя
                                    to_delete += 1
                            except VkAPIError as err:
                                print(err)

                    except VkAPIError as err:
                        print(err)

                    # просто вывод статистики в чат, можно переделать на логирование
                    await send_message(clean_id,
                                       message=f'Задача выполнена. В чате было {len(list_of_ids)}.\n\nПрошли проверку '
                                               f'{to_stay} пользователей. Удалено: {to_delete} пользователей.\n\n'
                                               f'И их осталось {len(list_of_ids) - to_delete}')

                # команда инициализирует полную очистку чата
                elif text.lower() == 'del':

                    try:
                        del_id = peer_id
                        user_ids = await get_conversation_members(del_id)
                        for vk_id in user_ids['items']:
                            if vk_id['member_id'] > 0:
                                list_of_ids.append(vk_id['member_id'])

                        for vk_id in list_of_ids:
                            try:
                                await remove_chat_user(del_id, vk_id)
                            except VkAPIError as err:
                                print(err)

                    except VkAPIError as err:
                        print(err)

                # присваивание номеров для лотереи от 1 до 1000 всем участникам чата
                elif text.lower() == 'lottery':
                    lottery_id = peer_id
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

    return Response(content='ok')
