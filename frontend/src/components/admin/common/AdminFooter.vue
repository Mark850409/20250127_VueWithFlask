<template>
  <footer class="bg-white border-t py-4 px-8 mt-auto">
    <div class="flex justify-between items-center text-sm text-gray-600">
      <div>
        Copyright © {{ currentYear }} 基於文字探勘與情感分析的點餐推薦系統 版權所有・翻印必究
      </div>
      <div class="flex items-center space-x-6">
        <a href="#" class="text-gray-600 hover:text-blue-600 transition-colors duration-300" title="Facebook">
          <i class="fab fa-facebook text-xl"></i>
        </a>
        <a href="#" class="text-gray-600 hover:text-pink-600 transition-colors duration-300" title="Instagram">
          <i class="fab fa-instagram text-xl"></i>
        </a>
        <a href="#" class="text-gray-600 hover:text-blue-400 transition-colors duration-300" title="Twitter">
          <i class="fab fa-twitter text-xl"></i>
        </a>
        <a href="#" class="text-gray-600 hover:text-blue-700 transition-colors duration-300" title="LinkedIn">
          <i class="fab fa-linkedin text-xl"></i>
        </a>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'AdminFooter',
  computed: {
    currentYear() {
      return new Date().getFullYear()
    }
  }
}
</script>

<style scoped>
.fab {
  transition: transform 0.3s ease;
}

.fab:hover {
  transform: translateY(-2px);
}
</style> 