from bs4 import BeautifulSoup
from pylatex.utils import NoEscape
import requests
import pathlib
import shutil
from readability import Document as ReadabilityDocument
from pylatex import Document, Section, Subsection, Subsubsection, Command, Itemize, Enumerate, Figure
from pylatex.section import Paragraph, Subparagraph


USER_AGENT = 'Mozilla/5.0'


def get_page_contents(url):
    # emulate signature from browser to avoid 403
    headers = {'User-Agent': USER_AGENT}

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
    elements = main_content.find_all(True)

    # iterate over elements
    for ele in elements:
        if ele.name == 'h1':
            doc.append(Section(ele.text))
        elif ele.name == 'h2':
            doc.append(Subsection(ele.text))
        elif ele.name == 'h3':
            doc.append(Subsubsection(ele.text))
        elif ele.name == 'h4':
            doc.append(Paragraph(ele.text))
        elif ele.name == 'h5':
            doc.append(Subparagraph(ele.text))
        elif ele.name == 'p':
            doc.append(ele.text + '\n')
        elif ele.name == 'ul':
            with doc.create(Itemize()) as item:
                for li in ele.find_all('li'):
                    item.add_item(li.text)
        elif ele.name == 'ol':
            with doc.create(Enumerate()) as enum:
                for li in ele.find_all('li'):
                    enum.add_item(li.text)
        elif ele.name == 'img':
            with doc.create(Figure(position='h!')) as fig:
                # create tmp directory for images
                pathlib.Path('build/images').mkdir(parents=True, exist_ok=True)

                # check if source is using // shorthand for http://
                src = ele['src']
                if src.startswith('//'):
                    src = 'http:' + src

                # generate image path
                image_path = 'images/' + src.split('/')[-1]

                # retrieve image
                print('downloading image ' + src)
                headers = {'User-Agent': USER_AGENT}
                response = requests.get(src, stream=True,
                                        headers=headers)
                with open('build/' + image_path, 'wb') as f:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, f)

                # append image
                fig.add_image(image_path)

    return doc


def build_latex(title, latex):
    # ensure build folder exists
    pathlib.Path('build').mkdir(exist_ok=True)

    # generate file name
    file_name = title.replace(' ', '-').lower()

    # generate tex and pdf files
    print('compiling latex')
    latex.generate_pdf('build/' + file_name, clean_tex=False)


url = input('Please enter the full url of the website to format: \n')
raw_content = get_page_contents(url)
cleaned_content = clean_page(raw_content)
soup = parse_content(cleaned_content.summary())
latex = format_latex(cleaned_content.title(), soup)
build_latex(cleaned_content.title(), latex)
