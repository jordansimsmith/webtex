import requests
from readability import Document


def get_page_contents(url):
    # emulate signature from browser to avoid 403
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

    # request the website contents
    response = requests.get(url, headers=headers)

    # return text
    return response.text


def clean_page(page):
    # parse text into readability document
    doc = Document(page)

    # return cleaned text
    return doc.summary()


url = 'https://www.jpattonassociates.com/dual-track-development/'
raw_content = get_page_contents(url)
cleaned_content = clean_page(raw_content)

print(cleaned_content)
