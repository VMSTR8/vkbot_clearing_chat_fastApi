from vk.exceptions import VkAPIError

from settings import GROUP_ID
from vkapi import get_conversation_members, is_member, remove_chat_user, send_message


async def clean(clean_id):
    """
    Проверяет членство в закрытой группе и удаляет в том случае, если проверка не пройдена
    :param clean_id: Сюда передается peer_id
    :return: Выполняет проверку и отправляет сообщение со статистикой в чат
    """
    # список нужен для работы с id'шниками
    list_of_ids = []

    # две переменные, для того чтобы считать сколько было пользователей и сколько удалено
    to_stay = 0
    to_delete = 0

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
