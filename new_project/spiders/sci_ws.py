import websocket
import threading
import _thread as thread

from common.tools import headersChange


def get_wss_header(SID):
    header = headersChange(f'''Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: no-cache
Connection: Upgrade
Cookie: _sp_ses.840c=*; bm_sz=30AA5A7AFA3A7BEA5E68D8FBEBCD8712~YAAQHu0BF5T76W2GAQAAXwb+chKEQXqwfZs2/0nO7rXXWl+O/uSahKyGurw/mzdinjypvgiOFq7y2E4+jUioWJLYxl99kdZgLLwU2yPOJt0xQbukyYnJJzNoAt+ymBpuDhbkE1paKFd4IR2yGVdL69+jNAOLIgJlXfAY2FxeTCkbp9zNAY4ct9ucra176sKYwzp7K0KgmA/Q5mahxQPz3j8QOoEzAi+crsD5QZc4AnowWyzNYuf9QrbadzcYzV7meX5f85QD85Way9HzKYHlZa2S/VmX5bWyDsQK4z+EO5gWNDC/nlYrdxI=~3425075~4600369; dotmatics.elementalKey=SLsLWlMhrHnTjDerSrlG; bm_mi=BC5B628B5F6056511218E4C2A15329BC~YAAQPO0BF1/KBWiGAQAArjcDcxJRDj3bW1WVsygZcEh8sD+g8otMO38aTHAAfp6FQMlTFOvFmaNhkP7iOHpD7mUTq03IE7izOHzr8bbxAvoOc+pepEL/mRnbdfYoi/IRbsGK80WRSPzdPPC3pWo/kaSHPqoEpKh9brlij9XDgxYyBKhKT8Jmn9mq3TsjP4d5Lv39pLyAkbeUX9Kkshilg/KKre48OkWaa3UqfP62Djod7ZvAsjZ8CZTcMKkkC+NFz+2+WI+uKzRAi5CWQHi/2O9OFT7tuDOUCViyRe/levSWz0ZZemg6BeoulV1X/f97mShnUt59NlM=~1; _abck=B773D71698BCCCB5E5A9AA1D0623AB0F~0~YAAQPO0BF2nKBWiGAQAAtjgDcwmnCU4Ij56xQvmp0Uco/+BA1ZNnEdty2yk7Z+0vySC0lKAsupbr3fpSd4rZrDpHUnIhHYDQNL5UTdst5qXvUqRDZZnvUxLjThBW/jEJWpX6t9HoupsINo24uhWn2/HAavmx7rCb8lT3BgqZzz5kT+7ittTMqm425jUvfG0FY5XgMCPSubszrMeFxpq5Ds6HGSJA7kVc33C9m4Q7V+GH25rv6sl5J9K/puWEdcVhCkublw7S9ZKT5wpS1XcLr6SXnmPjOAMpdSU56+uf9Wj8i5267JvQO7Apn1c0XzOtWZY4aF1Aap9aKC6FtzAuzfbax6qsr3ILgcn5rtuGG1QYGTLiHakyHSdMIAlQx6vKxN1NCf6E+OPBJTVWdq+LqsPvrmy3caVFzfvvla7V~-1~-1~-1; ak_bmsc=E1B52C4717609157D67C189B90293215~000000000000000000000000000000~YAAQPO0BF/rKBWiGAQAA9lADcxKygOouUU2/F9GeSgKkwKm4HrZN8TXftS4TnHiz6LwCJxscGXIWTinQOnNsIbrOJMPDu4SAn6iB7nQ1M5J8w1qYi1XrpbAV8qiPEa8qZ+CeLUSyZtvUUgBG6qxn0TwreFsRGULjwfq1Iqq4WuNKkbXxKZWoy27U1C5OfGUBy4/rigjdDIjKDR/YqWXdOPqycEEZK+tMfouEuYblqerXdzdrqgK/ZQmboN3Qnva+oiDBw/wnaEINl/zOvC0WVhtj0zDhxeXw+hDM/G/JGGkaML+Hjt/PEwSFuXW7pE8HmCw7rZDzhYaQwpaoaHFrHWuaBZd0kzs+tOFIC9RmFHeshIpN+vp+XCTaqiwu3WfQGTFntu79ycKNlazZNN6ZKnltYi3OqQ61bwT2EGg/W77bLpyUUSzz; OptanonAlertBoxClosed=2023-02-21T08:07:23.183Z; RT="z=1&dm=www.webofscience.com&si=b0d68a10-6184-4c3e-af34-82a6f3ef9279&ss=ledyr75i&sl=0&tt=0&bcn=%2F%2F17de4c1e.akstat.io%2F&ul=rhb8&hd=rhbv"; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Feb+21+2023+16%3A28%3A45+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=6.39.0&isIABGlobal=false&hosts=&consentId=1814a3a7-aad9-4991-812c-a1daff151d09&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1%2CC0005%3A1%2CC0002%3A1&geolocation=CN%3BHB&AwaitingReconsent=false; _sp_id.840c=47e9a5a1-af1c-4995-b99f-2a21c47ebd35.1676966495.25.1676968187..b7d78d90-e4f5-4c5a-aa6b-3ae773e56d77..3b68e798-ac79-4fe7-91f7-3cf478dba1db.1676966495144.31; bm_sv=4B4D074C56DAB23348BD98FBDD663028~YAAQrnRiaEFmqU6GAQAAzvgXcxJHN7tszNqJ5FkTVGM+2AdOP9b7jSvEomHRXnzxOEFrX4sPQohhiVYrcptKAv0J+1wiYVrF+FdrpozRAGxT4eX4tjWt13Y20fhWRSAshUPcWL8amM8JM3yOEbEhnlwAVI6eBKXvwfZkHpSeyTL0E/dOEdgOzrULFARN3hlOkD5S1qIwSOToJhVKDndLL9KSRjDOuEugOZ9FIPLBRWOojRYuea5gTnM1R/Rrqbyg8UxycBAO0g==~1
Host: www.webofscience.com
Origin: https://www.webofscience.com
Pragma: no-cache
Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits
Sec-WebSocket-Key: IkuThFH5936/JqJy19StWw==
Sec-WebSocket-Version: 13
Upgrade: websocket
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36
''')
    return header

def on_message(ws, message):
    print("message",message)


def on_error(ws, error):
    print(1,error)


def on_close(ws):
    print(2,"closed")


def on_open(ws):
    def run(*args):
        # message = '{"commandId": "runQueryGetRecordsStream", "params": {"qid": %s,"retrieve": {"first": %s,"sort": "relevance","count": 50,"jcr": true,"highlight": false,"analyzes": []},"product": "WOSCC","searchMode": "general","viewType": "records"},"id": 25}' % (qid, str((p - 1) * 50 + 1))
        message = '{"commandId":"runQueryGetRecordsStream","params":{"qid":"0d18c30b-0403-4a4b-9317-5018f0ee9d13-723846bd","retrieve":{"first":51,"sort":"relevance","count":50,"jcr":true,"highlight":false,"analyzes":[]},"product":"WOSCC","searchMode":"general","viewType":"records"},"id":33}'
        ws.send(message)
        #ws.close()
    thread.start_new_thread(run,())



def run(SID):
    websocket.enableTrace(False)
    ws_url = "wss://www.webofscience.com/api/wosnxcorews?SID=F5kCxYabndKJHSFszuj"
    _header = get_wss_header(SID)
    print(_header)
    ws = websocket.WebSocketApp(ws_url, on_error=on_error, on_close=on_close, header=get_wss_header(SID))
    ws.on_open = on_open
    ws.on_message = on_message
    wst = threading.Thread(target=ws.run_forever)
    wst.start()

if __name__ == '__main__':
    SID = 'USW2EC0AECJZELIJ8UyBgxdYCh8gg'
    run(SID)

