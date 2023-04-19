import requests
from bs4 import BeautifulSoup
from bs4.element import Comment


def fetch_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error fetching {url}: status code {response.status_code}")
        return None


def extract_articles(html):
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

        extracted_data.append({
            "titles": [heading, heading2, heading3],
            "content": p,
            "images": img_src
        })

    return extracted_data


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(string=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


def main():
    # Replace with the target blog URL
    url = "https://www.clarin.com/deportes/jorge-almiron-sumo-segunda-derrota-metio-historia-boca-dato-negativo-maximo-responsable-_0_71g8LOtJ5A.html"
    html = fetch_html(url)

    # if html:
    #     text = text_from_html(html)
    #     print(f"Text: {text}")

    if html:
        articles_data = extract_articles(html)
        print("Articles:")
        for article_data in articles_data:
            print(f"Title: {article_data['titles']}")
            print(f"Content: {article_data['content']}")
            print(f"Image source: {article_data['images']}\n")


if __name__ == "__main__":
    main()
