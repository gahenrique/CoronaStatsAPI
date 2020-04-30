from flask import Flask, request, make_response
from service import Access

app = Flask(__name__)

@app.route("/")
def home():
    return "Corona App API. Use the endpoint /chart to get the chart of the growth on different countries"

@app.route('/chart', methods=['GET'])
def chart():
    chartImg = Access.getDeathGrowthChart()
    response = make_response(chartImg)
    response.headers.set('Content-Type', 'image/png')
    return response

@app.route('/table', methods=['GET'])
def table():
    data = Access.getCasesData()
    return data

if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True, port=8080)