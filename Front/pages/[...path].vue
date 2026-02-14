<template>
  <div></div>
</template>

<script setup>
import { onMounted } from 'vue';
import { navigateTo } from '#app';

onMounted(() => {
  navigateTo('/error/404', { replace: true });
});
</script>

<style scoped>
</style>


