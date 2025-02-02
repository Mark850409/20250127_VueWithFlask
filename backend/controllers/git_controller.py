from flask_openapi3 import APIBlueprint, Tag
from services.git_service import GitService
from schemas.git_schema import (
    GitInitRequest,
    GitConfigRequest,
    GitCommitRequest,
    GitBranchRequest,
    GitRemoteRequest,
    GitPushRequest,
    GitResetRequest,
    GitPullRequest,
    ErrorResponse
)
git_bp = APIBlueprint('git', __name__)
git_tag = Tag(name='git', description='Git 操作')

@git_bp.post('/api/init', tags=[git_tag])
def init_repo(body: GitInitRequest):
    """初始化 Git 倉庫"""
    service = GitService()
    try:
        service.init_repo(body.path)
        return {'message': f'成功初始化倉庫於 {body.path}'}
    except Exception as e:
        return {'message': f'初始化倉庫失敗: {str(e)}'}, 500

@git_bp.get('/api/status', tags=[git_tag])
def check_status():
    """檢查 Git 狀態"""
    service = GitService()
    try:
        status = service.check_status()
        print("Status from service:", status)
        
        if status is None:
            return {'message': '倉庫尚未初始化'}, 404
            
        # 構建類似 git status 命令輸出的格式
        status_message = []
        status_message.append(f"On branch {status.branch}")
        
        if not any([status.untracked, status.modified, status.staged]):
            status_message.append("\nNothing to commit, working tree clean")
        else:
            if status.staged:
                status_message.append("\nChanges to be committed:")
                for file in status.staged:
                    status_message.append(f"\tmodified: {file}")
                    
            if status.modified:
                status_message.append("\nChanges not staged for commit:")
                for file in status.modified:
                    status_message.append(f"\tmodified: {file}")
                    
            if status.untracked:
                status_message.append("\nUntracked files:")
                for file in status.untracked:
                    status_message.append(f"\t{file}")
        
        return {
            'message': '\n'.join(status_message)
        }
        
    except Exception as e:
        print("Error in check_status:", str(e))
        return ErrorResponse(message=str(e)).dict(), 500

@git_bp.post('/api/add', tags=[git_tag])
def add_files():
    """添加文件到暫存區"""
    service = GitService()
    try:
        service.add_files()
        return {'message': '成功添加文件到暫存區'}
    except Exception as e:
        return {'message': f'添加文件失敗: {str(e)}'}, 500

@git_bp.post('/api/commit', tags=[git_tag])
def commit(body: GitCommitRequest):
    """提交更改"""
    service = GitService()
    try:
        service.commit(body.message)
        return {'message': '成功提交更改'}
    except Exception as e:
        return {'message': f'提交失敗: {str(e)}'}, 500

@git_bp.post('/api/branch/create', tags=[git_tag])
def create_branch(body: GitBranchRequest):
    """創建分支"""
    service = GitService()
    try:
        service.create_branch(body.name)
        return {'message': f'成功創建分支 {body.name}'}
    except Exception as e:
        return ErrorResponse(message=str(e)).dict(), 500

@git_bp.post('/api/branch/switch', tags=[git_tag])
def switch_branch(body: GitBranchRequest):
    """切換分支"""
    service = GitService()
    try:
        service.switch_branch(body.name)
        return {'message': f'成功切換到分支 {body.name}'}
    except Exception as e:
        return ErrorResponse(message=str(e)).dict(), 500

@git_bp.post('/api/config', tags=[git_tag])
def configure_git(body: GitConfigRequest):
    """配置 Git"""
    service = GitService()
    try:
        service.configure(body.name, body.email)
        return {'message': '成功更新 Git 配置'}
    except Exception as e:
        return ErrorResponse(message=str(e)).dict(), 500

@git_bp.post('/api/remote/add', tags=[git_tag])
def add_remote(body: GitRemoteRequest):
    """添加遠程倉庫"""
    service = GitService()
    try:
        service.add_remote(body.name, body.url)
        return {'message': f'成功添加遠程倉庫 {body.name}'}
    except Exception as e:
        return ErrorResponse(message=str(e)).dict(), 500

@git_bp.get('/api/commits', tags=[git_tag])
def get_commits():
    """獲取提交歷史"""
    service = GitService()
    try:
        commits = service.get_commits()
        # 直接返回提交列表，不需要額外的轉換
        return {'commits': commits}  # 原始格式就是字典列表
    except Exception as e:
        return ErrorResponse(message=f'獲取提交歷史失敗: {str(e)}').dict(), 500

@git_bp.post('/api/reset', tags=[git_tag])
def reset_commit(body: GitResetRequest):
    """版本回退"""
    service = GitService()
    try:
        message = service.reset_commit(body.hash, body.mode)
        return {'message': message}
    except Exception as e:
        return ErrorResponse(message=f'版本回退失敗: {str(e)}').dict(), 500

@git_bp.post('/api/pull', tags=[git_tag])
def pull(body: GitPullRequest):
    """拉取遠程更新"""
    service = GitService()
    try:
        message = service.pull(body.remote, body.branch)
        return {'message': message}
    except Exception as e:
        error_message = str(e)
        if "衝突" in error_message:
            return {'message': f'拉取失敗: {error_message}'}, 409
        else:
            return {'message': f'拉取失敗: {error_message}'}, 500

@git_bp.post('/api/push', tags=[git_tag])
def push(body: GitPushRequest):
    """推送到遠程倉庫"""
    service = GitService()
    try:
        service.push(body.remote, body.branch, body.force)
        return {'message': f'成功推送到遠程倉庫 {body.remote}/{body.branch}'}
    except Exception as e:
        error_message = str(e)
        if "認證" in error_message or "權限" in error_message:
            return {'message': f'推送失敗: {error_message}. 請確保已配置正確的認證信息'}, 401
        elif "拒絕" in error_message:
            return {'message': f'推送失敗: {error_message}'}, 409
        else:
            return {'message': f'推送失敗: {error_message}'}, 500