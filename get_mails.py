from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from base64 import urlsafe_b64decode
from mimetypes import guess_type as guess_mime_type


def setup_gmail_api():
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    credentials = None
    if os.path.exists('json_files/token.json'):
        flow = InstalledAppFlow.from_client_secrets_file(
            'json_files/credentials.json', SCOPES)
        credentials = flow.run_local_server()
    else:
        flow = InstalledAppFlow.from_client_config(
            'json_files/credentials.json', SCOPES)
        credentials = flow.run_local_server()
        with open('json_files/token.json', 'w') as token:
            token.write(credentials.to_json())

    service = build('gmail', 'v1', credentials=credentials)
    return service


def parse_parts(service, parts, folder_name, message, payload, sender, subject, date):
    if parts:
        for part in parts:
            filename = part.get("filename")
            mimeType = part.get("mimeType")
            body = part.get("body")
            data = body.get("data")
            headers = part.get("headers")
            if part.get("parts"):
                parse_parts(service, part.get("parts"),
                            folder_name, message, payload, sender, subject, date)
            parse_by_mime_type(mimeType, folder_name, filename,
                               headers, body, data, service, message, sender, subject, date)
    else:
        filename = payload["filename"]
        mimeType = payload["mimeType"]
        body = payload['body']
        data = body['data']
        headers = payload["headers"]
        parse_by_mime_type(mimeType, folder_name, filename,
                           headers, body, data, service, message, sender, subject, date)


def parse_by_mime_type(mimeType, folder_name, filename, headers, body, data, service, message, sender, subject, date):
    if mimeType == "text/plain":
        if data:
            text = urlsafe_b64decode(data).decode()
            text_data = {
                'text': text
            }
            description_data = {
                'sender': sender,
                'subject': subject,
                'date': date
            }
            filename = "text.json"
            filepath = os.path.join(folder_name, filename)
            with open(filepath, "w") as outfile:
                json.dump(text_data, outfile, indent=2)
            filename = "description.json"
            filepath = os.path.join(folder_name, filename)
            with open(filepath, "w") as outfile:
                json.dump(description_data, outfile, indent=2)
    elif mimeType == "text/html":
        if not filename:
            filename = "index.html"
        filepath = os.path.join(folder_name, filename)
        with open(filepath, "wb") as f:
            f.write(urlsafe_b64decode(data))
    else:
        for header in headers:
            part_header_name = header.get("name").lower()
            attachment_id = body.get("attachmentId")
            if part_header_name == "content-disposition":
                attachment = service.users().messages() \
                    .attachments().get(id=attachment_id, userId='me', messageId=message['id']).execute()
                data = attachment.get("data")
                filepath = os.path.join(folder_name, filename)
                if data:
                    with open(filepath, "wb") as f:
                        f.write(urlsafe_b64decode(data))


def clean(text):
    return "".join(c if c.isalnum() else "_" for c in text)


def get_all_emails():
    gmail_service = setup_gmail_api()

    results = gmail_service.users().messages().list(
        userId='me', labelIds=['INBOX']).execute()
    messages = results.get('messages', [])
    print(f"Total {len(messages)} messages found in your inbox:")

    emails = []

    for message in messages:
        msg = gmail_service.users().messages().get(
            userId='me', id=message['id']).execute()

        payload = msg['payload']
        headers = payload.get("headers")
        parts = payload.get("parts")
        folder_name = "email"
        if headers:
            for header in headers:
                name = header.get("name")
                value = header.get("value")
                if name.lower() == 'from':
                    sender = value
                if name.lower() == "subject":
                    has_subject = True
                    folder_name = clean(value)
                    folder_counter = 0
                    while os.path.isdir('email_files/'+folder_name):
                        folder_counter += 1
                        if folder_name[-1].isdigit() and folder_name[-2] == "_":
                            folder_name = f"{folder_name[:-2]}_{folder_counter}"
                        elif folder_name[-2:].isdigit() and folder_name[-3] == "_":
                            folder_name = f"{folder_name[:-3]}_{folder_counter}"
                        else:
                            folder_name = f"{folder_name}_{folder_counter}"
                    if not os.path.exists('email_files'):
                        os.mkdir('email_files')
                    os.mkdir(os.path.join('email_files', folder_name))
                    subject = value
                if name.lower() == "date":
                    date = value

        if not has_subject:
            new_folder_name = os.path.join('email_files', folder_name)
            if not os.path.isdir(new_folder_name):
                os.mkdir(new_folder_name)
        parse_parts(gmail_service, parts, 'email_files/' +
                    folder_name, message, payload, sender, subject, date)


if __name__ == '__main__':
    get_all_emails()
