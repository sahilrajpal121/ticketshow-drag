<template>
    <div>
      <input
        type="text"
        class="form-control"
        placeholder="Search"
        v-model="searchTerm"
      />
      <ul class="list-group mt-2" v-if="searchResults.length">
        <li class="list-group-item" v-for="result in searchResults" :key="result.id">
          {{ result.name }}
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import { ref, watch } from 'vue';
  
  export default {
    setup() {
      const searchTerm = ref('');
      const searchResults = ref([]);
  
      watch(searchTerm, () => {
        if (searchTerm.value) {
          // Call your search API or perform search logic here
          // Update the searchResults array based on the search term
          // For simplicity, let's assume we have a method called "performSearch" that returns an array of results
          searchResults.value = performSearch(searchTerm.value);
        } else {
          searchResults.value = ['test.'];
        }
      });
  
      function performSearch(term) {
        // Implement your search logic here
        // You can make an API call or search within local data
        // Return an array of search results
        // For simplicity, let's assume we have an array of objects with a "name" property
        const data = [
          { id: 1, name: 'Result 1' },
          { id: 2, name: 'Result 2' },
          { id: 3, name: 'Result 3' },
        ];
  
        return data.filter((result) =>
          result.name.toLowerCase().includes(term.toLowerCase())
        );
      }
  
      return {
        searchTerm,
        searchResults,
      };
    },
  };
  </script>