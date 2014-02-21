from bottle import run, route, static_file, template
import os
import urllib2
import sqlite3

root = os.path.expanduser('~/Music')

conn = sqlite3.connect('data.db')

@route('/')
@route('/hello/<name>')
def home(name="stranger"):
    return "<h1>Hello ", name, "</h1>"

def link_to(name, path):
    if os.path.isdir(os.path.join(root, path)) == False:
        return ("/play/"+path, name)
    else:
        return ("/show/"+path, name)

def name(path):
    return os.path.basename(path)


def render(element):
    return link_to(name(element), element)

@route('/static/<path:path>')
def render_img(path):
    return static_file(path, root='/')

@route('/local/')
def show_local():
    albums = conn.execute("select artist, album, title, path, art_path from songs group by artist, album, title")
    return template('local', albums=albums)


@route('/show/')
@route('/show/<path:path>')
def show_dir(path=''):
    page = []
    full_path = urllib2.unquote(os.path.join(root, path))
    print '---------------------'
    print full_path
    print '---------------------'
    for content in os.listdir(full_path):
        page.append(render(os.path.join(path, content)))
    return template('show_template', page=page)

@route('/play/<path:path>')
def play_file(path):
    full_path = urllib2.unquote(os.path.join(root, path))
    file_name = name(path)
    print name(full_path), full_path
    return static_file(file_name, root=full_path.replace(file_name, ''))

if __name__ == "__main__":
    run(host='localhost', port=8080, debug=True)
