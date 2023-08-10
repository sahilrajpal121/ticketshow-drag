<!-- <template>
    <div>
        <form @submit.prevent="editVenue">
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
                <input type="text" class="form-control" id="types" v-model="venue.type">
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    </div>
</template>
  
<script setup>
import axios from 'axios';
import { computed, onMounted, ref } from 'vue';
import { getToken } from '../helpers/authHelper';
import { useRoute } from 'vue-router';


const venue = ref({
    name: '',
    location: '',
    capacity: '',
    type: '',
    shows: []
});
// const venue_id = $route.params.id
const route = useRoute()
const venue_id = computed(() => route.params.id)
console.log(venue_id.value)

const getVenue = async () => {
    // make an api call to localhost:5000 with form data and auth token 
    const response = await axios.get(`http://127.0.0.1:5000/api/venue/${venue_id.value}`)
    console.log(response.data)
    venue.value = response.data
}


const editVenue = async () => {
    // make an api call to localhost:5000 with form data and auth token 
    axios.put(`http://127.0.0.1:5000/api/venue/${venue_id.value}`, venue.value, {
        headers: {
            'Authorization': `Bearer ${getToken()}`
        }
    }).then((response) => {
        console.log(response);
    }).catch((error) => {
        console.log(error);
    });
};

onMounted(() => {
    getVenue()
})
</script>
   -->

<template>
    <VenueForm :editMode="true"></VenueForm>
</template>

<script setup>
import VenueForm from '../components/VenueForm.vue';
</script>