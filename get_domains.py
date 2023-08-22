def get_inbox_domains(my_emails):
    extracted_emails = []
    domains = []
    for email_info in my_emails:
        email = email_info["From"]
        start_index = email.find('<') + 1
        end_index = email.find('>', start_index)

        if start_index != -1 and end_index != -1:
            extracted_content = email[start_index:end_index]
            extracted_emails.append(extracted_content)
    for email in extracted_emails:
        domain = email.split('@')[1]
        domains.append(domain)
    return domains


if __name__ == "__main__":
    domains = get_inbox_domains()
