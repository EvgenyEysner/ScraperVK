import os
import requests
import json
import datetime

# VK API
# https://dev.vk.com/api/access-token/implicit-flow-user
# https://oauth.vk.com/authorize?client_id=8057688&display=page&redirect_uri=https://oauth.vk.com&scope=friends,wall,groups,photos,offline&response_type=token&v=5.131

token = '721141f563dcc3f2106634cb5066dc82291811979a83334eaa0b4efb86778862e47975092bf51ddc3d25d'

# today date 00:00 Uhr
today_date = datetime.date.today().strftime('%Y-%m-%d %H:%M:%S')

# List all groups that are monitored
group_list = ['arendakvartir_ru', 'svoy.uyutnyi.ugolok', 'rentm']


# Get json from API
def get_json(url):
    req = requests.get(url)
    src = req.json()
    return src


# get all posts off the wall
def get_posts_wall(group_list):
    for group_name in group_list:
        url = f'https://api.vk.com/method/wall.get?domain={group_name}&count=10&access_token={token}&v=5.131'
        src = get_json(url)

        if os.path.exists(f'{group_name}'):
            print(f'Директория {group_name} уже существует')
        else:
            os.mkdir(group_name)

        # save json file
        with open(f'{group_name}/{group_name}.json', 'w', encoding='UTF-8') as file:
            json.dump(src, file, indent=4, ensure_ascii=False)

        new_posts_id = [] # collect id's of new posts
        posts = src['response']['items']
        for new_post_id in posts:
            new_post_id = new_post_id['id']
            new_posts_id.append(new_post_id)

            if not os.path.exists(f'{group_name}/exist_posts_{group_name}.txt'):
                print('File not found create file...')
                with open(f'{group_name}/exist_posts_{group_name}.txt', 'w') as file:
                    for item in new_posts_id:
                        file.write(str(item) + '\n')

                for post in posts:
                    post_published = []
                    created = datetime.datetime.fromtimestamp(int(post['date']))
                    owner_id = post['owner_id']
                    id = post['id']
                    text = post['text']
                    url = f'https://vk.com/arendakvartir_ru?w=wall{owner_id}_{id}'
                    post_published.append(id)

                    if 'собственник' in text.lower() and today_date < str(created):
                        new_post = {
                            'created': str(created),
                            'body': text,
                            'url': url
                        }
                        print(new_post)

            # else:
            #     with open(f'{group_name}/exist_posts_{group_name}.txt', 'r') as file:
            #         for item in file:
            #             if item in new_posts_id:
            #                 print('такой пост был')
                        # else:
                        #     for post in posts:
                        #
                        #         created = datetime.datetime.fromtimestamp(int(post['date']))
                        #         owner_id = post['owner_id']
                        #         id = post['id']
                        #         text = post['text']
                        #         url = f'https://vk.com/arendakvartir_ru?w=wall{owner_id}_{id}'
                        #
                        #         if 'собственник' in text.lower() and today_date < str(created):
                        #             print(text)
                        #             print(url)



def main():
    get_posts_wall(group_list)


if __name__ == '__main__':
    main()