from fastapi import FastAPI, Request

from starlette.responses import Response


from settings import CONFIRMATION_TOKEN, ADMIN_ID

from jobs.cleaning import clean
from jobs.deleting import delete
from jobs.lottery import lottery
from jobs.help import commands_help
from jobs.roll import roll


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

        # проверка на то, что текст прислал нужный пользователь и на то, что сообщение отправлено в чате
        if user_id != peer_id:
            if text.lower() in ['помощь', 'help', 'h']:
                help_id = peer_id
                await commands_help(help_id)

            # бросание кубика от 1 до 1000, потом доделаю, чтобы пользователь сам выбирал максимальное число
            elif text.lower() == 'roll':
                roll_id = peer_id
                await roll(roll_id, user_id)

            elif user_id == int(ADMIN_ID):

                # инициализирует команду очистки чата
                if text.lower() == 'clean':
                    clean_id = peer_id
                    await clean(clean_id)

                # команда инициализирует полную очистку чата
                elif text.lower() == 'del':
                    del_id = peer_id
                    await delete(del_id)

                # присваивание номеров для лотереи от 1 до 1000 всем участникам чата
                elif text.lower() == 'lottery':
                    lottery_id = peer_id
                    await lottery(lottery_id)

    return Response(content='ok')
