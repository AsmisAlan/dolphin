import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
from modules.web_scrapping.beautiful_soup.domain.beautiful_soup_configuration import BeautifulSoupConfiguration
from modules.web_scrapping.beautiful_soup.domain.beautiful_soup_data import BeautifulSoupInput, BeautifulSoupOutput


def _fetch_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error fetching {url}: status code {response.status_code}")
        return None


def extract_articles(url):
    html = _fetch_html(url)

    soup = BeautifulSoup(html, "html.parser")
    articles = soup.find_all("article")

    extracted_data = []
    for article in articles:
        heading = article.find("h1").text if article.find("h1") else None
        heading2 = article.find("h2").text if article.find("h2") else None
        heading3 = article.find("h3").text if article.find("h3") else None

        # Adjust the selector based on the actual HTML structure
        p = article.find_all("p")

        # get images
        img_src = article.find("img")["src"] if article.find("img") else None

        # append pre formatted
        pre = article.find("pre").text if article.find("pre") else None

        extracted_data.append({
            "titles": [heading, heading2, heading3],
            "content": p,
            "images": img_src,
            "preformated": pre
        })
    return extracted_data


def _tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'meta', '[document]', 'button', 'input', 'select', 'textarea', 'iframe']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def _to_raw_text(url):
    html = _fetch_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    texts = soup.findAll(string=True)
    visible_texts = filter(_tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


def scrap_pages(configuration: BeautifulSoupConfiguration, input: BeautifulSoupInput) -> BeautifulSoupOutput:
    output = BeautifulSoupOutput(urlsContent=[])
    for url in input.urls:
        try:
            print(f"Scrapping {url} (Running)")
            text = _to_raw_text(url)
            print(f"Scrapping {url} (Completed)")
            output.urlsContent.append((url, text))
        except Exception as e:
            print(f"Scrapping {url} (Failed)")
    return output


if __name__ == "__main__":
    # Get the data from the page
    configuration = BeautifulSoupConfiguration(max_results=10)
    inputs = BeautifulSoupInput(urls=["https://betterprogramming.pub/autoscraper-and-flask-create-an-api-from-any-website-in-less-than-5-minutes-3f0f176fc4a3",
                                      "https://stackoverflow.com/questions/62240421/the-correct-way-to-load-and-read-json-file-contains-special-characters-in-python"])

    result = scrap_pages(configuration, inputs)

    print(f"Text: {result}")
