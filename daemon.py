import boto
import functools
import sys
import pyinotify
import argparse
import os
from boto.s3.key import Key

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
BUCKET_NAME = 'hwatcher-bucket'

def setup_arg_parser():
    parser = argparse.ArgumentParser(description='Create a daemon that watches the given directory and the stores the pid of the newly created subprocess in the given pid file')
    parser.add_argument('-pid', help='The file to store the pid, this file should NOT exist before calling.')
    parser.add_argument('-dir', help='The directory to watch.')
    return parser

def upload_to_s3(filepath):
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(BUCKET_NAME)
    bucket_key = Key(bucket)
    bucket_key.key = os.path.basename(filepath)
    bucket_key.set_contents_from_filename(filepath)

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CLOSE_WRITE(self, event):        
        upload_to_s3(event.pathname)

if __name__ == '__main__':
    ## parse cmd arguments
    parser = setup_arg_parser()
    args = parser.parse_args()
    pid_file_path = args.pid
    watch_dir = args.dir    

    ## create watcher and notifier
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, EventHandler())
    wm.add_watch(watch_dir, pyinotify.IN_CLOSE_WRITE)
    
    ## start notifier
    notifier.loop(daemonize=True, pid_file=pid_file_path)

