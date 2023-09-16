import json


def get_file_hashes(filename, hash_function):
    with open('json_files/'+filename, 'r') as json_file:
        file_hashes = json.load(json_file)
        result = []
        for file_hash in file_hashes:
            if hash_function == 'sha256':
                sha256 = file_hash['file_hash256']
                result_json = {
                    'file': sha256,
                    'file_path': file_hash['file_path']
                }
                result.append(result_json)
            elif hash_function == 'sha1':
                sha1 = file_hash['file_hash1']
                result_json = {
                    'file': sha1,
                    'file_path': file_hash['file_path']
                }
                result.append(result_json)
        return result


def get_malicious_file_hashes(filename):
    with open('json_files/'+filename, 'r') as json_file:
        malicious_file_hashes = json.load(json_file)
        return malicious_file_hashes


def check_files(file_hashes, malicious_file_hashes):
    unsecure_file_hashes = []
    secure_file_hashes = []
    for file_hash in file_hashes:
        file_obj = {
            'file_path': file_hash['file_path'],
            'file_hash': file_hash['file']
        }
        if file_hash in malicious_file_hashes:
            unsecure_file_hashes.append(file_obj)
        else:
            secure_file_hashes.append(file_obj)
    print("UNSECURE FILE_HASHES : ", unsecure_file_hashes)
    print("SECURE FILE_HASHES : ", secure_file_hashes)


if __name__ == "__main__":
    inbox_file_hashes_SHA256 = get_file_hashes('file_hashes.json', 'sha256')
    inbox_file_hashes_SHA1 = get_file_hashes('file_hashes.json', 'sha1')
    malicious_file_hashes_SHA256 = get_malicious_file_hashes(
        'malicious_file_hashes_SHA256.json')
    malicious_file_hashes_SHA1 = get_malicious_file_hashes(
        'malicious_file_hashes_SHA1.json')
    print("-------------------Files with file SHA256 hash algorithm--------------------")
    check_files(inbox_file_hashes_SHA256, malicious_file_hashes_SHA256)
    print("\n-------------------Files with file SHA1 hash algorithm----------------------")
    check_files(inbox_file_hashes_SHA1, malicious_file_hashes_SHA1)
