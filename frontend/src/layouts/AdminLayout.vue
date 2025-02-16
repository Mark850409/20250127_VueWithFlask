<template>
  <!-- No changes to template section -->
</template>

<script>
export default {
  methods: {
    getBannerTitle() {
      const path = this.$route.path
      const titles = {
        '/admin/projects': '專案管理',
        '/admin/accounts': '帳號管理',
        // ... 其他路由
      }
      return titles[path] || '管理後台'
    },
    getBannerDescription() {
      const path = this.$route.path
      const descriptions = {
        '/admin/projects': '管理 Langflow 專案，包含新增、修改、刪除等功能',
        '/admin/accounts': '管理系統帳號，包含新增、修改、刪除等功能',
        // ... 其他路由
      }
      return descriptions[path] || ''
    }
  }
}
</script>

<style>
  /* No changes to style section */
</style> 