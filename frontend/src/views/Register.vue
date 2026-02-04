<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "../composables/useAuth";

const username = ref("");
const email = ref("");
const password = ref("");
const error = ref("");
const isLoading = ref(false);
const router = useRouter();
const { register } = useAuth();

const handleRegister = async () => {
  console.log("Register attempt started");
  error.value = "";
  isLoading.value = true;

  try {
    console.log("Sending request to /register");
    const result = await register(username.value, email.value, password.value);

    if (result.success) {
      console.log("Registration and login successful");
      router.push("/");
    } else {
      error.value = result.error;
    }
  } catch (err) {
    console.error("Registration failed:", err);
    error.value = "Error inesperado al registrarse";
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="flex justify-center items-center h-[80vh] px-4">
    <div
      class="card w-full max-w-md p-6 sm:p-10 border border-stone-200 shadow-none"
    >
      <h2
        class="text-2xl sm:text-3xl font-serif font-bold text-center mb-8 text-stone-900"
      >
        Crear Cuenta
      </h2>
      <form @submit.prevent="handleRegister" class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-stone-700 mb-2"
            >Usuario</label
          >
          <input
            v-model="username"
            type="text"
            class="input-field"
            required
            autocomplete="username"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-stone-700 mb-2"
            >Email</label
          >
          <input
            v-model="email"
            type="email"
            class="input-field"
            required
            autocomplete="email"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-stone-700 mb-2"
            >Contraseña</label
          >
          <input
            v-model="password"
            type="password"
            class="input-field"
            required
            autocomplete="new-password"
          />
        </div>
        <div v-if="error" class="text-terracotta-500 text-sm text-center">
          {{ error }}
        </div>
        <button
          type="submit"
          class="w-full btn-primary py-3 text-base disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="isLoading"
        >
          <span v-if="isLoading">Registrando...</span>
          <span v-else>Registrarse</span>
        </button>
      </form>
      <div class="mt-6 text-center">
        <router-link
          to="/login"
          class="text-sm text-olive-600 hover:text-olive-800 font-medium transition-colors"
          >¿Ya tienes cuenta? Inicia Sesión</router-link
        >
      </div>
    </div>
  </div>
</template>
