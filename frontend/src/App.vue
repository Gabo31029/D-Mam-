<script setup>
import { onMounted, ref } from "vue";
import { useAuth } from "./composables/useAuth";

const { isAuthenticated, logout, loadUser } = useAuth();
const isMobileMenuOpen = ref(false);

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false;
};

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
            <router-link
              to="/"
              class="flex-shrink-0 flex items-center group"
              @click="closeMobileMenu"
            >
              <!-- Logo text: Serif, solid color, minimal -->
              <span
                class="text-3xl font-serif font-bold text-olive-700 tracking-tight group-hover:text-olive-600 transition-colors"
                >D'Mamá</span
              >
            </router-link>
            <div class="hidden sm:ml-10 sm:flex sm:space-x-8">
              <router-link
                to="/"
                class="text-stone-600 hover:text-olive-600 px-1 py-2 text-sm font-medium transition-colors border-b-2 border-transparent hover:border-olive-600"
                >Inicio</router-link
              >
              <router-link
                to="/cookbooks"
                class="text-stone-600 hover:text-olive-600 px-1 py-2 text-sm font-medium transition-colors border-b-2 border-transparent hover:border-olive-600"
                >Recetarios</router-link
              >
            </div>
          </div>

          <!-- Desktop Menu -->
          <div class="hidden sm:flex items-center space-x-6">
            <div v-if="isAuthenticated" class="flex items-center space-x-6">
              <router-link to="/create-recipe" class="btn-primary"
                >Subir Receta</router-link
              >
              <router-link
                to="/profile"
                class="text-stone-600 hover:text-olive-600 text-sm font-medium transition-colors"
                >Mi Perfil</router-link
              >
              <button
                @click="logout"
                class="text-stone-500 hover:text-stone-800 text-sm font-medium transition-colors"
              >
                Cerrar Sesión
              </button>
            </div>
            <div v-else class="flex items-center space-x-6">
              <router-link
                to="/login"
                class="text-stone-600 hover:text-olive-600 text-sm font-medium transition-colors"
                >Iniciar Sesión</router-link
              >
              <router-link to="/register" class="btn-primary"
                >Registrarse</router-link
              >
            </div>
          </div>

          <!-- Mobile Menu Button -->
          <div class="flex items-center sm:hidden">
            <button
              @click="toggleMobileMenu"
              class="inline-flex items-center justify-center p-2 rounded-md text-stone-400 hover:text-stone-500 hover:bg-stone-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-olive-500"
            >
              <span class="sr-only">Abrir menú principal</span>
              <!-- Icon when menu is closed -->
              <svg
                v-if="!isMobileMenuOpen"
                class="block h-6 w-6"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
              <!-- Icon when menu is open -->
              <svg
                v-else
                class="block h-6 w-6"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Mobile Menu -->
      <div
        v-if="isMobileMenuOpen"
        class="sm:hidden bg-white border-b border-stone-200"
      >
        <div class="pt-2 pb-3 space-y-1">
          <router-link
            to="/"
            @click="closeMobileMenu"
            class="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-stone-600 hover:bg-stone-50 hover:border-olive-500 hover:text-olive-700"
            >Inicio</router-link
          >
          <router-link
            to="/cookbooks"
            @click="closeMobileMenu"
            class="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-stone-600 hover:bg-stone-50 hover:border-olive-500 hover:text-olive-700"
            >Recetarios</router-link
          >
        </div>
        <div class="pt-4 pb-4 border-t border-stone-200">
          <div v-if="isAuthenticated" class="space-y-1">
            <router-link
              to="/create-recipe"
              @click="closeMobileMenu"
              class="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-stone-600 hover:bg-stone-50 hover:border-olive-500 hover:text-olive-700"
              >Subir Receta</router-link
            >
            <router-link
              to="/profile"
              @click="closeMobileMenu"
              class="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-stone-600 hover:bg-stone-50 hover:border-olive-500 hover:text-olive-700"
              >Mi Perfil</router-link
            >
            <button
              @click="
                () => {
                  logout();
                  closeMobileMenu();
                }
              "
              class="block w-full text-left pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-stone-600 hover:bg-stone-50 hover:border-olive-500 hover:text-olive-700"
            >
              Cerrar Sesión
            </button>
          </div>
          <div v-else class="space-y-1">
            <router-link
              to="/login"
              @click="closeMobileMenu"
              class="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-stone-600 hover:bg-stone-50 hover:border-olive-500 hover:text-olive-700"
              >Iniciar Sesión</router-link
            >
            <router-link
              to="/register"
              @click="closeMobileMenu"
              class="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-stone-600 hover:bg-stone-50 hover:border-olive-500 hover:text-olive-700"
              >Registrarse</router-link
            >
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-10 sm:px-6 lg:px-8">
      <router-view></router-view>
    </main>
  </div>
</template>
