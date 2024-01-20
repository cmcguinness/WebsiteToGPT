#
#   This is a standalone utility to get the lists of posts to a substack
#   I do not represent that:
#
#   * It works for any substack, not even mine (but it did when ran it)
#   * It won't make substack mad at you
#   * It captures everything you want
#
#   I include this as an example for how to get a list of documents in some sort
#   of library; you will undoubtedly need to do something different.
#
#   This is meant to be run once to generate the articles.csv file, and after that
#   the data I need is in that CSV file.  I suppose I could run it again every time
#   I add new articles to the substack. Or just update the CSV file by hand.
#

import requests
import json
import time


def get_article_urls(substack_name:str):

    index = 0
    f = open('articles.csv', 'w')

    while True:
        res = requests.get(f'https://{substack_name}/api/v1/archive?sort=new&search=&offset={index}&limit=12')
        if res.status_code != 200:
            print(f'Fetch error {res.status_code}')
            f.close()

        batch = json.loads(res.content)
        if len(batch) == 0:
            f.close()
            return

        for article in batch:
            f.write(f'"{article["title"]}",{article["canonical_url"]},"{article["post_date"]}","{article["description"]}"\n')

        index += 12
        time.sleep(1)

    return      # This code is unreachable...


if __name__ == '__main__':
    substack_name = "replace-me-with-something-like-mcguinnessai"
    get_article_urls(substack_name + '.substack.com')
    print("All Done!")
