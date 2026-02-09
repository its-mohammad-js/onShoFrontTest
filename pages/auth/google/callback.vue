<template>
  <div class="container my-5 d-flex flex-column align-items-center justify-content-center" style="min-height: 60vh;">
    <div v-if="loading" class="text-center">
      <div class="spinner-border text-danger" role="status">
        <span class="visually-hidden">در حال پردازش...</span>
      </div>
      <p class="mt-3 text-muted">در حال ورود با گوگل...</p>
    </div>
    <div v-else-if="error" class="text-center">
      <i class="fas fa-exclamation-circle text-danger" style="font-size: 3rem;"></i>
      <h4 class="mt-3 text-danger">خطا در ورود</h4>
      <p class="text-muted">{{ error }}</p>
      <button class="btn btn-danger mt-3" @click="goToLogin">
        بازگشت به صفحه ورود
      </button>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: "auth"
})

const route = useRoute();
const router = useRouter();
const { $api, $sweetalert } = useNuxtApp();
const authStore = useAuthStore();

const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  const code = route.query.code;
  const errorParam = route.query.error;
  const state = route.query.state;

  // اگر خطایی از Google آمده باشد
  if (errorParam) {
    error.value = "خطا در احراز هویت گوگل. لطفاً دوباره تلاش کنید.";
    loading.value = false;
    return;
  }

  // اگر کد وجود نداشته باشد
  if (!code) {
    error.value = "کد تأیید دریافت نشد. لطفاً دوباره تلاش کنید.";
    loading.value = false;
    return;
  }

  try {
    // ارسال کد به backend برای دریافت token
    const response = await $api.post('/auth/google/callback', {
      code: code,
      state: state
    });

    if (response.data.status && response.data.data.token) {
      // ذخیره token
      authStore.setToken(response.data.data.token);
      
      // دریافت اطلاعات کاربر
      await authStore.init();
      
      if (authStore.authenticated) {
        // هدایت به صفحه حساب کاربری
        await router.push('/account');
      } else {
        error.value = "خطا در دریافت اطلاعات کاربر";
        loading.value = false;
      }
    } else {
      error.value = response.data.message || "خطا در ورود با گوگل";
      loading.value = false;
    }
  } catch (err) {
    console.error('Google callback error:', err);
    if (err.response?.data?.message) {
      error.value = err.response.data.message;
    } else {
      error.value = "خطایی در ارتباط با سرور رخ داد. لطفاً دوباره تلاش کنید.";
    }
    loading.value = false;
  }
});

const goToLogin = () => {
  router.push('/auth');
};
</script>

<style scoped>
.spinner-border {
  width: 3rem;
  height: 3rem;
}
</style>

