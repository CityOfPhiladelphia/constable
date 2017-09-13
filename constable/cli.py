import os
import multiprocessing
import socket

import click
import requests
import gunicorn.app.base
from gunicorn.six import iteritems
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .app import app
from .models import db
from .worker import run as run_worker

class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

def get_worker_id():
    worker_components = []

    ## AWS
    try:
        response = requests.get('http://169.254.169.254/latest/meta-data/instance-id', timeout=0.1)
        if response.status_code == 200:
            worker_components.append(response.text)
    except:
        pass

    ## ECS (AWS Batch uses ECS as well)
    try:
        response = requests.get('http://172.17.0.1:51678/v1/tasks', timeout=0.1)
        if response.status_code == 200:
            tasks = response.json()['Tasks']
            short_docker_id = os.getenv('HOSTNAME', None) ## ECS marks the short docker id as the HOSTNAME
            if short_docker_id != None:
                matched = list(filter(
                    lambda ecs_task: ecs_task['Containers'][0]['DockerId'][0:12] == short_docker_id,
                    tasks))
                if len(matched) > 0:
                    worker_components.append(matched[0]['Containers'][0]['Arn'])
    except:
        pass

    ## fallback to IP
    if len(worker_components) == 0:
        return socket.gethostbyname(socket.gethostname())
    else:
        return '-'.join(worker_components)

@click.group()
def main():
    pass

def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1

@main.command()
@click.option('--bind-host', default='0.0.0.0')
@click.option('--bind-port', default='5000', type=int)
@click.option('--worker-class', default='sync')
@click.option('--prod', is_flag=True, default=False)
def server(bind_host, bind_port, worker_class, prod):
    if prod:
        options = {
            'bind': '{}:{}'.format(bind_host, bind_port),
            'workers': number_of_workers(),
            'worker_class': worker_class
        }
        StandaloneApplication(app, options).run()
    else:
        app.run(host=bind_host, port=bind_port)

@main.command()
@click.option('--sql-alchemy-connection')
def init_db(sql_alchemy_connection):
    connection_string = sql_alchemy_connection or os.getenv('SQLALCHEMY_DATABASE_URI')

    engine = create_engine(connection_string)

    db.Model.metadata.create_all(engine)

@main.command()
@click.option('--sql-alchemy-connection')
@click.option('--worker-id')
def worker(sql_alchemy_connection, worker_id):
    connection_string = sql_alchemy_connection or os.getenv('SQLALCHEMY_DATABASE_URI')

    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    session = Session()

    worker_id = worker_id or get_worker_id()

    ## TODO: consumption rate
    ## TODO: loop

    run_worker(session, worker_id)
