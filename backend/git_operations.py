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

    def delete_commit(self, commit_hash):
        if not self.repo:
            raise Exception("倉庫未初始化")
        
        try:
            # 獲取所有提交
            commits = list(self.repo.iter_commits())
            target_commit = None
            commits_to_cherry_pick = []
            
            # 找到目標提交和之後的提交
            found_target = False
            for commit in commits:
                if commit.hexsha.startswith(commit_hash):
                    found_target = True
                    target_commit = commit
                    continue
                if found_target:
                    commits_to_cherry_pick.insert(0, commit)
            
            if not target_commit:
                raise Exception("找不到指定的提交")
            
            # 檢查是否為第一個提交
            if not target_commit.parents:
                raise Exception("無法刪除第一個提交，這可能會破壞倉庫。如果確實需要，請考慮重新初始化倉庫。")
            
            # 重置到目標提交的父提交
            parent = target_commit.parents[0]
            self.repo.git.reset('--hard', parent.hexsha)
            
            # 重新應用之後的提交
            for commit in commits_to_cherry_pick:
                try:
                    self.repo.git.cherry_pick(commit.hexsha)
                except git.exc.GitCommandError as e:
                    # 如果cherry-pick失敗，中止操作並還原
                    self.repo.git.cherry_pick('--abort')
                    # 嘗試還原到原始狀態
                    try:
                        self.repo.git.reset('--hard', target_commit.hexsha)
                    except:
                        pass
                    raise Exception(f"重新應用提交時失敗：{str(e)}")
            
            return f"成功刪除提交 {commit_hash}"
        except git.exc.GitCommandError as e:
            raise Exception(f"刪除提交失敗：{str(e)}")
        except Exception as e:
            raise Exception(f"刪除提交失敗：{str(e)}")

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