from flask import Flask, request, jsonify
from flask_cors import CORS
from git_operations import GitOperations
import os

app = Flask(__name__)
CORS(app)

git_ops = None

@app.route('/init', methods=['POST'])
def init_repo():
    global git_ops
    data = request.json
    path = data.get('path')
    
    if not path:
        return jsonify({'message': '請提供有效的倉庫路徑'}), 400
    
    try:
        git_ops = GitOperations(path)
        git_ops.init_repo()
        return jsonify({'message': f'成功初始化倉庫於 {path}'})
    except Exception as e:
        return jsonify({'message': f'初始化倉庫失敗: {str(e)}'}), 500

@app.route('/status', methods=['GET'])
def check_status():
    if not git_ops:
        return jsonify({'message': '請先初始化倉庫'}), 400
    
    try:
        status = git_ops.check_status()
        return jsonify({'message': status})
    except Exception as e:
        return jsonify({'message': f'獲取狀態失敗: {str(e)}'}), 500

@app.route('/add', methods=['POST'])
def add_files():
    if not git_ops:
        return jsonify({'message': '請先初始化倉庫'}), 400
    
    try:
        git_ops.add_files()
        return jsonify({'message': '成功添加文件到暫存區'})
    except Exception as e:
        return jsonify({'message': f'添加文件失敗: {str(e)}'}), 500

@app.route('/commit', methods=['POST'])
def commit():
    if not git_ops:
        return jsonify({'message': '請先初始化倉庫'}), 400
    
    data = request.json
    message = data.get('message')
    
    if not message:
        return jsonify({'message': '請提供提交信息'}), 400
    
    try:
        git_ops.commit(message)
        return jsonify({'message': '成功提交更改'})
    except Exception as e:
        return jsonify({'message': f'提交失敗: {str(e)}'}), 500

@app.route('/branch/create', methods=['POST'])
def create_branch():
    if not git_ops:
        return jsonify({'message': '請先初始化倉庫'}), 400
    
    data = request.json
    name = data.get('name')
    
    if not name:
        return jsonify({'message': '請提供分支名稱'}), 400
    
    try:
        git_ops.create_branch(name)
        return jsonify({'message': f'成功創建分支 {name}'})
    except Exception as e:
        return jsonify({'message': f'創建分支失敗: {str(e)}'}), 500

@app.route('/branch/switch', methods=['POST'])
def switch_branch():
    if not git_ops:
        return jsonify({'message': '請先初始化倉庫'}), 400
    
    data = request.json
    name = data.get('name')
    
    if not name:
        return jsonify({'message': '請提供分支名稱'}), 400
    
    try:
        git_ops.switch_branch(name)
        return jsonify({'message': f'成功切換到分支 {name}'})
    except Exception as e:
        return jsonify({'message': f'切換分支失敗: {str(e)}'}), 500

@app.route('/config', methods=['POST'])
def configure_git():
    if not git_ops:
        return jsonify({'message': '請先初始化倉庫'}), 400
    
    data = request.json
    name = data.get('name')
    email = data.get('email')
    
    if not name or not email:
        return jsonify({'message': '請提供用戶名和郵箱'}), 400
    
    try:
        git_ops.configure(name, email)
        return jsonify({'message': '成功更新 Git 配置'})
    except Exception as e:
        return jsonify({'message': f'配置更新失敗: {str(e)}'}), 500

@app.route('/remote/add', methods=['POST'])
def add_remote():
    if not git_ops:
        return jsonify({'message': '請先初始化倉庫'}), 400
    
    data = request.json
    name = data.get('name', 'origin')
    url = data.get('url')
    
    if not url:
        return jsonify({'message': '請提供遠程倉庫URL'}), 400
    
    try:
        git_ops.add_remote(name, url)
        return jsonify({'message': f'成功添加遠程倉庫 {name}'})
    except Exception as e:
        return jsonify({'message': f'添加遠程倉庫失敗: {str(e)}'}), 500

@app.route('/push', methods=['POST'])
def push():
    if not git_ops:
        return jsonify({'message': '請先初始化倉庫'}), 400
    
    data = request.json
    if not data:
        return jsonify({'message': '無效的請求數據'}), 400
    
    remote = data.get('remote', 'origin')
    branch = data.get('branch', 'master')
    
    try:
        git_ops.push(remote, branch)
        return jsonify({'message': f'成功推送到遠程倉庫 {remote}/{branch}'})
    except Exception as e:
        error_message = str(e)
        if "認證" in error_message or "權限" in error_message:
            return jsonify({'message': f'推送失敗: {error_message}. 請確保已配置正確的認證信息'}), 401
        elif "拒絕" in error_message:
            return jsonify({'message': f'推送失敗: {error_message}. 請先拉取並合併遠程更改'}), 409
        else:
            return jsonify({'message': f'推送失敗: {error_message}'}), 500

if __name__ == '__main__':
    app.run(debug=True) 