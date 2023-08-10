<template>
    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <!-- <h3>{{ venue.name }}</h3>
                    <span class="form-text"> {{ venue.location }}</span> -->
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <h5>{{ props.showData.venue }}</h5>
                    <h6>{{ props.showData.name }}</h6>
                    <p>Time: {{ props.showData.start_time }}</p>
                    <p>Available Tickets: {{ availableTickets }}</p>
                    <label for="ticketQuantity">Number of Tickets:</label>
                    <input type="number" id="ticketQuantity" v-model="ticketQuantity">
                    <br/><br/>
                    <p>Total Price: Rs. <strong> {{ props.showData.price * ticketQuantity }}</strong></p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary" @click="confirmBooking"
                        :disabled="availableTickets - ticketQuantity < 0">Confirm</button>
                </div>
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

const decodedToken = decodeToken(getToken());
console.log(decodedToken)

//  get prop showData from parent component

const props = defineProps({
    showData: Object
})
// const showData = props.showData

// console.log(props.showData)
// console.log(showData)

const route = useRoute();
const show_id = route.params.id;
console.log(show_id)

const venue = ref(null);
console.log(venue.value)
const ticketQuantity = ref(1);
const availableTickets = ref(0);
// console.log("available tickets", availableTickets.value)

const admin = computed(() => isAdmin())


const confirmBooking = async () => {
    try {
        const response = await axios.post(`http://localhost:5000/api/booking`, {
            show_id: props.showData.id,
            user_id: decodedToken.id,
            num_seats: ticketQuantity.value
        }, {
            headers: {
                Authorization: `Bearer ${getToken()}`
            }
        });
        console.log(response.data)
        window.location.reload();


    } catch (error) {
        console.log(error.response.data)
    }
}



const getVenue = async () => {
    const response = await axios.get(`http://localhost:5000/api/venue/${props.showData.venue_id}`, {
        headers: {
            Authorization: `Bearer ${getToken()}`
        }
    });
    console.log("venue details from BookTicket component", response.data)
    venue.value = response.data;
}

const getAvailableTickets = async () => {
    const response = await axios.get(`http://localhost:5000/api/booking?show_id=${props.showData.id}`, {
        headers: {
            Authorization: `Bearer ${getToken()}`
        }
    }
    );
    console.log("tickets", response.data)
    const ticketsSold = response.data.reduce((acc, curr) => acc + curr.num_seats, 0)
    availableTickets.value = venue.value.capacity - ticketsSold;
    console.log("available tickets", availableTickets.value)
    console.log("sold tickets", ticketsSold)

}

// create a watch that will update props
watch(() => props.showData, () => {
    getVenue();
    getAvailableTickets();
})
</script>