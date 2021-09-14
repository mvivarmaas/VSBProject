import datetime
import math
import json
import requests
import xml.etree.ElementTree as ET
import math
import threading
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import time
from mainpage.models import Users, CRN
from background_task import background
import colorama
from colorama import Fore, Back, Style
from VSBProject import settings
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


colorama.init(autoreset=True)

ASIC_text = """
███████╗██████╗█████╗███╗   █████╗   ███████████████╗     ██╗     ██████╗ █████╗██████╗█████████████╗ 
██╔════██╔════██╔══██████╗  ██████╗  ████╔════██╔══██╗    ██║    ██╔═══████╔══████╔══████╔════██╔══██╗
█████████║    █████████╔██╗ ████╔██╗ ███████╗ ██████╔╝    ██║    ██║   ███████████║  ███████╗ ██║  ██║
╚════████║    ██╔══████║╚██╗████║╚██╗████╔══╝ ██╔══██╗    ██║    ██║   ████╔══████║  ████╔══╝ ██║  ██║
███████╚████████║  ████║ ╚██████║ ╚█████████████║  ██║    ███████╚██████╔██║  ████████╔█████████████╔╝
╚══════╝╚═════╚═╝  ╚═╚═╝  ╚═══╚═╝  ╚═══╚══════╚═╝  ╚═╝    ╚══════╝╚═════╝╚═╝  ╚═╚═════╝╚══════╚═════╝                                                                                                     
"""


class selectedclass:
    def __init__(self, name, discription, courseCode, term):
        self.name = name
        self.term = term
        self.discription = discription
        self.courseCode = courseCode
        self.added_CRNs = []
        self.array_blocks = []
        self.dictory_time_code = {}

    def add_time(self, code, time):
        self.dictory_time_code[code] = time

    def add_block(self, CRN, Professor, Waitlist, Notes, Classtime, Type, Sec, me, os, ws, wc):
        if CRN not in self.added_CRNs:
            self.added_CRNs.append(CRN)
            arrayofKeys = []
            for key in Classtime:
                arrayofKeys.append(self.dictory_time_code.get(key, "NA"))
            dict = {"crn": CRN, "instructor": Professor, "Waitlist": Waitlist, "Notes": Notes,
                    "classTimes": arrayofKeys,
                    "Type": Type, "Sec": Sec, "me": me, "numberAvailableSeats": os, "numberAvailableWaitList": ws,
                    "numberMaxWaitList": wc,
                    "seatsAvailable": FoundCRN(availableSeats=os, maxWaitlist=wc, avalibleWaitList=ws)}

            self.array_blocks.append(dict)

    def to_dict(self):
        return {"classTitle": self.name, "classDescription": self.discription, "className": self.courseCode,
                "timeBlock": self.array_blocks, "term": self.term, "crnArray": self.added_CRNs}


def get_date():
    # annoying function that needs to be entered for the time to be validated. Hopefully this does not change,
    # if this app crashes due to requests look for nWindow() in the vsb source code and copy that exactly here.
    array = ["&t=", "&e="]
    time = int(datetime.datetime.utcnow().timestamp()) * 1000
    # x 1000 to convert from Python to Javascript datetime object
    updated_time = (math.floor(time / 60000)) % 1000

    e = (updated_time % 3) + (updated_time % 19) + (updated_time % 42)
    e = str(e)
    updated_time = str(updated_time)
    return array[0] + updated_time + array[1] + e


def get_class(class_name, term):
    term = str(term)
    url_base = "https://vsb.mcgill.ca/vsb/getclassdata.jsp"
    url_term = "?term=" + term
    url_course = "&course_1_0=" + class_name
    url_useless = "&rq_1_0=null&nouser=1"
    url_date = get_date()
    final_url = url_base + url_term + url_course + url_useless + url_date
    r = requests.get(final_url,verify=False)


    if r.status_code == 200:

        myroot = ET.fromstring(r.text)
        if myroot.find(".//course") == None:
            print("error done")
            raise ArithmeticError

        valuefind = myroot.find(".//course").attrib
        xClass = selectedclass(valuefind["title"], valuefind["desc"], valuefind["key"], str(term))

        for x in myroot.findall(".//timeblock"):
            x = x.attrib
            xClass.add_time(x["id"], attrib_to_date_string(x))

        for x in myroot.findall(".//block"):
            x = x.attrib
            xClass.add_block(x["key"], x["teacher"], x["me"], "", x["timeblockids"].split(","), x["type"], x["secNo"],
                             me=x["me"], os=x["os"], ws=x["ws"], wc=x["wc"])

        return xClass
    else:
        return "fail"


def attrib_to_date_string(attrib):
    day = attrib_to_date(attrib["day"])
    start = calcProperTime(attrib["t1"])
    end = calcProperTime(attrib["t2"])
    return day + " : " + start + " - " + end


def calcProperTime(string):
    number = int(string)
    min = number % 60
    hour = math.floor(number / 60)

    if min < 10:
        min = str(min)
        min = "0" + min

    if hour >= 12:
        hour = hour - 12
        hour = str(hour)
        min = str(min)
        return hour + ":" + min + " PM"
    else:
        hour = str(hour)
        min = str(min)
        return hour + ":" + min + " AM"


def attrib_to_date(attrib_text):
    switcher = {
        "1": "Sunday",
        "2": "Monday",
        "3": "Tuesday",
        "4": "Wednesday",
        "5": "Thursday",
        "6": "Friday",
        "7": "Saturday",
    }
    return switcher.get(attrib_text, "NA")


@background(schedule=15)
def Scanner():
    print(Fore.RED + "SCAN START")
    class_checked_array = []
    for user in list(Users.objects.all()):
        for crn in user.crn.all():
            if (crn.class_name, crn.term) not in class_checked_array:
                class_checked_array.append((crn.class_name, crn.term))
                scanning_CRN = get_class(crn.class_name, crn.term).to_dict()
                print("Scanning:|", crn.class_name, "|", crn.term, "|")
                time.sleep(7)
                for block in scanning_CRN.get("timeBlock"):
                    if block.get("available"):
                        if CRN.objects.filter(CRN=block.get("CRN"), term=crn.term).exists():
                            final_crn = CRN.objects.get(CRN=block.get("crn"), term=crn.term)
                            if Users.objects.filter(crn=final_crn):
                                print(Fore.RED + "Found:  ", "|", crn.class_name, "|", crn.term, "|",
                                      block.get("crn"))
                                mass_email_phone(final_crn)


def FoundCRN(availableSeats, avalibleWaitList, maxWaitlist):
    availableSeats = int(availableSeats)
    avalibleWaitList = int(avalibleWaitList)
    maxWaitlist = int(maxWaitlist)

    if maxWaitlist > 0:
        if avalibleWaitList > 0:
            return True
    else:
        if availableSeats > 0:
            return True
        else:
            return False
    return False


def mass_email_phone(crn):
    group_users = Users.objects.filter(crn=crn)
    if group_users.exists():
        group_list = list(group_users)
        for user in group_list:
            send_email(name=crn.class_name, crn=crn.CRN, address=user.email)
    crn.delete()


def send_email(name, crn, address):
    # loop through all of the possible classes,
    # check if there is a waitlist avabile
    # if there is a waitlist avalible send the email and clear the users
    # once the users are cleared start again.

    message = Mail(
        from_email='support@freeseatfinder.com',
        to_emails=address,
        subject='Class found',
        html_content="Class:" + str(name) + "with CRN:" + str(crn) + "has waitlist space avaliable")
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(Fore.CYAN + "Email:  ", "| Status:", Fore.CYAN + str(response.status_code), "|", address)

    except Exception as e:
        print(e)
