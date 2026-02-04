<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuth } from "../composables/useAuth";
import api from "../api";

const route = useRoute();
const router = useRouter();
const { user } = useAuth();

const cookbook = ref(null);

const isOwner = computed(() => {
  return (
    user.value && cookbook.value && user.value.id === cookbook.value.owner_id
  );
});

const downloadPdf = async () => {
  try {
    const response = await api.get(`/cookbooks/${route.params.id}/pdf`);
    const url = response.data.url;
    window.open(url, "_blank");
  } catch (err) {
    console.error("Error downloading PDF", err);
    alert("Error al generar PDF");
  }
};

const translateType = (type) => {
  const types = {
    salty: "Salado",
    sweet: "Dulce",
  };
  return types[type] || type;
};

const deleteCookbook = async () => {
  if (
    !confirm(
      "¿Estás seguro de que quieres eliminar este recetario? Las recetas seguirán existiendo fuera de la colección.",
    )
  )
    return;

  try {
    await api.delete(`/cookbooks/${cookbook.value.id}`);
    router.push("/profile");
  } catch (err) {
    console.error("Error deleting cookbook", err);
    alert("Error al eliminar el recetario");
  }
};

onMounted(async () => {
  try {
    const response = await api.get(`/cookbooks/${route.params.id}`);
    cookbook.value = response.data;
  } catch (err) {
    console.error("Error loading cookbook", err);
  }
});
</script>

<template>
  <div v-if="cookbook" class="px-4 pb-12">
    <!-- Editorial Header -->
    <div class="mb-12 border-b border-stone-200 pb-8 text-center sm:text-left">
      <h1 class="text-3xl sm:text-5xl font-serif font-bold text-stone-900 mb-4">
        {{ cookbook.title }}
      </h1>
      <p
        class="text-xl text-stone-500 font-light max-w-3xl leading-relaxed mb-6"
      >
        {{ cookbook.description }}
      </p>

      <!-- Author Info -->
      <p v-if="cookbook.owner" class="text-sm text-stone-600 mb-6">
        Curado por
        <span class="font-semibold text-olive-700">{{
          cookbook.owner.username
        }}</span>
      </p>

      <div class="flex gap-3 justify-center sm:justify-start flex-wrap">
        <button
          @click="downloadPdf"
          class="inline-flex items-center gap-2 px-6 py-2 bg-stone-800 text-white rounded-full text-sm font-medium hover:bg-stone-700 transition-colors shadow-sm focus:ring-2 focus:ring-offset-2 focus:ring-stone-500"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="w-4 h-4"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3"
            />
          </svg>
          Descargar Recetario
        </button>

        <button
          v-if="isOwner"
          @click="$router.push(`/cookbooks/${cookbook.id}/edit`)"
          class="inline-flex items-center gap-2 px-6 py-2 bg-olive-600 text-white rounded-full text-sm font-medium hover:bg-olive-700 transition-colors shadow-sm focus:ring-2 focus:ring-offset-2 focus:ring-olive-500"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="w-4 h-4"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10"
            />
          </svg>
          Editar Recetario
        </button>

        <button
          v-if="isOwner"
          @click="deleteCookbook"
          class="inline-flex items-center gap-2 px-6 py-2 bg-red-50 text-red-600 border border-red-200 rounded-full text-sm font-medium hover:bg-red-100 transition-colors shadow-sm focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="w-4 h-4"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0"
            />
          </svg>
          Eliminar
        </button>
      </div>
    </div>

    <div class="flex items-center justify-between mb-8">
      <h2 class="text-2xl font-serif font-bold text-stone-800">
        Recetas en esta colección
      </h2>
      <!-- Decorative line or counter could go here -->
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <div
        v-for="recipe in cookbook.recipes"
        :key="recipe.id"
        class="card group p-8 border border-stone-200 hover:border-olive-500/50 transition-all duration-300 relative overflow-hidden cursor-pointer"
        @click="$router.push(`/recipes/${recipe.id}`)"
      >
        <!-- Top accent -->
        <div
          class="absolute top-0 left-0 w-full h-1 bg-stone-100 group-hover:bg-olive-500 transition-colors"
        ></div>

        <h3
          class="text-2xl font-serif font-bold text-stone-900 mb-3 group-hover:text-olive-700 transition-colors mt-2"
        >
          {{ recipe.title }}
        </h3>

        <div class="flex items-center justify-between mt-6">
          <span
            class="text-xs uppercase tracking-widest font-medium text-stone-400 border border-stone-200 px-2 py-1 rounded"
            >{{ translateType(recipe.type) }}</span
          >
          <span
            class="text-stone-400 text-sm group-hover:text-olive-600 transition-colors"
            >&rarr;</span
          >
        </div>
      </div>
      <div
        v-if="!cookbook.recipes || cookbook.recipes.length === 0"
        class="col-span-full py-16 text-center bg-stone-50 rounded-lg border border-dashed border-stone-200"
      >
        <p class="text-stone-400 font-serif italic text-lg">
          Este recetario aún no tiene páginas escritas.
        </p>
      </div>
    </div>
  </div>
</template>
