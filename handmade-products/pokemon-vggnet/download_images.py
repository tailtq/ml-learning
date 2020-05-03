import os
import cv2
import requests
from requests import exceptions

subscription_key = '000460b0592148c986e27d35dcfd38a9'
search_url = 'https://api.cognitive.microsoft.com/bing/v7.0/images/search'
search_terms = ['gastly']
headers = {'Ocp-Apim-Subscription-Key': subscription_key}

MAX_RESULTS = 500
GROUP_SIZE = 50
EXCEPTIONS = {
    IOError,
    FileNotFoundError,
    exceptions.RequestException,
    exceptions.HTTPError,
    exceptions.ConnectionError,
    exceptions.Timeout
}

for term in search_terms:
    output = 'dataset/{}'.format(term)

    if not os.path.exists(output):
        os.mkdir(output)

    params = {'q': term, 'offset': 0, 'count': GROUP_SIZE}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    results = response.json()

    total = 0
    estNumResults = min(results['totalEstimatedMatches'], MAX_RESULTS)

    for offset in range(0, estNumResults, GROUP_SIZE):
        params['offset'] = offset
        search = requests.get(search_url, headers=headers, params=params)
        search.raise_for_status()
        results = search.json()

        for value in results['value']:
            try:
                result = requests.get(value['contentUrl'], timeout=30)
                extension = value['contentUrl'][value['contentUrl'].rfind('.'):]
                p = os.path.sep.join([output, '{}{}'.format(str(total).zfill(8), extension)])

                f = open(p, 'wb')
                f.write(result.content)
                f.close()

                image = cv2.imread(p)
                if image is None:
                    os.remove(p)
                    continue

                total += 1
            except Exception as e:
                if type(e) in EXCEPTIONS:
                    print('[INFO] skipping: {}'.format(value['contentUrl']))
                    continue
