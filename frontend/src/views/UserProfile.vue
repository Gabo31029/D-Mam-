

<script setup>
import { ref, computed, onMounted, onActivated, watch } from 'vue';
import { useAuth } from '../composables/useAuth';
import api from '../api';

const { user: authUser, loadUser } = useAuth();

const user = ref(null);
const loading = ref(true);
const error = ref(null);

// Usar el usuario del composable si está disponible
const userFromAuth = computed(() => authUser.value);

const loadProfile = async (forceRefresh = false) => {
    try {
        loading.value = true;
        error.value = null;
        
        // Siempre hacer una petición fresca para obtener datos actualizados
        const response = await api.get('/users/me');
        user.value = response.data;
        
        console.log('Profile loaded:', user.value);
    } catch (err) {
        console.error("Error loading profile", err);
        error.value = err.response?.data?.detail || 'Error al cargar el perfil';
    } finally {
        loading.value = false;
    }
};

// Observar cambios en authUser
watch(userFromAuth, (newUser) => {
    if (newUser) {
        user.value = newUser;
        loading.value = false;
    }
});

const translateType = (type) => {
    const types = {
        'salty': 'Salado',
        'sweet': 'Dulce'
    };
    return types[type] || type;
};

onMounted(loadProfile);

// Recargar perfil cada vez que se activa la vista (cuando navegas de vuelta)
onActivated(() => {
    console.log('Vista de perfil activada, recargando datos...');
    loadProfile();
});
</script>


<template>
  <!-- Loading State -->
  <div v-if="loading" class="flex items-center justify-center min-h-screen">
      <div class="text-center">
          <div class="animate-pulse text-stone-400 font-serif text-lg mb-2">Cargando perfil...</div>
      </div>
  </div>

  <!-- Error State -->
  <div v-else-if="error" class="flex items-center justify-center min-h-screen">
      <div class="text-center max-w-md">
          <h2 class="text-2xl font-serif text-stone-800 mb-4">Error al cargar perfil</h2>
          <p class="text-stone-600 mb-6">{{ error }}</p>
          <router-link to="/login" class="btn-primary">Iniciar sesión</router-link>
      </div>
  </div>

  <!-- Profile Content -->
  <div v-else-if="user" class="px-4 pb-12 max-w-7xl mx-auto">
    <!-- Header -->
    <div class="mb-12 border-b border-stone-200 pb-8">
        <h1 class="text-4xl font-serif font-bold text-stone-900 mb-2">Mi Perfil de Cocina</h1>
        <p class="text-xl text-stone-500 font-light">Bienvenido, {{ user.username }}</p>
    </div>

    <!-- My Recipes -->
    <section class="mb-16">
        <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-serif font-bold text-stone-800">Mis Recetas</h2>
            <router-link to="/create-recipe" class="text-sm font-medium text-olive-600 hover:text-olive-800 transition-colors uppercase tracking-wider">+ Nueva Receta</router-link>
        </div>
        
        <div v-if="user.recipes && user.recipes.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div v-for="recipe in user.recipes" :key="recipe.id" class="card group p-6 border border-stone-200 hover:border-olive-500/50 transition-all duration-300 cursor-pointer" @click="$router.push(`/recipes/${recipe.id}`)">
                <div class="flex items-center justify-between mb-4">
                    <span class="text-xs uppercase tracking-widest font-medium text-stone-400">{{ translateType(recipe.type) }}</span>
                </div>
                <h3 class="text-xl font-serif font-bold text-stone-900 mb-2 truncate group-hover:text-olive-700 transition-colors">{{ recipe.title }}</h3>
            </div>
        </div>
        <div v-else class="text-center py-12 bg-stone-50 rounded-lg border border-dashed border-stone-200">
            <p class="text-stone-400 italic mb-4">No has subido ninguna receta aún.</p>
            <router-link to="/create-recipe" class="btn-primary inline-block">Crear mi primera receta</router-link>
        </div>
    </section>

    <!-- My Cookbooks -->
    <section>
        <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-serif font-bold text-stone-800">Mis Recetarios</h2>
            <router-link to="/create-cookbook" class="text-sm font-medium text-olive-600 hover:text-olive-800 transition-colors uppercase tracking-wider">+ Nuevo Recetario</router-link>
        </div>

        <div v-if="user.cookbooks && user.cookbooks.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div v-for="book in user.cookbooks" :key="book.id" class="card group p-8 border border-stone-200 gap-4 hover:border-olive-500/50 transition-all cursor-pointer flex flex-col items-left justify-center" @click="$router.push(`/cookbooks/${book.id}`)">
                <h3 class="text-xl font-serif font-bold text-stone-900 group-hover:text-olive-700 transition-colors">{{ book.title }}</h3>
                <span class="text-xs font-medium text-stone-400">N° recetas: {{ book.recipes.length }}</span>
            </div>
        </div>
         <div v-else class="text-center py-12 bg-stone-50 rounded-lg border border-dashed border-stone-200">
            <p class="text-stone-400 italic mb-4">No tienes recetarios creados.</p>
            <router-link to="/create-cookbook" class="btn-primary inline-block">Crear mi primer recetario</router-link>
        </div>
    </section>
  </div>
</template>
