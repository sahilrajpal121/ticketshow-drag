<template>
    <div class="container mt-5">
        <!-- Repeat this card for each movie in your data -->

        <div class="card movie-card">
            <div class="row">
                <div class="col-md-4 mb-4 col   ">
                    <img class="img-fluid w-100" :src="`/src/assets/images/shows/${show.image}`" alt="Card image cap">
                </div>
                <!-- <div class="col-md-4 mb-4 col-2">
                </div> -->
                <div class="col-md-4 mb-4 col">
                    <div class="movie-details">
                        <h5 class="card-title movie-title">{{ show.name }}</h5>
                        <p class="card-text movie-description">{{ show.description }}</p>
                        <div class="movie-details">
                            <p><strong>Price:</strong> Rs.{{ show.price }}</p>
                            <p><strong>Rating:</strong> {{ show.rating }}/5</p>
                            <p><strong>Tags:</strong> <span class="movie-tags">{{ show.tags }}</span></p>
                            <p><strong>Start Time:</strong> {{ show.start_time }}</p>
                            <p><strong>End Time:</strong> {{ show.end_time }}</p>
                        </div>
                        <div class="container">
                        <button class="btn mt-3 btn-sm btn-dark" data-bs-toggle="modal" data-bs-target="#exampleModal"
                            v-if="!admin">Book Tickets</button>
                        <button class="btn mt-3 btn-sm btn-dark" v-if="admin">Edit Show</button>
                        <button class="btn mt-3 btn-sm btn-dark" v-if="admin" data-bs-toggle="modal"
                            data-bs-target="#deleteConfirmationModal">Delete Show</button>
                            </div> 
                    </div>
                </div>
            </div>
            <!-- End of card -->
        </div>
    </div>
    <div class="modal fade" id="deleteConfirmationModal" tabindex="-1" aria-labelledby="deleteConfirmationModalLabel"
        aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="deleteConfirmationModalLabel">Confirm Deletion</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    Are you sure you want to delete this show?
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-danger" @click="deleteShow">Delete</button>
                </div>
            </div>
        </div>
    </div>


    <!-- Modal -->
    <BookTicket :showData="show"></BookTicket>
    <!-- <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Modal title</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    ...
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary">Save changes</button>
                </div>
            </div>
        </div>
    </div> -->
</template>

<script setup>

import { onMounted, ref, onBeforeMount } from 'vue'
import axios from 'axios';
import { isAdmin, getToken } from '../helpers/authHelper';
import { useRoute } from 'vue-router';
import BookTicket from '../components/BookTicket.vue';

const admin = isAdmin();

const route = useRoute();
const show_id = route.params.id;
console.log(show_id)

const show = ref({
    name: '',
    description: '',
    price: '',
    rating: '',
    tags: '',
    start_time: '',
    end_time: '',
    venue_id: '',
});

const formatDate = (dateString) => {

    const date = new Date(dateString);
    const options = {
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        hour12: true
    };

    const formattedDate = new Intl.DateTimeFormat('en-US', options).format(date);
    console.log(formattedDate);
    return formattedDate;
}

const getShow = async () => {
    try {
        const response = await axios.get(`http://localhost:5000/api/show/${show_id}`);
        console.log(response.data);
        show.value = response.data;
        show.value.start_time = formatDate(show.value.start_time);
        show.value.end_time = formatDate(show.value.end_time);
    } catch (error) {
        console.error(error);
    }
}

const deleteShow = async () => {
    try {
        const response = await axios.delete(`http://localhost:5000/api/show/${show_id}`,
            {
                headers: {
                    Authorization: `Bearer ${getToken()}`
                }
            });
        console.log(response.data);
        window.location.href = '/venues';
    } catch (error) {
        console.error(error);
    }
}

onBeforeMount(() => {
    getShow();
});

</script>

<style scoped>
.movie-card {
    background-color: #fff;
    border: none;
    border-radius: 15px;
    box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.1);
    display: flex;
    transition: transform 0.2s;
}

.movie-card:hover {
    transform: scale(1.03);
}

.movie-card img {
    border-radius: 15px 0 0 15px;
    width: 150px;
    object-fit: cover;
}

.movie-details {
    padding: 20px;
    flex-grow: 1;
    /* To allow the details section to expand and fill the remaining space */
}

.movie-title {
    font-size: 1.5rem;
    color: #333;
}

.movie-description {
    color: #777;
}

.movie-details strong {
    color: #333;
}

.movie-tags {
    color: #007bff;
}

.book-button {
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 5px;
    padding: 8px 15px;
    cursor: pointer;
    transition: background-color 0.2s;
}

.book-button:hover {
    background-color: #0056b3;
}
</style>