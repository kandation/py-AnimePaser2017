import requests
from bs4 import BeautifulSoup
import os

def get_contents_by_id(id):
    lk = []
    urls = "http://neko-miku.com/"+str(id)
    re = requests.get(urls)
    print(urls)
    soup = BeautifulSoup(re.text, "html.parser")
    title_name = str(soup.find("title").text).split("ตอนที่")

    text = soup.find("div", class_="b1 well-sm")
    print(title_name[0])


    for link in text.find_all("a"):
        type = "none"
        n = link['href'].split("http://neko-miku.com/play/")[1].split("/")[0]
        url = "http://neko-miku.com/player/"+str(n)+"/"
        print(url)
        rea = requests.get(url)
        soups = BeautifulSoup(rea.text, "html.parser")
        title = link.text

        try:
            tt = soups.find("iframe")['src']
            type = "online"
        except:
            pass

        if type == "none":
            try:
                tt = soups.find("center").find("a")['href']
                print(">>",tt)
                type = "download"
            except:
                type = "other"

        if type == "online":
            if "openload" in tt:
                op_link = "https://openload.co/f/"+str(tt.split("embed/")[1])
                str_link = op_link
                title += " (openload)"
            else:
                str_link = tt
            data = {'name': title,
                    'url': str_link
                    }
            lk.append(data)
        elif type == "download":
            print(title, url, tt)
            data = {'name': title,
                    'url': tt
                    }
            lk.append(data)
        elif type == "other":
            data = {
                'name': title+" (Neko)",
                'url': url
            }
            lk.append(data)
    return lk



def __init__(id):
    path = "neko/list/" + str(id)
    try:
        os.makedirs(path)
    except:
        pass
    fw = open("./"+path+"/index.html", mode="w", encoding='utf-8')
    links = get_contents_by_id(id)
    content = "<!DOCTYPE html><html><head><title>anime</title><meta charset='utf-8' /></head><body>"
    for link in links:
        html = '<div><a href="'+link["url"]+'">'+str(link['name'])+'</a></div>'
        content += html
    content += "</body></html>"
    fw.write(content)

