from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class GitInitRequest(BaseModel):
    path: str

class GitConfigRequest(BaseModel):
    name: str
    email: str

class GitCommitRequest(BaseModel):
    message: str

class GitBranchRequest(BaseModel):
    name: str

class GitRemoteRequest(BaseModel):
    name: str = 'origin'
    url: str

class GitPushRequest(BaseModel):
    remote: str = 'origin'
    branch: str = 'master'
    force: bool = False

class GitCommitResponse(BaseModel):
    hash: str
    author: str
    date: datetime
    message: str
    branch: str

class GitStatusResponse(BaseModel):
    untracked: List[str] = []
    modified: List[str] = []
    staged: List[str] = []
    branch: str = ''

    class Config:
        orm_mode = True

class ErrorResponse(BaseModel):
    message: str

class GitResetRequest(BaseModel):
    hash: str
    mode: str = 'hard'

class GitPullRequest(BaseModel):
    remote: str = 'origin'
    branch: str = 'master' 