import requests

def fetch_api_data():

    url = "https://api.deskbee.io/api/bookings/me?page=1&limit=50&search=type:%3Bsearch:%3Bperiod:%3Bfilter:&include=service%3Brecurrences%3Bmeeting%3Bcalendar_integration%3Bis_extend%3Bresources%3Bcheckin%3Btype%3Bparking%3Btolerance%3Breason%3Bparent"

    payload = {}
    headers = {
    'authority': 'api.deskbee.io',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9,pt;q=0.8',
    'authorization': f'Bearer {input("Enter your bearer token: ")}',
    'cache-control': 'no-cache',
    'origin': 'https://objectedge.deskbee.app',
    'pragma': 'no-cache',
    'referer': 'https://objectedge.deskbee.app/',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'x-app-account': 'objectedge',
    'x-app-version': '1.149.2718'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.text
