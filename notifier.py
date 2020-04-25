import xml.etree.ElementTree as ET
from dataclasses import dataclass
import requests
import os
import sys
import urllib.parse as urlencoder

@dataclass
class Bot():
    token: str
    chat_id: int

@dataclass
class Testsuite():
    errors: int
    failures: int
    hostname: str
    name: str
    skipped: int
    tests: int
    time: float
    timestamp: str

bot = Bot(token=os.environ["TELEGRAM_TOKEN"], chat_id=int(os.environ["TELEGRAM_CHAT_ID"]))
home = os.environ["CIRCLE_WORKING_DIRECTORY"].replace("~", os.environ["HOME"])



def _send_test_report(subject: str, testsuite: Testsuite):
    result = "✅" if testsuite.failures != 0 or testsuite.errors != 0 else "❌"
    message = """*Test Report \\({}\\)* {}
    ```
successs:  {:>3}
failures:  {:>3}

errors:    {:>3}
    ```
    """.format(subject, result, testsuite.tests, testsuite.failures, testsuite.errors)
    encoded_message = urlencoder.quote_plus(message)
    response = requests.post(f"https://api.telegram.org/bot{bot.token}/sendMessage?chat_id={bot.chat_id}&text={encoded_message}&parse_mode=markdownv2")
    assert response.status_code == 200

def send_test_report(subject: str, path: str):
    tree = ET.parse(home + path)
    root = tree.getroot()
    testsuite = Testsuite(**root[0].attrib)
    _send_test_report(subject, testsuite)

send_test_report("unit", "/test-results/junit.xml")
send_test_report("integration", "/test-results/junit-integration.xml")

sys.exit(0)


    
