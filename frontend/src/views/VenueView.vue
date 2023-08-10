<template>
        <div class="container">
            <div class="card-header">
                {{ venue.name }}
                <span class="form-text">{{ venue.location }}</span>
                <template v-if="admin">
                    <div class="dropdown float-end" style="display: inline-block;">
                        <svg class="dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false"
                            aria-label="More options" color="#262626" fill="#262626" height="24" role="img"
                            viewBox="0 0 24 24" width="24">
                            <circle cx="12" cy="12" r="1.5"></circle>
                            <circle cx="6" cy="12" r="1.5"></circle>
                            <circle cx="18" cy="12" r="1.5"></circle>
                        </svg>
                        <ul class="dropdown-menu">
                            <li>
                                <RouterLink class="dropdown-item" :to="`/admin/venue/${venue_id}/edit`">Edit Venue
                                </RouterLink>
                            </li>
                            <li>
                                <RouterLink class="dropdown-item" :to="`/admin/venue/${venue_id}/addshow`">Add Show
                                </RouterLink>
                            </li>
                            <li><button class="dropdown-item" type="button" data-bs-toggle="modal"
                                    :data-bs-target="`#deleteVenueModal-${venue_id}`">Delete Venue</button></li>
                        </ul>
                    </div>
                </template>
            </div>


            <div class="card-body">
                <!-- make carousel with three cards for each show in venue  -->
                <div class="container">
                    <div id="carouselExample" class="carousel slide container flex justify-content-center">
                        <div class="carousel-inner">
                            <!-- Loop through the images and render them -->
                            <div v-for="(set, index) in getTransformedList(venue.shows)" :key="index" class="carousel-item"
                                :class="{ 'active': index === 0 }">
                                <div class="row">
                                    <div v-for="(show, index) in set" :key="index" class="col-4">
                                        <div class="card">
                                            <RouterLink :to="`/show/${show.id}`">
                                                <img :src="`../src/assets/images/shows/${show.image}`"
                                                    class="resized-image d-block w-100" alt="..." height="278" width="417">
                                            </RouterLink>
                                            <div class="card-body">
                                                <h4 class="card-title">{{ show.name }}</h4>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                            </div>
                        </div>
                        <button class="carousel-control-prev" type="button" data-bs-target="#carouselExample"
                            data-bs-slide="prev">
                            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                            <span class="visually-hidden">Previous</span>
                        </button>
                        <button class="carousel-control-next" type="button" data-bs-target="#carouselExample"
                            data-bs-slide="next">
                            <span class="carousel-control-next-icon" aria-hidden="true"></span>
                            <span class="visually-hidden">Next</span>
                        </button>
                    </div>
                </div>
            </div>
        
    </div>
</template>

<script setup>

import { onMounted, ref, onBeforeMount } from 'vue'
import axios from 'axios';
import { isAdmin, getToken } from '../helpers/authHelper';
import { useRoute } from 'vue-router';


const admin = isAdmin();

const route = useRoute();
const venue_id = route.params.id;
console.log(venue_id);

const venue = ref({
    name: '',
    location: '',
    capacity: '',
    shows: []
});


function getTransformedList(list) {
    const result = []
    const chunkSize = 3
    for (let i = 0; i < list.length; i += chunkSize) {
        result.push(list.slice(i, i + chunkSize))
    }
    return result
}


const getVenue = async () => {
    const response = await axios.get(`http://localhost:5000/api/venue/${venue_id}`);
    venue.value = response.data;
    console.log(venue.value);
}

onMounted(() => {
    console.log('venue onMounted called')
    getVenue();
})


</script>