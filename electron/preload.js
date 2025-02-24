const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electron', {
  showOpenDialog: async (options) => {
    try {
      return await ipcRenderer.invoke('dialog:showOpen', options)
    } catch (error) {
      console.error('Error in showOpenDialog:', error)
      throw error
    }
  }
}) 