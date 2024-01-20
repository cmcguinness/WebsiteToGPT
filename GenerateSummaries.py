#
#   Generate Article Summaries of the substack posts
#


import csv
import openai
from GetContentsOfArticle import get_article_text

system_prompt = """
The user will give you the text of an article for you to summarize.

You will write a one paragraph summary of the article that describes the topics it is
discussing. Someone reading the summary should be able to decide if the article is
likely to answer the question they have or not

Try to keep the paragraphs as brief as possible, but no more than 8 sentences regardless.
"""
def get_summary(text):
    client = openai.OpenAI()
    print('Calling ChatGPT...', end='', flush=True)
    result = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": text
            }
        ],
        model="gpt-3.5-turbo-1106"
    )
    print('Done', flush=True)

    resp = result.choices[0].message.content

    return resp


def process_article(f, row):
    print(row[0][:16]+'  ', end='', flush=True)
    article = get_article_text(row[1])
    summary = get_summary(article)
    f.write('\n---\n\n')      # Horizontal rule
    f.write(f'## Article Title: {row[0]}\n')
    f.write(f'Article URL: [`{row[1]}`]({row[1]})\n\n')
    f.write('Article Summary:\n\n')
    lines = summary.splitlines()
    for l in lines:
        f.write(f'> {l}\n')

def process_articles(title):
    md = open('summaries.md','w')
    md.write(f'# Summaries of articles on {title}\n')
    first_row = True
    limit = 999
    with open('articles.csv','r') as f:
        cr = csv.reader(f)
        for row in cr:
            if first_row:
                first_row = False
                continue
            process_article(md, row)
            limit -= 1
            if limit == 0:
                return

if __name__ == "__main__":
    process_articles('McGuinness On AI Substack')




