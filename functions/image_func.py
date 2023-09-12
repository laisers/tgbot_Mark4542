import asyncio
from PIL import ImageDraw, Image, ImageFont, ImageFilter
import os
import random, requests
from utils.db_api import db_commands
from loader import vkapi, google




def rounding(img, size):
    bigsize = img.size[0] * 3, img.size[1] * 3
    img = img.resize(size, resample=Image.Resampling.LANCZOS)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(img.size, resample=Image.Resampling.LANCZOS)
    img.putalpha(mask)
    return img


async def create_main_template(user: dict):
    path_pack = 'Files/Photos/Packs'
    random_pack = os.path.join(path_pack, random.choice(os.listdir(path_pack)))
    random_photos = [os.path.join(random_pack, x) for x in os.listdir(random_pack)]
    setting = await db_commands.select_setting_template()
    list_cords = [[setting.get(f'coord{x}'), setting.get(f'size{x}'), setting.get(f'crop{x}')] for x in
                  random.sample(range(1, 9), 8)]
    main_templates = Image.open(setting.get('main_template'))
    template_list = []
    templates = list(await db_commands.select_template())
    for template in random.sample(templates, random.randint(setting.get('template_from'), setting.get('template_to'))):
        result = await create_template(user, dict(template), random_photos.pop(random.randrange(len(random_photos))))
        template_list.append(result)
    for en, coord in enumerate(list_cords):
        if en >= len(template_list):
            photo = Image.open(random_photos.pop(random.randrange(len(random_photos))))
        else:
            photo = template_list[en]
        if coord[2]:
            new_image = photo.resize((int(coord[1].split(' ')[0]), int(coord[1].split(' ')[0])))
            new_image = new_image.crop((0, 0, int(coord[1].split(' ')[0]), int(coord[1].split(' ')[1])))
        else:
            new_image = photo.resize(tuple([int(x) for x in coord[1].split(' ')]))
        main_templates.paste(new_image, tuple([int(x) for x in coord[0].split(' ')]))
    # Вставка Авы
    user_img = Image.open(requests.get(user['photo'], stream=True).raw)
    circle = rounding(user_img, tuple([int(x) for x in setting.get('size_ava').split(' ')]))
    main_templates.paste(circle, tuple([int(x) for x in setting.get('coord_ava').split(' ')]), circle)
    circle.close()
    # Вставка ФИО
    font = ImageFont.truetype(font='Files/Fonts/FIO.ttf', size=int(setting.get('size_name')), encoding='utf-8')
    draw_text = ImageDraw.Draw(main_templates)
    xy = tuple([int(x) for x in setting.get('coord_name').split(' ')])
    draw_text.text(xy, f"{user['first_name']} {user['last_name']}", fill=(setting.get('color_name')), font=font)

    # BLUR
    mask = Image.new('L', main_templates.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle([(44, 210), (532, 1218)], fill=255)
    blurred = main_templates.filter(ImageFilter.GaussianBlur(setting.get('blur')))
    main_templates.paste(blurred, mask=mask)

    if setting.get('is_watermark'):
        # Вставка watermark
        watermark = Image.open('django_project/telegrambot/Files/' + setting.get('watermark'))

        main_templates.paste(watermark, tuple([int(x) for x in setting.get('coord_watermark').split(' ')]), watermark)
        watermark.close()
    photo_path = f'Files/Photos/Drain/Template/template_{user["id"]}.png'
    main_templates.save(photo_path)
    await asyncio.sleep(2)
    await google.upload_file(r"Files\Photos\Drain\Template\template_151352583.jpg")
    return main_templates


async def create_template(user: dict, template: dict, random_photo):
    views = await db_commands.select_templates(template_name_id=template['id'])
    user_img = Image.open(requests.get(user['photo'], stream=True).raw)
    template = Image.open(template['template'])
    friend1 = await vkapi.get_info_friend(user['id'], 1)
    friend2 = await vkapi.get_info_friend(user['id'], 2)

    for view in views:
        xy = (view.get('coord_x1'), view.get('coord_y1'))
        size = tuple([int(x) for x in view.get('size').split(' ')])
        if view.get('method') == '1':
            # Вставить круглую аву
            circle = rounding(user_img, size)
            template.paste(circle, xy, circle)
            circle.close()
        if view.get('method') == '2':
            # Вставить аву
            new_image = user_img.resize(size)
            template.paste(new_image, xy)
        if view.get('method') in ['3', '5']:
            # Ава друга/подруги
            if view.get('method') == '3':
                photo_max = friend1['photo_max']
            else:
                photo_max = friend2['photo_max']
            try:
                circle = rounding(Image.open(requests.get(photo_max, stream=True).raw), size)
            except (requests.exceptions.InvalidURL, requests.exceptions.MissingSchema):
                circle = rounding(Image.open(photo_max), size)
            template.paste(circle, xy, circle)
            circle.close()
        if view.get('method') in ['4', '6']:
            # Фото друга/подруги
            if view.get('method') == '4':
                photo_max = friend1['photo_max']
            else:
                photo_max = friend2['photo_max']
            try:
                photo = Image.open(requests.get(photo_max, stream=True).raw)
            except (requests.exceptions.InvalidURL, requests.exceptions.MissingSchema):
                photo = rounding(Image.open(photo_max), size)
            new_image = photo.resize(size)
            template.paste(new_image, xy)
            photo.close()
        if view.get('method') == '7':
            # Выбор рандом фото
            random_dir_photo = Image.open(random_photo)
            new_image = random_dir_photo.resize(size)
            template.paste(new_image, xy)
            random_dir_photo.close()
        if view.get('method') == '8':
            # ФИО
            font = ImageFont.truetype(font='Files/Fonts/FIO.ttf', size=int(view.get('size')), encoding='utf-8')
            draw_text = ImageDraw.Draw(template)
            draw_text.text(xy, f"{user['first_name']} {user['last_name']}", fill=(view.get('color')), font=font)
        if view.get('method') in ['9', '10']:
            # ФИО друга
            if view.get('method') == '9':
                inf = friend1
            else:
                inf = friend2
            font = ImageFont.truetype(font='Files/Fonts/FIO-friend.ttf', size=int(view.get('size')), encoding='utf-8')
            draw_text = ImageDraw.Draw(template)
            draw_text.text(xy, f"{inf['first_name']} {inf['last_name']}", fill=(view.get('color')), font=font)
    return template
