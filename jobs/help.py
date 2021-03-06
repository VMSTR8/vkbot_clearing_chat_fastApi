from vkapi import send_message


async def commands_help(help_id):
    """
    Выводит список команд в чат
    :param help_id: Сюда передается peer_id
    :return: Отправляет сообщение со списоком команд в чат
    """
    await send_message(help_id, message='Есть следующие команды:\n'
                                        'roll - бросает кубик от 1 до 1000\n\n'
                                        'Админские команды:\n'
                                        'clean - проверяет членство в закрытой группе, и удаляет тех, '
                                        'кто в закрытой группе не состоит\n'
                                        'del - удаляет всех пользователей чата, кроме админов\n'
                                        'lottery - присваивает всем участникам номера от 1 до 1000')
