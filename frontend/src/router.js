
import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import Cookbooks from './views/Cookbooks.vue'
import CookbookDetail from './views/CookbookDetail.vue'
import CreateRecipe from './views/CreateRecipe.vue'

import RecipeDetail from './views/RecipeDetail.vue'

import UserProfile from './views/UserProfile.vue'
import CreateCookbook from './views/CreateCookbook.vue'

const routes = [
    { path: '/', component: Home, name: 'Home' },
    { path: '/login', component: Login, name: 'Login' },
    { path: '/register', component: Register, name: 'Register' },
    { path: '/cookbooks', component: Cookbooks, name: 'Cookbooks' },
    { path: '/cookbooks/:id', component: CookbookDetail, name: 'CookbookDetail', props: true },
    { path: '/cookbooks/:id/edit', component: CreateCookbook, name: 'EditCookbook', props: true, meta: { requiresAuth: true } },
    { path: '/recipes/:id', component: RecipeDetail, name: 'RecipeDetail', props: true },
    { path: '/recipes/:id/edit', component: CreateRecipe, name: 'EditRecipe', props: true, meta: { requiresAuth: true } },
    { path: '/create-recipe', component: CreateRecipe, name: 'CreateRecipe', meta: { requiresAuth: true } },
    { path: '/profile', component: UserProfile, name: 'UserProfile', meta: { requiresAuth: true } },
    { path: '/create-cookbook', component: CreateCookbook, name: 'CreateCookbook', meta: { requiresAuth: true } },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

router.beforeEach((to, from, next) => {
    const isAuthenticated = !!localStorage.getItem('token')
    if (to.meta.requiresAuth && !isAuthenticated) {
        next('/login')
    } else {
        next()
    }
})

export default router
