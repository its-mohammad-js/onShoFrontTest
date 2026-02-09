<template>
  <section class="py-5 bg-white">
    <div class="container text-center">
      <div class="mb-4">
        <i class="fa-solid fa-server text-danger" style="font-size: 4rem;"></i>
      </div>
      <h1 class="fw-bold display-5 mb-3">خطای داخلی سرور</h1>
      <p class="text-muted mb-4">مشکلی در سرور به وجود آمده است. لطفاً بعداً دوباره امتحان کنید.</p>
      <div class="d-flex justify-content-center gap-3">
        <button class="btn btn-danger px-4" @click="$router.go(0)">تلاش مجدد</button>
        <nuxt-link to="/" class="btn btn-outline-secondary px-4">بازگشت به خانه</nuxt-link>
      </div>
    </div>
  </section>
</template>

<script setup>
</script>

<style scoped>
</style>


