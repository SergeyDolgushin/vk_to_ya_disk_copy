from pprint import pprint
import requests
from ya_disk import YandexDisk
from folders_files import check_file_exist, read_token_from_file, create_temp_folder, remove_temp_folder, write_json_file
import os
from vk_api import VkUser
import pandas as pd

name = "token_ya_disk.txt"






if __name__ == '__main__':
   
    token = read_token_from_file(check_file_exist("token_ya_disk.txt"))
    print(token)
    vk_client = VkUser(token["VK"], '5.131')
    res = vk_client.get_photos()
    write_json_file(res)


    # ya = YandexDisk(token=read_token_from_file(check_file_exist("token_ya_disk.txt"))["YA"])
    # responce = ya.create_new_folder("test")
    # print(responce)
    # ya.upload_file_to_disk("test/test.txt", check_file_exist("test.txt"))
    

    