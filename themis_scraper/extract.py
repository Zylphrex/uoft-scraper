import html
import unicodedata

def extract(soup, tag_id):
    tags = soup.find_all(id=tag_id)
    if len(tags) > 0:
        unescaped = html.unescape(tags[1].text).strip()
        return unicodedata.normalize('NFKD', unescaped).encode('ascii','ignore').decode('ascii')
    else:
        return 'None'
