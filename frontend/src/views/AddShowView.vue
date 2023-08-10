<template>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6 mt-5">
                <!-- show an alert message if there is an error along with the error message -->
                <div v-if="isError" class="alert alert-danger" role="alert" href="#error">
                    {{ errorMessage }}
                </div>
                <form @submit.prevent="addShow" class="border rounded p-3 shadow" enctype="multipart/form-data">
                    <h2 class="text-center mb-4">TicketShow</h2>
                    <!-- create a form with name, rating, tags, ticketprice and multiple select list to select theatres -->
                    <div class="mb-3">
                        <label for="name" class="form-label">Name</label>
                        <input v-model="form.name" type="text" class="form-control" id="name" required>
                    </div>

                    <div class="mb-3">
                        <label for="rating" class="form-label">Rating</label>
                        <input v-model="form.rating" type="number" step="0.1" class="form-control" id="rating" min="1"
                            max="5" required>
                    </div>

                    <div class="mb-3">
                        <label for="tags" class="form-label">Tags</label>
                        <input v-model="form.tags" type="text" class="form-control" id="tags" required>
                    </div>

                    <div class="mb-3">
                        <label for="duration" class="form-label">duration</label>
                        <input v-model="form.duration" type="number" class="form-control" id="duration" required>
                    </div>

                    <div class="mb-3">
                        <label for="ticketPrice" class="form-label">Ticket Price</label>
                        <input v-model="form.price" type="number" class="form-control" id="ticketPrice" required>
                    </div>

                    <div class="mb-3">
                        <label for="releaseDate" class="form-label">Release Date</label>
                        <input v-model="form.start_time" type="datetime-local" class="form-control" id="releaseDate" required>
                    </div>

                    <div class="mb-3">
                        <label for="endDate" class="form-label">End Date</label>
                        <input v-model="form.end_time" type="datetime-local" class="form-control date datepicker" id="endDate"
                            required>
                    </div>

                    <div class="mb-3">
                        <label for="image" class="form-label">Image</label>
                        <input type="file" @change="onFileChange" class="form-control-file" id="image">
                    </div>

                    <div class="mb-3">
                        <label for="description" class="form-label">Description</label>
                        <textarea v-model="form.description" class="form-control" id="description"></textarea>
                    </div>

                    <div class="mb-3" v-if="form.selectedTheaters.length">
                        <label>Selected Theaters:</label>
                        <ul class="list-group">
                            <li v-for="theater in form.selectedTheaters" type="button" :key="theater.id"
                                class="list-group-item d-flex justify-content-between align-items-center"
                                @click="removeTheater(theater)">
                                {{ theater.name }}
                                <span>[x]</span>
                            </li>
                        </ul>
                    </div>

                    <div class="mb-3">
                        <label for="theaterSearch">Theater Search:</label>
                        <input type="text" id="theaterSearch" v-model="searchQuery" @input="searchTheaters">
                        <ul v-if="searchResults.length" class="list-group overflow-auto" style="max-height: 200px;">
                            <li v-for="theater in searchResults" type="button" :key="theater.id"
                                @click="addTheater(theater)"
                                class="list-group-item d-flex justify-content-between align-items-center">
                                {{ theater.name }}
                            </li>
                        </ul>
                    </div>

                    <button type="submit" class="btn btn-primary" :disabled="!isFormValid">Add Show</button>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { getToken } from '../helpers/authHelper'


const router = useRouter();

const form = ref({
    name: '',
    rating: '',
    tags: '',
    duration: '',
    price: '',
    start_time: '',
    end_time: '',
    image: '',
    description: '',
    selectedTheaters: [],
});


const isError = ref(false);
const errorMessage = ref('');

const isFormValid = computed(() => {
    return form.value.name && form.value.rating && form.value.tags && form.value.price && form.value.start_time && form.value.end_time && form.value.image && form.value.description && form.value.selectedTheaters;
});

const addShow = async () => {
    try {
        const fd = new FormData();
        fd.append('name', form.value.name);
        fd.append('tags', form.value.tags);
        fd.append('price', form.value.price);
        fd.append('start_time', form.value.start_time);
        fd.append('end_time', form.value.end_time);
        fd.append('image', form.value.image);
        fd.append('description', form.value.description);
        fd.append('duration', form  .value.duration);
        fd.append('rating', form.value.rating);
        // append only the ids of selectedTheaters
        fd.append('venues', form.value.selectedTheaters.map(theater => theater.id));
        // fd.append('venues', form.value.selectedTheaters)
        console.log(form.value.selectedTheaters.map(theater => theater.id))

        console.log(form.value)
        console.log(fd)
        const response = await axios.post('http://127.0.0.1:5000/api/show', fd,
            {
                headers: {
                    Authorization: `Bearer ${getToken()}`,
                    'Content-Type': 'multipart/form-data'
                    // 'Access-Control-Allow-Origin': '*', // Allow CORS
                },
            });
        console.log('response', response);
    } catch (error) {
        console.log('error', error);
        isError.value = true;
        errorMessage.value = error.response.data.message;
    }
};

const onFileChange = (event) => {
    form.value.image = event.target.files[0];
    console.log(form.value.image)
};

const searchQuery = ref('');
const searchResults = ref([]);

const searchTheaters = async () => {
    try {
        // make an api call to localhost:5000/api/venue and pass the query inside body
        const response = await axios.get(`http://localhost:5000/api/venue?search=${searchQuery.value}`, {
            headers: {
                Authorization: `Bearer ${getToken()}`,
            },
        });

        console.log(response.data)
        searchResults.value = response.data;
    } catch (error) {
        console.log('error', error.response.data);
    }
};

const addTheater = (theater) => {
    if (!form.value.selectedTheaters.includes(theater)) {
        form.value.selectedTheaters.push(theater);
    }
};

const removeTheater = (theater) => {
    const index = form.value.selectedTheaters.indexOf(theater);
    if (index !== -1) {
        form.value.selectedTheaters.splice(index, 1);
    }
};

</script>
