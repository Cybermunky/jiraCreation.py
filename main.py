import requests
from requests.auth import HTTPBasicAuth
import json
from dotenv import load_dotenv
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--Payload', type=str, required=True, help='JSON payload for the program data')
args = parser.parse_args()
load_dotenv()
JIRA_URL = os.getenv("JIRA_ENDPOINT")
JIRA_API = os.getenv("JIRA_API")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_AUTH = HTTPBasicAuth(JIRA_EMAIL, JIRA_API)
JIRA_KEY = "NI-3935"
HEADERS = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

def Get_Jira_Case():
    print(4)
    CASE_URL = JIRA_URL + JIRA_KEY
    print(CASE_URL)
    response = requests.get(CASE_URL, data=PAYLOAD, auth=JIRA_AUTH, headers=HEADERS)
    print(response)
    return response.text

def Create_Case(PAYLOAD):
    PAYLOAD = json.dumps(PAYLOAD)
    response = requests.post(JIRA_URL, data=PAYLOAD, auth=JIRA_AUTH, headers=HEADERS)
    return response.text

def Create_Payload(FAMILY, HOME, IP, ANALYST, PENTEST, RT, RA, ISP, ASN, CNTRY, CITY, STATE, SUMMARY, ISSUE_TYPE):
    PAYLOAD = {
        "fields": {
            "project": {
                "key": "NI"
            },
            "priority": {
              "self": "https://blackcloak.atlassian.net/rest/api/3/priority/3",
              "iconUrl": "https://blackcloak.atlassian.net/images/icons/priorities/medium.svg",
              "name": "Medium",
              "id": "3"
            },
            "customfield_10048": {
                # "self": "https://blackcloak.atlassian.net/rest/api/3/customFieldOption/10044",
                "value": ANALYST,
                # "id": "10044"
            },
            "customfield_10049": {
              #"self": "https://blackcloak.atlassian.net/rest/api/3/customFieldOption/10044",
              "value": PENTEST,
              #"id": "10044"
            },
            "customfield_10082": RT,
            "customfield_10083": RA,
            "customfield_10052": "Tracking ID",
            "customfield_10045": FAMILY, # Family ATC ID
            "customfield_10046": HOME, # Home Record ID
            "customfield_10047": IP, # IP Address
            "customfield_10063": ISP, # Internet Service Provider
            "customfield_10064": ASN, # ASN
            "customfield_10065": "DEVELOPMENT", # NMAP Stage
            "customfield_10060": CITY, # City
            "customfield_10061": STATE, # State
            "customfield_10062": CNTRY, # Country
            "summary": SUMMARY,
            "issuetype": {
                "name": ISSUE_TYPE
            }
        }
    }
    return PAYLOAD
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("[+] Jira Ticket Creation")

    payload = json.loads(args.Payload)
    FAMILY = payload['familyAtcId']
    HOME = payload['homeRecordId']
    IP = payload['ipAddress']
    ANALYST = payload['analystDetermination']
    PENTEST = payload['ptDetermination']
    RT = payload['requestType']
    RA = payload['requestAction']
    ISP = payload['isp']
    ASN = payload['asn']
    CNTRY = payload['country']
    CITY = payload['city']
    STATE = payload['state']
    SUMMARY = payload['summary']
    ISSUE_TYPE = payload['issueType']

    PAYLOAD = Create_Payload(FAMILY, HOME, IP, ANALYST, PENTEST, RT, RA, ISP, ASN, CNTRY, CITY, STATE, SUMMARY, ISSUE_TYPE)

    RESPONSE = Create_Case(PAYLOAD)
    # RESPONSE = Get_Jira_Case()
    print(RESPONSE)