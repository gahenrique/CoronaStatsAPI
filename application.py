from flask import Flask, request, make_response, abort
from service import Access

app = Flask(__name__)

@app.route("/")
def home():
    return "Corona App API. Use the endpoint /chart to get the chart of the growth on different countries and /table to get a list of cases"

@app.route('/chart', methods=['GET'])
def chart():
    if not request.args:
        abort(400)

    reqKeys = request.args.keys()
    countries = ""

    if "country1" in reqKeys:
        countries += request.args["country1"]
    if "country2" in reqKeys:
        countries += ", " + request.args["country2"]
    if "country3" in reqKeys:
        countries += ", " + request.args["country3"]
    if "country4" in reqKeys:
        countries += "," + request.args["country4"]
    
    chartImg = Access.getDeathGrowthChart(countries)
    response = make_response(chartImg)
    response.headers.set('Content-Type', 'image/png')
    return response

@app.route('/table', methods=['GET'])
def table():
    data = Access.getCasesData()
    return data

if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True, port=8000)
    