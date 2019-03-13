import requests
import pathlib
from readability import Document as ReadabilityDocument
from pylatex import Document, Section, Subsection, Subsubsection, Command
from pylatex.utils import NoEscape
from bs4 import BeautifulSoup


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
    doc = ReadabilityDocument(page)

    # return cleaned content
    return doc


def parse_content(content):
    # parse text using beautiful soup
    soup = BeautifulSoup(content, features='lxml')

    # return soup object
    return soup


def format_latex(title, soup):
    # create document
    doc = Document()

    # set preamble
    doc.preamble.append(Command('title', title))
    doc.append(NoEscape(r'\maketitle'))

    # get the main content body
    main_content = soup.body.find('div').find('div')

    # iterate over elements
    for ele in main_content.find_all(True):
        if ele.name == "h1":
            doc.append(Section(ele.text))
        elif ele.name == "h2":
            print(ele.text)
            doc.append(Subsection(ele.text))

    return doc


def build_latex(title, latex):
    # ensure build folder exists
    pathlib.Path('build').mkdir(exist_ok=True)

    # generate file name
    file_name = title.replace(" ", "-").lower()

    # generate tex and pdf files
    latex.generate_pdf('build/' + file_name, clean_tex=False)


url = 'https://www.jpattonassociates.com/dual-track-development/'
raw_content = get_page_contents(url)
cleaned_content = clean_page(raw_content)
soup = parse_content(cleaned_content.summary())
latex = format_latex(cleaned_content.title(), soup)
build_latex(cleaned_content.title(), latex)
