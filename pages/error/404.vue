<template>
  <section class="py-5 bg-white">
    <div class="container text-center">
      <div class="mb-4">
        <i class="fa-solid fa-triangle-exclamation text-danger" style="font-size: 4rem;"></i>
      </div>
      <h1 class="fw-bold display-5 mb-3">
        {{ isDomainError ? 'دامنه یافت نشد' : 'صفحه مورد نظر یافت نشد' }}
      </h1>
      <p class="text-muted mb-4">
        {{ isDomainError 
          ? 'دامنه مورد نظر در سیستم ثبت نشده است. لطفاً آدرس را بررسی کنید.' 
          : 'به نظر می‌رسد آدرس وارد شده نادرست است یا صفحه حذف شده است.' 
        }}
      </p>
      <div class="d-flex justify-content-center gap-3">
        <nuxt-link to="https://onsho24.ir" class="btn btn-danger px-4">بازگشت به خانه</nuxt-link>
        <nuxt-link to="https://onsho24.ir/courses" class="btn btn-outline-secondary px-4">مشاهده دوره‌ها</nuxt-link>
      </div>
    </div>
  </section>
</template>

<script setup>
const route = useRoute()
const isDomainError = computed(() => {
  return route.query.reason === 'domain_not_found' || route.query.reason === 'domain_check_failed'
})
</script>

<style scoped>
</style>


