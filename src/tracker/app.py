import psutil
import time
from flask import Flask, jsonify, request
from threading import Thread
import mysql.connector
import yaml
import time

# how often to update the database in seconds
UPDATE_INTERVAL = 60

if __name__ == "__main__":
    db_keys = yaml.load(open("db.yaml"),Loader=yaml.FullLoader)
    
    # connect to db
    db = mysql.connector.connect(
        host=db_keys['mysql_host'],
        user=db_keys['mysql_user'],
        password=db_keys['mysql_password'],
        port="3306",
        database="tracker"
        )
    
    # try and debug if anything works here lol
    mycursor = db.cursor()
    
    # create first table
    create_table_command = """CREATE TABLE IF NOT EXISTS tracking (
                                T datetime NOT NULL, 
                                Upload_speed float, 
                                Download_speed float, 
                                Memory_usage float, 
                                Cpu_usage float, 
                                Uptime int, 
                                Readtime float, 
                                Writetime float);"""
                                    
    # create database table if it doesn't exist with the following columns (id, timestamp, upload, download, upload_speed, download_speed)
    mycursor.execute(create_table_command)
    mycursor.execute("commit")

    # create table if it doesn't exist which records processes and their cpu usage and memory usage over time
    create_table_command = """CREATE TABLE IF NOT EXISTS processes (
                                T datetime NOT NULL, 
                                Name varchar(255), 
                                Memory_usage float, 
                                Cpu_usage float);"""    
    
    mycursor.execute(create_table_command)
    mycursor.execute("commit")
    
    # counter for io
    io = psutil.net_io_counters()
    bytes_sent, bytes_recv = io.bytes_sent, io.bytes_recv
    
    
    while True:
        time.sleep(UPDATE_INTERVAL)
        
        # get current datetime
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')

        # get network usage
        io_2 = psutil.net_io_counters()
        us, ds = io_2.bytes_sent - bytes_sent, io_2.bytes_recv - bytes_recv
        bytes_sent, bytes_recv = io_2.bytes_sent, io_2.bytes_recv

        # get memory percentage
        memory_percent = psutil.virtual_memory().percent
        
        # get cpu usage
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # get uptime
        boot_time_timestamp = psutil.boot_time()
        current_time_timestamp = time.time()
        uptime_seconds = current_time_timestamp - boot_time_timestamp
        
        # get readtime and writetime
        io_counters = psutil.disk_io_counters()
        readtime = io_counters.read_time
        writetime = io_counters.write_time
                
        # string to insert values into database
        sql = """INSERT INTO tracking 
                (T, Download_speed, Upload_speed, Memory_usage, Cpu_usage, Uptime, Readtime, Writetime) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        values =  (current_time, (ds / UPDATE_INTERVAL), (us / UPDATE_INTERVAL), memory_percent, cpu_percent, uptime_seconds, readtime, writetime)
        
        mycursor.execute(sql, values)  
        mycursor.execute("commit")
        
        # get processes
        processes = psutil.process_iter()
        
        # loop through processes
        for process in processes:
            # get process name
            name = process.name()
            
            # get process memory usage
            memory_usage = process.memory_percent()
            
            # get process cpu usage
            cpu_usage = process.cpu_percent()
            
            # string to insert values into database
            sql_2 = """INSERT INTO processes 
                    (T, Name, Memory_usage, Cpu_usage) 
                    VALUES (%s, %s, %s, %s, %s)"""
            values_2 =  (current_time, name, memory_usage, cpu_usage)
            
            mycursor.execute(sql_2, values_2)  
            mycursor.execute("commit")
        
        
        