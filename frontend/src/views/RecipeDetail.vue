<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuth } from "../composables/useAuth";
import api from "../api";

const route = useRoute();
const router = useRouter();
const { user } = useAuth();

const recipe = ref(null);
const loading = ref(true);

const isOwner = computed(() => {
  return user.value && recipe.value && user.value.id === recipe.value.owner_id;
});

const downloadPdf = async () => {
  try {
    const response = await api.get(`/recipes/${route.params.id}/pdf`, {
      responseType: "blob",
    });
    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `${recipe.value.title}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  } catch (err) {
    console.error("Error downloading PDF", err);
    alert("Error al generar PDF");
  }
};

onMounted(async () => {
  try {
    const response = await api.get(`/recipes/${route.params.id}`);
    recipe.value = response.data;
  } catch (err) {
    console.error("Error loading recipe", err);
  } finally {
    loading.value = false;
  }
});

const deleteRecipe = async () => {
  if (
    !confirm(
      "¿Estás seguro de que quieres eliminar esta receta? Esta acción no se puede deshacer.",
    )
  )
    return;

  try {
    await api.delete(`/recipes/${recipe.value.id}`);
    router.push("/profile");
  } catch (err) {
    console.error("Error deleting recipe", err);
    alert("Error al eliminar la receta");
  }
};

const translateType = (type) => {
  const types = {
    salty: "Salado",
    sweet: "Dulce",
  };
  return types[type] || type; // Fallback to original if not found
};

const translateDifficulty = (difficulty) => {
  const levels = {
    easy: "Fácil",
    medium: "Media",
    hard: "Difícil",
    chef: "Chef",
  };
  return levels[difficulty] || difficulty;
};
</script>

<template>
  <div v-if="loading" class="text-center py-20">
    <div class="animate-pulse text-stone-400 font-serif text-lg">
      Cargando receta...
    </div>
  </div>

  <div v-else-if="recipe" class="max-w-4xl mx-auto px-4 pb-20">
    <!-- Hero Section -->
    <div class="mb-10 text-center">
      <div class="flex items-center justify-center gap-2 mb-4">
        <span
          class="inline-block px-3 py-1 text-xs font-medium tracking-widest text-olive-700 bg-olive-50 rounded-full border border-olive-100 uppercase"
          >{{ recipe.country || "Internacional" }}</span
        >
        <span
          class="inline-block px-3 py-1 text-xs font-medium tracking-widest text-stone-600 bg-stone-100 rounded-full border border-stone-200 uppercase"
          >{{ translateType(recipe.type) }}</span
        >
      </div>
      <h1
        class="text-3xl sm:text-5xl font-serif font-bold text-stone-900 mb-4 leading-tight"
      >
        {{ recipe.title }}
      </h1>

      <div
        class="flex items-center justify-center gap-6 text-stone-500 text-sm font-medium tracking-wide mb-6"
      >
        <span class="flex items-center gap-2">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="w-5 h-5 text-olive-600"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          {{ recipe.preparation_time_minutes }} min
        </span>
        <span class="flex items-center gap-2">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="w-5 h-5 text-olive-600"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z"
            />
          </svg>
          {{ translateDifficulty(recipe.difficulty) }}
        </span>
        <span class="flex items-center gap-2">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="w-5 h-5 text-olive-600"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5"
            />
          </svg>
          {{ new Date(recipe.created_at).toLocaleDateString() }}
        </span>
      </div>

      <!-- Author Info -->
      <div v-if="recipe.owner" class="mb-6">
        <p class="text-stone-600 text-sm">
          Por
          <span class="font-semibold text-olive-700">{{
            recipe.owner.username
          }}</span>
        </p>
      </div>

      <div class="flex gap-3 justify-center mb-6">
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
          Descargar PDF
        </button>

        <button
          v-if="isOwner"
          @click="$router.push(`/recipes/${recipe.id}/edit`)"
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
          Editar Receta
        </button>

        <button
          v-if="isOwner"
          @click="deleteRecipe"
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

      <div class="h-1 w-24 bg-terracotta-500 mx-auto rounded-full mt-8"></div>
    </div>

    <!-- Main Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-12">
      <!-- Ingredients Sidebar -->
      <div class="lg:col-span-4 order-2 lg:order-1">
        <div
          class="bg-stone-50 p-8 rounded-lg border border-stone-200 sticky top-24"
        >
          <h3
            class="font-serif text-2xl font-bold text-stone-800 mb-6 border-b border-stone-200 pb-2"
          >
            Ingredientes
          </h3>
          <div class="prose prose-stone prose-sm">
            <ul class="list-none space-y-3 p-0 m-0">
              <!-- Handle array of ingredients -->
              <template v-if="Array.isArray(recipe.ingredients)">
                <li
                  v-for="(ing, index) in recipe.ingredients"
                  :key="index"
                  class="flex items-start text-stone-700 leading-relaxed justify-between border-b border-stone-100 pb-2 last:border-0"
                >
                  <div class="flex items-start">
                    <span class="text-terracotta-500 mr-2 mt-1.5 text-xs"
                      >●</span
                    >
                    <span class="font-medium">{{ ing.name }}</span>
                  </div>
                  <div
                    class="text-stone-500 text-xs font-mono ml-4 text-right whitespace-nowrap"
                  >
                    {{ ing.amount }} {{ ing.unit }}
                  </div>
                </li>
              </template>
              <!-- Fallback for legacy string data if any -->
              <template v-else>
                <li
                  v-for="(line, index) in (recipe.ingredients || '').split(
                    '\n',
                  )"
                  :key="index"
                  class="flex items-start text-stone-700 leading-relaxed"
                >
                  <span class="text-terracotta-500 mr-2 mt-1.5 text-xs">●</span>
                  {{ line }}
                </li>
              </template>
            </ul>
          </div>
        </div>
      </div>

      <!-- Instructions & Image -->
      <div class="lg:col-span-8 order-1 lg:order-2">
        <!-- Image -->
        <div
          v-if="recipe.image_url"
          class="mb-10 rounded-xl overflow-hidden border border-stone-200 shadow-sm aspect-video"
        >
          <img
            :src="recipe.image_url"
            class="w-full h-full object-cover"
            :alt="recipe.title"
          />
        </div>

        <!-- Notes Block -->
        <div
          v-if="recipe.notes"
          class="mb-10 p-6 bg-stone-50 border-l-4 border-olive-400 rounded-r-md"
        >
          <h4 class="font-serif font-bold text-stone-800 mb-2">
            Notas del Chef:
          </h4>
          <p class="text-stone-600 italic">{{ recipe.notes }}</p>
        </div>

        <!-- Instructions -->
        <div class="prose prose-stone max-w-none">
          <h3 class="font-serif text-3xl font-bold text-stone-800 mb-6">
            Preparación
          </h3>

          <!-- Numbered Steps (if format is 'numbered') -->
          <div
            v-if="recipe.instructions_format === 'numbered'"
            class="space-y-6"
          >
            <div
              v-for="(step, index) in recipe.instructions.split('\n')"
              :key="index"
              class="flex gap-4"
            >
              <div
                class="flex-shrink-0 w-8 h-8 rounded-full bg-olive-100 text-olive-700 flex items-center justify-center font-bold font-serif"
              >
                {{ index + 1 }}
              </div>
              <p class="text-stone-700 text-lg leading-relaxed mt-0.5">
                {{ step }}
              </p>
            </div>
          </div>

          <!-- Plain Text (if format is 'plain') -->
          <div v-else class="space-y-4">
            <p
              v-for="(step, index) in recipe.instructions.split('\n')"
              :key="index"
              class="text-stone-700 text-lg leading-relaxed"
            >
              {{ step }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="text-center py-20">
    <h2 class="text-2xl font-serif text-stone-400">Receta no encontrada</h2>
    <router-link
      to="/"
      class="text-olive-600 hover:text-olive-800 underline mt-4 inline-block"
      >Volver al inicio</router-link
    >
  </div>
</template>
