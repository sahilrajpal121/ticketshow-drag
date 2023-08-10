<template>
        <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6 mt-5">
                <div v-if="isError" class="alert alert-danger" role="alert" href="#error">
                    {{ errorMessage }}
                </div>
                <form @submit.prevent="addShow" class="border rounded p-3 shadow" enctype="multipart/form-data">
                    <h2 class="text-center mb-4">TicketShow</h2>
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

                    <button type="submit" class="btn btn-primary" :disabled="!isFormValid">Add Show</button>
                </form>
            </div>
        </div>
    </div>
</template>


<script setup>

import axios from 'axios';
import { ref, computed} from 'vue';
import { getToken } from '../helpers/authHelper';
import { useRoute } from 'vue-router';

const route = useRoute();
const venue_id = route.params.id;
console.log(venue_id.value)

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
    venues:[venue_id]
});

const isError = ref(false);
const errorMessage = ref('');

const isFormValid = computed(() => {
    return form.value.name && form.value.rating && form.value.tags && form.value.price && form.value.start_time && form.value.end_time && form.value.image && form.value.description;
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
        fd.append('venues', form.value.venues);
        // fd.append('venues', form.value.selectedTheaters)
        console.log(form.value.venues)

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


</script>