import requests
from bs4 import BeautifulSoup
import pprint, json, os


def load_images(url, id):
    path = "./neko/cover/"
    if not os.path.exists(path+str(id)+".jpg"):
        re = requests.get(url, stream=True)
        if re.status_code == 200:
            try:
                os.makedirs(path)
            except:
                pass
            print("Get images", id)
            with open(path+str(id)+".jpg", 'wb') as f:
                for chunk in re:
                    f.write(chunk)


def get_anime_contianer(start, stop):
    anime_list = []
    print("Get anime Contianer")
    for k in range(start, stop):
        url_main = "http://neko-miku.com/catalog/18/&number="+str(k)
        re = requests.get(url_main)
        soup = BeautifulSoup(re.text, "html.parser")
        div_container = soup.find_all("div", class_="center_lnwphp")
        for content in div_container:
            c = content.find("a")
            name = c['title']
            link = c['href']
            img = c.find('img')['src']
            id = str(link).split("http://neko-miku.com/")[1].split("/")[0]
            link = "/neko/" + str(id)
            load_images(img, id)
            anime_box = {'name': name,
                         'link': link,
                         'img': "./neko/cover/"+str(id)+".jpg"
                         }
            anime_list.append(anime_box)
    print("Get anime contianer Finish")
    return anime_list


def get_anime_list(stop):
    list = get_anime_contianer(1,stop)
    list = json.dumps(list)

    try:
        os.mkdir("./anime_list")
    except:
        pass
    fw = open("./anime_list/list.txt", mode="w", encoding="utf-8")
    fw.write(list)
    fw.close()


def __init__():
    get_anime_list(48)