<template>
  <section class="py-5 bg-white">
    <div class="container text-center">
      <div class="mb-4">
        <i class="fa-solid fa-ban text-danger" style="font-size: 4rem;"></i>
      </div>
      <h1 class="fw-bold display-5 mb-3">دسترسی غیرمجاز</h1>
      <p class="text-muted mb-4">شما مجوز دسترسی به این صفحه را ندارید.</p>
      <div class="d-flex justify-content-center gap-3">
        <nuxt-link to="/" class="btn btn-danger px-4">بازگشت به خانه</nuxt-link>
        <nuxt-link to="/auth" class="btn btn-outline-secondary px-4">ورود / ثبت‌نام</nuxt-link>
      </div>
    </div>
  </section>
</template>

<script setup>
</script>

<style scoped>
</style>


