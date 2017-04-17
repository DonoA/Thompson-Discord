from lxml import etree
import urllib.request, requests
from splinter import Browser
import time, json

class Ideone:
    # Executes the given code in the given language and returns the id of the result
    def execute(self):
        with Browser() as browser:
            self.logger("Screen ready")
            browser.visit("http://ideone.com/")
            req_data = {
                "Submit": "",
                "_lang": browser.find_by_xpath("//*[@data-label=\"{}\"]".format(self.language)).first["data-id"],
                "clone_link": "/",
                "file": self.code,
                "input": self.std_in,
                "note": "",
                "p1": browser.find_by_xpath("//*[@id=\"p1\"]").first["value"],
                "p2": browser.find_by_xpath("//*[@id=\"p2\"]").first["value"],
                "p3": browser.find_by_xpath("//*[@id=\"p3\"]").first["value"],
                "p4": browser.find_by_xpath("//*[@id=\"p4\"]").first["value"],
                "public": "",
                "run": 1,
                "syntax": 0,
                "timeline": 0
            }
            self.logger("Req data compiled {}".format(json.dumps(req_data)))
            cookies = browser.cookies.all()
            del browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                'Cookie': "PHPSESSID={};JIDEONE={}".format(cookies["PHPSESSID"], cookies["JIDEONE"])
            }
            self.logger("Headers compiled {}".format(json.dumps(headers)))

            r = requests.post("http://ideone.com/ideone/Index/submit/", data=req_data, stream=True, headers=headers)
            html = etree.HTML(r.content)
            self.url = html.xpath("//*[@id=\"info\"]/legend[1]/text()")[0][1:]
            self.logger("Received url {}".format(self.url))
            self.id = self.url[-6:]

    # tries to find std out if execution has completed
    def fetch_results(self):
        self.logger("Attempting result fetch")
        r = requests.get(self.url)
        html = etree.HTML(r.content)
        stat = html.xpath("//*[@id=\"view_status\"]/span/span/text()")[0]
        if stat == "Success":
            self.std_out = html.xpath("//*[@id=\"output-text\"]")[0].text
        elif stat != "Running":
            self.error = stat
        else:
            self.logger("Running")

    def __init__(self, code, language, logger, std_in=""):
        self.logger = logger.log
        self.code = code
        self.language = language.title()
        print(self.language)
        self.id = None
        self.url = None
        self.error = None
        self.std_in = std_in
        self.std_out = None
