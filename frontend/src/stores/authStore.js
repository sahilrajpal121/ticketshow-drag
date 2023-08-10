import { defineStore } from 'pinia';
import jwtDecode from 'jwt-decode'; // A library to decode JWT tokens

export const useAuthStore = defineStore('auth', {
    state: () => {
        return { token: null }
    },
    persist: true,
    getters: {
        isAuthenticated: (state) => state.token !== null && !this.isTokenExpired(state.token),
    },
    actions: {
        setToken(token) {
            console.log('token set from pinia')
            this.token = token;
        },
        clearToken() {
            console.log('token cleared from pinia')
            this.token = null;
        },
        isTokenExpired(token) {
            const decodedToken = jwtDecode(token);
            const currentTime = Date.now() / 1000;
            console.log('token expired from pinia', decodedToken.exp < currentTime) // Get current time in seconds
            return decodedToken.exp < currentTime;
        },
        getToken() {
            if (this.token !== null && !this.isTokenExpired(this.token)) {
                console.log('token is fine')
                return this.token;
            }
            else {
                console.log('token is not fine')
                this.token = null;
                return null;
            }

        }
    },

});
