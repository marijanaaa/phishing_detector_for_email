from bs4 import BeautifulSoup
import os
import json
from urlextract import URLExtract
import hashlib


def process_folders(root_directory, folder_paths):
    for folder_name in os.listdir(root_directory):
        folder_path = os.path.join(root_directory, folder_name)
        if os.path.isdir(folder_path):
            folder_paths.append(folder_path)
            process_folders(folder_path, folder_paths)


def process_files(folder_paths):
    file_paths = []
    for folder_path in folder_paths:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                file_paths.append(file_path)
    return file_paths


def extract_links_from_file(file_path):
    link_info = []
    if file_path.endswith('.html'):
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            soup = BeautifulSoup(html_content, 'html.parser')
            links = soup.find_all('a')

            for link in links:
                if link.has_attr('href'):
                    link_info.append(link['href'])
                else:
                    link_info.append(link.get_text())
    elif file_path.endswith('text.json'):
        with open(file_path, 'r') as json_file:
            text_file = json.load(json_file)
            text = text_file['text']
            extractor = URLExtract()
            link_info = extractor.find_urls(text)
    return link_info


def extract_domain_from_file(file_path):
    domain = ''
    if file_path.endswith('description.json'):
        with open(file_path, 'r') as json_file:
            description_file = json.load(json_file)
            sender = description_file['sender']
            start_index = sender.find('<') + 1
            end_index = sender.find('>', start_index)

            if start_index != -1 and end_index != -1:
                extracted_content = sender[start_index:end_index]
                domain = extracted_content.split('@')[1]
            return domain


def calculate_file_hash(file_path, hash_function):
    # Open the file in binary mode to read its content
    with open(file_path, 'rb') as file:
        # Create a hash object based on the specified hash function
        if hash_function == 'sha1':
            hash_obj = hashlib.sha1()
        elif hash_function == 'sha256':
            hash_obj = hashlib.sha256()
        else:
            raise ValueError("Unsupported hash function")

        # Read and update hash string value in blocks of 4K
        for chunk in iter(lambda: file.read(4096), b""):
            hash_obj.update(chunk)

        # Return the hexadecimal representation of the hash
        return hash_obj.hexdigest()


def write_to_file(filename, data):
    with open("json_files/"+filename, "w")as outfile:
        outfile.write(data)


if __name__ == '__main__':
    root_directory = 'email_files'
    folder_paths = []
    process_folders(root_directory, folder_paths)
    file_paths = process_files(folder_paths)
    links = []
    domains = []
    file_hashes = []
    counter = 0
    for file_path in file_paths:
        if file_path.endswith('text.json') or file_path.endswith('.html'):
            link_info = extract_links_from_file(file_path)
            link_obj = {
                'file_path': file_path,
                'links': link_info
            }
            links.append(link_obj)
        if file_path.endswith('description.json'):
            domain = extract_domain_from_file(file_path)
            domains.append(domain)
        if not file_path.endswith('.json') and not file_path.endswith('.html'):
            # fja
            # dictionary da ako je isti folder
            counter += 1
            print(counter, file_path)
            file_hash1 = calculate_file_hash(file_path, 'sha256')
            file_hash256 = calculate_file_hash(file_path, 'sha1')
            file_hash_obj = {
                'file_path': file_path,
                'file_hash1': file_hash1,
                'file_hash256': file_hash256
            }
            file_hashes.append(file_hash_obj)
    links_json = json.dumps(links, indent=2)
    domains_json = json.dumps(domains, indent=2)
    file_hashes_json = json.dumps(file_hashes, indent=2)
    write_to_file("links.json", links_json)
    write_to_file("domains.json", domains_json)
    write_to_file("file_hashes.json", file_hashes_json)
