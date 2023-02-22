import requests
import os
import shutil
import os.path
from pprint import pprint
import yadisk
id_user = int(input('Please, enter id user: '))
url = ' https://api.vk.com/method/photos.get'
with open('token vk.ini') as f:
    token_vk = f.read().strip()
headers = {
    'Authorization': token_vk
    # 'Content-Type': 'multipart/form-data'
}
params = {
    'v': '5.131',
    'album_id': 'wall',
    'owner_id': id_user,
    'rev': '0',
    'extended':'1',
    'photo_sizes': '0',  
    'photo_ids': '457239736, 457239735, 457239734, 457239733, 457239704'
}
res = requests.get(url=url, headers=headers,params=params)
photo_final = {}
n = 0
os.mkdir('temp/')
for i in res.json()['response']['items']:
    for photo in i['sizes']:
        if photo['type'] == 'w':
            n += 1
            photo_final[f'photo{n}'] = {'likes': i['likes']['count'], 'date': i['date'], 'url': photo['url']}
            with open ('token ya.ini') as file:
                token_ya = file.read().strip()
                y = yadisk.YaDisk(token=token_ya)
                link = photo_final[f'photo{n}']['url']
                file_name = photo_final[f'photo{n}']['likes']
                file_name1 = f"{photo_final[f'photo{n}']['likes']} + {photo_final[f'photo{n}']['date']}"
                if os.path.exists(f'temp/{file_name}.jpg'):
                    with open(f'temp/{file_name1}.jpg', 'wb+') as fi:
                        response = requests.get(link)
                        fi.write(response.content)  
                        y.upload(f'temp/{file_name1}.jpg', f'vk/{file_name1}.jpg', overwrite=True)
                else:           
                    with open(f'temp/{file_name}.jpg', 'wb+') as fi:
                        response = requests.get(link)
                        fi.write(response.content)  
                        y.upload(f'temp/{file_name}.jpg', f'vk/{file_name}.jpg', overwrite=True)

shutil.rmtree('temp/')
print('Copying to yandex disk completed successfully')
            