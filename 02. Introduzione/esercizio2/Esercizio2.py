import os
from os.path import join, getsize


def search_file_h():
    dir = "/home/zippo/PycharmProjects/sar/esercizio2"
    files = dict()
    for root, dirnames, filenames in os.walk(dir):
        for filename in filenames:
            if filename.endswith(".h"):
                if not filename in files:
                    files[filename] = 1
                else:
                    files[filename] += 1
    files = ["n: " + "".join("*" * files[file]).join("<>") for file in files]
    return files


if __name__ == '__main__':
    print(search_file_h())
