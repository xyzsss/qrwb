#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# config __init__ content
#

import os
import web
import sqlite3
import urllib2
import imghdr
import datetime
import subprocess
import urlparse


urls = (
    '/', 'index',
    '/create', 'create'
)
con = sqlite3.connect('qr.db', check_same_thread=False)
cur = con.cursor()
render = web.template.render('templates/')


class index:

    def GET(self):
        todos = cur.execute('select * from todo;')
        return render.qres(todos)


class create:

    def __init__(self):
        self.down_path = os.getcwd() + "/static/images/downloads"
        self.trans_path = os.getcwd() + "/static/images/converts"
        self.cuter_bin = "/usr/local/bin/CuteR"

    def is_valid_url(self, url):
        parts = urlparse.urlsplit(url)
        if not parts.scheme or not parts.netloc:
            print "Not valid url string"
            raise web.seeother('/')
        else:
            return True

    def download_image_file(self, photo, filename=None):
        try:
            file_name = photo.split('/')[-1]
            u = urllib2.urlopen(photo)
            path_file_name = os.path.join(self.down_path, file_name)
            local_file = open(path_file_name, "wb")
            local_file.write(u.read())
            local_file.close()
            u.close()
            return path_file_name
        except urllib2.HTTPError:
            print("HTTPError-404")
            return False

    def is_image_type(self, file_name):
            pic_list = (
                'rgb', 'gif', 'pbm', 'pgm', 'ppm', 'tiff',
                'rast', 'xbm', 'jpeg', 'bmp', 'png')
            img_type = imghdr.what(file_name)
            if img_type in pic_list:
                return file_name
            else:
                new_file_name = datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")\
                    + ".unknow"
                new_path_file = os.path.join(self.down_path, new_file_name)
                os.rename(file_name, new_path_file)
                print "File not image types."
                return False

    def is_html_input_empty(self, title, content):
        if title == "" or content == "":
            todos = cur.execute('select * from todo;')
            return render.qrres(todos, res="empty")
        else:
            return False

    def insert_record_to_todo(self, file_name, title, content):
        output_file = self.trans_path + "/" +\
            datetime.datetime.now().strftime("%H-%M-%S") + ".png"
        command = [
            self.cuter_bin,
            '-C', '-r', '100', '50', '100']
        command.append(file_name)
        command.append(content)
        command.append("-o")
        command.append(output_file)
        filepath = "/static/images/converts/" + output_file.split('/')[-1]
        try:
            command_res = subprocess.call(command)
            if command_res != 0:
                print "conver fialed ."
            else:
                cur.execute(
                    """INSERT INTO todo (title, content, filepath) VALUES (?,?,?);""",
                    (title, content, filepath)
                )
                con.commit()
        except Exception:
            print "\nTrans failed\n"

    def POST(self):
        i = web.input()
        title = i.title.strip()
        content = i.content.strip()

        self.is_valid_url(title)
        if self.is_html_input_empty(title, content) is False:
            file_name = self.download_image_file(title)
            if self.is_image_type(file_name) is False:
                print "File type unknow ,keep file already!"
                raise web.seeother('/')
            self.insert_record_to_todo(file_name, title, content)
            raise web.seeother('/')


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
