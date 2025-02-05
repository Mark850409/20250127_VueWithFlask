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

  /**
   * 更新選單排序
   * @param {Object} data - 包含選單排序資訊的物件
   * @returns {Promise} - API 回應
   */
  updateMenuOrder(data) {
    // 確保 section_order 從 1 開始
    const processedData = {
      menus: data.menus.map(menu => ({
        ...menu,
        section_order: menu.section_order !== undefined ? Math.max(1, parseInt(menu.section_order)) : 1,
        sort_order: menu.sort_order !== undefined ? parseInt(menu.sort_order) : 0
      }))
    };
    
    console.log('Sending menu order update:', processedData);
    return axios.put('/menus/order', processedData)
      .catch(error => {
        console.error('UpdateMenuOrder Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 獲取主功能區塊列表
  getMenuSections() {
    return axios.get('/menus/sections')
      .catch(error => {
        console.error('GetMenuSections Error:', error.response?.data || error.message)
        throw error
      })
  }
} 