import json
import os
# from pathlib import Path
import wget

class MyFiles:
    def __init__(self, path = os.getcwd()):
        self.path = path
    
    def check_file_exist(self, name):
        '''ищем файл в каталогах, если нашли - возвращаем полный путь + имя'''
        not_found = True
        current_path = self.path
        count = 0
        
        while not_found and count <=2:
            if name in os.listdir(self.path):           
                print(self.path)
                not_found = False
                path_of_file = self.path + '\\' + name
            os.chdir(self.path + os.sep + os.pardir)
            self.path = os.getcwd()
            count += 1
        os.chdir(current_path)
        self.path = os.getcwd()
        if not_found == False:
            print(self.path)
            return path_of_file
        else:
            print('Такого файла не существует')
            return -1

    def read_token_from_file(self, path_of_file):
        '''читаем токены из файла'''
        tokens = {"YA": 0,"VK": 0}
        with open(path_of_file, 'rt', encoding = 'utf-8') as text:
            tokens["YA"] = text.readline().rstrip("\n")
            tokens["VK"] = text.readline().rstrip("\n")
        return tokens
       
    def remove_temp_folder(self):
        if os.path.exists(self.path + "\\temp"):
            try:
                os.rmdir(self.path + "\\temp")
            except OSError:
                self.remove_files_in_temp_folder()
                os.rmdir(self.path + "\\temp")

    def create_temp_folder(self):
        if not(os.path.exists(self.path + "\\temp")):
            os.mkdir(self.path + "\\temp")


    def remove_files_in_temp_folder(self):
        '''удаление всех файлов из временной директории temp'''
        path = self.path + "\\temp"
        for name in os.listdir(path):
            print("Удаление:", path + os.sep + name) 
            os.remove(path + os.sep + name)
        
    
    def write_json_file(self, data, file_name = '/test.json'):
        '''запись информации о файле ВК'''
        with open(self.path + file_name, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def read_json_file(self, file_name = '/test.json'):
        '''для тестирования'''
        with open(self.path + file_name, encoding = "utf-8") as f:
            return json.load(f)

    def save_url_to_disk(self, res):
        '''разбор JSON-ответа VK и запись фото на диск в папку temp'''
        self.create_temp_folder()
        id_foto = {}
        temp = []
        file_info = dict.fromkeys(['file_name', 'size'])
        file_info_list = []
        for i in range(len(res)):
            file_info_list = []
            id_foto.fromkeys([res[i]['id']])  
            temp.append(res[i]['likes']['count'])
            file_name = str(res[i]['likes']['count'])
            if os.path.exists(self.path + '\\temp\\' + file_name + '.jpg'):
                file_name += f"_{res[i]['date']}" 
                if os.path.exists(self.path + '\\temp\\' + file_name + '.jpg'):
                    file_name += "_1"      
            file_info['file_name'] = file_name + '.jpg'                  
            temp.append(res[i]['date'])   
            temp.append((sorted(res[i]['sizes'], key = lambda x: x['height']))[-1])
            id_foto[res[i]['id']] = temp
            url = str(temp[-1]['url'])
            file_info['size'] = temp[-1]['type']
            file_info_list.append(file_info)
            self.write_json_file(file_info_list, file_name = '\\temp\\' + file_name + '.json')
            wget.download(url, self.path + '\\temp\\' + file_name + '.jpg') 
            temp = []


# if __name__ == '__main__':

#     myfiles = MyFiles()
#     print(myfiles.check_file_exist('token_ya_disk.txt'))
#     print(myfiles.read_token_from_file(myfiles.check_file_exist('token_ya_disk.txt')))
#     myfiles.remove_temp_folder()