// plugins/bootstrap.client.ts
import { defineNuxtPlugin } from '#app'

// Import the Bootstrap JavaScript
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

export default defineNuxtPlugin(() => {
    console.log("Bootstrap plugin loaded!");
  });