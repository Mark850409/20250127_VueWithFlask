<template>
  <transition-group 
    :name="viewMode === 'grid' ? 'layout-grid' : 'layout-list'"
    tag="div"
    :class="{
      'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8': viewMode === 'grid',
      'space-y-4': viewMode === 'list'
    }"
  >
    <div v-for="drink in drinks" :key="drink.id" 
        :class="[
          'bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden transform transition-all duration-300',
          viewMode === 'grid' ? 'hover:scale-105' : 'hover:shadow-xl'
        ]">
      <!-- 網格視圖 -->
      <template v-if="viewMode === 'grid'">
        <img :src="drink.image" :alt="drink.name" class="w-full h-48 object-cover">
        <div class="p-4">
          <div class="flex justify-between items-center mb-2">
            <h3 class="text-xl font-bold text-gray-900 dark:text-white">{{ drink.name }}</h3>
            <div class="flex items-center">
              <span class="text-yellow-400">★</span>
              <span class="ml-1 text-gray-700 dark:text-gray-300">{{ drink.rating }}</span>
            </div>
          </div>
          <p class="text-gray-600 dark:text-gray-400 mb-2">{{ drink.description }}</p>
          <div class="flex justify-between items-center">
            <span class="text-gray-800 dark:text-gray-200 font-bold">${{ drink.price }}</span>
            <span class="text-gray-500 dark:text-gray-400">{{ drink.views }} 瀏覽</span>
          </div>
        </div>
      </template>
      
      <!-- 列表視圖 -->
      <template v-else>
        <div class="flex">
          <img :src="drink.image" :alt="drink.name" class="w-48 h-32 object-cover">
          <div class="flex-1 p-4">
            <div class="flex justify-between items-start">
              <div>
                <h3 class="text-xl font-bold mb-2 text-gray-900 dark:text-white">{{ drink.name }}</h3>
                <p class="text-gray-600 dark:text-gray-400">{{ drink.description }}</p>
              </div>
              <div class="flex flex-col items-end">
                <div class="flex items-center mb-2">
                  <span class="text-yellow-400">★</span>
                  <span class="ml-1 text-gray-700 dark:text-gray-300">{{ drink.rating }}</span>
                </div>
                <span class="text-gray-800 dark:text-gray-200 font-bold mb-1">${{ drink.price }}</span>
                <span class="text-gray-500 dark:text-gray-400">{{ drink.views }} 瀏覽</span>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>
  </transition-group>
</template>

<script>
export default {
  name: 'DrinkShopList',
  props: {
    drinks: {
      type: Array,
      required: true
    },
    viewMode: {
      type: String,
      required: true,
      validator: value => ['grid', 'list'].includes(value)
    }
  }
}
</script>

<style scoped>
/* 網格布局動畫 */
.layout-grid-move {
  transition: transform 0.5s ease;
}

/* 列表布局動畫 */
.layout-list-move {
  transition: transform 0.5s ease;
}

/* 進入和離開動畫 */
.layout-grid-enter-active,
.layout-grid-leave-active,
.layout-list-enter-active,
.layout-list-leave-active {
  transition: all 0.5s ease;
}

.layout-grid-enter-from,
.layout-grid-leave-to,
.layout-list-enter-from,
.layout-list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

/* 確保動畫期間元素不會消失 */
.layout-grid-leave-active,
.layout-list-leave-active {
  position: absolute;
}
</style> 