import load_story, generate_html, windows, server
import os,time
import socket
import _thread


id_adr = socket.gethostbyname(socket.gethostname())


def sv(id_adr):
    print("New Thread server")
    server.run(id_adr)

def window(id_adr):
    windows.__init__(id_adr)


if os.path.exists("./anime_list/list.txt"):
    a = os.path.getatime("./anime_list/list.txt")
    b = time.time()

    print(time.ctime(a), time.ctime(b), time.ctime(b-a))

    print(a,b, b-a)
    update_time = 5
    update_time_sec = update_time * 60 * 60
    if b-a > update_time_sec:
        print("Out of date!  Load new Data")
        load_story.__init__()
else:
    load_story.__init__()
generate_html.__init__()

_thread.start_new_thread(sv, (id_adr,))
window(id_adr)
