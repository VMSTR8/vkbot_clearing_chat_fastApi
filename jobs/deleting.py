from vk.exceptions import VkAPIError

from vkapi import get_conversation_members, remove_chat_user


async def delete(del_id):
    """
    Удаляет всех членов беседы, кроме администраторов и самого бота
    :param del_id: Сюда передается peer_id
    :return: Выполняет удаление
    """
    # список нужен для работы с id'шниками
    list_of_ids = []

    try:
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
