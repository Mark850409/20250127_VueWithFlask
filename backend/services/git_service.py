from models.git import GitStatus, GitCommit
from git_operations import GitOperations
from typing import List, Optional

class GitService:
    _instance = None
    _git_ops = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GitService, cls).__new__(cls)
        return cls._instance

    def init_repo(self, path: str):
        """初始化或獲取已存在的倉庫"""
        if not self._git_ops:
            self._git_ops = GitOperations(path)
        try:
            self._git_ops.init_repo()
        except Exception as e:
            if "已經是一個 Git 倉庫" in str(e):
                # 如果已經是 Git 倉庫，就直接使用
                pass
            else:
                raise e

    def _ensure_git_ops(self) -> GitOperations:
        """確保 git_ops 存在，如果不存在則拋出異常"""
        if not self._git_ops:
            raise Exception('請先初始化倉庫')
        return self._git_ops

    def check_status(self) -> Optional[GitStatus]:
        """檢查 Git 狀態，如果倉庫未初始化則返回 None"""
        try:
            if not self._git_ops:
                print("Git ops not initialized")  # 添加日誌
                return None
            
            status = self._git_ops.check_status()
            print("Got status from git_ops:", status)  # 添加日誌
            return status
        
        except Exception as e:
            print("Error in service check_status:", str(e))  # 添加日誌
            if '請先初始化倉庫' in str(e):
                return None
            raise e

    def add_files(self):
        git_ops = self._ensure_git_ops()
        git_ops.add_files()

    def commit(self, message: str):
        git_ops = self._ensure_git_ops()
        git_ops.commit(message)

    def create_branch(self, name: str):
        git_ops = self._ensure_git_ops()
        git_ops.create_branch(name)

    def switch_branch(self, name: str):
        git_ops = self._ensure_git_ops()
        git_ops.switch_branch(name)

    def configure(self, name: str, email: str):
        git_ops = self._ensure_git_ops()
        git_ops.configure(name, email)

    def add_remote(self, name: str, url: str):
        git_ops = self._ensure_git_ops()
        git_ops.add_remote(name, url)

    def push(self, remote: str, branch: str, force: bool = False):
        git_ops = self._ensure_git_ops()
        git_ops.push(remote, branch, force)

    def get_commits(self) -> List[GitCommit]:
        git_ops = self._ensure_git_ops()
        return git_ops.get_commit_history()

    def reset_commit(self, commit_hash: str, mode: str = 'hard') -> str:
        git_ops = self._ensure_git_ops()
        return git_ops.reset_to_commit(commit_hash, mode)

    def pull(self, remote: str = 'origin', branch: str = 'master') -> str:
        git_ops = self._ensure_git_ops()
        return git_ops.pull(remote, branch)

    def get_current_path(self) -> Optional[str]:
        """獲取當前倉庫路徑"""
        return self._git_ops.path if self._git_ops else None 