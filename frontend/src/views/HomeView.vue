<script setup>
import { onMounted, ref } from 'vue';
import { getToken } from '../helpers/authHelper';

const images = ref([])
const user = ref('')
const isAdmin = ref(false)

const fetchImages = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/test') // Replace with your API endpoint
    const data = await response.json()
    console.log(data)
    images.value = data.images
    console.log('images', images.value)
  } catch (error) {
    console.error(error)
  }
}

import jwtDecode from 'jwt-decode'; // A library to decode JWT tokens

// check if there is any token in localStorage and if there is, get the email out of it 
const checkUser = () => {
  const token = getToken();
  // console.log(token, authStore.token)
  if(token){
    const decodedToken = jwtDecode(token);
    console.log('decodedToken', decodedToken)
    user.value = decodedToken.email;
    isAdmin.value = decodedToken.roles.includes('admin');
  }
}

onMounted(() => {
  fetchImages();
  checkUser();
})

</script>

<template>
  <main>
    <div> hello {{ user  }}</div>
    <div v-if="isAdmin"> You are an admin</div>
    <div id="carouselExample" class="carousel slide container flex justify-content-center">
      <div class="carousel-inner">
        <!-- Loop through the images and render them -->
        <div v-for="(image, index) in images" :key="index" class="carousel-item" :class="{ 'active': index === 0 }">
          <img :src="`src/assets/images/${image}`" class="resized-image d-block w-100 " alt="...">
        </div>
      </div>
      <button class="carousel-control-prev" type="button" data-bs-target="#carouselExample" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#carouselExample" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>
  </main>
</template>

<style scoped>
.resized-image {
  width: 1000px;
  height: 234px;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}
</style>