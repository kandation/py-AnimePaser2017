import requests
from bs4 import BeautifulSoup
import json, os


list_path = "./misa/anime_list/"

def load_images(url, id):
    path = "./misa/cover/"
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

def id_paser(url):
    id = str(url).split("https://misa-anime.com/")[1].split("/")[0]
    return id

def save_to_file_story(path, data):
    try:
        os.makedirs(path)
    except:
        pass

    try:
        os.remove(path)
    except:
        pass

    fw = open(path+"list.txt" , mode="w", encoding='utf-8')
    content = json.dumps(data)
    fw.write(content)
    fw.close()


def get_story():
    couter_page = 1
    couter_all_anime = 0
    list = []
    while True:
        url_main = "https://misa-anime.com/main/"+str(couter_page)
        re = requests.get(url_main)
        soup_main = BeautifulSoup(re.text, "html.parser")
        grid = soup_main.find_all("div", class_="anime_grid")

        print(couter_page, url_main)

        for box in soup_main.find_all("div", class_="anime_grid"):
            link = box.find("a", class_="animsition-link")['href']
            id = id_paser(link)
            img = box.find("img", class_="img_anime")['src']
            title = str(box.find("div", class_="title_anime").text).strip()
            update = str(box.find("span", class_="ribbon").text).strip()
            couter_all_anime += 1
            data = {'title': title,
                    'link': link,
                    'img': img,
                    'update': update,
                    'id': id
                    }
            list.append(data)


        if len(grid) <= 0:
             break
        couter_page += 1
    print("Load summery Get all [ "+str(couter_page-1)+" ] pages and anime [ "+str(couter_all_anime)+" ] stories")

    save_to_file_story(list_path, list)


def openload_paser(url):
    return str(url).replace('https://oload.stream/embed/','https://openload.co/f/')


def load_story(url):
    #url_story = "https://misa-anime.com/1001/houseki-no-kuni/"
    url_story = url
    re = requests.get(url_story).text
    content = BeautifulSoup(re, "html.parser")
    content = content.find("div", id="content").find_all("a")
    story_pack = []
    for story in content:
        story_url = story['href']
        story_title = str(story.text).strip()
        res = requests.get(story_url).text
        player_content = BeautifulSoup(res, "html.parser")
        story_link = player_content.find("iframe", class_="embed-responsive-item")['src']
        if 'https://oload.stream/embed/' in story_link:
            story_link = openload_paser(story_link)
            story_title += " (openload)"
        if '/preview' in story_link:
            story_link = str(story_link).replace('/preview', '')
        story_data = {'link': story_link,
                      'title': story_title
                      }
        story_pack.append(story_data)
    return story_pack

def get_link_form_story():
    fo = open(list_path+"list.txt", encoding="utf-8")
    file_read = fo.read()
    fo.close()
    data = json.loads(file_read, encoding="utf-8")






def __init__():
    #get_story()
    get_link_form_story()
    print(load_story("https://misa-anime.com/1001/houseki-no-kuni/"))

__init__()

