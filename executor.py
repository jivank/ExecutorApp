from flask import Flask
import json
import os
import subprocess
import time
from os.path import isfile,join
app = Flask(__name__)
app.debug = True
active_processes = []

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
    for pr in active_processes:
        pr.poll()
    return app.send_static_file(path)

@app.route('/execute/<script>')
def execute(script):
    script = script.split('/')[-1]
    if script not in files(): return 'Error'
    active_processes.append((script,subprocess.Popen([get_mypath()+'/'+script],stdout=subprocess.PIPE)))

    active_processes[-1][1].been_read = False
    active_processes[-1][1].output = ''
    active_processes[-1][1].started = time.time()*1000
    return json.dumps({'pid':active_processes[-1][1].pid})

@app.route('/listing')
def listing():
    return json.dumps({'scripts':files()})

@app.route('/running')
def running():
    running = []
    for name,pr in active_processes:
        pr.poll()
        status = 'unknown'
        if pr.returncode is None:
            status = 'running'
        else:
            if pr.returncode == 0:
                status = 'done'
            elif pr.returncode == 1:
                status = 'error'
            elif pr.returncode < 0:
                status = 'killed'
            if not pr.been_read:
                for i in iter(pr.stdout.readline,''):
                    pr.output+= i+'\n'
        running.append({'name':name.split('/')[-1],
                        'status':status,
                        'output':pr.output,
                        'date':pr.started})
    return json.dumps(running)

def get_mypath():
    return os.getcwd() + '/scripts'

def files():
    mypath = get_mypath()
    return [f for f in os.listdir(mypath) if isfile(join(mypath,f))]

if __name__ == '__main__':
    app.run(host='0.0.0.0')
