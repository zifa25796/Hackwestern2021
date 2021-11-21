import sys
from productArray import *
from flask import Flask, request, render_template
from urllib.parse import unquote
from time import sleep

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def init():
    if request.method == "GET":
        stat = "[]"
        item = request.args.get("itemname")
        url = request.args.get("url")
        if url != None:
            pAdd(item, url)
            stat = pGetStat()
        return render_template("index.html", text=stat)


def pAdd(name, url):
    tempProductArray.add(product(name, url))


def pChangeToHtml(array):
    ret = ""
    for product in array:
        ret += "["
        for item in product:
            ret += '"' + item + '",'
        ret += "], "
    return ret[0:-4] + "]"


def pGetStat():
    if (len(tempProductArray.array) == 0):
        return "[]"
    return unquote("[" + pChangeToHtml(tempProductArray.getStats()) + "]")


tempProductArray = productArray()
if __name__ == '__main__':
    app.run(debug=True)
    # pAdd("", "https://www.bestbuy.ca/en-ca/product/intel-core-i9-12900k-octa-core-3-2ghz-processor/15778670")
    # pGetStat()

    # for item in ['https://www.bestbuy.ca/en-ca/product/amazon-fire-tv-stick-4k-2021-media-streamer-with-alexa-voice-remote/15665552',
    #              'https://www.bestbuy.ca/en-ca/product/intel-core-i9-12900k-octa-core-3-2ghz-processor/15778670',
    #              'https://www.amazon.ca/dp/B074DXFB66/ref=sspa_dk_detail_3?psc=1&pd_rd_i=B074DXFB66&pd_rd_w=XINrl&pf_rd_p=354dffd6-5655-4a2b-a4e7-19708ddd8a8b&pd_rd_wg=tD6AY&pf_rd_r=SWMKVM5TKZ6HVDNRMQZH&pd_rd_r=0ce5c51d-0100-4972-8b76-d45027351170&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEySDJSSkdGTDBNWkQmZW5jcnlwdGVkSWQ9QTA1MjcxOTIxMUNJNEFXQlU4REkxJmVuY3J5cHRlZEFkSWQ9QTA4NTcyMDUzREwyMVEzT081STImd2lkZ2V0TmFtZT1zcF9kZXRhaWxfdGhlbWF0aWMmYWN0aW9uPWNsaWNrUmVkaXJlY3QmZG9Ob3RMb2dDbGljaz10cnVl',
    #              'https://www.amazon.ca/Intel-i9-12900K-Desktop-Processor-Unlocked/dp/B09FXDLX95/ref=sr_1_1?crid=4P0YPFJKV0BN&keywords=intel+core+i9-12900k&qid=1637385974&sprefix=intel+cor%2Caps%2C176&sr=8-1',
    #              'https://www.amazon.ca/GeForce-RTX-2060-Architecture-Graphics/dp/B07MC23VS4/ref=sr_1_1?keywords=2060&qid=1637388317&sr=8-1']:
    #     tempProductArray.add(product("", item))
    #
    # sendEmail("\n".join(str(e) for e in tempProductArray.getStats()))
