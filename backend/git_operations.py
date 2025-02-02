import git
import os
from models.git import GitStatus

class GitOperations:
    def __init__(self, repo_path):
        self.path = repo_path
        self.repo = None

    def init_repo(self):
        """初始化 Git 倉庫"""
        try:
            print(f"Initializing repo at path: {self.path}")
            
            # 確保目錄存在
            if not os.path.exists(self.path):
                print(f"Creating directory: {self.path}")
                os.makedirs(self.path)
            
            # 檢查是否已經是 Git 倉庫
            if not os.path.exists(os.path.join(self.path, '.git')):
                print("Initializing new git repository...")
                self.repo = git.Repo.init(self.path)
                
                # 配置 Git 用戶信息
                self.repo.config_writer().set_value("user", "name", "System").release()
                self.repo.config_writer().set_value("user", "email", "system@example.com").release()
                
                # 創建初始提交
                print("Creating initial commit...")
                # 創建一個 README 文件
                readme_path = os.path.join(self.path, 'README.md')
                if not os.path.exists(readme_path):
                    with open(readme_path, 'w') as f:
                        f.write('# Git Repository\nInitialized by system.')
                
                # 添加並提交
                self.repo.index.add(['README.md'])
                self.repo.index.commit("Initial commit")
                print("Initial commit created")
            else:
                print("Loading existing repository...")
                self.repo = git.Repo(self.path)
            
            return self.repo
        except Exception as e:
            print(f"Error initializing repository: {str(e)}")
            raise Exception(f"初始化 Git 倉庫失敗：{str(e)}")

    def check_status(self) -> GitStatus:
        """檢查 Git 狀態"""
        try:
            print(f"Checking repo at path: {self.path}")
            if not self.repo:
                try:
                    print("Initializing repo object...")
                    self.repo = git.Repo(self.path)
                except git.exc.InvalidGitRepositoryError as e:
                    print(f"Invalid git repository: {str(e)}")
                    raise Exception("不是有效的 Git 倉庫")
            
            print("Getting branch info...")
            try:
                branch = self.repo.active_branch.name
                print(f"Current branch: {branch}")
            except (TypeError, AttributeError) as e:
                print(f"Error getting branch: {str(e)}")
                branch = 'HEAD detached'
            
            # 獲取未追蹤的文件
            untracked = list(self.repo.untracked_files)
            
            # 獲取已修改的文件
            modified = []
            if self.repo.head.is_valid():
                try:
                    modified = [item.a_path for item in self.repo.index.diff(None)]
                except Exception as e:
                    print(f"Error getting modified files: {e}")
            
            # 獲取已暫存的文件
            staged = []
            if self.repo.head.is_valid():
                try:
                    staged = [item.a_path for item in self.repo.index.diff('HEAD')]
                except Exception as e:
                    print(f"Error getting staged files: {e}")
            
            return GitStatus(
                untracked=untracked,
                modified=modified,
                staged=staged,
                branch=branch
            )
        except Exception as e:
            raise Exception(f"獲取 Git 狀態失敗：{str(e)}")

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

    def push(self, remote_name='origin', branch='master', force=False):
        if not self.repo:
            raise Exception("倉庫未初始化")
        
        try:
            remote = self.repo.remote(name=remote_name)
            if not remote:
                raise Exception(f"遠程倉庫 {remote_name} 不存在")
            
            if not self.repo.heads:
                raise Exception("沒有可推送的提交")
            
            # 添加強制推送選項
            if force:
                remote.push(refspec=f'refs/heads/{branch}:refs/heads/{branch}', force=True)
            else:
                remote.push(refspec=f'refs/heads/{branch}:refs/heads/{branch}')
            
        except git.exc.GitCommandError as e:
            if "Permission denied" in str(e):
                raise Exception("推送被拒絕：權限不足，請檢查認證信息")
            elif "rejected" in str(e):
                raise Exception("推送被拒絕：請先拉取最新更改或使用強制推送")
            else:
                raise Exception(f"推送失敗：{str(e)}")

    def get_commit_history(self):
        if not self.repo:
            raise Exception("倉庫未初始化")
        
        commits = []
        for commit in self.repo.iter_commits():
            commits.append({
                'hash': commit.hexsha[:7],
                'message': commit.message.replace('\n', '\n'),  # 保留原始換行
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
                    full_path = os.path.join(self.path, file_path)
                    if os.path.exists(full_path):
                        os.remove(full_path)
                
                # 清理空目錄
                for root, dirs, files in os.walk(self.path, topdown=False):
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

    def pull(self, remote_name='origin', branch='master'):
        if not self.repo:
            raise Exception("倉庫未初始化")
        
        try:
            remote = self.repo.remote(name=remote_name)
            if not remote:
                raise Exception(f"遠程倉庫 {remote_name} 不存在")
            
            # 先獲取遠程更新
            remote.fetch()
            
            # 檢查是否有衝突
            if self.repo.is_dirty():
                raise Exception("有未提交的更改，請先提交或暫存更改")
            
            # 執行拉取
            remote.pull(branch)
            return f"成功從 {remote_name}/{branch} 拉取更新"
        except git.exc.GitCommandError as e:
            if "resolve" in str(e) or "conflict" in str(e):
                raise Exception("拉取時發生衝突，請手動解決衝突")
            else:
                raise Exception(f"拉取失敗：{str(e)}") 