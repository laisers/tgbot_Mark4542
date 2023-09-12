from loader import dp, vkapi, google
from aiogram import types
from keyboards.inline.search_result_keyboard import download_keyboard
from functions import forming_text
from filters.filters_chat import Is_Search, Is_Vk_Link
from functions.image_func import *

import asyncio
import logging



@dp.message_handler(Is_Search())
async def search(message: types.Message):
    text = await db_commands.select_text()
    await message.answer(text.get('search_text'))


@dp.message_handler(Is_Vk_Link())
async def search_vk(message: types.Message):
    #TODO Вернуть try
    #try:
        user_id = message.text.split('vk.com')[1].replace('/', '')
        user_data = await vkapi.get_user_data(user_id)
        result_text, pk = await forming_text.forming_result_text(user_data)

        if not result_text:
            text = await db_commands.select_simulation(False)
            loading = await message.answer(text[0].get('name'))
            await asyncio.sleep(text[0].get('timing'))
            for txt in text[1:]:
                await loading.edit_text(txt.get('name'))
                await asyncio.sleep(txt.get('timing'))
                await db_commands.update_user(message.from_user.id, last_search_link=user_data)
            return
        simulation_text = await db_commands.select_simulation(True)
        loading = await message.answer(simulation_text[0].get('name'))
        await asyncio.sleep(simulation_text[0].get('timing'))
        for txt in simulation_text[1:]:
            await loading.edit_text(txt.get('name'))
            await asyncio.sleep(txt.get('timing'))
        text = await db_commands.select_text()
        dtain_data = await db_commands.select_drain_data_values(id=pk)
        poli = types.MediaGroup()
        poli.attach_photo(photo=user_data['photo'], caption=result_text)
        poli.attach_photo(photo=open(dtain_data.get('template'), 'rb'))

        await loading.delete()
        await message.answer_media_group(poli)
        await message.answer(text['set_download_text'], reply_markup=download_keyboard(pk))
    # except Exception as e:
    #     logging.error(e)
    #     await message.answer('❌ <b>Произошла ошибка, проверьте ссылку на страницу...</b>')
