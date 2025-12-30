import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';

// Estado global reactivo para la autenticación
const token = ref(localStorage.getItem('token'));
const user = ref(null);

export function useAuth() {
    const router = useRouter();

    const isAuthenticated = computed(() => !!token.value);

    const login = async (username, password) => {
        try {
            const formData = new FormData();
            formData.append('username', username);
            formData.append('password', password);

            const response = await api.post('/token', formData);
            const accessToken = response.data.access_token;

            // Guardar token en localStorage y estado reactivo
            localStorage.setItem('token', accessToken);
            token.value = accessToken;

            // Cargar información del usuario
            await loadUser();

            return { success: true };
        } catch (error) {
            console.error('Login error:', error);
            return {
                success: false,
                error: error.response?.data?.detail || 'Credenciales inválidas'
            };
        }
    };

    const register = async (username, email, password) => {
        try {
            await api.post('/register', { username, email, password });
            // Después de registrarse, hacer login automáticamente
            return await login(username, password);
        } catch (error) {
            console.error('Register error:', error);
            return {
                success: false,
                error: error.response?.data?.detail || 'Error al registrarse'
            };
        }
    };

    const logout = () => {
        localStorage.removeItem('token');
        token.value = null;
        user.value = null;
        router.push('/login');
    };

    const loadUser = async () => {
        if (!token.value) {
            user.value = null;
            return;
        }

        try {
            const response = await api.get('/users/me');
            user.value = response.data;
        } catch (error) {
            console.error('Error loading user:', error);
            // Si falla la carga del usuario, probablemente el token es inválido
            if (error.response?.status === 401) {
                logout();
            }
        }
    };

    return {
        isAuthenticated,
        user,
        login,
        register,
        logout,
        loadUser
    };
}
