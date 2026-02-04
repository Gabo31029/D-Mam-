<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";

const props = defineProps({
  recipe: {
    type: Object,
    required: true,
  },
});

const router = useRouter();

const translateType = (type) => {
  const types = {
    salty: "Salado",
    sweet: "Dulce",
  };
  return types[type] || type;
};

const displayCountry = computed(() => props.recipe.country || "Internacional");
</script>

<template>
  <div
    class="card group cursor-pointer hover:-translate-y-1 transition-all duration-300 bg-white rounded-lg shadow-sm border border-stone-200 overflow-hidden"
    @click="router.push(`/recipes/${recipe.id}`)"
  >
    <!-- Image Area -->
    <div
      class="h-64 w-full overflow-hidden border-b border-stone-100 relative bg-stone-100"
    >
      <img
        v-if="recipe.image_url"
        :src="recipe.image_url"
        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-out"
        :alt="recipe.title"
      />
      <div
        v-else
        class="w-full h-full flex items-center justify-center text-stone-400 font-serif italic text-lg"
      >
        Sin Imagen
      </div>
      <!-- Type Badge -->
      <div
        class="absolute top-4 right-4 px-3 py-1 bg-white/95 backdrop-blur-sm border border-stone-200 text-xs font-medium text-olive-700 uppercase tracking-wider shadow-sm rounded-sm"
      >
        {{ translateType(recipe.type) }}
      </div>
    </div>

    <!-- Content Area -->
    <div class="p-6">
      <div class="mb-3 flex items-center justify-between">
        <span
          class="text-xs font-bold tracking-widest text-stone-400 uppercase"
        >
          {{ displayCountry }}
        </span>
      </div>
      <h3
        class="text-xl font-serif font-bold text-stone-900 mb-3 leading-tight group-hover:text-olive-700 transition-colors"
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
        >
          Ver Receta &rarr;
        </span>
      </div>
    </div>
  </div>
</template>
