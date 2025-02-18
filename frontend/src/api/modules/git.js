import axios from '@/utils/axios'

export default {
  // Git 配置
  configureGit(data) {
    return axios.post('/config', data)
      .catch(error => {
        console.error('ConfigureGit Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 添加遠程倉庫
  addRemote(data) {
    return axios.post('/remote/add', data)
      .catch(error => {
        console.error('AddRemote Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 獲取倉庫狀態
  getStatus() {
    return axios.get('/status')
      .catch(error => {
        console.error('GetStatus Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 添加文件到暫存區
  addFiles(files) {
    return axios.post('/add', { files })
      .catch(error => {
        console.error('AddFiles Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 提交更改
  commit(message) {
    return axios.post('/commit', { message })
      .catch(error => {
        console.error('Commit Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 創建分支
  createBranch(name) {
    return axios.post('/branch/create', { name })
      .catch(error => {
        console.error('CreateBranch Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 切換分支
  switchBranch(name) {
    return axios.post('/branch/switch', { name })
      .catch(error => {
        console.error('SwitchBranch Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 拉取更新
  pull() {
    return axios.post('/pull')
      .catch(error => {
        console.error('Pull Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 推送更改
  push(force = false) {
    return axios.post(force ? '/force-push' : '/push')
      .catch(error => {
        console.error('Push Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 獲取提交歷史
  getHistory(params) {
    return axios.get('/commits', { params })
      .catch(error => {
        console.error('GetHistory Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 初始化倉庫
  initRepo(path) {
    return axios.post('/init', { path })
      .catch(error => {
        console.error('InitRepo Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 版本回退
  resetToCommit(hash) {
    return axios.post('/reset', { hash })
      .catch(error => {
        console.error('ResetToCommit Error:', error.response?.data || error.message)
        throw error
      })
  }
} 