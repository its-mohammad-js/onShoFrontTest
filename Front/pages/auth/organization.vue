<template>
  <div></div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

onMounted(() => {
  // Redirect to merged auth page with organization type
  const query = { ...route.query, type: 'organization' };
  router.replace({ path: '/auth', query });
});

definePageMeta({
  layout: "auth"
});
</script>
