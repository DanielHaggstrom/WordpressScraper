from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

# Colocar las URLs adecuadas y escoger nombre del archivo

starting_url = "poner URL inicial aquí"
ending_url = "aquí va la URL final"

name = "Nombre de nuestro archivo"


# parte sobre obtener url

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


# parte para obtener siguiente capitulo

def getNextUrl(url):
    current_url = url
    raw_html = simple_get(current_url)
    html = BeautifulSoup(raw_html, 'html.parser')
    for link in html.find_all('link', {'rel': 'next'}):
        current_url = link.get('href')
        return current_url


# parte para obtener el cuerpo y titulo de un capitulo

def getChapter(url):
    raw_html = simple_get(url)
    html = BeautifulSoup(raw_html, 'html.parser')
    div_content = html.find("div", {"class": "entry-content"})
    text = ""
    for p in div_content.find_all('p'):
        text = text + str(p)

    title = str(html.find("h1", {"class": "entry-title"}))
    chapter = title + '\n' + text
    return chapter


# codigo
current_url = starting_url

finished = False

f = open(name, "a+", encoding="utf-8")

while not finished:

    print(current_url)
    f.write(getChapter(current_url))
    if current_url == ending_url:
        finished = True
    else:
        current_url = getNextUrl(current_url)

f.close()
print("Done!")