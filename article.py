from newspaper import Article
from newspaper import ArticleException

def get_text(url):
    '''
    mengambil text yang ada pada suatu web (input parameter berupa URL)
    '''
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text.replace('\n', ' ').replace('\n\n', '\n')

    except ArticleException:
        return ''
    

