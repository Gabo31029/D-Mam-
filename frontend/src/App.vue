

<script setup>
import { onMounted } from 'vue';
import { useAuth } from './composables/useAuth';

const { isAuthenticated, logout, loadUser } = useAuth();

// Cargar información del usuario al montar la aplicación
onMounted(() => {
  if (isAuthenticated.value) {
    loadUser();
  }
});
</script>


<template>
  <div class="min-h-screen bg-cream-50 font-sans text-stone-800">
    <!-- Navbar: Simple, clean, editorial -->
    <nav class="bg-white border-b border-stone-200 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-20">
          <div class="flex items-center">
            <router-link to="/" class="flex-shrink-0 flex items-center group">
              <!-- Logo text: Serif, solid color, minimal -->
              <span class="text-3xl font-serif font-bold text-olive-700 tracking-tight group-hover:text-olive-600 transition-colors">D'Mamá</span>
            </router-link>
            <div class="hidden sm:ml-10 sm:flex sm:space-x-8">
              <router-link to="/" class="text-stone-600 hover:text-olive-600 px-1 py-2 text-sm font-medium transition-colors border-b-2 border-transparent hover:border-olive-600">Inicio</router-link>
              <router-link to="/cookbooks" class="text-stone-600 hover:text-olive-600 px-1 py-2 text-sm font-medium transition-colors border-b-2 border-transparent hover:border-olive-600">Recetarios</router-link>
            </div>
          </div>
          <div class="flex items-center space-x-6">
            <div v-if="isAuthenticated" class="flex items-center space-x-6">
               <router-link to="/create-recipe" class="btn-primary">Subir Receta</router-link>
               <router-link to="/profile" class="text-stone-600 hover:text-olive-600 text-sm font-medium transition-colors">Mi Perfil</router-link>
               <button @click="logout" class="text-stone-500 hover:text-stone-800 text-sm font-medium transition-colors">Cerrar Sesión</button>
            </div>
            <div v-else class="flex items-center space-x-6">
               <router-link to="/login" class="text-stone-600 hover:text-olive-600 text-sm font-medium transition-colors">Iniciar Sesión</router-link>
               <router-link to="/register" class="btn-primary">Registrarse</router-link>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-10 sm:px-6 lg:px-8">
      <router-view></router-view>
    </main>
  </div>
</template>
