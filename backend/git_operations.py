import git
import os

class GitOperations:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.repo = None

    def init_repo(self):
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)
        
        if not os.path.exists(os.path.join(self.repo_path, '.git')):
            self.repo = git.Repo.init(self.repo_path)
        else:
            self.repo = git.Repo(self.repo_path)

    def check_status(self):
        if not self.repo:
            raise Exception("倉庫未初始化")
        
        status = self.repo.git.status()
        return status

    def add_files(self):
        if not self.repo:
            raise Exception("倉庫未初始化")
        
        self.repo.git.add('.')

    def commit(self, message):
        if not self.repo:
            raise Exception("倉庫未初始化")
        
        self.repo.index.commit(message)

    def create_branch(self, branch_name):
        if not self.repo:
            raise Exception("倉庫未初始化")
        
        current = self.repo.create_head(branch_name)
        current.checkout()

    def switch_branch(self, branch_name):
        if not self.repo:
            raise Exception("倉庫未初始化")
        
        self.repo.git.checkout(branch_name)

    def configure(self, name, email):
        if not self.repo:
            raise Exception("倉庫未初始化")
        
        with self.repo.config_writer() as git_config:
            git_config.set_value('user', 'name', name)
            git_config.set_value('user', 'email', email)

    def add_remote(self, name, url):
        if not self.repo:
            raise Exception("倉庫未初始化")
        try:
            self.repo.create_remote(name, url)
        except Exception as e:
            if "remote {} already exists".format(name) in str(e):
                self.repo.delete_remote(name)
                self.repo.create_remote(name, url)

    def push(self, remote_name='origin', branch='master'):
        if not self.repo:
            raise Exception("倉庫未初始化")
        
        try:
            remote = self.repo.remote(name=remote_name)
            if not remote:
                raise Exception(f"遠程倉庫 {remote_name} 不存在")
            
            if not self.repo.heads:
                raise Exception("沒有可推送的提交")
            
            remote.push(refspec=f'refs/heads/{branch}:refs/heads/{branch}')
        except git.exc.GitCommandError as e:
            if "Permission denied" in str(e):
                raise Exception("推送被拒絕：權限不足，請檢查認證信息")
            elif "rejected" in str(e):
                raise Exception("推送被拒絕：請先拉取最新更改")
            else:
                raise Exception(f"推送失敗：{str(e)}")

    def get_commit_history(self):
        if not self.repo:
            raise Exception("倉庫未初始化")
        
        commits = []
        for commit in self.repo.iter_commits():
            commits.append({
                'hash': commit.hexsha[:7],
                'message': commit.message,
                'author': f"{commit.author.name} <{commit.author.email}>",
                'date': commit.committed_datetime.strftime('%Y-%m-%d %H:%M:%S')
            })
        return commits

    def reset_to_commit(self, commit_hash, mode='hard'):
        if not self.repo:
            raise Exception("倉庫未初始化")
        
        try:
            # 先執行reset
            self.repo.git.reset('--' + mode, commit_hash)
            
            # 清理未追蹤的文件
            if mode == 'hard':
                # 獲取所有未追蹤的文件
                untracked_files = self.repo.untracked_files
                # 刪除未追蹤的文件
                for file_path in untracked_files:
                    full_path = os.path.join(self.repo_path, file_path)
                    if os.path.exists(full_path):
                        os.remove(full_path)
                
                # 清理空目錄
                for root, dirs, files in os.walk(self.repo_path, topdown=False):
                    for name in dirs:
                        try:
                            dir_path = os.path.join(root, name)
                            if not os.listdir(dir_path):  # 如果目錄為空
                                os.rmdir(dir_path)
                        except:
                            pass
            
            return f"成功回退到提交 {commit_hash}"
        except git.exc.GitCommandError as e:
            raise Exception(f"版本回退失敗：{str(e)}") 