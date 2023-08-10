<!-- <template>
    <div>
        <form @submit.prevent="addVenue">
            <div class="mb-3">
                <label for="name" class="form-label">Venue Name</label>
                <input type="text" class="form-control" id="name" v-model="venue.name">
            </div>
            <div class="mb-3">
                <label for="location" class="form-label">Location</label>
                <input type="text" class="form-control" id="location" v-model="venue.location">
            </div>
            <div class="mb-3">
                <label for="capacity" class="form-label">Capacity</label>
                <input type="number" class="form-control" id="capacity" v-model="venue.capacity">
            </div>
            <div class="mb-3">
                <label for="type" class="form-label">Type</label>
                <input type="text" class="form-control" id="type" v-model="venue.type">
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    </div>
</template>
  
<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { getToken } from '../helpers/authHelper';

const venue = ref({
    name: '',
    location: '',
    capacity: '',
    type: ''
});

const addVenue = () => {
    // make an api call to localhost:5000 with form data and auth token 
    axios.post('http://127.0.0.1:5000/api/venue', venue.value, {
        headers: {
            'Authorization': `Bearer ${getToken()}`
        }
    }).then((response) => {
        console.log(response);
    }).catch((error) => {
        console.log(error);
    });
};
</script>
   -->

<template>
    <VenueForm></VenueForm>
</template>

<script setup>
import VenueForm from '../components/VenueForm.vue';
</script>