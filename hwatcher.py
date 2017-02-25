import subprocess
import argparse
import json
import os
import random
import subprocess

############################################

daemons_file_path = '/tmp/hwatcher_daemons_list.hw'

def load_daemons_list():
    if (os.path.isfile(daemons_file_path)):
        with open(daemons_file_path, 'r') as daemons_file:
            return json.loads(daemons_file.read())
    return {}

def save_daemons_list(daemons_list):
    with open(daemons_file_path, 'w') as daemons_file:
        daemons_file.write(json.dumps(daemons_list))

############################################

def generate_pid_file():
    return '/tmp/hwatcher'+ str(int(random.random()*10e10)) +'.pid'

def generate_watcher_id(daemons):
    rand_id = str(int(random.random()*10e10))
    while (rand_id in daemons):
        rand_id = str(int(random.random()*10e10))
    return rand_id

def wait_for_pid_file(pid_file):
    while (not os.path.isfile(pid_file)):
        continue

def read_pid(pid_file):
    with open(pid_file, 'r') as pid_contents:
        pid = pid_contents.read().strip('\n')
        return pid

def create_daemon(pid_file, work_dir):
    subprocess.call(['python', 'daemon.py',
                    '-pid', pid_file,
                    '-dir', work_dir])

def start_watcher(dir_to_watch):
    pid_file = generate_pid_file()
    create_daemon(pid_file, dir_to_watch)
    wait_for_pid_file(pid_file)
    pid = read_pid(pid_file)
    os.remove(pid_file)
    return pid

def kill_watcher(pid):
    return subprocess.check_output(['kill', '-9', pid])

############################################

# start a new daemon
def start_func(args):
    print 'Starting a new hwather to watch', args.dir
    if (not os.path.isdir(args.dir)):
        print args.dir, 'is not found, can\'t create a watcher on a non-existing dir.'
        return
    daemons = load_daemons_list()
    pid = start_watcher(args.dir)
    wid = generate_watcher_id(daemons)
    daemons[wid] = {'wid': wid, 'pid': pid, 'dir': args.dir}
    save_daemons_list(daemons)
    print 'Done, a new watcher with id', wid, 'has been created.'

# kill an existing daemon
def kill_func(args):
    print 'Killing watcher with id', args.wid
    daemons = load_daemons_list()
    if (not args.wid in daemons):
        print 'Can\'t find watcher with id', args.wid, '.'
        return
    kill_watcher(daemons[args.wid]['pid'])
    del daemons[args.wid]
    save_daemons_list(daemons)
    print 'Watcher with id', args.wid, 'has been killed.'

# list all daemons
def list_func(args):
    daemons = load_daemons_list()
    for daemon in daemons.values():
        print daemon['wid'] + '\t' + daemon['dir']

############################################

def setup_arg_parser():
    parser = argparse.ArgumentParser(description='hwatcher manage daemons for watching directories')
    subparsers = parser.add_subparsers()
    
    ## subparser - start
    parser_start = subparsers.add_parser('start')
    parser_start.add_argument('-dir')
    parser_start.set_defaults(func=start_func)
    
    ## subparser - kill
    parser_kill = subparsers.add_parser('kill')
    parser_kill.add_argument('-wid')
    parser_kill.set_defaults(func=kill_func)
    
    ## subparser - list
    parser_list = subparsers.add_parser('list')
    parser_list.set_defaults(func=list_func)

    return parser

if __name__ == '__main__':
    parser = setup_arg_parser()
    args = parser.parse_args()
    args.func(args)

