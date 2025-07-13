import os
import boto3
from flask import Flask, request, jsonify

app = Flask(__name__)

s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name=os.environ.get('AWS_REGION', 'ap-southeast-1')
)
BUCKET = os.environ.get('S3_BUCKET', 'pht-flaskapp-bucket')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    s3.upload_fileobj(file, BUCKET, file.filename)
    return jsonify({'message': 'Upload successful', 'filename': file.filename})

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    s3.download_file(BUCKET, filename, filename)
    return jsonify({'message': f'Downloaded {filename}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
