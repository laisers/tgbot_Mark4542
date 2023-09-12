# !/usr/lib/python3 python
# -*- coding: utf-8 -*-
import json
from vkbottle import BaseStateGroup, Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Bot, Message

TOKEN = 'vk1.a.QgaYRm9UWfqIvi-OGCbspu9gkPYjguqE1dBWaAZX8Z1_IuVJ1eGubImLF4QVUefxm9TwUs3arpYa0Qjo-5eT_GtNI3ynpIn1XEdNwTCMyO0zJ9Cd_M0rL4bMVMEa5wtVbLOaFMqXXIxsBsGPuOxRDCdXQ8i8teNzHMTFz8iOuap5NRfuXpD_xPCnDecGDV7A0Z-_rHn-VZ1QPHudZj663Q'
bot = Bot(token=TOKEN)

with open('text.json', encoding='utf-8') as f:
    txt = json.load(f)
TEXT = txt['Q']
TEXT_END = txt['finish']


class MenuState(BaseStateGroup):
    Q = 1


@bot.on.private_message(state=None)
async def start_handler(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    send_text = TEXT[0][0].replace('%name%', users_info[0].first_name)
    keyboard = Keyboard(inline=True)
    for but in TEXT[0][1]:
        keyboard.row()
        keyboard.add(Text(but), color=KeyboardButtonColor.PRIMARY)
    await message.answer(send_text, keyboard=keyboard.get_json())
    await bot.state_dispenser.set(message.peer_id, MenuState.Q, index=1)


@bot.on.private_message(state=MenuState.Q)
async def info_handler(message: Message):
    try:
        index = message.state_peer.payload["index"]
        if message.text not in TEXT[index - 1][1]:
            await message.answer('Воспользуйтесь кнопками на клавиатуре выше')
            await bot.state_dispenser.set(message.peer_id, MenuState.Q, index=index)
            return
        users_info = await bot.api.users.get(message.from_id)
        send_text = TEXT[index][0].replace('%name%', users_info[0].first_name)
        keyboard = Keyboard(inline=True)
        for but in TEXT[index][1]:
            keyboard.row()
            keyboard.add(Text(but), color=KeyboardButtonColor.PRIMARY)
        await message.answer(send_text, keyboard=keyboard.get_json())
        await bot.state_dispenser.set(message.peer_id, MenuState.Q, index=index + 1)
    except IndexError:
        await message.answer(TEXT_END)
        await bot.state_dispenser.delete(message.peer_id)
    except Exception as e:
        print(e)
        await bot.state_dispenser.delete(message.peer_id)


bot.run_forever()
