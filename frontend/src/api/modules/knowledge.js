import axios from '@/utils/axios'

export default {
  // 刪除檔案
  deleteFile(flowId, fileName) {
    return axios.delete(`v1/files/delete/${flowId}/${fileName}`)
      .catch(error => {
        console.error('DeleteFile Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 下載檔案
  downloadFile(flowId, fileName) {
    return axios.get(`v1/files/download/${flowId}/${fileName}`, {
      responseType: 'blob'
    }).catch(error => {
      console.error('DownloadFile Error:', error.response?.data || error.message) 
      throw error
    })
  },

  // 列出檔案
  listFiles(flowId) {
    return axios.get(`v1/files/list/${flowId}`)
      .catch(error => {
        console.error('ListFiles Error:', error.response?.data || error.message)
        throw error
      })
  },

  // 上傳檔案
  uploadFile(flowId, formData) {
    return axios.post(`v1/files/upload/${flowId}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).catch(error => {
      console.error('UploadFile Error:', error.response?.data || error.message)
      throw error
    })
  },

  // 批次下載檔案
  batchDownload(flowId, fileNames) {
    return axios.post('v1/files/batch-download', {
      flowId,
      fileNames
    }, {
      responseType: 'blob'
    }).catch(error => {
      console.error('BatchDownload Error:', error.response?.data || error.message)
      throw error
    })
  }
} 