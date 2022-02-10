import os
import sys
from colorama import Fore
from collections import deque
import requests
from bs4 import BeautifulSoup


def read_file(filename):
    with open(filename, 'r', encoding="utf-8") as file:
        print(file.read())


def main():
    args = sys.argv
    webs = deque()

    if not os.access(args[1], os.F_OK):
        os.mkdir(args[1])

    while True:
        url = input()
        if '.' in url:
            new_url = url if url.startswith("https://") else "https://" + url
            try:
                r = requests.get(new_url)
            except requests.exceptions.ConnectionError:
                print("Incorrect URL")
            else:
                if os.listdir(args[1]) and webs:
                    if webs[-1] != os.listdir(args[1])[-1]:
                        webs.append(os.listdir(args[1])[-1])
                elif os.listdir(args[1]):
                    webs.append(os.listdir(args[1])[-1])
                soup = BeautifulSoup(r.content, "html.parser")
                tags = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li'])
                list_tags = [i.text + '\n' for i in tags if i.text]
                for tag in tags:
                    if tag.get('href'):
                        print(Fore.BLUE + tag.text)
                    else:
                        print(tag.text)
                name = url.split('.')[0]
                file = open(f"{args[1]}/{name}", mode='w', encoding="utf-8")
                file.writelines(list_tags)
                file.close()
        elif url == "back":
            if webs:
                read_file(f"{args[1]}/{webs.pop()}")
        elif url == "exit":
            break
        else:
            print("Incorrect URL")


if __name__ == "__main__":
    main()
