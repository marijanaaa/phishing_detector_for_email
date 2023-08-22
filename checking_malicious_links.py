import json


def get_links(filename):
    with open('json_files/'+filename, 'r') as json_file:
        links = json.load(json_file)
        return links


def check_links(links, malicious_links, file_path):
    unsecure_links = []
    secure_links = []
    for link in links:
        if link in malicious_links:
            unsecure_links.append(link)
        else:
            secure_links.append(link)
    print(f"UNSECURE LINKS {unsecure_links} for FILE_PATH {file_path}: ")
    print(f"SECURE LINKS {secure_links} FOR FILE_PATH {file_path}: ")


if __name__ == "__main__":
    malicious_links = get_links("malicious_links.json")
    links_info = get_links("links.json")
    for link_info in links_info:
        file_path = link_info['file_path']
        links = link_info['links']
        check_links(links, malicious_links, file_path)
