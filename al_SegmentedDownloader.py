import threading
#import click
import requests
import os

def Handler(start, end, url, filename):
    headerss = {'Range' : 'bytes=%d-%d' % (start,end)}
    r = requests.get(url, headers=headerss, stream=True)
    with open(filename, "r+b") as fp:
        fp.seek(start)
        var = fp.tell()
        fp.write(r.content)

def download_file():
    url_of_file  	=	 str(input("Enter URL: "))
    file_name	 	=	 str(input("Enter file name: "))
    no_of_threads	=	 int(input("Enter number of threads: "))

    r = requests.head(url_of_file)
    file_size = int(r.headers['content-length'])


    part =  int(file_size) // no_of_threads
    fp = open(file_name, "w")
    fp.write( '\0' * file_size)
    fp.close()


    for i in range(no_of_threads):
        start = i * part
        end = start + part
        t = threading.Thread(target=Handler,kwargs={'start':start, 'end':end, 'url':url_of_file, 'filename':file_name})
        t.setDaemon(True)
        t.start()

    main_thread = threading.current_thread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        t.join()

    print('File downloaded :)')

if __name__ == '__main__':
    download_file()

