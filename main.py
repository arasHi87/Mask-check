import collections

from utils import *
from config import *
from fuzzywuzzy import fuzz

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    TextMessage, 
    MessageEvent,
    PostbackEvent,
    CarouselColumn, 
    PostbackAction,
    TextSendMessage,
    CarouselTemplate, 
    LocationSendMessage,
    TemplateSendMessage, 
)

app = Flask(__name__)

line_bot_api = LineBotApi(CNANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CNANNEL_SECRET)
DataAll = LoadData()

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent)
def handle_message(event):
    global DataAll
    interval = CalcTime(DataAll[0][6])
    if interval[0] > 1 or interval[1] > 300:
        # line_bot_api.reply_message(event.reply_token, TextSendMessage('更新資料中，請稍後數秒'))
        DownloadMask()
        DataAll = LoadData()
    
    if event.message.type == 'location':
        lat = event.message.latitude
        lon = event.message.longitude
        ret = GetDistance(np.matrix([[float(x[7]), float(x[8])] for x in DataAll]),
                          np.matrix([[lat, lon]])).argsort(axis=0)[:10]
        alt_text = ""
        carousel_data = []

        for idx in ret:
            data = DataAll[int(idx)]
            alt_text += "{}:\n  成人剩餘{}個、孩童剩餘{}個\n".format(
                data[1], data[4], data[5]
            )
            carousel_data.append([
                data[1],
                "aldut last {}\nchild last {}".format(data[4], data[5]),
                'get map',
                str(data[1]),
                "address:{},{},{},{}".format(data[7],
                                  data[8],
                                  data[1],
                                  data[2]) 
            ])
        
        line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
            alt_text = alt_text,
            template = CarouselTemplate(
                columns = [
                    CarouselColumn(
                        thumbnail_image_url = 'https://i.giphy.com/media/Nm8ZPAGOwZUQM/giphy.webp',
                        title = data[0],
                        text = data[1],
                        actions = [
                            PostbackAction(
                                label = data[2],
                                display_text = data[3],
                                data = data[4]
                            )
                        ]
                    ) for data in carousel_data
                ]
            )
        ))
    else:
        name = event.message.text
        score = []
        cnt = 0

        for data in DataAll:
            score.append((fuzz.partial_token_set_ratio(data[1], name), cnt))
            cnt += 1
        
        score.sort(reverse = True)
        idx = score[0][1]
        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text = '{}\n成人剩餘{}個、小孩剩餘{}個'.format(
                DataAll[idx][1],
                DataAll[idx][4],
                DataAll[idx][5]
        )))

@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data.startswith('address:'):
        data = event.postback.data.split(':')[1].split(',')
        lat = data[0]
        lon = data[1]
        address = data[2]
        
        line_bot_api.reply_message(event.reply_token, LocationSendMessage(
            title = data[2],
            address = data[3],
            latitude = lat,
            longitude = lon
        ))

if __name__ == "__main__":
    app.run()