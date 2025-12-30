
<script setup>
import { ref, onMounted, watch } from 'vue';
import api from '../api';
import debounce from 'lodash.debounce'; // Ideally we'd install lodash, but for now I'll implement simple debounce or just standard watch

const cookbooks = ref([]);
const search = ref('');

const loadCookbooks = async () => {
    let url = '/cookbooks/';
    if (search.value) url += `?search=${search.value}`;
    try {
        const response = await api.get(url);
        cookbooks.value = response.data;
    } catch (err) {
        console.error("Error loading cookbooks", err);
    }
};

let timeout;
watch(search, (newVal) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
        loadCookbooks();
    }, 300);
});

onMounted(loadCookbooks);
</script>

<template>
  <div class="px-4 pb-12">
    <!-- Header -->
    <div class="mb-12 flex flex-col sm:flex-row gap-6 justify-between items-end border-b border-stone-200 pb-6">
       <div>
         <h1 class="text-4xl font-serif font-bold text-stone-900 mb-2">Colección de Recetarios</h1>
         <p class="text-stone-500 font-light">Compendios curados para cada ocasión.</p>
       </div>
       <div class="w-full sm:w-auto">
           <input v-model="search" type="text" placeholder="Buscar por título..." class="input-field max-w-sm" />
       </div>
    </div>

    <!-- Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div v-for="book in cookbooks" :key="book.id" class="card p-8 group cursor-pointer border border-stone-200 hover:border-olive-500/50 transition-all duration-300" @click="$router.push(`/cookbooks/${book.id}`)">
            <!-- Book Cover / Header -->
            <div class="mb-6 h-32 bg-stone-100/50 rounded-sm border border-stone-200 flex items-center justify-center relative overflow-hidden">
                <!-- If we had an image it would go here, else just a nice typographic placement could be here or just empty texture -->
                 <div class="text-stone-300 font-serif italic text-sm">Sin Portada</div>
            </div>
            
            <h3 class="text-2xl font-serif font-bold text-stone-900 mb-3 group-hover:text-olive-700 transition-colors">{{ book.title }}</h3>
            <p class="text-stone-600 mb-6 font-light leading-relaxed line-clamp-3">{{ book.description }}</p>
            
            <!-- Author Info -->
            <p v-if="book.owner" class="text-xs text-stone-500 mb-4">
                Por <span class="font-semibold text-olive-600">{{ book.owner.username }}</span>
            </p>
            
            <div class="pt-4 border-t border-stone-100">
                <span class="text-sm text-olive-600 font-medium uppercase tracking-widest group-hover:text-olive-800 transition-colors">Explorar &rarr;</span>
            </div>
        </div>
    </div>
  </div>
</template>
