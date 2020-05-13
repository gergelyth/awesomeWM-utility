#!/usr/bin/python

from gmail_service import get_gmail_service

def main():
    service = get_gmail_service()

    # verify there is at least 1 unread thread
    # TODO: probably unnecessary query
    unread_thread_count = service.users().labels().get(userId="me", id="INBOX").execute()['threadsUnread']
    if (unread_thread_count == 0):
        return

    threads = service.users().threads().list(userId="me", labelIds=["INBOX", "UNREAD"]).execute().get('threads', [])
    for thread in threads:
        threadInfo = service.users().threads().get(userId="me", id=thread["id"]).execute()
        message = threadInfo['messages'][0]['payload']

        for header in message['headers']:
            if header['name'] == 'Subject':
                subject = header['value']
            # if header['name'] == 'Date':
            #     print(header['value'])
            if header['name'] == 'From':
                from_string = header['value']

        if from_string:
            print(from_string)
        if subject:  
            print(subject)

        message_count = len(threadInfo['messages'])
        last_message = threadInfo['messages'][message_count - 1]['snippet']
        print(last_message)

    # for label in labels:
    #     result = service.users().labels().get(userId="me", id=label['id']).execute()['threadsUnread']
    #     print(label['name'], label['id'], result, sep=" ")

    # if not messages:
    #     print('No messages found.')
    # else:
    #     print('Messages:')
    #     for message in messages:
    #         print(message)
    #         snippet = service.users().messages().get(userId="me", id=message['id']).execute()
    #         snippet_string = snippet['snippet']
    #         print(snippet_string)

if __name__ == '__main__':
    main()
