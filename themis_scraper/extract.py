def extract(soup, tag_id):
    tags = soup.find_all(id=tag_id)
    if len(tags) > 1:
        return tags[1].text.strip()
    else:
        return 'None'
