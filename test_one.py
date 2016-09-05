#import required libraries
import requests, json, hmac, hashlib, datetime, base64, os
import pprint
#credentials and endpoint
f = open('config.txt','r')
token = f.readline()[:-1]
secret = f.readline()[:-1]
endpoint = f.readline()

f.close()
#specific api call
api_path = '/api/order/validate'

#sign the request
timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(timestamp)
string_to_sign = 'POST' + ' ' + api_path + ' ' + timestamp
print(string_to_sign)
signature = hmac.new(str.encode(secret), str.encode(string_to_sign), hashlib.sha1).hexdigest()
oneflow_auth = token + ':' + signature

headers = { 'content-type': 'application/json',
            'x-oneflow-authorization': oneflow_auth,
            'x-oneflow-date': timestamp }
data = '''{
  "destination": {
    "name": "pureprint"
  },
  "orderData": {
    "sourceOrderId": "42",
    "items": [
      {
        "shipmentindex": "42",
        "sourceItemId": "123",
        "sku": "IGO-BK-LON-HM-SB",
        "quantity": 1,
        "components": [
          {
            "code": "text",
            "path": "https://oneflow-public.s3.amazonaws.com/CardSample.pdf",
            "fetch": true
          },
          {
            "code": "cover",
            "path": "https://oneflow-public.s3.amazonaws.com/CardSample.pdf",
            "fetch": true
          }
        ]
      }
    ],
    "shipments": [
      {
        "shipTo": {
          "name": "Nigel Watson",
          "companyName": "OneFlow Systems",
          "address1": "1 Primrose Street",
          "town": "London",
          "postcode": "EC2A 4EX",
          "isoCountry": "GB",
          "email": "info@oneflowsystems.com",
          "phone": "02037074173"
        },
        "carrier": {
          "alias": "domesticstandardigo"
        }
      }
    ]
  }
}'''
#read in the orderdata from the file, this could be constructed inside the app
# order=open('order.json','r').read()
# data = json.dumps(order)

#make the POST request to the endpoint
r = requests.post(endpoint + api_path, data, headers=headers)
pp = pprint.PrettyPrinter(width=150)
#output the results
print(r.content)