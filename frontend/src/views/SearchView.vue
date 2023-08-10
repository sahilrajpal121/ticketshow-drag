<template>
<div>
    {{ route.query.q }}
</div>
</template>

<script setup>

import { useRoute } from 'vue-router';

const route = useRoute();

</script>