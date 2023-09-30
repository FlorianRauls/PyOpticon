import psutil
import time
from flask import Flask, jsonify, request

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


# while True:
    # sleep for `UPDATE_DELAY` seconds
    #time.sleep(UPDATE_INTERVAL)
    # get the stats again
    #io_2 = psutil.net_io_counters()
    # new - old stats gets us the speed
    #us, ds = io_2.bytes_sent - bytes_sent, io_2.bytes_recv - bytes_recv
    # print the total download/upload along with current speeds
    #print(f"Upload: {get_size(io_2.bytes_sent)}   "
     #     f", Download: {get_size(io_2.bytes_recv)}   "
      #    f", Upload Speed: {get_size(us / UPDATE_INTERVAL)}/s   "
       #   f", Download Speed: {get_size(ds / UPDATE_INTERVAL)}/s      ", end="\r")
    # update the bytes_sent and bytes_recv for next iteration
    #bytes_sent, bytes_recv = io_2.bytes_sent, io_2.bytes_recv

if __name__ == "__main__":
    app.run(debug=True, port=3000, host='0.0.0.0')