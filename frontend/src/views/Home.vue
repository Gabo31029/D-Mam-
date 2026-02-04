<script setup>
import { ref, onMounted, watch } from "vue";
import api from "../api";

const recipes = ref([]);
const filters = ref({
  country: "",
  type: "",
});

const loadRecipes = async () => {
  let url = "/recipes/";
  const params = [];
  if (filters.value.country) params.push(`country=${filters.value.country}`);
  if (filters.value.type) params.push(`type=${filters.value.type}`);
  if (params.length) url += `?${params.join("&")}`;

  try {
    const response = await api.get(url);
    recipes.value = response.data;
  } catch (err) {
    console.error("Error loading recipes", err);
  }
};

const countries = ref([]);

const loadCountries = async () => {
  try {
    const response = await api.get("/recipes/countries");
    countries.value = response.data;
  } catch (err) {
    console.error("Error loading countries", err);
  }
};

watch(filters, loadRecipes, { deep: true });

onMounted(() => {
  loadRecipes();
  loadCountries();
});

const translateType = (type) => {
  const types = {
    salty: "Salado",
    sweet: "Dulce",
  };
  return types[type] || type;
};
</script>

<template>
  <div class="px-4 pb-12">
    <!-- Header & Filters -->
    <div
      class="mb-12 flex flex-col sm:flex-row gap-6 justify-between items-end border-b border-stone-200 pb-6"
    >
      <div>
        <h1 class="text-4xl font-serif font-bold text-stone-900 mb-2">
          La Cocina D'Mamá
        </h1>
        <p class="text-stone-500 font-light">
          Explora nuestra colección de sabores tradicionales.
        </p>
      </div>
      <div class="flex gap-4 w-full sm:w-auto">
        <select
          v-model="filters.country"
          class="input-field max-w-[200px] cursor-pointer"
        >
          <option value="">Global</option>
          <option v-for="country in countries" :key="country" :value="country">
            {{ country }}
          </option>
        </select>
        <select
          v-model="filters.type"
          class="input-field max-w-[200px] cursor-pointer"
        >
          <option value="">Todos los Tipos</option>
          <option value="sweet">Dulce</option>
          <option value="salty">Salado</option>
        </select>
      </div>
    </div>

    <!-- Empty State -->
    <div
      v-if="recipes.length === 0"
      class="text-center py-20 bg-stone-50 rounded-lg border border-dashed border-stone-300"
    >
      <p class="text-xl font-serif text-stone-500 italic">
        No se encontraron recetas para tu búsqueda.
      </p>
    </div>

    <!-- Recipe Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <div
        v-for="recipe in recipes"
        :key="recipe.id"
        class="card group cursor-pointer hover:-translate-y-1 transition-all duration-300"
        @click="$router.push(`/recipes/${recipe.id}`)"
      >
        <!-- Image Area -->
        <div
          class="h-64 w-full overflow-hidden border-b border-stone-100 relative bg-stone-100"
        >
          <img
            v-if="recipe.image_url"
            :src="recipe.image_url"
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-out"
            alt="Recipe Image"
          />
          <div
            v-else
            class="w-full h-full flex items-center justify-center text-stone-400 font-serif italic text-lg"
          >
            Sin Imagen
          </div>
          <!-- Type Badge -->
          <div
            class="absolute top-4 right-4 px-3 py-1 bg-white/95 backdrop-blur-sm border border-stone-200 text-xs font-medium text-olive-700 uppercase tracking-wider shadow-sm"
          >
            {{ translateType(recipe.type) }}
          </div>
        </div>

        <!-- Content Area -->
        <div class="p-6">
          <div class="mb-3 flex items-center justify-between">
            <span
              class="text-xs font-bold tracking-widest text-stone-400 uppercase"
              >{{ recipe.country || "Internacional" }}</span
            >
          </div>
          <h3
            class="text-2xl font-serif font-bold text-stone-900 mb-3 leading-tight group-hover:text-olive-700 transition-colors"
          >
            {{ recipe.title }}
          </h3>

          <!-- Author Info -->
          <p v-if="recipe.owner" class="text-xs text-stone-500 mb-2">
            Por
            <span class="font-semibold text-olive-600">{{
              recipe.owner.username
            }}</span>
          </p>

          <div
            class="mt-4 pt-4 border-t border-stone-100 flex justify-between items-center"
          >
            <span
              class="text-xs text-stone-500 font-medium group-hover:text-terracotta-600 transition-colors uppercase tracking-widest"
              >Ver Receta &rarr;</span
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
