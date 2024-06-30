from flask import Flask, request, jsonify
from drive import *
from youtube import *

app = Flask(__name__)

@app.route('/upload_video', methods=['POST'])
def upload_video_endpoint():
    data = request.get_json()
    file_id = data.get('file_id')
    file_name = "outputfile.mp4"
    title = data.get('title', 'Default Title')
    description = data.get('description', 'Default Description')
    
    download_file(file_id, file_name)
    upload_video(file_name, title, description)
    


    return jsonify({"status": "success", "file_name": file_name})

if __name__ == '__main__':
    app.run(debug=True)
