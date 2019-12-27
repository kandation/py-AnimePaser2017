import requests
from bs4 import BeautifulSoup
import json, os, time


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
    return path+str(id)+".jpg"

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

    fw = open(path+"index.html" , mode="w", encoding='utf-8')
    content = json.dumps(data)
    fw.write(content)
    fw.close()


def text_clean_link(id):
    return "./misa/story/"+str(id)


def get_story():
    if is_shoud_load("./misa/anime_list/index.html", 5):
        load_content()
    data = load_json_story()
    generate_html_from_json(data)

def load_content():
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
            link = text_clean_link(id)
            img = box.find("img", class_="img_anime")['src']
            title = str(box.find("div", class_="title_anime").text).strip()
            update = str(box.find("span", class_="ribbon").text).strip()
            update = text_clean_update(update)
            img_local = load_images(img, id)
            couter_all_anime += 1
            data = {'title': title,
                    'link': link,
                    'img': img,
                    'img_local': img_local,
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


def has_file(path):
    if os.path.exists(path):
        return True
    else:
        return False


def is_update(path, hour):
    a = os.path.getatime(path)
    b = time.time()
    print(time.ctime(a), time.ctime(b), time.ctime(b - a))

    print(a, b, b - a)
    update_time = hour
    update_time_sec = update_time * 60 * 60 *60
    if b - a > update_time_sec:
        print("Out of date!")
        return False
    else:
        print("Up to date")
        return True


def is_shoud_load(path, hour):
    if has_file(path):
        if not is_update(path, hour):
            return True
        else:
            return False
    else:
        return True


def load_story(url):
    #url_story = "https://misa-anime.com/1001/houseki-no-kuni/"
    print("Load Story from:", url)
    url_story = url
    re = requests.get(url_story).text
    content = BeautifulSoup(re, "html.parser")
    story_pack = []
    try:
        content = content.find("div", id="content").find_all("a")
        for story in content:
            story_url = story['href']
            story_title = str(story.text).strip()
            story_link = load_story_player(story_url)[0]
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
    except:
        story_link = load_story_player(url)
        if 'https://oload.stream/embed/' in story_link:
            story_link = openload_paser(story_link)
            story_title += " (openload)"
        if '/preview' in story_link:
            story_link = str(story_link).replace('/preview', '')
        story_data = {'link': story_link[0],
                      'title': story_link[1]
                      }
        story_pack.append(story_data)
    return story_pack



def load_story_player(story_url):
    res = requests.get(story_url).text
    player_content = BeautifulSoup(res, "html.parser")
    story_link = player_content.find("iframe", class_="embed-responsive-item")['src']
    return [story_link,player_content.find("title").text]


def load_story_by_id(id):
    url_story = "https://misa-anime.com/"+str(id)+"/"
    return load_story(url_story)


def generate_story_in_html(id):
    now_path = "./misa/story/" + str(id) + "/index.html"
    if is_shoud_load(now_path, 5):
        print("I think we should download new story data")
        data = load_story_by_id(id)
        generate_html_story_from_list(data, now_path)

def generate_html_story_from_list(data, path):
    print("Generate Story Html")
    try:
        os.makedirs(str(path).replace("index.html",""))
    except:
        pass
    fw = open(path, mode="w", encoding='utf-8')
    content = "<!DOCTYPE html><html><head><title>Story</title><meta charset='utf-8' /></head><body>"
    for box in data:
        html = '<div><a href="' + box["link"] + '">' + str(box['title']) + '</a></div>'
        content += html
    content += "</body></html>"
    fw.write(content)
    fw.close()


def generate_html_from_json(data):
    print("Generate Html")
    fw = open("./index.html", mode="w", encoding='utf-8')
    content = "<!DOCTYPE html><html><head><title>anime</title><meta charset='utf-8' /></head><body>"
    for box in data:
        ani_box = '<div style="float:left;width:150px;">' \
                  '<a href="' + box['link'] + '"><img src="' + box["img_local"] + '" width="150px" height="220px" title="' + \
                  box["title"] + '"/></a><div style="height:120px">' + box["title"] + '</div></div>'

        content += ani_box
    content += "</body></html>"

    fw.write(content)

def load_json_story():
    fo = open(list_path+"index.html", encoding="utf-8")
    file_read = fo.read()
    fo.close()
    data = json.loads(file_read, encoding="utf-8")
    return data


def text_clean_update(time_str):
    t = str(time_str).replace("อัพเดตเมื่อ ","").replace("ที่แล้ว", "")
    time_mul = 1
    timer = 0
    timer_prefix = ["ปี", "เดือน", "วัน", "ชั่วโมง", "นาที"]
    time_to_sec = [60,60,24,30,12]

    return_time = []

    for i,k in enumerate(timer_prefix):
        if k in t:
            timer = int(str(t).replace(k, "").strip())
            for s in range(0, i+1):
                time_mul *= time_to_sec[s]
            return_time = [timer, k]

    # return timer*time_mul
    return return_time


def __init__ ():
    os.chdir(os.path.abspath(__file__))
    get_story()

