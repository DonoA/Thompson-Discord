from lxml import etree
import urllib.request, requests
from splinter import Browser
from pyvirtualdisplay import Display
import time

display = Display(visible=0, size=(800, 600))
display.start()

class Ideone:
    # Executes the given code in the given language and returns the id of the result
    def execute_code(code, language, stdin=""):
        with Browser() as browser:
            browser.visit("http://ideone.com/")
            print("visited")
            req_data = {
                "Submit": "",
                "_lang": browser.find_by_xpath("//*[@data-label=\"{}\"]".format(language.title())).first["data-id"],
                "clone_link": "/",
                "file": code,
                "input": stdin,
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
            print("constructed req")
            cookies = browser.cookies.all()
            del browser
            # gc.collect()
            print("destroyed disp")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                'Cookie': "PHPSESSID={};JIDEONE={}".format(cookies["PHPSESSID"], cookies["JIDEONE"])
            }

            r = requests.post("http://ideone.com/ideone/Index/submit/", data=req_data, stream=True, headers=headers)
            html = etree.HTML(r.content)
            return html.xpath("//*[@id=\"info\"]/legend[1]/text()")[0][-6:]
