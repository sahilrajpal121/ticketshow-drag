<template>
  <div>
    <form @submit.prevent="submitForm">
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
      <button type="submit" class="btn btn-primary">{{ editMode ? 'Update' : 'Create' }}</button>
    </form>
  </div>
</template>
  
<script setup>
import axios from 'axios';
import { computed, onMounted, ref } from 'vue';
import { getToken } from '../helpers/authHelper';
import { useRoute } from 'vue-router';
import { useRouter } from 'vue-router';

const router = useRouter();

const props = defineProps({
  editMode: {
    type: Boolean, // A prop to determine if the component is in edit mode or create mode
    default: false
  }
});

const venue = ref({
  name: '',
  location: '',
  capacity: '',
  type: '',
  shows: []
});

const route = useRoute();
const venue_id = computed(() => route.params.id);

const getVenue = async () => {
  const response = await axios.get(`http://127.0.0.1:5000/api/venue/${venue_id.value}`);
  venue.value = response.data;
};

const submitForm = async () => {
  if (props.editMode) {
    await editVenue();
  } else {
    await createVenue();
  }
};

const editVenue = async () => {
  try {
    await axios.put(`http://127.0.0.1:5000/api/venue/${venue_id.value}`, venue.value, {
      headers: {
        'Authorization': `Bearer ${getToken()}`
      }
    });
    console.log('Venue updated successfully');
  } catch (error) {
    console.error('Error updating venue:', error);
  }
};

const createVenue = async () => {
  try {
    await axios.post('http://127.0.0.1:5000/api/venue', venue.value, {
      headers: {
        'Authorization': `Bearer ${getToken()}`
      }
    });
    console.log('Venue created successfully');
    router.push('/venues');
  } catch (error) {
    console.error('Error creating venue:', error);
  }
};

onMounted(() => {
  if (props.editMode) {
    getVenue();
  }
});
</script>
  