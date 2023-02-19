class UserVK:
    def __init__(self, user_id, token_vk, count='5', version='5.131'):
        self.token_vk = token_vk
        self.user_id = user_id
        self.version = version
        self.count = count
        self.params = {'Autorization': f'Bearer {self.token_vk}',
                       'access_token': self.token_vk,
                       'owner_id': self.user_id,
                       'v': self.version,
                       'count': self.count,
                       'album_id': 'profile',
                       'photo_sizes': '1',
                       'extended': '1',
                       'rev': '1'}

    def get_photos(self):
        """Метод запрашивает фотографии с профиля пользователя vk"""
        url = 'https://api.vk.com/method/photos.get'
        response = requests.get(url, params=self.params)
        return response.json()

class UploaderYaD:
    def __init__(self, token_yad):
        self.token_yad = token_yad

    def _get_headers_(self):
        """Метод возвращает заголовки для работы с яндекс диском"""
        return {'Content-Type': 'applicaation/json',
                'Authorization': f'OAuth {self.token_yad}'}

    def create_folder(self, folder_name):
        """Метод создает папку на яндекс диске"""
        url = HOST + '/v1/disk/resources'
        headers = self._get_headers_()
        params = {'path': f'/{folder_name}'}
        response = requests.put(url, headers=headers, params=params)
        if response.status_code == 201:
            print("Папка успешно создана")
        else:
            print(response.status_code)

    def upload_to_yad_by_url(self, file_url, file_name):
        """Метод загружает файл на яндекс диск по URL"""
        url = HOST + '/v1/disk/resources/upload'
        params = {'path': f'/{folder_name}/{file_name}', 'url': file_url}
        headers = self._get_headers_()
        response = requests.post(url, headers=headers, params=params)

if __name__ == '__main__':
    from settings import TOKEN
    import requests
    from tqdm import tqdm
    import json
    HOST = 'https://cloud-api.yandex.net:443'
    list_s = ['w', 'z', 'y', 'r', 'q', 'p', 'o', 'x', 'm', 's']
    user_id = input('Введите id пользователя vk ')
    token_yad = input('Введите токен яндекс диска ')
    folder_name = f'photo_id{user_id}'
    user = UserVK(user_id, TOKEN)
    uploader = UploaderYaD(token_yad)
    res = user.get_photos()
    photo_json = []
    photo_url = []
    for photo in res['response']['items']:
        for s in list_s:
            f = 0
            for size in photo['sizes']:
                if s == size['type']:
                    photo_json.append({'file_name': f"{photo['likes']['count']}_{photo['date']}.pjg", 'size': s})
                    photo_url.append(size['url'])
                    f = 1
                    break
            if f == 1:
                break
    with open(f'photo_json_id{user_id}.json', 'w') as f:
        json.dump(photo_json, f, ensure_ascii=False, indent=2)
    uploader.create_folder(folder_name)
    photo_zip = zip(photo_url, photo_json)
    for url in tqdm(list(photo_zip), desc="Uploading to yandex disk"):
        uploader.upload_to_yad_by_url(list(url)[0], list(url)[1]['file_name'])
