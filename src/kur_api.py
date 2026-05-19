# The API service being used is "https://api.genelpara.com/"

import requests
import json

reqapi = "https://api.genelpara.com/json/?list=doviz,altin&sembol=USD,EUR,GA,C"  # data on dollar, euro, quarter gold and gram gold is being collected

def kur():
  headers  = {"User-Agent": "curl/8.5.0", "Accept": "*/*"}  # to avoid receiving a "403 Forbidden Error" and to prevent the service from mistaking the application for a bot, the request is sent as a curl request

  try:
    response = requests.get(reqapi, headers=headers)  # exchange rate data
    response.raise_for_status()
    json_data = response.json()
  except requests.exceptions.ConnectionError:   # it returns 1 if it cannot connect to the service
    return 1
  except requests.exceptions.Timeout:  # if the request times out, it will return 2
    return 2

  try:
    if response.status_code != 200:
        return "request invalid"

    data = json_data["data"]
    usd = data["USD"]   # example: usd["alis"], usd["satis"], usd["degisim"]
    eur = data["EUR"]   # example: eur["alis"], eur["satis"], eur["degisim"]
    ga  = data["GA"]     # example: ga["alis"], ga["satis"], ga["degisim"]
    ceyrek = data["C"]  # example: ceyrek["alis"], ceyrek["satis"], ceyrek["degisim"]

    return {
        'usd': usd,
        'eur': eur,
        'ga': ga,
        'ca': ceyrek
    }
  except Exception as e:
      return e

