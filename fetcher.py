import requests

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def fetch_pubmed_ids(query: str):
    url = f"{BASE_URL}esearch.fcgi"
    params = {
        'db': 'pubmed',
        'term': query,
        'retmax': 10,
        'retmode': 'json'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data['esearchresult']['idlist']

def fetch_paper_details(pmid: str):
    url = f"{BASE_URL}efetch.fcgi"
    params = {
        'db': 'pubmed',
        'id': pmid,
        'retmode': 'xml'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.text