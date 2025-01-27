<template>
  <section class="py-16 bg-white">
    <div class="container mx-auto px-4">
      <h2 class="text-3xl font-bold text-center mb-8">熱門飲料推薦</h2>
      
      <!-- 排序和視圖切換選項 -->
      <div class="flex justify-between items-center mb-8">
        <div class="flex space-x-4">
          <button 
            v-for="sort in sortOptions" 
            :key="sort.value"
            @click="currentSort = sort.value"
            :class="[
              'px-4 py-2 rounded-full transition duration-300',
              currentSort === sort.value 
                ? 'bg-gray-800 text-white' 
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            ]"
          >
            {{ sort.label }}
          </button>
        </div>
        
        <!-- 視圖切換按鈕 -->
        <div class="flex space-x-2">
          <button 
            @click="viewMode = 'grid'"
            :class="[
              'p-2 rounded-lg transition-colors',
              viewMode === 'grid' 
                ? 'bg-gray-800 text-white' 
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            ]"
          >
            <i class="fas fa-th-large"></i>
          </button>
          <button 
            @click="viewMode = 'list'"
            :class="[
              'p-2 rounded-lg transition-colors',
              viewMode === 'list' 
                ? 'bg-gray-800 text-white' 
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            ]"
          >
            <i class="fas fa-list"></i>
          </button>
        </div>
      </div>

      <!-- 飲料列表容器 -->
      <transition-group 
        :name="viewMode === 'grid' ? 'layout-grid' : 'layout-list'"
        tag="div"
        :class="{
          'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8': viewMode === 'grid',
          'space-y-4': viewMode === 'list'
        }"
      >
        <div v-for="drink in sortedDrinks" :key="drink.id" 
            :class="[
              'bg-white rounded-lg shadow-lg overflow-hidden transform transition-all duration-300',
              viewMode === 'grid' ? 'hover:scale-105' : 'hover:shadow-xl'
            ]">
          <!-- 網格視圖 -->
          <template v-if="viewMode === 'grid'">
            <img :src="drink.image" :alt="drink.name" class="w-full h-48 object-cover">
            <div class="p-4">
              <div class="flex justify-between items-center mb-2">
                <h3 class="text-xl font-bold">{{ drink.name }}</h3>
                <div class="flex items-center">
                  <span class="text-gray-700 mr-1">★</span>
                  <span>{{ drink.rating }}</span>
                </div>
              </div>
              <p class="text-gray-600 mb-2">{{ drink.description }}</p>
              <div class="flex justify-between items-center">
                <span class="text-gray-800 font-bold">${{ drink.price }}</span>
                <span class="text-gray-500">{{ drink.distance }}km</span>
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
                    <h3 class="text-xl font-bold mb-2">{{ drink.name }}</h3>
                    <p class="text-gray-600">{{ drink.description }}</p>
                  </div>
                  <div class="flex flex-col items-end">
                    <div class="flex items-center mb-2">
                      <span class="text-gray-700 mr-1">★</span>
                      <span>{{ drink.rating }}</span>
                    </div>
                    <span class="text-gray-800 font-bold mb-1">${{ drink.price }}</span>
                    <span class="text-gray-500">{{ drink.distance }}km</span>
                  </div>
                </div>
              </div>
            </div>
          </template>
        </div>
      </transition-group>
    </div>
  </section>
</template>

<script>
export default {
  data() {
    return {
      viewMode: 'grid',
      currentSort: 'default',
      sortOptions: [
        { label: '預設排序', value: 'default' },
        { label: '評分排序', value: 'rating' },
        { label: '距離排序', value: 'distance' },
        { label: '熱門排序', value: 'popular' }
      ],
      drinks: [
        {
          id: 1,
          name: '珍珠奶茶',
          description: '經典台灣味道，香濃奶茶搭配QQ珍珠',
          price: 60,
          rating: 4.8,
          distance: 0.3,
          popular: 985,
          image: 'https://images.unsplash.com/photo-1558857563-c0c976477e51?w=500'
        },
        {
          id: 2,
          name: '抹茶拿鐵',
          description: '日本進口抹茶粉，搭配香醇鮮奶',
          price: 75,
          rating: 4.7,
          distance: 0.5,
          popular: 876,
          image: 'https://images.unsplash.com/photo-1515823662972-da6a2e4d3002?w=500'
        },
        {
          id: 3,
          name: '芒果冰沙',
          description: '使用當季新鮮芒果，清爽消暑',
          price: 85,
          rating: 4.9,
          distance: 0.8,
          popular: 1024,
          image: 'https://images.unsplash.com/photo-1546173159-315724a31696?w=500'
        },
        {
          id: 4,
          name: '美式咖啡',
          description: '嚴選咖啡豆，純粹香醇',
          price: 55,
          rating: 4.6,
          distance: 0.2,
          popular: 756,
          image: 'https://images.unsplash.com/photo-1521302080334-4bebac2763a6?w=500'
        },
        {
          id: 5,
          name: '草莓奶昔',
          description: '新鮮草莓打製，香甜可口',
          price: 90,
          rating: 4.8,
          distance: 0.6,
          popular: 892,
          image: 'https://images.unsplash.com/photo-1553787499-6f5f32966e02?w=500'
        },
        {
          id: 6,
          name: '檸檬綠茶',
          description: '台灣高山茶配上新鮮檸檬片',
          price: 45,
          rating: 4.5,
          distance: 0.4,
          popular: 678,
          image: 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=500'
        },
        {
          id: 7,
          name: '焦糖瑪奇朵',
          description: '香濃義式咖啡搭配焦糖風味',
          price: 80,
          rating: 4.7,
          distance: 0.7,
          popular: 845,
          image: 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=500'
        },
        {
          id: 8,
          name: '藍莓優格昔',
          description: '新鮮藍莓與希臘優格調製',
          price: 95,
          rating: 4.6,
          distance: 1.0,
          popular: 734,
          image: 'https://images.unsplash.com/photo-1502741338009-cac2772e18bc?w=500'
        },
        {
          id: 9,
          name: '蘋果醋氣泡飲',
          description: '天然發酵蘋果醋，清新爽口',
          price: 65,
          rating: 4.4,
          distance: 0.9,
          popular: 567,
          image: 'https://images.unsplash.com/photo-1473115209096-e0375dd6b3b3?w=500'
        },
        {
          id: 10,
          name: '紅茶拿鐵',
          description: '錫蘭紅茶搭配香醇鮮奶',
          price: 70,
          rating: 4.7,
          distance: 0.5,
          popular: 823,
          image: 'https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=500'
        }
      ]
    }
  },
  computed: {
    sortedDrinks() {
      switch (this.currentSort) {
        case 'rating':
          return [...this.drinks].sort((a, b) => b.rating - a.rating);
        case 'distance':
          return [...this.drinks].sort((a, b) => a.distance - b.distance);
        case 'popular':
          return [...this.drinks].sort((a, b) => b.popular - a.popular);
        default:
          return this.drinks;
      }
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