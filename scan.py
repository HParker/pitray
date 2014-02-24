# take a directory and find all the media in it and put it in a db.
import os
import sqlite3
import eyed3

conn = sqlite3.connect('data.db')

def insert(item_path, art_path='None'):

    if item_path.endswith('.mp3') or item_path.endswith('.mp4'):
        file_info = eyed3.load(item_path)
        try:
            conn.execute("INSERT INTO songs (title, artist, album, path, art_path) VALUES (?,?,?,?,?)",
                     (file_info.tag.title,
                      file_info.tag.artist,
                      file_info.tag.album,
                      item_path,
                      art_path))
            conn.commit()
        except:
            print "TROUBLE WITH", item_path



def scan(directory):
    print "scanning", directory

    if os.path.isdir(directory) and 'itunes' not in directory:
        art_path = [os.path.join(directory, art) for art in os.listdir(directory) if art.endswith('.jpg') or art.endswith('.png')]
        print art_path
        for item in os.listdir(directory):
            full_path = os.path.join(directory, item)
            if os.path.isdir(full_path):
                scan(full_path)
            else:
                if art_path:
                    insert(full_path, art_path[0])
                else:
                    insert(full_path)


if __name__ == "__main__":
    root = os.path.expanduser('~/Music')
    scan(root)
