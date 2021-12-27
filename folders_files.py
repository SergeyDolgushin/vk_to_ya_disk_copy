import os

name = "token_ya_disk.txt"

def check_file_exist(name, path = os.getcwd()):
    '''ищем файл в каталогах, если нашли - возвращаем полный путь + имя'''
    for dir in reversed(path.split("\\")):
         path = os.path.normpath(path + os.sep + os.pardir)
         if name in os.listdir(path):           
            print(path)
            return path + '\\' + name
         else:   
            print("Такого файла не существует")
            return -1             

def read_token_from_file(path_name):
    '''читаем токены из файла'''
    tokens = {"YA": 0,"VK": 0}
    with open(path_name, 'rt', encoding = 'utf-8') as text:
        tokens["YA"] = text.readline().rstrip("\n")
        tokens["VK"] = text.readline().rstrip("\n")
    return tokens

def create_temp_folder(path = os.getcwd()):
    os.mkdir(path + "\\temp")
    
def remove_temp_folder(path = os.getcwd()):
    os.rmdir(path + "\\temp")

def remove_files_in_temp_folder(path = os.getcwd()):
    '''удаление всех файлов из временной директории temp'''
    path = os.getcwd() + "\\temp"
    for name in os.listdir(path): 
        os.remove(path + "\\" + name) 
    
def write_test_file(file_name = 'test.txt', path = os.getcwd() + "\\temp\\"):
    '''создание тестового файла во временной директории'''
    with open(path + file_name, 'w') as text:
        return text.write("test text")


# if __name__ == '__main__':
#     print(os.getcwd())
#     print(check_file_exist(name, path = os.getcwd()))
#     print(read_token_from_file(check_file_exist(name, path = os.getcwd()))["VK"])
#     create_temp_folder()
    # remove_temp_folder()
        
    # write_test_file()        
    