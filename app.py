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
        res={}
        return jsonify(res)
        #return jsonify({'success':True,'project_id':project_id})
    except Exception as e:
        Log("Error",str(e))
        return jsonify({'success':False,'error':'Error creating project folder'})

@app.route('/process',methods=['POST'])
def process():
    #extract json request
    data=request.json
    for img in data:
        face_path=img.face_path
        original=img.original
        source_path=img.source_path
        x=img.x
        xw=img.xw
        y=img.y
        yh=img.yh
    return jsonify(data)

@app.route('/<path:filename>')
def custom_static(filename):
    return send_from_directory('projects', filename)
    
if __name__ == '__main__':
    app.run(debug=True)
