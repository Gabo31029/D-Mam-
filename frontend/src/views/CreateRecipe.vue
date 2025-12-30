
<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import api from '../api';

const router = useRouter();
const route = useRoute();

const isEditing = computed(() => !!route.params.id);
const recipeId = computed(() => route.params.id);

const form = ref({
    title: '',
    country: '',
    type: 'salty',
    ingredients: [{ name: '', amount: '', unit: '' }],
    instructions: '',
    instructions_format: 'numbered', // 'numbered' or 'plain'
    cookbook_id: null,
    image_url: '',
    preparation_time_minutes: 45,
    difficulty: 'medium',
    notes: ''
});
const cookbooks = ref([]);
const uploading = ref(false);
const loading = ref(false);

// Nueva referencia para pasos de instrucciones
const instructionSteps = ref(['']);

const addIngredient = () => {
    form.value.ingredients.push({ name: '', amount: '', unit: '' });
};

const removeIngredient = (index) => {
    if (form.value.ingredients.length > 1) {
        form.value.ingredients.splice(index, 1);
    }
};

const addStep = () => {
    instructionSteps.value.push('');
};

const removeStep = (index) => {
    if (instructionSteps.value.length > 1) {
        instructionSteps.value.splice(index, 1);
    }
};

const loadMyCookbooks = async () => {
    try {
        const response = await api.get('/users/me'); 
        cookbooks.value = response.data.cookbooks || []; 
    } catch (err) {
        console.error("Error loading user cookbooks", err);
    }
};

const loadRecipe = async () => {
    if (!isEditing.value) return;
    
    loading.value = true;
    try {
        const response = await api.get(`/recipes/${recipeId.value}`);
        const recipe = response.data;
        
        // Cargar datos en el formulario
        form.value = {
            title: recipe.title,
            country: recipe.country || '',
            type: recipe.type,
            ingredients: recipe.ingredients.length > 0 ? recipe.ingredients : [{ name: '', amount: '', unit: '' }],
            instructions: recipe.instructions,
            instructions_format: recipe.instructions_format,
            cookbook_id: recipe.cookbook_id,
            image_url: recipe.image_url || '',
            preparation_time_minutes: recipe.preparation_time_minutes,
            difficulty: recipe.difficulty,
            notes: recipe.notes || ''
        };

        // Inicializar pasos si es numerado
        if (form.value.instructions_format === 'numbered') {
            instructionSteps.value = recipe.instructions ? recipe.instructions.split('\n') : [''];
        }

    } catch (err) {
        console.error('Error loading recipe:', err);
        alert('Error al cargar la receta');
        router.push('/');
    } finally {
        loading.value = false;
    }
};

// Sincronizar formatos al cambiar
const setInstructionFormat = (format) => {
    if (format === form.value.instructions_format) return;
    
    if (format === 'numbered') {
        // Convertir texto plano a array
        instructionSteps.value = form.value.instructions.split('\n').filter(line => line.trim() !== '');
        if (instructionSteps.value.length === 0) instructionSteps.value.push('');
    } else {
        // Convertir array a texto plano
        form.value.instructions = instructionSteps.value.join('\n');
    }
    form.value.instructions_format = format;
};

onMounted(async () => {
    await loadMyCookbooks();
    await loadRecipe();
});

const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    uploading.value = true;
    try {
        const response = await api.post('/upload/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
        form.value.image_url = response.data.url;
    } catch (err) {
        alert('Error subiendo imagen');
    } finally {
        uploading.value = false;
    }
};

const submitRecipe = async () => {
    try {
        // Asegurar que instructions string esté actualizado si estamos en modo numerado
        if (form.value.instructions_format === 'numbered') {
            form.value.instructions = instructionSteps.value.join('\n');
        }

        if (isEditing.value) {
            await api.put(`/recipes/${recipeId.value}`, form.value);
            alert('Receta actualizada exitosamente');
        } else {
            await api.post('/recipes/', form.value);
        }
        router.push('/profile');
    } catch (err) {
        console.error('Error:', err);
        alert(isEditing.value ? 'Error actualizando receta' : 'Error creando receta');
    }
};
</script>

<template>
  <div class="min-h-screen bg-stone-50 py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto">
      
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-serif font-bold text-stone-800">
          {{ isEditing ? 'Editar Receta' : 'Crear Nueva Receta' }}
        </h1>
        <p class="text-stone-600 mt-2">Comparte tu creación culinaria con el mundo.</p>
      </div>

      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-olive-600 mx-auto"></div>
        <p class="mt-4 text-stone-500">Cargando receta...</p>
      </div>

      <form v-else @submit.prevent="submitRecipe" class="space-y-8 bg-white p-6 sm:p-8 rounded-xl shadow-sm border border-stone-200">
        
        <!-- Basic Info & Image -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <!-- Image Upload Section -->
            <div class="lg:col-span-1">
                <label class="block text-sm font-medium text-stone-700 uppercase tracking-wide mb-2">Foto del Plato</label>
                <div class="relative group aspect-square bg-stone-100 rounded-lg overflow-hidden border-2 border-dashed border-stone-300 hover:border-olive-500 transition-colors flex items-center justify-center cursor-pointer">
                    <img v-if="form.image_url" :src="form.image_url" class="absolute inset-0 w-full h-full object-cover">
                    <div v-if="!form.image_url" class="text-center p-4">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-8 h-8 mx-auto text-stone-400">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
                        </svg>
                        <span class="text-xs text-stone-500 mt-2 block">{{ uploading ? 'Subiendo...' : 'Subir Imagen' }}</span>
                    </div>
                    <input type="file" @change="handleFileUpload" accept="image/*" class="absolute inset-0 opacity-0 cursor-pointer">
                </div>
            </div>

            <!-- Main Fields -->
            <div class="lg:col-span-2 space-y-5">
                <div>
                    <label class="block text-sm font-medium text-stone-700 mb-1">Título de la Receta</label>
                    <input v-model="form.title" type="text" class="input-field" placeholder="Ej: Paella Valenciana" required>
                </div>

                <div class="grid grid-cols-2 gap-4">
                     <div>
                        <label class="block text-sm font-medium text-stone-700 mb-1">País / Región</label>
                        <input v-model="form.country" type="text" class="input-field" placeholder="Ej: España">
                    </div>
                     <div>
                        <label class="block text-sm font-medium text-stone-700 mb-1">Tipo de Plato</label>
                        <select v-model="form.type" class="input-field">
                            <option value="salty">Salado</option>
                            <option value="sweet">Dulce</option>
                        </select>
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-4">
                     <div>
                        <label class="block text-sm font-medium text-stone-700 mb-1">Tiempo (min)</label>
                        <input v-model="form.preparation_time_minutes" type="number" min="0" class="input-field">
                    </div>
                     <div>
                        <label class="block text-sm font-medium text-stone-700 mb-1">Dificultad</label>
                        <select v-model="form.difficulty" class="input-field">
                            <option value="easy">Fácil</option>
                            <option value="medium">Media</option>
                            <option value="hard">Difícil</option>
                        </select>
                    </div>
                </div>
            </div>
        </div>

        <hr class="border-stone-100">

        <!-- Ingredients -->
        <div>
            <div class="flex items-center justify-between mb-2">
                <label class="block text-sm font-medium text-stone-700 uppercase tracking-wide">Ingredientes</label>
            </div>
            
            <div class="space-y-3">
                <div v-for="(ingredient, index) in form.ingredients" :key="index" class="flex gap-2 items-start animate-fade-in-up">
                    <div class="grid grid-cols-6 gap-2 flex-grow">
                        <input v-model="ingredient.amount" placeholder="Cant." class="input-field col-span-1">
                        <input v-model="ingredient.unit" placeholder="Unidad" class="input-field col-span-1">
                        <input v-model="ingredient.name" placeholder="Nombre del ingrediente" class="input-field col-span-4">
                    </div>
                    <button type="button" @click="removeIngredient(index)" class="mt-2 text-stone-400 hover:text-red-500 transition-colors bg-stone-50 p-1 rounded-md" title="Eliminar ingrediente">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
            </div>
            
            <button type="button" @click="addIngredient" class="text-sm text-olive-600 font-medium hover:text-olive-700 mt-2 flex items-center gap-1">
                <span class="text-lg leading-none">+</span> Agregar Ingrediente
            </button>
        </div>

        <!-- Instructions -->
        <div>
            <div class="flex items-center justify-between mb-2">
                <label class="block text-sm font-medium text-stone-700 uppercase tracking-wide">Instrucciones</label>
                
                 <!-- Format Toggle (Moved up) -->
                 <div class="flex gap-2">
                    <button 
                        type="button"
                        @click="setInstructionFormat('numbered')"
                        :class="[
                            'px-3 py-1 text-xs font-medium rounded-md transition-all flex items-center gap-1',
                            form.instructions_format === 'numbered' 
                                ? 'bg-olive-600 text-white' 
                                : 'bg-stone-100 text-stone-600 hover:bg-stone-200'
                        ]"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-3 h-3">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M8.242 5.992h12m-12 6.003H20.24m-12 5.999h12M4.117 7.495v-3.75H2.99m1.125 3.75H2.99m1.125 0H5.24m-1.92 2.577a1.125 1.125 0 111.591 1.59l-1.83 1.83h2.16M2.99 15.745h1.125a1.125 1.125 0 010 2.25H3.74m0-.002h.375a1.125 1.125 0 010 2.25H2.99" />
                        </svg>
                        Pasos
                    </button>
                    <button 
                        type="button"
                        @click="setInstructionFormat('plain')"
                        :class="[
                            'px-3 py-1 text-xs font-medium rounded-md transition-all flex items-center gap-1',
                            form.instructions_format === 'plain' 
                                ? 'bg-olive-600 text-white' 
                                : 'bg-stone-100 text-stone-600 hover:bg-stone-200'
                        ]"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-3 h-3">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 12h16.5m-16.5 3.75h16.5M3.75 19.5h16.5M5.625 4.5h12.75a1.875 1.875 0 010 3.75H5.625a1.875 1.875 0 010-3.75z" />
                        </svg>
                        Texto
                    </button>
                </div>
            </div>

            <!-- Numbered Steps Interface -->
            <div v-if="form.instructions_format === 'numbered'" class="space-y-3">
                 <div v-for="(step, index) in instructionSteps" :key="index" class="flex gap-3 items-start animate-fade-in-up">
                     <span class="mt-3 text-stone-400 font-serif font-bold text-sm w-6 text-right select-none">{{ index + 1 }}.</span>
                     <div class="flex-grow">
                         <textarea 
                             v-model="instructionSteps[index]" 
                             placeholder="Describe este paso..." 
                             class="input-field py-2 min-h-[50px] resize-y" 
                             rows="2"
                         ></textarea>
                     </div>
                     <button type="button" @click="removeStep(index)" class="mt-3 text-stone-400 hover:text-red-500 transition-colors" title="Eliminar paso">
                         <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                         </svg>
                     </button>
                 </div>
                 <button type="button" @click="addStep" class="text-sm text-olive-600 font-medium hover:text-olive-700 mt-2 flex items-center gap-1">
                    <span class="text-lg leading-none">+</span> Agregar Paso
                 </button>
            </div>

            <!-- Plain Text Interface -->
            <div v-else>
                 <textarea v-model="form.instructions" class="input-field min-h-[200px] leading-relaxed" required placeholder="Describe el proceso de preparación paso a paso..."></textarea>
                 <p class="text-xs text-stone-400 mt-1 italic">Escribe cada paso en una nueva línea.</p>
            </div>
        </div>

        <!-- Organization -->
        <div class="bg-stone-50 p-6 rounded-md border border-stone-100">
            <label class="block text-sm font-medium text-stone-700 mb-2 uppercase tracking-wide">Añadir a Recetario (Opcional)</label>
            <select v-model="form.cookbook_id" class="input-field bg-white cursor-pointer">
                <option :value="null">Ninguno (Receta suelta)</option>
                <option v-for="book in cookbooks" :key="book.id" :value="book.id">{{ book.title }}</option>
            </select>
        </div>

         <!-- Notes -->
        <div>
            <label class="block text-sm font-medium text-stone-700 mb-2 uppercase tracking-wide">Notas del Chef (Opcional)</label>
            <textarea v-model="form.notes" class="input-field min-h-[80px]" placeholder="Trucos, variaciones, historia..."></textarea>
        </div>

        <div class="pt-4">
            <button type="submit" class="btn-primary w-full py-3 text-base shadow-sm hover:shadow-md transition-shadow">
                {{ isEditing ? 'Actualizar Receta' : 'Publicar Receta' }}
            </button>
        </div>
    </form>
    </div>
  </div>
</template>
