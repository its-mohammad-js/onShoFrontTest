<template>
    <div class="flex items-center justify-center h-screen">
      <button class="px-6 py-3 bg-red-600 text-white rounded-lg" @click="googleLogin">
        Login with Google
      </button>
    </div>
  </template>
  
  <script setup>
  const config = useRuntimeConfig()
  
  const googleLogin = () => {
    window.location.href = `${config.public.backendUrl}/auth/google/login`
  }
  </script>
  