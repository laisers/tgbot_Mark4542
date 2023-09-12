from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.menu_keyboard import *
from utils.db_api import db_commands
from loader import dp, bot
#from functions.image_func import *

@dp.message_handler(CommandStart())
async def register_user(message: types.Message):
    f_user = message.from_user

    if not await db_commands.select_user(user_id=f_user.id):
        invited_by = None
        if message.get_args().isdigit():
            invited_by = message.get_args()
            ref_user = await db_commands.select_user(user_id=invited_by)
            if await db_commands.select_user(user_id=invited_by):
                await db_commands.update_user(int(invited_by), ref_count=ref_user.get('ref_count') + 1,
                                              ref_link=ref_user.get('ref_link') + 1)
        await db_commands.add_user(f_user.id, f_user.username, f_user.first_name, invited_by)
    un = f_user.last_name
    if not un:
        un = ''
    text = await db_commands.select_text()
    caption = text.get('start_text').replace('%FN%', f_user.first_name).replace('%LN%', un)
    await message.answer_photo(open(text.get('start_photo'), 'rb'), caption=caption, reply_markup=await menu_buts())
