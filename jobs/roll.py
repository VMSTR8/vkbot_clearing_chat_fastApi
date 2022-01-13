from random import randint

from vkapi import users_get, send_message


async def roll(roll_id, user_id):
    """
    Кидает кубик от 1 до 1000
    :param roll_id: Сюда передается peer_id
    :param user_id: Сюда передается user_id
    :return: Отправляет сообщение в чат с информацией кто запустил команду и сколько выпало на кубике
    """
    for data in await users_get(user_id):
        await send_message(roll_id, message=f"Команду запустил @id{user_id}({data['first_name']} "
                                            f"{data['last_name']}). Выпало {randint(1, 1000)}")
