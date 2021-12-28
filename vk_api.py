import time
import requests
import pandas as pd

my_id = 1584850

class VkUser:
    url = 'https://api.vk.com/method/'
    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version    
        }
        
    def search_groups(self, q, sorting=0):
        '''
        Параметры sort
        0 — сортировать по умолчанию (аналогично результатам поиска в полной версии сайта);
        1 — сортировать по скорости роста;
        2 — сортировать по отношению дневной посещаемости к количеству пользователей;
        3 — сортировать по отношению количества лайков к количеству пользователей;
        4 — сортировать по отношению количества комментариев к количеству пользователей;
        5 — сортировать по отношению количества записей в обсуждениях к количеству пользователей.        
        '''
        group_search_url = self.url + 'groups.search'
        group_search_params = {
            'q': q,
            'sort': sorting,
            'count': 300
        }
        req = requests.get(group_search_url, params={**self.params, **group_search_params}).json()
        return req['response']['items']
    
    
    def search_groups_ext(self, q, sorting=0):
        group_search_ext_url = self.url + 'groups.getById'
        target_groups = self.search_groups(q, sorting)
        target_group_ids = ','.join([str(group['id']) for group in target_groups])
        groups_info_params = {
            'group_ids': target_group_ids,
            'fields':  'members_count,activity,description'
        }
        req = requests.get(group_search_ext_url, params={**self.params, **groups_info_params}).json()
        return req['respone']
    
    
    def get_followers(self, user_id=None):
        followers_url = self.url + 'users.getFollowers'
        followers_params = {
            'count': 1000,
            'user_id': user_id
        }
        res = requests.get(followers_url, params={**self.params, **followers_params}).json()
        return res['response']['items']
    
    def get_groups(self, user_id=None):
        groups_url = self.url + 'groups.get'
        groups_params = {
            'count': 1000,
            'user_id': user_id,
            'extended': 1,
            'fields': 'members_count'
        }
        res = requests.get(groups_url, params={**self.params, **groups_params})
        return res.json()    
    
    def get_news(self, query):
        groups_url = self.url + 'newsfeed.search'
        groups_params = {
            'q': query,
            'count': 200
        }
        
        newsfeed_df = pd.DataFrame()

        while True:
            result = requests.get(groups_url, params={**self.params, **groups_params})
            time.sleep(0.33)
            newsfeed_df = pd.concat([newsfeed_df, pd.DataFrame(result.json()['response']['items'])])
            if 'next_from' in result.json()['response'].keys():
                groups_params['start_from'] = result.json()['response']['next_from']
            else:
                break
        return newsfeed_df

    def get_photos(self, album_id='profile', user_id = my_id, extended =1):
        photos_url = self.url + 'photos.get'
        photos_params = {
            'album_id': album_id,
            'count': 100,
            'user_id': user_id,
            'extended': extended
        }
        res = requests.get(photos_url, params={**self.params, **photos_params}).json()
        return res