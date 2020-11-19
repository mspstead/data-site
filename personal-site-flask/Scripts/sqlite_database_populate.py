import sqlite3
import sys
from Scripts.flickr_public_photos import Flickr_Grabber

def create_db(Database_Path):
    """Initialise SQLite database"""
    connection = None
    try:
        connection = sqlite3.connect(Database_Path)
        print("Connected to sqlite database at {} .".format(Database_Path))
        return connection
    except (sqlite3.OperationalError) as e:
        print('Connection failed: {}'.format(e))
        return connection

def create_map_photos_table(connection):

    map_photo_table = """CREATE TABLE IF NOT EXISTS MapPhotos (
        MapPhotoID INTEGER PRIMARY KEY,
        PhotoURL TEXT NOT NULL UNIQUE,
        DateTaken TEXT,
        Latitude REAL NOT NULL,
        Longitude REAL NOT NULL);
    """

    try:
        cursor = connection.cursor()
        cursor.execute(map_photo_table)
        return True, 'MapPhotos table created successfully'

    except:
        e = sys.exc_info()[0]
        return False, 'Failed execution: {}'.format(e)

def insert_map_photo(connection,photo):

    insert_photo_sql = '''INSERT INTO MapPhotos (PhotoURL,DateTaken,Latitude,Longitude)
                  VALUES(?,?,?,?) '''

    try:
        cursor = connection.cursor()
        cursor.execute(insert_photo_sql,photo)
        connection.commit()
        return cursor.lastrowid

    except sqlite3.IntegrityError as e:
        return -1


def run_custom_sql(connection,sql_script):

    try:
        cursor = connection.cursor()
        cursor.execute(sql_script)
        rows = cursor.fetchall()
        return rows
    except:
        e = sys.exc_info()[0]
        print('Failed to run query, {}'.format(e))
        return([])

def populate_with_flickr_photos(connection,flickr_API_KEY,flickr_user_id):

    flikr = Flickr_Grabber(flickr_API_KEY, flickr_user_id)
    photos = flikr.get_public_user_photos()

    for ph in photos:
        photo = (ph.get('url'), ph.get('dateTaken'), ph.get('lat'), ph.get('lon'))
        if None in photo:
            pass
        else:
            row_id = insert_map_photo(connection, photo)
            if row_id!=-1:
                print("INSERTED {} at row {}".format(photo,row_id))
            else:
                print("Photo {} already in database".format(photo))

def close_connection(connection):
    connection.close()

if __name__ == '__main__':

    database_path = '/Users/mike/Documents/Website/personal-site-flask/blog-site.db'
    flickr_API_KEY = "76ea06081c719ea20e95f2d608049fc2"
    flickr_user_id = "191088024@N02"

    conn = create_db(database_path)
    if conn is not None:

        table_created = create_map_photos_table(conn)

        if table_created[0]==True:
            populate_with_flickr_photos(conn,flickr_API_KEY,flickr_user_id)

        print(run_custom_sql(conn,"SELECT * FROM MapPhotos LIMIT 10"))
        close_connection(conn)








