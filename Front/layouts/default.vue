<template>
  <Header />
  <slot />
  <FirstFooter />
  <FooterSection />
</template>

<script setup>
import Header from "./components/Header.vue";
import FooterSection from "./components/FooterSection.vue";
import FirstFooter from "./components/FirstFooter.vue";
</script>
