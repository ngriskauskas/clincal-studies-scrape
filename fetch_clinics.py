import requests
import json
from pprint import pprint
def fetch_all_pages(url, params, num_pages):
    all_data = []
    page = 1
    while page <= num_pages:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Error: Failed to fetch data from API. Status code: {response.status_code}")
            break
        data = json.loads(response.text)
        all_data.extend(data['studies'])
        if 'nextPageToken' not in data:
            break
        params['pageToken'] = data['nextPageToken']
        page += 1
    print(f"Number of Pages Fetched: {page}")
    return all_data


def get_unique_orgs(data):
    unique_orgs = set()
    for study in data:
        org_name = study['protocolSection']['identificationModule']['organization']['fullName']
        unique_orgs.add(org_name)
    return unique_orgs

url = 'https://clinicaltrials.gov/api/v2/studies'
query_params = {'filter.geo': 'distance(38.634841,-90.439453,50mi)', 'filter.overallStatus': [ 'RECRUITING' ]}
all_data = fetch_all_pages(url, query_params, 50)



unique_orgs = get_unique_orgs(all_data)
pprint(unique_orgs)
print(f"Total Number of Clinics:  {len(unique_orgs)}")

# print(json.dumps(all_data, indent=1))
