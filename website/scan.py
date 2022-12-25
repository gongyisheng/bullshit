import json
import os

path = ["../fragments", "../opinion", "../poetry", "../short_story", "../unnamed_things"]
data = []

def list_file(path):
    #list all files in the path
    files = os.listdir(path)
    return files

def read_content(path):
    f = open(path, "r", encoding="utf_8")
    content = f.read()
    f.close()
    return content

def add_item(item):
    data.append(item)

def save_json(data):
    f = open("data.js", "w", encoding="utf_8")
    f.write("data="+json.dumps(data))
    f.close()

def main():
    for p in path:
        category = p.split("/")[-1]
        items = list_file(p)
        if category in ["fragments", "opinion"]:
            for year in items:
                files = list_file(f"{p}/{year}")
                for file in files:
                    content = read_content(f"{p}/{year}/{file}")
                    dp = {
                        "category": category,
                        "time_created": os.path.getctime(f"{p}/{year}/{file}"),
                        "content": content
                    }
                    add_item(dp)
        else:
            for file in items:
                content = read_content(f"{p}/{file}")
                dp = {
                    "category": category,
                    "time_created": os.path.getctime(f"{p}/{file}"),
                    "content": content
                }
                add_item(dp)
    save_json(data)


if __name__ == "__main__":
    main()