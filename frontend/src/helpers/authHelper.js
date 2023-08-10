import jwtDecode from 'jwt-decode';
import { useAuthStore } from '../stores/authStore';

export function isAdmin() {
  const authStore = useAuthStore();
  const token = authStore.getToken();
  if (!token) {
    return false;
  }
  const decodedToken = jwtDecode(token);
  return decodedToken.roles.includes('admin');
}

export function getToken(){
    const authStore = useAuthStore();
    return authStore.getToken();
}

export function logout(){
    const authStore = useAuthStore();
    authStore.clearToken();
    window.location.href = '/';

}

export function setToken(token){
    const authStore = useAuthStore();
    authStore.setToken(token);
}

export function decodeToken(token){
  // const token = getToken();
  console.log('decode token: ', token);
  if (!token) {
    return null;
  }
  return jwtDecode(token);
}