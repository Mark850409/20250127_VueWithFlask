<template>
  <section class="py-16 bg-white">
    <div class="container mx-auto px-4">
      <h2 class="text-3xl font-bold text-center mb-8">熱門飲料推薦</h2>
      
      <!-- 排序選項 -->
      <div class="flex justify-center mb-8 space-x-4">
        <button 
          v-for="sort in sortOptions" 
          :key="sort.value"
          @click="currentSort = sort.value"
          :class="[
            'px-4 py-2 rounded-full transition duration-300',
            currentSort === sort.value 
              ? 'bg-red-600 text-white' 
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          ]"
        >
          {{ sort.label }}
        </button>
      </div>

      <!-- 飲料列表 -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div v-for="drink in sortedDrinks" :key="drink.id" 
             class="bg-white rounded-lg shadow-lg overflow-hidden transform 
                    transition duration-300 hover:scale-105">
          <img :src="drink.image" :alt="drink.name" class="w-full h-48 object-cover">
          <div class="p-4">
            <div class="flex justify-between items-center mb-2">
              <h3 class="text-xl font-bold">{{ drink.name }}</h3>
              <div class="flex items-center">
                <span class="text-yellow-500 mr-1">★</span>
                <span>{{ drink.rating }}</span>
              </div>
            </div>
            <p class="text-gray-600 mb-2">{{ drink.description }}</p>
            <div class="flex justify-between items-center">
              <span class="text-red-600 font-bold">${{ drink.price }}</span>
              <span class="text-gray-500">{{ drink.distance }}km</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  data() {
    return {
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
          image: '/src/assets/food/bubble-tea.jpg'
        },
        // ... 更多飲料數據
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