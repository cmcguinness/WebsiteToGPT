#
#   This will extract the text from a substack article.
#
#   To be clear, it does the very least it could do to be passable.
#
#   In our context, where we're going to feed this text to GPT to
#   generate summaries, that's all we need to do.  If you have some
#   other use, it probably isn't all you need to do.
#
#   Also note that this is "tuned" (that is, I got it working good enough
#   for my purposes) to my style of substack article, it may not work well
#   for any other author's substack.
#

import requests
from bs4 import BeautifulSoup

def get_article_text(url: str):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    # title = soup.find(class_='post-title').text
    # subtitle = soup.find(class_='subtitle').text
    lines = []

    body = soup.find(class_='body')

    for ele in body:
        if ele.name == 'p':
            lines.append(ele.text)
        if ele.name == 'ol':
            point = 1
            for li in ele:
                lines.append(f'{point}.   {li.text}')
                point += 1
        if ele.name == 'ul':
            for li in ele:
                lines.append(f'*     {li.text}')

    return '\n'.join(lines)


if __name__ == "__main__":
    lines = get_article_text('https://mcguinnessai.substack.com/p/not-to-rag-on-next-year-but')
    print(lines)
