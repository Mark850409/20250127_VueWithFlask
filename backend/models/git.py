from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class GitStatus:
    untracked: list[str]
    modified: list[str]
    staged: list[str]
    branch: str

    def __dict__(self):
        return {
            'untracked': list(self.untracked),  # 確保是列表
            'modified': list(self.modified),
            'staged': list(self.staged),
            'branch': self.branch
        }

    def __post_init__(self):
        # 確保所有列表字段都是列表類型
        self.untracked = list(self.untracked or [])
        self.modified = list(self.modified or [])
        self.staged = list(self.staged or [])

@dataclass
class GitCommit:
    hash: str
    author: str
    date: datetime
    message: str
    branch: str 