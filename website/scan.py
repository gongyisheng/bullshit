import json
import os

# The goal of this script is to scan contents from markdown files and 
# generate data.js, which will be used by the website

base_path = ["../fragments", "../opinion", "../poetry", "../short_story", "../unnamed_things"]
data = []

def list_file(path: str):
    #list all files in the path
    files = os.listdir(path)
    return files

def read_content(path: str):
    f = open(path, "r", encoding="utf_8")
    content = f.read()
    f.close()
    return content

def get_time_created(file_path: str):
    raw_result = os.popen(f"git log --follow --format=%ad --date raw {file_path} | tail -1").read()
    return int(raw_result.split(" ")[0])

def add_item(item: dict):
    """
    add a content item to data, including category, time_created, content
    """
    data.append(item)

def save_json(data: dict):
    """
    save data to data.js, which will be used by the website
    data will be overwritten
    """
    f = open("data.js", "w", encoding="utf_8")
    f.write("data="+json.dumps(data))
    f.close()

def process_category(base_path: str):
    """
    base function to process a category (one of fragments, opinion, poetry, short_story, unnamed_things)
    """
    category = base_path.split("/")[-1]
    items = list_file(base_path)
    if category in ["fragments", "opinion"]:
        process_with_year(base_path, category, items)
    else:
        process_without_year(base_path, category, items)

def process_with_year(base_path: str, category: str, items: list):
    """
    process category with nested year folders, such as fragments and opinion
    """
    for year in items:
        files = list_file(f"{base_path}/{year}")
        for file in files:
            file_path = f"{base_path}/{year}/{file}"
            if category == "fragments":
                process_fragments(file_path=file_path)
            if category == "opinion":
                process_opinion(file_path=file_path)

def process_without_year(base_path: str, category: str, items: list):
    """
    process category without nested year folders, such as poetry, short_story, unnamed_things
    """
    for file in items:
        file_path = f"{base_path}/{file}"
        content = read_content(file_path)
        dp = {
            "category": category,
            "time_created": get_time_created(file_path),
            "content": content
        }
        add_item(dp)

def process_fragments(file_path: str):
    """
    customized function to process fragments
    several fragments are stored in a single file, each line is a fragment
    split the file by line and add each content to data
    """
    for content in read_content(file_path).split("\n"):
        if len(content.strip()) > 0:
            dp = {
                "category": "fragments",
                "time_created": get_time_created(file_path),
                "content": content
            }
            add_item(dp)

def process_opinion(file_path: str):
    """
    customized function to process opinion
    opinion is stored in a single file, each file is a single opinion
    add the content to data
    """
    content = read_content(file_path).strip()
    dp = {
        "category": "opinion",
        "time_created": get_time_created(file_path),
        "content": content
    }
    add_item(dp)

def main():
    for category_base_path in base_path:
        process_category(category_base_path)
    save_json(data)


if __name__ == "__main__":
    main()