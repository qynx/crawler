def convert_html_to_text(tag):
    '''
    @param tag: lxml html node: such as root.xpath('//div[@id="nr1"]')[0]
    '''
    content = tostring(tag, method="html", pretty_print=True, encoding="utf-8")
    content = content.decode("utf-8")
    content = content.replace("\xa0", "")
    content=content.replace("<br>", "")
    content=content.replace('<div id="nr1">', '')
    content=content.replace('</div>', "")
    return content