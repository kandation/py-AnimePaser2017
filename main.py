import load_story, generate_html, windows, server
import os,time

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
server.run()
windows.__init__()
