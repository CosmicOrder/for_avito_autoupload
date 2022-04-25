import openpyxl
import pandas as pd

from img_parser_svn import ImgParserSVN
from imgbb import make_valid_url
from progress.bar import IncrementalBar

filename = r'C:\Users\Igor\Desktop\Славик\Prays_SVN_ot_11_04_22_1.xlsx'
book = openpyxl.open(filename)

sheet = book['SVN']

article = []
title = []
category = ['Аудио и видео']
goodstype = ['Видеокамеры']
address = ['Россия, Калужская область, Калуга, Грабцевское шоссе, 33']
description_1 = []
description_2 = []
description_3 = []
description_4 = []
contact_method = ['По телефону и в сообщениях']
manager_name = ['Святослав']
contact_phone = ['+7 (910) 603-21-35']
price = []
condition = ['новое']
images = []

for row in range(2, sheet.max_row + 1):
    if sheet[row][2].value and sheet[row][0].value != 'Артикул' and \
            'без лого' not in sheet[row][0].value and \
            sheet[row][9].value != 'нет':
        article.append(sheet[row][0].value)
        title.append('Видеокамера ' + sheet[row][0].value)
        description_1.append(sheet[row][2].value)
        description_2.append(sheet[row][3].value)
        description_3.append(sheet[row][4].value)
        description_4.append(sheet[row][5].value)
        price.append(sheet[row][6].value)

img_parser_svn = ImgParserSVN()
bar = IncrementalBar('Countdown', max=len(article))

for i in article:
    img_url = img_parser_svn.get_img_url(i)
    if img_url:
        images.append(make_valid_url(img_url))
        # img_parser_svn.save_img(i)
        bar.next()
    else:
        images.append('https://i.ibb.co/CWJqvx0/image.jpg')
        bar.next()
    bar.finish()

description_1 = [str(i) if i is not None else '' for i in description_1]
description_2 = [', ' + str(i) if i is not None else '' for i in description_2]
description_3 = [', ' + str(i) if i is not None else '' for i in description_3]
description_4 = [', ' + str(i) if i is not None else '' for i in description_4]

description = []
for i in range(len(description_1)):
    description.append(description_1[i] + description_2[i] +
                       description_3[i] + description_4[i])

category = category * len(article)
goodstype = goodstype * len(article)
address = address * len(article)
contact_method = contact_method * len(article)
manager_name = manager_name * len(article)
contact_phone = contact_phone * len(article)
condition = condition * len(article)

avito_table = {'Id': article, 'Title': title, 'Description': description,
               'Category': category, 'GoodsType': goodstype,
               'Address': address, 'ContactMethod': contact_method,
               'ManagerName': manager_name, 'ContactPhone': contact_phone,
               'Price': price, 'Condition': condition, 'Images': images}

df = pd.DataFrame(avito_table)

target_path = r'C:\Users\Igor\Desktop\Славик\for_avito.xlsx'
df.to_excel(target_path, index=False)
