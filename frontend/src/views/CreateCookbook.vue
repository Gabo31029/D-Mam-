
<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import api from '../api';

const router = useRouter();
const route = useRoute();

const isEditing = computed(() => !!route.params.id);
const cookbookId = computed(() => route.params.id);

const form = ref({
    title: '',
    description: ''
});
const selectedRecipes = ref([]);
const userRecipes = ref([]);
const loading = ref(false);

const loadData = async () => {
    loading.value = true;
    try {
        // 1. Cargar recetas del usuario
        const userRes = await api.get('/users/me');
        // El usuario tiene todas sus recetas, incluidas las que ya están en recetarios
        userRecipes.value = userRes.data.recipes || [];

        // 2. Si estamos editando, cargar el recetario
        if (isEditing.value) {
            const cbRes = await api.get(`/cookbooks/${cookbookId.value}`);
            const cookbook = cbRes.data;
            
            form.value = {
                title: cookbook.title,
                description: cookbook.description || ''
            };
            
            // Pre-seleccionar recetas que ya están en este recetario
            if (cookbook.recipes) {
                selectedRecipes.value = cookbook.recipes.map(r => r.id);
            }
        }
    } catch (err) {
        console.error('Error loading data:', err);
        alert('Error al cargar datos');
        router.push('/profile');
    } finally {
        loading.value = false;
    }
};

onMounted(loadData);

const submitCookbook = async () => {
    try {
        const payload = {
            ...form.value,
            recipe_ids: selectedRecipes.value
        };

        if (isEditing.value) {
            await api.put(`/cookbooks/${cookbookId.value}`, payload);
            alert('Recetario actualizado exitosamente');
        } else {
            await api.post('/cookbooks/', payload);
        }
        router.push('/profile');
    } catch (err) {
        console.error('Error:', err);
        alert(isEditing.value ? 'Error actualizando recetario' : 'Error creando recetario');
    }
};
</script>

<template>
  <div class="max-w-3xl mx-auto px-4 pb-12">
    <div v-if="loading" class="text-center py-20">
      <div class="animate-pulse text-stone-400 font-serif text-lg">Cargando recetario...</div>
    </div>
    
    <div v-else>
      <div class="mb-8 border-b border-stone-200 pb-4">
        <h1 class="text-4xl font-serif font-bold text-stone-900">{{ isEditing ? 'Editar Recetario' : 'Nuevo Recetario' }}</h1>
        <p class="text-stone-500 mt-2">{{ isEditing ? 'Actualiza los detalles de tu recetario.' : 'Crea una colección para organizar tus recetas favoritas.' }}</p>
      </div>

      <form @submit.prevent="submitCookbook" class="card p-10 space-y-8 border border-stone-200 shadow-none">
          <div>
              <label class="block text-sm font-medium text-stone-700 mb-2 uppercase tracking-wide">Título del Recetario</label>
              <input v-model="form.title" type="text" class="input-field text-lg font-serif placeholder-stone-300" placeholder="Ej. Postres de la Abuela" required />
          </div>

          <div>
              <label class="block text-sm font-medium text-stone-700 mb-2 uppercase tracking-wide">Descripción</label>
              <textarea v-model="form.description" class="input-field min-h-[100px] leading-relaxed" placeholder="¿De qué trata esta colección?"></textarea>
          </div>

          <!-- Selección de Recetas -->
          <div>
              <h3 class="block text-sm font-medium text-stone-700 mb-4 uppercase tracking-wide">Seleccionar Recetas</h3>
              
              <div v-if="userRecipes.length === 0" class="text-stone-500 italic text-sm p-4 bg-stone-50 rounded border border-stone-200 text-center">
                  No tienes recetas creadas aún. <router-link to="/create-recipe" class="text-olive-600 underline">Crea una primero</router-link>.
              </div>

              <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4 max-h-[400px] overflow-y-auto p-1">
                  <div v-for="recipe in userRecipes" :key="recipe.id" 
                       :class="[
                           'flex items-start p-4 border rounded-lg cursor-pointer transition-all hover:shadow-sm',
                           selectedRecipes.includes(recipe.id) ? 'border-olive-500 bg-olive-50' : 'border-stone-200'
                       ]"
                       @click="selectedRecipes.includes(recipe.id) 
                           ? selectedRecipes = selectedRecipes.filter(id => id !== recipe.id) 
                           : selectedRecipes.push(recipe.id)"
                  >
                      <input 
                          type="checkbox" 
                          :value="recipe.id" 
                          v-model="selectedRecipes"
                          class="mt-1 h-4 w-4 text-olive-600 focus:ring-olive-500 border-gray-300 rounded cursor-pointer"
                          @click.stop
                      />
                      <div class="ml-3">
                          <span class="block text-sm font-medium text-stone-900">{{ recipe.title }}</span>
                          <span v-if="recipe.cookbook_id && recipe.cookbook_id !== parseInt(cookbookId)" class="block text-xs text-amber-600 mt-1">
                              ⚠ Actualmente en otro recetario
                          </span>
                      </div>
                  </div>
              </div>
          </div>

          <div class="pt-4">
              <button type="submit" class="btn-primary w-full py-3 text-base shadow-sm hover:shadow-md transition-shadow">
                {{ isEditing ? 'Actualizar Colección' : 'Crear Colección' }}
              </button>
          </div>
      </form>
    </div>
  </div>
</template>
