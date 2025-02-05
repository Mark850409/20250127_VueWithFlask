import axios from '@/utils/axios'

export default {
  // 獲取選單列表
  getMenus() {
    console.log('Fetching menus...')
    return axios.get('/menus/')
      .then(response => {
        console.log('Menus response:', response.data)
        return response
      })
      .catch(error => {
        console.error('GetMenus API Error:', {
          status: error.response?.status,
          data: error.response?.data,
          message: error.message
        })
        throw error
      })
  },

  // 新增選單
  createMenu(data) {
    console.log('Creating menu with data:', data)
    // 確保所有必要欄位都是字串類型
    const formattedData = {
      ...data,
      name: String(data.name || ''),
      path: String(data.path || ''),
      icon: String(data.icon || ''),
      description: String(data.description || ''),
      status: String(data.status ? 'Enabled' : 'Disabled')
    }
    
    return axios.post('/menus/', formattedData)
      .catch(error => {
        console.error('CreateMenu API Error:', {
          status: error.response?.status,
          data: error.response?.data,
          message: error.message
        })
        throw error
      })
  },

  // 更新選單
  updateMenu(id, data) {
    return axios.put(`/menus/${id}`, data)
      .catch(error => {
        console.error('UpdateMenu Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 刪除選單
  deleteMenu(id) {
    return axios.delete(`/menus/${id}`)
      .catch(error => {
        console.error('DeleteMenu Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 更新選單排序
  updateMenuOrder(data) {
    console.log('Updating menu order with data:', data);
    return axios.put('/menus/order', data)
      .catch(error => {
        console.error('UpdateMenuOrder Error:', error.response?.data || error.message)
        throw error
      })
  }
} 