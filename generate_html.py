import json

def __init__():
    fo = open("./anime_list/list.txt", mode="r", encoding='utf-8')
    lists = fo.read()

    lists = json.loads(lists, encoding='utf-8')
    fw = open("./index.html", mode="w", encoding='utf-8')
    content = "<!DOCTYPE html><html><head><title>anime</title><meta charset='utf-8' /></head><body>"

    for box in lists:
        ani_box = '<div style="float:left;width:150px;">' \
                  '<a href="'+box['link']+'"><img src="'+box["img"]+'" width="150px" height="220px" title="'+box["name"]+'"/></a></div>'
        content += ani_box
    content += "</body></html>"

    fw.write(content)
