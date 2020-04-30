import requests, shutil
from io import BytesIO
import numpy as np

class Access:
    @staticmethod
    def __deathGrowth(countries, nDays):
        endPoint = "https://corona.lmao.ninja/v2/historical/%s?lastdays=%d" % (countries, nDays + 1)
        request = requests.get(endPoint)
        countriesParse = request.json()

        days = list(countriesParse[0]["timeline"]["deaths"].keys())[1:]
        daysFormatted = [Access.__formatDate(d) for d in days]
        growth = {"days": daysFormatted, "deaths":[]}

        for c in countriesParse:
            today = np.array(list(c["timeline"]["deaths"].values())[1:])
            yesterday = np.array(list(c["timeline"]["deaths"].values())[:-1])
            growthCountry = (today/yesterday - 1) * 100
            growth["deaths"].append({"country": c["country"], "growth": growthCountry.tolist()})
        return growth

    @staticmethod
    def getDeathGrowthChart():
        data = Access.__deathGrowth("Brazil, USA, Spain, China", 30)
        json={"x": [], "y": [], "labels": []}

        for d in data["deaths"]:
            json["x"].append(data["days"])
            json["y"].append(d["growth"])
            json["labels"].append(d["country"])
        
        # endPoint = "http://chartapi-env.eba-cppqupxx.us-east-1.elasticbeanstalk.com/plot/line"
        endPoint = "http://localhost:8000/plot/line"
        r = requests.post(endPoint, json=json, stream=True)
        buffer = BytesIO()
        shutil.copyfileobj(r.raw, buffer)
        return buffer.getvalue()

    @staticmethod
    def __formatDate(date):
        dateSplit = date.split("/")
        return "%s/%s" % (dateSplit[1], dateSplit[0])
    
    @staticmethod
    def getCasesData():
        endPoint = "https://disease.sh/v2/countries"
        request = requests.get(endPoint)
        countriesParse = request.json()

        data = {"countries": [], "recovered": [], "deaths": [], "casesPerMillion": []}

        for c in countriesParse:
            data["countries"].append(c["country"])
            data["recovered"].append(c["recovered"])
            data["deaths"].append(c["deaths"])
            data["casesPerMillion"].append(c["casesPerOneMillion"])
        
        return data