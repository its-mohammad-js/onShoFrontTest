<template>
  <section class="py-5 bg-white">
    <div class="container text-center">
      <div class="mb-4">
        <i class="fa-solid fa-circle-exclamation text-danger" style="font-size: 4rem;"></i>
      </div>
      <h1 class="fw-bold display-5 mb-3">{{ title }}</h1>
      <p class="text-muted mb-4">{{ description }}</p>
      <div class="d-flex justify-content-center gap-3">
        <nuxt-link to="/" class="btn btn-danger px-4">بازگشت به خانه</nuxt-link>
        <button class="btn btn-outline-secondary px-4" @click="handleTryAgain">تلاش مجدد</button>
        <nuxt-link :to="errorRoute" class="btn btn-outline-secondary px-4">مشاهده صفحه خطا</nuxt-link>
      </div>
    </div>
  </section>
</template>

<script setup>
const props = defineProps({
  error: {
    type: Object,
    required: true
  }
});

const statusCode = computed(() => Number(props.error?.statusCode || props.error?.status || 500));

const title = computed(() => {
  switch (statusCode.value) {
    case 404: return 'صفحه مورد نظر یافت نشد';
    case 401: return 'نیاز به ورود';
    case 403: return 'دسترسی غیرمجاز';
    case 500: return 'خطای داخلی سرور';
    default: return `خطا (${statusCode.value})`;
  }
});

const description = computed(() => props.error?.statusMessage || props.error?.message || 'خطای نامشخص رخ داده است.');

const errorRoute = computed(() => {
  const code = statusCode.value;
  const known = [401, 403, 404, 500];
  return known.includes(code) ? `/error/${code}` : '/error/500';
});

const handleTryAgain = () => {
  if (process.client) {
    window.location.reload();
  }
};
</script>

<style scoped>
</style>


