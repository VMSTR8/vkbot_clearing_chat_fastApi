from fastapi import FastAPI, Request

from starlette.responses import Response

from vk.exceptions import VkAPIError

from settings import CONFIRMATION_TOKEN, ADMIN_ID, GROUP_ID

from vkapi import is_member, remove_chat_user, get_conversation_members, send_message

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
        if user_id != peer_id and user_id == int(ADMIN_ID):
            if text.lower() == 'чистка':  # инициализирует команду очистки чата

                print('Команда принята.')

                try:
                    user_ids = await get_conversation_members(peer_id)  # смотрим, кто сидит в чате
                    for vk_id in user_ids['items']:  # циклом складываем в список только id пользователей
                        if vk_id['member_id'] > 0:
                            list_of_ids.append(vk_id['member_id'])

                    before_delete = len(list_of_ids)  # считаем, сколько людей в чате до удаления

                    for vk_id in list_of_ids:  # запуск цикла удаления тех, кого нет в закрытой группе
                        try:
                            if await is_member(int(GROUP_ID), vk_id):  # проверяем, есть ли человек в закрытой группе
                                print(f'{vk_id} прошел проверку')
                                to_stay += 1
                            else:
                                await remove_chat_user(peer_id - 2000000000, vk_id)  # удаляем пользователя
                                to_delete += 1
                        except VkAPIError as err:
                            print(err)

                    # просто вывод статистики в чат, можно переделать на логирование
                    await send_message(peer_id,
                                       message=f'Задача выполнена. В чате было {before_delete}.\n\nПрошли проверку '
                                               f'{to_stay} пользователей. Удалено: {to_delete} пользователей.\n\n'
                                               f'И их осталось {before_delete - to_delete}')

                except VkAPIError as err:
                    print(err)

            elif text.lower() == 'del':  # команда инициализирует полную очистку чата

                try:
                    user_ids = await get_conversation_members(peer_id)
                    for vk_id in user_ids['items']:
                        if vk_id['member_id'] > 0:
                            list_of_ids.append(vk_id['member_id'])

                    for vk_id in list_of_ids:
                        try:
                            await remove_chat_user(peer_id, vk_id)
                        except VkAPIError as err:
                            print(err)

                except VkAPIError as err:
                    print(err)

    return Response(content='ok')
