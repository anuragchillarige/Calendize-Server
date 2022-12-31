import requests
from datetime import datetime, timedelta
import icalendar
import recurring_ical_events

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from os import walk

cred = credentials.Certificate(
    {
        "type": "service_account",
        "project_id": "calendize-956a9",
        "private_key_id": "4a2411dce38590ae5c7c503dd3a6dc1a7613f763",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCqb8ddrgAfeT/j\neMi8hNNeRilveGpdvDTr58GAKm31Ov9rWPuia/RyUyN17DJE1ue+NXzkGfduHAVL\nu2T92vNlrsablhQ0CpaBIH7lyt3N4LipwHQ4y/xJY/OrqWiX05wFBKTLqXA9GAu/\n2zZy+Z3VJlDsLOnclvROg7PfwfddQStW6K/kVywAHZu0io/q0p2dDmF6KFKJtjvU\nRZvpei40t1AStn3KvVFE49s3NlsJzb6YFlGWMMytSrFAJNAoO4IgTosMvUJLHeyV\n+7DDtnx2gGgOTT8AXg4Gp+4W7OFOcFkX65j/6sV/yWLxEx2/OPb3dpvqJ7WGjpdE\nqymIJ6p9AgMBAAECggEAJskdM4JfYMo08c0Q0WXgu/l3gHiErCQiXvT0ofgF4eK1\nMXakfQfYLxQgY7uGjQfi4PRHIZmPJy2VPvC8QNDMxv0JEWsL2fP24BfHCQArjahw\nHaFAUZSKKyFl2FDLDpIHVVUDM52xfxWzxstaDrwjYNhBXh2ycpKfsiZijq8TXdMR\nsdYJ5jBsQyfmR2Ny7rov6u8ChEnxn0+HljxRi/OdgCqU9mQ1sAE9VmqsfTpabEsA\nhK1Xbemajc87+s4vaCba2ozjcBS2wdF5PAIyQDeF5ra8SULZ56JcqJoOXJ29R7R7\nvajNltfuJMOYaz1H+UjAjiRa3uQ0bOENNFHpTAXw+QKBgQDWR0mgDw8MyX1Nq4Fu\n1cPv/u2X/CexiLf2XxKdQyR/v7LPy9K261y4vS7e+lV+VI6xh/46YyJ8d56XVFJp\nvXat1MHyaYRit/S36zEOCwjCmSUlaGfMnLTW98t5US7d8uf5QGJ41V+JhC4yV5si\nCUSEFL7a9YRJCYw69gBz65bB/wKBgQDLnzHT7E/N267NRmwzV8akd3TWNNZEXA0n\nu18lpOg/DzoskDLoEO8lW7rXGCFxcxFPMDH5Rr5ie75nIQfh//aXO2JWBTtvCA0b\nCArCidJjfGWt9tPH9094k+mfVI3Quufsuv95f9QIGRmtGcQA9B1FJHqPXImM8i/h\nhOOrc3ObgwKBgQC2+2dvDI0AkWu0kPnVySwqXRtOB6Fp5OObu3Js4zJe+TfcZSUK\n2ZBznfJRrZqmZ9T227gI6jE/8vJ2Lia2b3nSVfZNaTgJCSgsiuZ4JIoVi6wB9td1\nDnkLfc2/Ssln9Y+M9SNiJmwQRdUhXlh2x01AMWsOFk0iBco/a2XVl+BExwKBgE1l\nDv1sHtEyJPjlQY8qV9h/hys8Hg0Rp/ZoI7wdOCFv2j7B+Hd4qE1c1mGXTG7gu72L\nphMHrqmkOzTbuzFNpx7IdZIYnwSO3NxfbCeRVyR1TfiXjtu8xrogDnZ/HwAtaqXy\nVdSKn78MO1QuLO/n2ZBEU0lWdPnbvBNN/XNXiKOdAoGBAMJ1wOxE2Oo4EnB3xtfE\nDn9M8TSzXiFNN73v5/cD6gjqSHkkIFbHrAPZZdsIPI5i9nr3JE5lLeiMwT71WjJ7\nmTB5eJO016NfackJo8rlwRQmXAvh/txgAcXthFwWgvxiuWNWi+g+Ijk09NN2FGuy\nD3SIO+zIg/BdnwwO1RI5Rse7\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-siqo4@calendize-956a9.iam.gserviceaccount.com",
        "client_id": "101739568031838917084",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-siqo4%40calendize-956a9.iam.gserviceaccount.com"
    }

)
firebase_admin.initialize_app(cred)
db = firestore.client()


def add_to_db(events, docID):

    try:
        for event in events:
            name = str(event['SUMMARY'])
            description = str(event['DESCRIPTION'])
            if (description.__contains__('To see detailed information for automatically created events like this one, use the official Google Calendar app.')):
                description = ""
            start = event['DTSTART'].dt
            start_time = start.strftime("%H:%M")
            duration = str(event['DTEND'].dt - start)

            day = event['DTSTART'].dt
            end = event['DTEND'].dt

            data = {
                "day": day,
                "duration": {
                    "hours": duration[0: duration.index(":")],
                    "mins": duration[duration.index(":") + 1: duration.rindex(":")]
                },
                "start_time": start_time,
                "name": name,
                "details": description,
                "end": end
            }

            db.collection("users").document(docID).collection("events").document(
                f'iCal {name} ON {start} AT {start_time}').set(data)
            print("added to db?")
        return True
    except Exception as e:
        print(e)
        return False


def read_ical(url, docID):
    today = datetime.now()
    start = (today.year, today.month, today.day)
    ending = datetime.now() + timedelta(days=10)
    end = (ending.year, ending.month, ending.day)

    try:
        cal = icalendar.Calendar.from_ical(requests.get(url).text)
        print("got request")
        events = recurring_ical_events.of(cal).between(start, end)
        add_to_db(events, docID)
    except Exception as e:
        print(e)


def read_ics(file_name, docID):
    today = datetime.now()
    start = (today.year, today.month, today.day)
    ending = datetime.now() + timedelta(days=10)
    end = (ending.year, ending.month, ending.day)

    try:
        file = open(file_name, "rb")
        cal = icalendar.Calendar.from_ical(file.read())
        events = recurring_ical_events.of(cal).between(start, end)
        add_to_db(events, docID)
    except Exception as e:
        print(e)


def addCalendars(docID):

    docRef = db.collection("users").document(docID)

    doc = docRef.get()

    if (doc.exists):
        links = doc.to_dict()['iCalLinks']
        for link in links:
            added = read_ical(link, docID)
            if (added == False):
                print("err")

    filenames = next(walk("Calendize/icsFiles"), (None, None, []))[2]
    icsFiles = []
    for file in filenames:
        if file[file.rindex("."):] == '.ics':
            icsFiles.append("Calendize/icsFiles/" + file)

    for file in icsFiles:
        read_ics(file, docID)

    return "<h1> TESTING </h1>"


def readRssLinks(docID):
    docRef = db.collection("users").document(docID)
    doc = docRef.get()

    links = []
    if(doc.exists):
        links = doc.to_dict()['rssLinks']
    return links
