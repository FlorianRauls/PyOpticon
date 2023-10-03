import psutil
import time
from flask import Flask, jsonify, request
from threading import Thread
import mysql.connector
import yaml

UPDATE_INTERVAL = 1

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def get_size(bytes):
    """
    Returns size of bytes in a nice format
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024
        
        
# get the network I/O stats from psutil
io = psutil.net_io_counters()
# extract the total bytes sent and received
bytes_sent, bytes_recv = io.bytes_sent, io.bytes_recv



def collectData(cursor):
    while True:
        time.sleep(UPDATE_INTERVAL)

        io_2 = psutil.net_io_counters()
        us, ds = io_2.bytes_sent - bytes_sent, io_2.bytes_recv - bytes_recv
        print(f"Upload: {get_size(io_2.bytes_sent)}   "
            f", Download: {get_size(io_2.bytes_recv)}   "
            f", Upload Speed: {get_size(us / UPDATE_INTERVAL)}/s   "
            f", Download Speed: {get_size(ds / UPDATE_INTERVAL)}/s      ", end="\r")

        bytes_sent, bytes_recv = io_2.bytes_sent, io_2.bytes_recv
        # insert data into database
        cursor.execute("INSERT INTO tracker (upload, download, upload_speed, download_speed) VALUES (%s, %s, %s, %s)", (get_size(io_2.bytes_sent), get_size(io_2.bytes_recv), get_size(us / UPDATE_INTERVAL), get_size(ds / UPDATE_INTERVAL)))
        
        cursor.execute("SHOW TABLES")
        
        for x in cursor:
            print(x, flush=True)

def run():
    app.run(debug=True, port=3000, host='0.0.0.0', useReloader=False)
    

if __name__ == "__main__":
    
    flaskThread = Thread(target=run)
    flaskThread.start()
    
    print("Doing Stuff...")
    
    app.secret_key = 'This'
    db_keys = yaml.load(open("db.yaml"),Loader=yaml.FullLoader)
    
    # connect to db
    db = mysql.connector.connect(
        host=db_keys['mysql_host'],
        user=db_keys['mysql_user'],
        password=db_keys['mysql_password']
        )
    
    # try and debug if anything works here lol
    mycursor = db.cursor()
    
    # create database table if it doesn't exist with the following columns (id, upload, download, upload_speed, download_speed)
    mycursor.execute("CREATE TABLE IF NOT EXISTS tracker (id INT AUTO_INCREMENT PRIMARY KEY, upload VARCHAR(255), download VARCHAR(255), upload_speed VARCHAR(255), download_speed VARCHAR(255))")
    
    
    # run collect data in new thread and pass in mysql cursor
    thread = Thread(target=collectData, args=(mycursor,))
   
    # start thread
    thread.start()
    