FROM python:3.7

RUN apt-get update -qq 
RUN apt-get install latexmk texlive-latex-extra -y

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD ["python", "webtex.py"]
