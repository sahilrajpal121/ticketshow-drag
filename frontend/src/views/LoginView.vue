<template>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6 mt-5">
                <!-- show an alert message if there is an error along with the error message -->
                <div v-if="isError" class="alert alert-danger" role="alert">
                    {{ errorMessage }}
                </div>
                <form @submit.prevent="login" class="border rounded p-3 shadow">
                    <h2 class="text-center mb-4">TicketShow</h2>
                    <div class="mb-3">
                        <label for="email" class="form-label">Email address</label>
                        <input v-model="form.email" type="email" class="form-control" id="email"
                            aria-describedby="emailHelp" required>
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
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import {setToken} from '../helpers/authHelper'

const router = useRouter();

const form = ref({
    email: '',
    password: '',
});

const errorMessage = ref('');
const isError = computed(() => errorMessage.value !== '');

const isFormValid = computed(() => {
    return form.value.email && form.value.password;
});

const login = async () => {
    try {
        const response = await axios.post('http://127.0.0.1:5000/api/login', form.value);
        setToken(response.data.access_token)
        errorMessage.value = '';
        router.push('/');
    } catch (error) {
        console.log(error);
        errorMessage.value = error.response.data.message;
    }
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