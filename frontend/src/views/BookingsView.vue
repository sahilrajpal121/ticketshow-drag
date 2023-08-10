<template>
    <div class="container">
        <div class="row">
            <div class="col-12">
                <h1>Bookings</h1>
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <!-- <th></th> -->
                            <th scope="col">Show</th>
                            <th scope="col">Venue</th>
                            <th scope="col">Date</th>
                            <th scope="col">Show Time</th>
                            <th scope="col">Seats</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="booking in bookings" :key="booking.id">
                            <td> <img class="img-fluid" width="100" height="50" :src="`/src/assets/images/shows/${booking.show.image}`"
                                    alt="Card image cap">  {{ booking.show.name }}</td>
                            <!-- <td>{{ booking.show.name }}</td> -->
                            <td>{{ booking.show.venue.name }}</td>
                            <td>{{ formatDate(booking.show.start_time) }}</td>
                            <td>{{ formatTime(booking.show.start_time) }}</td>
                            <td>{{ booking.num_seats }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, defineProps, watch } from 'vue';
import { isAdmin } from '../helpers/authHelper';
import { useRoute } from 'vue-router';
import axios from 'axios';
import { decodeToken, getToken } from '../helpers/authHelper';
import jwtDecode from 'jwt-decode';

const token = getToken();
const decodedToken = jwtDecode(token);

const user_id = decodedToken.id;
const bookings = ref([]);

function formatDate(datetime) {
    const date = new Date(datetime);
    return date.toLocaleDateString();
}

function formatTime(datetime) {
    const date = new Date(datetime);
    return date.toLocaleTimeString();
}

const getBookings = async () => {
    try {
        const response = await axios.get(`http://localhost:5000/api/booking?user_id=${user_id}`, {
            headers: {
                Authorization: `Bearer ${getToken()}`
            }
        });
        console.log(response.data)
        bookings.value = response.data
    } catch (error) {
        console.log(error.response.data)
    }
}

onMounted(() => {
    getBookings()
})
</script>