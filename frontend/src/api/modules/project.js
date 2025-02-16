import axios from '@/utils/axios'

export default {
  // 獲取專案列表
  getProjects() {
    return axios.get('/v1/folders/')
      .catch(error => {
        console.error('GetProjects Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 獲取單一專案詳情
  getProject(id) {
    return axios.get(`/v1/folders/${id}`)
      .catch(error => {
        console.error('GetProject Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 新增專案
  createProject(data) {
    console.log(data)
    return axios.post('/v1/folders/', {
      name: data.name,
      description: data.description,
      components_list: ["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
      flows_list: ["3fa85f64-5717-4562-b3fc-2c963f66afa6"]
    })
      .catch(error => {
        console.error('CreateProject Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 更新專案
  updateProject(id, data) {
    console.log(data)
    return axios.patch(`/v1/folders/${id}`, {
      name: data.name,
      description: data.description,
      components: ["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
      flows: ["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
      parent_id: "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    })
      .catch(error => {
        console.error('UpdateProject Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 刪除專案
  deleteProject(id) {
    return axios.delete(`/v1/folders/${id}`)
      .catch(error => {
        console.error('DeleteProject Error:', error.response?.data || error.message)
        throw error
      })
  }
} 