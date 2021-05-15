import requests
import csv
from datetime import datetime, time
import smtplib
import re
import sched
import time as time_module

# set to save text_sms as sms_text is not be duplicate
dup_msg = set()


# validate mobile number should be with length of 10
def isvalid_number(number):
    if len(number) == 10:
        return True
    else:
        print("Mobile number is not valid")
    return False


# validate sms text length and text sms should not be duplicate
def isvalidText(text):
    if (len(text) >= 1) and (len(text) <= 160):
        if text not in dup_msg:
            dup_msg.add(text)
            return True
    else:
        print("sms text is not valid")
    return False


# validate country should only contain INDIA and USA
def valid_country(country):
    if country in ["INDIA", "USA"]:
        return True
    return False


# validate Email
def validmail(email):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if re.search(regex, email):
        return True
    return False


# check validation of all in one function
def validateAll(text, number, country, email):
    return isvalidText(text) and isvalid_number(number) and valid_country(country) and validmail(email)


def request_call(payload):
    response = requests.request("POST", url, data=payload, headers=headers)
    if response.json()['status'] == "submitted":
        print("Success\n")

# run below command on cmd to start local smtp server
# python -m smtpd -c DebuggingServer -n localhost:1025
def sendmail(receiver_email, message):
    # mail sender and port
    port = 1025  # For SSL
    smtp_server = "localhost"
    sender_email = "my@gmail.com"
    with smtplib.SMTP(smtp_server, port) as server:
        server.sendmail(sender_email, receiver_email, message)


# url and header to post the data to API
url = "https://api.sms-magic.com/v1/sms/send"

headers = {
    'apiKey': "f0270c1b14951bcfd79360190c7abfa4",
    'content-type': "application/x-www-form-urlencoded",
}

# id of message sender
sender_id = 121321

# creating dictionary object to send data with post request
ans = dict()
with open("Sample.csv", "r")as csvfile:
    # reading csv
    reader = csv.reader(csvfile)
    i = 0
    for line in reader:
        # skip the first line as it contains attribute headers
        if not i == 0:

            # read sms_text from csv
            text = line[0]

            # read email from csv
            email = line[1]

            # read country from csv
            country = line[3]

            # read date for when to send request from csv
            date = line[4]

            # reading mobile number from csv
            mobile = line[2]

            print(email, mobile, text)
            print(str(text))

            if validateAll(text, mobile, country, email):
                sendmail(email, text);

                ans["sms_text"] = text
                ans["sender_id"] = sender_id
                ans["mobile_number"] = mobile
                payload = ans


                # print(today)
                # date += " 10:00:00"
                # scheduler = sched.scheduler(time_module.time, time_module.sleep)

                # t = time_module.mktime(t)
                # print(t)
                # scheduler_e = scheduler.enter(delay=10,priority=1,action= request_call(payload))

                # match today's date to given date  and should have valid time window
                # t = datetime.strptime(date, '%d/%m/%Y')
                # print(t.date())
                # if today == t.date():

                # check request is in valid time window
                now = datetime.now().time()
                today = datetime.now().date()
                if time(10, 00) <= now <= time(23, 00):
                    request_call(payload)
                else:
                    print("not valid time window")
                ans.clear()
            else:
                print("validation error occurred")
        i += 1
