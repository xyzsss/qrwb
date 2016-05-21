# qrwb
web qr generator


## Based on 
[CuteR](https://github.com/chinuno-usami/CuteR)

#### file list
init_dir.py    # init the directory
qr.py    # main file
qr.db    # sqlite datafile
template/qres.html    # the frontend file
template/qrres.html    # the 404 page file


#### 1. env requirement
```
apt-get install libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev
apt-get install python-dev Pillow
pip install CuteR
`which CuteR`   # change the CuteR path of the file 'qr.py'
pip install web.py
```

#### 2. database config
```
apt-get install sqlite3
cd /data
sqlite3 qr.db


CREATE TABLE todo ( 
id serial primary key, 
title text, 
content text,
filepath text,
created timestamp default CURRENT_TIMESTAMP ,
done boolean deault 'f' );

>.quit
```
 
 
#### 3. init images directory
`python init_dir.py`

#### 4. RUN
`python qr.py`
