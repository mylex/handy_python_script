import os


def getfiles(path, text):
    os.chdir(path)
    files = os.listdir()
    for file_name in files:
        abs_path = os.path.abspath(file_name)
        if os.path.isdir(abs_path):
            if getfiles(abs_path, text):
                return True
        if os.path.isfile(abs_path):
            with open(file_name, "r") as f:
                if text in f.read():
                    print(f"{text} found in:")
                    final_path = os.path.abspath(file_name)
                    print(final_path)
                    return True

    print(f"{text} not found!")
    return False


text = input("input text: ")
path = input("path: ")

getfiles(path, text)
