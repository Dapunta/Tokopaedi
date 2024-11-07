#--> Standard Module & Library
import json, urllib
from typing import Generator

#--> Flask
from flask import Flask, Response, request
from flask_cors import CORS
app = Flask(import_name=__name__)
CORS(app=app)

#--> Local Module
from tokopedia.tokopedia import Tokopedia
from tokopedia.heuristic import Heuristic

#--> Landing
@app.route(rule='/')
def stream() -> Response:
    response: dict[str,str] = {
        'status'  : 'failed',
        'message' : 'yo ndak tau, kok tanya saya'}
    return Response(response=json.dumps(obj=response, sort_keys=False), mimetype='application/json')

#--> Fetch Product
@app.route(rule='/fetch', methods=['GET'])
def fetchRoute() -> Response:
    product_link : str = urllib.parse.unquote(request.args.get(key='url', default=None))
    def generate() -> Generator[str, any, None]:
        TP = Tokopedia()
        for product_info in TP.searchProductBySimilarity(product_link=product_link):
            try:
                yield 'data: {}\n\n'.format(json.dumps(obj=product_info))
            except:
                continue
        yield 'event: end\ndata: end_of_stream\n\n'
    return Response(response=generate(), mimetype='text/event-stream')

#--> Count Score & Get Result
@app.route(rule='/heuristic', methods=['POST'])
def heuristicRoute() -> Response:
    data : list = request.get_json().get('data',None)
    HS = Heuristic(list_product=data)
    best : list[dict] = HS.search(count=3)
    return Response(response=json.dumps(obj={'data':best}, sort_keys=False), mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)