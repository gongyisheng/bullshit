import json
import os

base_path = ["../fragments", "../opinion", "../poetry", "../short_story", "../unnamed_things"]
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

def process_category(base_path):
    category = base_path.split("/")[-1]
    items = list_file(base_path)
    if category in ["fragments", "opinion"]:
        process_with_year(base_path, category, items)
    else:
        process_without_year(base_path, category, items)

def process_with_year(base_path, category, items):
    for year in items:
        files = list_file(f"{base_path}/{year}")
        for file in files:
            if category == "fragments":
                process_fragments(file_path=f"{base_path}/{year}/{file}")
            if category == "opinion":
                process_opinion(file_path=f"{base_path}/{year}/{file}")

def process_without_year(base_path, category, items):
    for file in items:
        content = read_content(f"{base_path}/{file}")
        dp = {
            "category": category,
            "time_created": os.path.getctime(f"{base_path}/{file}"),
            "content": content
        }
        add_item(dp)

def process_fragments(file_path):
    for content in read_content(file_path).split("\n"):
        if len(content.strip()) > 0:
            dp = {
                "category": "fragments",
                "time_created": os.path.getctime(file_path),
                "content": content
            }
            add_item(dp)

def process_opinion(file_path):
    content = read_content(file_path).strip()
    dp = {
        "category": "opinion",
        "time_created": os.path.getctime(file_path),
        "content": content
    }
    add_item(dp)


def main():
    for category_base_path in base_path:
        process_category(category_base_path)
    save_json(data)


if __name__ == "__main__":
    main()