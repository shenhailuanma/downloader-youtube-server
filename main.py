from flask import Flask, request, jsonify
import subprocess
import json

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)

        return_code = result.returncode
        stdout = result.stdout
        stderr = result.stderr
        
        return return_code, stdout, stderr
    except Exception as e:
        return -1, "", str(e)


app = Flask(__name__)

try:
    with open('config.json', 'r') as file:
        config_data = json.load(file)
except FileNotFoundError:
    config_data = {"proxy":""}

app.config.update(config_data)

print("load config, proxy:", app.config['proxy'])

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# get video info
@app.route("/api/v1/youtube/video/info")
def get_video_info():
    video_url = request.args.get('video')
    if not video_url:
        return jsonify({"error": "no video url", "code": 400}), 400
    
    # to get video info by use yt-dlp
    command = f"yt-dlp --dump-json '{video_url}'"
    if app.config['proxy']:
        command += f" --proxy {app.config['proxy']}"


    print(f"command: {command}")
    response_data = {}

    return_code, stdout, stderr = run_command(command)
    print(f"return_code: {return_code}")
    # print(f"stdout:\n{stdout}")
    # print(f"stderr:\n{stderr}")
    if return_code != 0:
        return jsonify(response_data), 400

    video_data =  json.loads(stdout)

    
    response_data['id'] = video_data['id']
    response_data['title'] = video_data['title']
    response_data['channel_id'] = video_data['channel_id']
    response_data['channel_url'] = video_data['channel_url']
    response_data['ext'] = video_data['ext']

    
    return jsonify(response_data)

# get channel video list info
@app.route("/api/v1/youtube/channel/info")
def get_channel_info():
    channel = request.args.get('channel')
    if not channel:
        return jsonify({"error": "no video channel", "code": 400}), 400
    
    # to get channel info by use yt-dlp
    command = f"yt-dlp --flat-playlist --dump-json '{channel}'"
    if app.config['proxy']:
        command += f" --proxy {app.config['proxy']}"


    print(f"command: {command}")
    response_data = []

    return_code, stdout, stderr = run_command(command)
    print(f"return_code: {return_code}")
    # print(f"stdout:\n{stdout}")
    # print(f"stderr:\n{stderr}")
    if return_code != 0:
        return jsonify(response_data), 400


    lines = stdout.splitlines()
    for line in lines:
        print("line:", line)
        video_data =  json.loads(line)
        response_data_one = {}
        response_data_one['id'] = video_data['id']
        response_data_one['title'] = video_data['title']
        response_data_one['url'] = video_data['url']

        response_data.append(response_data_one)

    
    return jsonify(response_data), 200


# download video
@app.route("/api/v1/youtube/video/download")
def download_video():
    video_url = request.args.get('video')
    if not video_url:
        return jsonify({"error": "no video url", "code": 400}), 400
    dest = request.args.get('dest')
    if not dest:
        return jsonify({"error": "no dest", "code": 400}), 400
    
    # to download video by use yt-dlp
    command = f"yt-dlp '{video_url}' -o '{dest}'"
    if app.config['proxy']:
        command += f" --proxy {app.config['proxy']}"


    print(f"command: {command}")

    response_data = {}

    return_code, stdout, stderr = run_command(command)
    print(f"return_code: {return_code}")
    if return_code != 0:
        return jsonify(response_data), 400

    return jsonify(response_data), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=15000)