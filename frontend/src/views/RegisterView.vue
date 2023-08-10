<template>
  <!-- create a form with email, password, confirm password, and submit button and use bootstrap -->
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-md-6 mt-5">
        <form @submit.prevent="register" class="border rounded p-3 shadow">
          <h2 class="text-center mb-4">Create an account</h2>
          <div class="mb-3">
            <label for="email" class="form-label">Email address</label>
            <input v-model="form.email" type="email" class="form-control" id="email" aria-describedby="emailHelp" required>
            <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
          </div>

          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input v-model="form.password" type="password" class="form-control" id="password" required>
          </div>

          <div class="mb-3">
            <label for="confirmPassword" class="form-label">Confirm Password</label>
            <input v-model="form.confirmPassword" type="password" class="form-control" id="confirmPassword" required>
            <div v-if="!passwordsMatch" class="text-danger">Passwords do not match</div>
          </div>

          <div class="d-grid gap-2">
            <button :disabled="!isFormValid" type="submit" class="btn btn-primary">Create Account</button>
          </div>

          <div class="text-center mt-3">
            <span>Already have an account?</span>
            <router-link to="/login">Log in</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();

const form = ref({
  email: '',
  password: '',
  confirmPassword: '',
  passwordsMatch: true,
});

const passwordsMatch = computed(() => {
  return form.value.password === form.value.confirmPassword;
});

const isFormValid = computed(() => {
  return form.value.email && form.value.password && form.value.confirmPassword && passwordsMatch.value;
});

const register = async () => {
  // if the password and confirm password do not match, display an error message
  if (!passwordsMatch.value) {
    console.log('passwords do not match')
    return;
  }
  else {
    console.log('passwords match')
    console.log(form.value)
  }

  await axios.post('http://127.0.0.1:5000/api/user', form.value)
    .then(() => {
      // Handle successful creation of the venue
      console.log('User registered successfully!');
      router.push('/');
    })
    .catch((error) => {
      // Handle error during venue creation
      console.error('Error registering venue:', error.response.data);
    });
};
</script>

<style scoped>
form {
  background-color: #fff;
  padding: 20px;
}

.btn-primary {
  background-color: #000000;
  border-color: #141516;
}

.btn-primary:hover {
  background-color: #183654;
  border-color: rgb(30, 41, 53);
}

.btn-primary:focus {
  box-shadow: 0 0 0 0.25rem rgba(38, 143, 255, 0.5);
}

.text-danger {
  font-size: 0.875rem;
}

a {
  color: #007bff;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>
