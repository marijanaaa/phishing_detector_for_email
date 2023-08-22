import json


def get_domains(filename):
    with open('json_files/'+filename, 'r') as json_file:
        domains = json.load(json_file)
        return domains


def check_domains(domains, malicious_domains):
    unsecure_domains = []
    secure_domains = []
    for domain in domains:
        if domain in malicious_domains:
            unsecure_domains.append(domain)
        else:
            secure_domains.append(domain)
    print("UNSECURE DOMAINS : ", unsecure_domains)
    print("SECURE DOMAINS : ", secure_domains)


if __name__ == "__main__":
    inbox_domains = get_domains('domains.json')
    malicious_domains = get_domains('malicious_domains.json')
    check_domains(inbox_domains, malicious_domains)
