from flask import Flask,request, render_template, jsonify, send_from_directory
import os
import zipfile
import uuid
import numpy as np
from utils.Log import Log
from utils.CleanDirectories import CleanDirectories
import shutil

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PROJECT_FOLDER = 'projects'
EXTRACT_FOLDER = 'extracted'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXTRACT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload-zip',methods=['POST'])
def uploadZip():
    #Check if both source zip and target zip are present
    if 'source' not in request.files or 'target' not in request.files:
        return jsonify({'success':False,'error':'Invalid Request'})
    project_id=str(uuid.uuid4())
    source_zip=request.files['source']
    target_zip=request.files['target']
    try:
        os.makedirs(os.path.join("projects",project_id),exist_ok=True)
        source_zip.save(os.path.join("projects",project_id,"source.zip"))
        target_zip.save(os.path.join("projects",project_id,"target.zip"))
        shutil.unpack_archive(f"projects/{project_id}/source.zip",f"projects/{project_id}/source")
        shutil.unpack_archive(f"projects/{project_id}/target.zip",f"projects/{project_id}/target")
        
        #remove the source zip files
        os.remove(f"projects/{project_id}/source.zip")
        os.remove(f"projects/{project_id}/target.zip")
        obj=CleanDirectories(project_id)

        #simulate test response
        res=[]
        return res
        #return jsonify({'success':True,'project_id':project_id})
    except Exception as e:
        Log("Error",str(e))
        return jsonify({'success':False,'error':'Error creating project folder'})



@app.route('/configure-faces')
def configFaces():
    target='faces/1.jpg'

    targets=['faces/1.jpg','faces/2.jpg','faces/3.jpg','faces/4.jpg','faces/5.jpg','faces/6.jpg']
    sources=['faces/4.jpg','faces/5.jpg','faces/6.jpg']
    x,w,y,h=[0,10,0,10]
    t_x,t_w,t_y,t_h=[0,10,0,10]

    res=[]
    for target in targets:
        srcs=[]
        for source in sources:
            src={
                "source":source,
                "x":x,
                "w":w,
                "y":y,
                "h":h,
            }
            srcs.append(src)
        obj={
            "target":target,
            "x":x,
            "w":w,
            "y":y,
            "h":h,
            "sources":srcs
        }
        res.append(obj)

    return jsonify({'Success':res})

@app.route('/<path:filename>')
def custom_static(filename):
    return send_from_directory('projects', filename)
    
if __name__ == '__main__':
    app.run(debug=True)
