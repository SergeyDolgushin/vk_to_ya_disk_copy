from ya_disk import YandexDisk
import files
import os
from vk_api import VkUser
import progressbar
import time



if __name__ == '__main__':
    temp_path = os.getcwd() + "\\temp\\"
    name = "token_ya_disk.txt"
    myfiles = files.MyFiles()
    status_ya = []
   
    myfiles.remove_temp_folder()
    

    token = myfiles.read_token_from_file(myfiles.check_file_exist(name))
    ya = YandexDisk(token=token["YA"])
    vk_client = VkUser(token["VK"], '5.131')

    res = vk_client.get_albums(count = "40")                                                        
    for alb_id in res["response"]["items"]:
        if alb_id['id'] != -9000:
            res = (vk_client.get_photos(album_id = alb_id['id'], count = "1"))['response']['items']
            myfiles.save_url_to_disk(res)
            time.sleep(0.25)
   
    responce = ya.create_new_folder("test")
    bar = progressbar.ProgressBar(max_value = progressbar.UnknownLength)
    for name in os.listdir(temp_path):
        if '.jpg' in name:
            count = 0
            status_ya.append(ya.upload_file_to_disk("test/" + f"{name}", temp_path + name))
            time.sleep(0.05)
            count += 1
            bar.update(count)
    print()     
    print(status_ya)
    

    