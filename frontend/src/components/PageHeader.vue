<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    default: "",
  },
});
</script>

<template>
  <div class="mb-12 border-b border-stone-200 pb-8">
    <div class="flex flex-col sm:flex-row gap-6 justify-between items-end">
      <div>
        <h1
          class="text-3xl sm:text-4xl font-serif font-bold text-stone-900 mb-2"
        >
          {{ title }}
        </h1>
        <p v-if="description" class="text-stone-500 font-light text-lg">
          {{ description }}
        </p>
        <slot name="description"></slot>
      </div>
      <div v-if="$slots.actions" class="w-full sm:w-auto">
        <slot name="actions"></slot>
      </div>
    </div>
  </div>
</template>
