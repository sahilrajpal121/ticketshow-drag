<template>
    <form @submit.prevent="login" class="border rounded p-3 shadow">
      <h2 class="text-center mb-4">TicketShow</h2>
      <div class="mb-3">
        <label for="email" class="form-label">Email address</label>
        <input v-model="form.email" type="email" class="form-control" id="email" aria-describedby="emailHelp" required>
      </div>
  
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input v-model="form.password" type="password" class="form-control" id="password" required>
      </div>
  
      <div class="d-grid gap-2">
        <button :disabled="!isFormValid" type="submit" class="btn btn-primary">Log in</button>
      </div>
  
      <div class="text-center mt-3">
        <span>New here?</span>
        <router-link to="/register">Register</router-link>
      </div>
    </form>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  import { useAuthStore } from '../stores/authStore';
  
  const authStore = useAuthStore();
  console.log('component', authStore.token);
  
  const router = useRouter();
  
  const form = ref({
    email: '',
    password: '',
  });
  
  const isError = ref(false);
  const errorMessage = ref('');
  
  const isFormValid = computed(() => {
    return form.value.email && form.value.password;
  });
  
  const login = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/api/login', form.value);
      authStore.setToken(response.data.access_token);
      isError.value = false;
      errorMessage.value = '';
      router.push('/');
    } catch (error) {
      console.log(error);
      isError.value = true;
      errorMessage.value = error.response.data.message;
    }
  };
  </script>