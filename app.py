from flask import Flask
from flask import render_template
import requests
import os

from flask.logging import default_handler
TOKEN = os.getenv('TOKEN')

app = Flask(__name__)
app.logger.removeHandler(default_handler)

def get_project_id():
    url = "https://api.clo.ru/v1/projects"

    # defining a dict of headers to be sent to the API
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {TOKEN}'}

    # sending get request and saving the response as response object
    try:
        r = requests.get(url = url, headers = headers)

    except:
        app.logger.info( str(r.content ) )
        return -1
    return r.json()['results'][0]['id']

def get_servers(project_id):
    url = f"https://api.clo.ru/v1/projects/{project_id}/servers"

    # defining a dict of headers to be sent to the API
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {TOKEN}'}

    # sending get request and saving the response as response object
    try:
        r = requests.get(url = url, headers = headers)
        return r.json()['results']
    except:
        return -1

def get_image_list(project_id):
    url = f"https://api.clo.ru/v1/projects/{project_id}/images"

    # defining a dict of headers to be sent to the API
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {TOKEN}'}

    # sending get request and saving the response as response object
    r = requests.get(url = url, headers = headers)
    return r.json()['results']

def get_image_name(image_id):
    image_list=get_image_list()
    image_name='not found'
    for item in image_list:
        if item['id']==image_id:
            image_name=item['name']
    return image_name


def get_server_detail(server_id):
    url = f"https://api.clo.ru/v1/servers/{server_id}/detail"

    # defining a dict of headers to be sent to the API
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {TOKEN}'}

    # sending get request and saving the response as response object
    r = requests.get(url = url, headers = headers)
    app.logger.info( str(r.content ) )
    return r.json()['result']

@app.route("/")
def hello_world():
    project_id=get_project_id()
    servers=get_servers(project_id)
    image_list=get_image_list(project_id)
    image_list_dict={}
    servers_dict={}
    status_dict={'ACTIVE':'bg-success','BUILDING':'bg-warning','DELETING':'bg-danger','STOPPED':'bg-danger'}
    for item in servers:
        addresses=get_server_detail(item['id'] )['addresses']
        # servers_dict[item ['id']]=str(rez)
        ip=''
        for item2 in addresses:
            if item2['external']:
                ip=item2['name']
        servers_dict[item ['id'] ]={'ip':ip, 'bg_color': status_dict [item['status']]  }


    for item in image_list:
        if item['name'].lower().startswith('ubuntu'):
            img_src="https://img.icons8.com/color/48/000000/ubuntu--v1.png"
        elif  item['name'].lower().startswith('centos'):
            img_src="https://img.icons8.com/color/48/000000/centos.png"
        elif item['name'].lower().startswith('debian') :
            img_src="https://img.icons8.com/color/48/000000/debian.png"
        image_list_dict[item ['id'] ]={'name': item['name'], 'img_src':img_src}
    #return "<p>Hello, World!</p>"+str(servers)
    return render_template('index.html',servers=servers,image_list=image_list, image_list_dict=image_list_dict,servers_dict=servers_dict)
