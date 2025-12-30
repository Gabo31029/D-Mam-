

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '../composables/useAuth';

const username = ref('');
const password = ref('');
const error = ref('');
const router = useRouter();
const { login } = useAuth();

const handleLogin = async () => {
  error.value = '';
  const result = await login(username.value, password.value);
  
  if (result.success) {
    router.push('/');
  } else {
    error.value = result.error;
  }
};
</script>


<template>
  <div class="flex justify-center items-center h-[80vh]">
    <div class="card w-full max-w-md p-10 border border-stone-200 shadow-none">
      <h2 class="text-3xl font-serif font-bold text-center mb-8 text-stone-900">Bienvenido de nuevo</h2>
      <p class="text-center text-stone-500 mb-6 -mt-6">Tu libro de cocina personal te espera.</p>
      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-stone-700 mb-2">Usuario</label>
          <input v-model="username" type="text" class="input-field" required autocomplete="username" />
        </div>
        <div>
          <label class="block text-sm font-medium text-stone-700 mb-2">Contraseña</label>
          <input v-model="password" type="password" class="input-field" required autocomplete="current-password" />
        </div>
        <div v-if="error" class="text-terracotta-500 text-sm text-center">{{ error }}</div>
        <button type="submit" class="w-full btn-primary py-3 text-base">Iniciar Sesión</button>
      </form>
      <div class="mt-6 text-center">
        <router-link to="/register" class="text-sm text-olive-600 hover:text-olive-800 font-medium transition-colors">¿No tienes cuenta? Regístrate</router-link>
      </div>
    </div>
  </div>
</template>
