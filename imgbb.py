import requests


def make_valid_url(img_url):
    api_url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": '596efa2da9a9fb9867a04e27184b0dd2',
        "image": f'{img_url}',
    }
    res = requests.post(api_url, payload)
    return res.json()['data']['url']
