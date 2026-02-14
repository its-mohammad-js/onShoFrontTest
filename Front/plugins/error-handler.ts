export default defineNuxtPlugin((nuxtApp) => {
    nuxtApp.hook('app:error', (error) => {
      console.error('خطا رخ داد:', error);
      // اعمال لاگ یا رفتار خاص برای خطاها
    });
  });
  