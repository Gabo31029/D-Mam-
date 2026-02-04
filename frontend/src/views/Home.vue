<script setup>
import { ref, onMounted, watch } from "vue";
import api from "../api";
import PageHeader from "../components/PageHeader.vue";
import RecipeCard from "../components/RecipeCard.vue";

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
</script>

<template>
  <div class="px-4 pb-12">
    <!-- Header & Filters -->
    <PageHeader
      title="La Cocina D'Mamá"
      description="Explora nuestra colección de sabores tradicionales."
    >
      <template #actions>
        <div class="flex gap-4 w-full sm:w-auto">
          <select
            v-model="filters.country"
            class="input-field max-w-[200px] cursor-pointer"
          >
            <option value="">Global</option>
            <option
              v-for="country in countries"
              :key="country"
              :value="country"
            >
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
      </template>
    </PageHeader>

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
      <RecipeCard v-for="recipe in recipes" :key="recipe.id" :recipe="recipe" />
    </div>
  </div>
</template>
