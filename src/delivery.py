ects/youtube-monitor $ 
(venv) daniel@raspberrypi:~/projects/youtube-monitor $ 
(venv) daniel@raspberrypi:~/projects/youtube-monitor $ 
(venv) daniel@raspberrypi:~/projects/youtube-monitor $ 
(venv) daniel@raspberrypi:~/projects/youtube-monitor $ git fetch origin
git reset --hard origin/master
remote: Enumerating objects: 7, done.
remote: Counting objects: 100% (7/7), done.
remote: Compressing objects: 100% (4/4), done.
remote: Total 4 (delta 2), reused 0 (delta 0), pack-reused 0 (from 0)
Unpacking objects: 100% (4/4), 1.14 KiB | 390.00 KiB/s, done.
From https://github.com/thedza49/youtube-monitor
   70c9491..4d192f9  master     -> origin/master
HEAD is now at 4d192f9 Update fetcher.py
(venv) daniel@raspberrypi:~/projects/youtube-monitor $ 
(venv) daniel@raspberrypi:~/projects/youtube-monitor $ 
(venv) daniel@raspberrypi:~/projects/youtube-monitor $ python3 src/main.py
Traceback (most recent call last):
  File "/home/daniel/projects/youtube-monitor/src/main.py", line 6, in <module>
    from delivery import TelegramDelivery
ImportError: cannot import name 'TelegramDelivery' from 'delivery' (/home/daniel/projects/youtube-monitor/src/delivery.py)
(venv) daniel@raspberrypi:~/projects/youtube-monitor $ 
(venv) daniel@raspberrypi:~/projects/youtube-monitor $ 
