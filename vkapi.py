import random

import vk

from settings import OPEN_GROUP_TOKEN, CLOSED_GROUP_TOKEN, SERVICE_TOKEN

session = vk.Session()
api = vk.API(session, v='5.131')


async def send_message(peer_id: int, message: str, attachment=''):
    """
    Отправляет сообщение
    :param peer_id: Передаете сюда peer_id
    :param message: Передаете сообщение, которое нужно отправить (Не больше 4096 символов)
    :param attachment: Передаете ссылку на файл, который нужно отправить в формате <type><owner_id>_<media_id>
    :return: Отправляет сообщение
    """
    api.messages.send(access_token=OPEN_GROUP_TOKEN,
                      peer_id=peer_id,
                      message=message,
                      attachment=attachment,
                      random_id=random.getrandbits(64),
                      dont_parse_links=1)


async def remove_chat_user(chat_id: int, user_id: int):
    """
    Удаляет пользователя из чата
    :param chat_id: Передаете сюда peer_id
    :param user_id: Передаете сюда user_id
    :return: Удаляет пользователя из чата
    """
    api.messages.removeChatUser(access_token=OPEN_GROUP_TOKEN,
                                chat_id=chat_id - 2000000000,
                                user_id=user_id)


async def is_member(group_id: int, user_id: int) -> bool:
    """
    Проверяет, является ли пользователь членом указанной группы
    :param group_id: Передаете сюда group_id
    :param user_id: Передаете сюда user_id
    :return: Возвращает True или False
    """
    return api.groups.isMember(access_token=CLOSED_GROUP_TOKEN,
                               group_id=group_id,
                               user_id=user_id)


async def get_conversation_members(peer_id: int) -> dict:
    """
    Позволяет получить список участников беседы
    :param peer_id: Передаете сюда peer_id
    :return: Возвращает словарь, который содержит информацию о всех пользователях беседы
    """
    return api.messages.getConversationMembers(access_token=OPEN_GROUP_TOKEN,
                                               peer_id=peer_id)


async def users_get(user_ids):
    return api.users.get(access_token=SERVICE_TOKEN,
                         user_ids=user_ids,
                         name_case='nom')
