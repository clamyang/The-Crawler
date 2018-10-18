import requests
import os
from multiprocessing.pool import Pool
from hashlib import md5
from urllib.parse import urlencode


headers = {
        'Referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'

        }

def get_page(offset):
    base_url = 'https://www.toutiao.com/search_content/?'
    params = {
            'offset': offset,
            'format': 'json',
            'keyword': '街拍',
            'autoload': 'true',
            'count': 20,
            'cur_tab': 1,
            'from': 'search_tab'
            }

    url = base_url + urlencode(params)
    response = requests.get(url, headers=headers)
    try:
        if response.status_code == 200:
            return response.json()

    except requests.ConnectionError:
        return None

def get_images(json):
    if json.get('data'):
        data = json.get('data')
        for item in data:
            if item.get('cell_type') is not None:
                continue
            title = item.get('title')
            image_url = item.get('image_list')
            for image in image_url:
               yield {            
                        'image': 'https:' +  image.get('url'),
                        'title': title
                        }

def save_image(item):
    #图片存储路径
    image_path = 'image' + os.path.sep + item.get('title')
    if not os.path.exists(image_path):
        os.makedirs(image_path)  # 创建目录

    try:
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            file_path = image_path + os.path.sep + '{file_name}.{file_suffix}'.format(file_name=md5(response.content).hexdigest(), file_suffix='jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print('Downloaded image path is %s' % file_path)
            else:
                print('Already Downloaded', file_path)

    except requests.ConnectionError:
        print('Failed to Save Image, item %s' % item)



def main(offset):
    json = get_page(offset)
    items = get_images(json)
    for  item in items:
        print(item)
        save_image(item)

GROUP_START = 0
GROUP_END = 7

if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])

    # map() 函数 映射关系,一个 groups 中的元素对应一个 main() 函数
    pool.map(main, groups)
    pool.close()
    pool.join()












