<template>
    <!-- create a boostrap card for each venue. show the venue name and location and also have a dropdown for the admin to edit or delete the venue  -->
    <div class="container">
        <div v-for="venue in venues" class="card mt-3">
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
                                <RouterLink class="dropdown-item" :to="`/admin/venue/${venue.id}/edit`">Edit Venue
                                </RouterLink>
                            </li>
                            <li>
                                <RouterLink class="dropdown-item" :to="`/admin/venue/${venue.id}/addshow`">Add Show
                                </RouterLink>
                            </li>
                            <li><button class="dropdown-item" type="button" data-bs-toggle="modal"
                                    :data-bs-target="`#deleteVenueModal-${venue.id}`">Delete Venue</button></li>
                        </ul>

                        <!-- <div class="modal fade" :id="`DeleteVenue${venue.id}`" tabindex="-1"
                            :aria-labelledby="`DeleteVenueBody${venue.id}`" aria-hidden="true">
                            <div class="modal-dialog">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <h1 class="modal-title fs-5" :id="`DeleteVenueBody${venue.id}`">Confirm?</h1>
                                        <button type="button" class="btn-close" data-bs-dismiss="modal"
                                            aria-label="Close"></button>
                                    </div>
                                    <div class="modal-body">
                                        Are you sure you want to delete this post?
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary"
                                            data-bs-dismiss="modal">Close</button>
                                        <a class="btn btn-danger" href="/delete">Delete</a>
                                    </div>
                                </div>
                            </div>
                        </div> -->
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
                                                <img :src="`src/assets/images/shows/${show.image}`"
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
        
    </div>
    <div v-for="venue in venues" :key="`deleteVenueModal-${venue.id}`" class="modal fade"
            :id="`deleteVenueModal-${venue.id}`" tabindex="-1" :aria-labelledby="`deleteVenueModalLabel-${venue.id}`"
            aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" :id="`deleteVenueModalLabel-${venue.id}`">Confirm?</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        Are you sure you want to delete this venue?
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            Close
                        </button>
                        <button type="button" class="btn btn-danger" @click="deleteVenue(venue.id)">
                            Delete
                        </button>
                    </div>
                </div>
            </div>
        </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { getToken, isAdmin } from "../helpers/authHelper"
import axios from 'axios'
import { RouterLink, useRoute } from 'vue-router';

const route = useRoute();

function getTransformedList(list) {
    const result = []
    const chunkSize = 3
    for (let i = 0; i < list.length; i += chunkSize) {
        result.push(list.slice(i, i + chunkSize))
    }
    return result
}

const admin = computed(() => isAdmin())
const venues = ref([])
const getVenues = async () => {
    try {
        const response = await axios.get('http://localhost:5000/api/venue')
        console.log(response.data)
        venues.value = response.data
    } catch (error) {
        console.log(error)
    }
}

const deleteVenue = async (id) => {
    try {
        const response = await axios.delete(`http://localhost:5000/api/venue/${id}`, {
            headers: {
                Authorization: `Bearer ${getToken()}`
            }
        })
        console.log(response.data)
        route.reload()
        getVenues()
    } catch (error) {
        console.log(error)
    }
}

onMounted(() => {
    getVenues()
})

</script>