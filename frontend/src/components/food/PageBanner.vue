<template>
  <section class="relative h-[600px]">
    <div class="absolute inset-0">
      <img 
        src="https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&q=80&w=1920&h=400" 
        class="w-full h-full object-cover" alt="banner">
      <div class="absolute inset-0 bg-gradient-to-r from-black/70 to-black/50"></div>
    </div>
    <div class="relative container mx-auto px-4 h-full flex flex-col justify-center items-center text-white">
      <h1 class="text-5xl font-bold mb-4">{{ title }}</h1>
      <p class="text-xl mb-6">{{ subtitle }}</p>
      <p class="text-lg mb-6 max-w-2xl text-center text-gray-200">
        {{ description }}
      </p>
      <div class="flex space-x-6">
        <router-link to="/features" 
          class="inline-flex items-center px-6 py-3 border-2 border-white hover:bg-white/10 
                 rounded-lg transition duration-300">
          <i class="fas fa-star mr-2"></i>
          功能特色
        </router-link>
        <router-link to="/learning" 
          class="inline-flex items-center px-6 py-3 border-2 border-white hover:bg-white/10 
                 rounded-lg transition duration-300">
          <i class="fas fa-book mr-2"></i>
          學習中心
        </router-link>
        <router-link to="/pricing" 
          class="inline-flex items-center px-6 py-3 border-2 border-white hover:bg-white/10 
                 rounded-lg transition duration-300">
          <i class="fas fa-tag mr-2"></i>
          價格方案
        </router-link>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      required: true
    },
    subtitle: {
      type: String,
      required: true
    },
    description: {
      type: String,
      required: true
    }
  }
}
</script> 