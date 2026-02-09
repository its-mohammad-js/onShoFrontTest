// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2024-04-03",
  devtools: {
    enabled: true,
  },
  components: true,
  ssr: false,
  app: {
    head: {
      link: [{ rel: "icon", type: "image/png", href: "/images/logo-fani.png" }],
    },
  },
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.API_BASE_URL || "http://127.0.0.1:8000/",
      // apiBaseUrl: 'https://onsho24.ir/api/'
      // apiBaseUrl: 'http://185.8.174.188:1371/'
      googleClientId: process.env.GOOGLE_CLIENT_ID || "",
    },
  },
  vite: {
    server: {
      allowedHosts: ["localhost", "127.0.0.1", "www.onsho24.ir"],
      // allowedHosts: 'all', // dev only
    },
  },
  css: [
    "@fortawesome/fontawesome-free/css/all.css",
    "assets/css/style.css",
    "bootstrap/dist/css/bootstrap.min.css",
    // "@fortawesome/fontawesome-free/css/all.min.css",
    "@/assets/css/hafez-icofont.css",
    "swiper/css",
    "@/assets/scss/_variable.scss",
  ],
  plugins: [
    "~/plugins/axios.ts",
    "~/plugins/load.ts",
    "~/plugins/permission.ts",
    "~/plugins/convertNumbers.client.ts",
    // '~/plugins/subdomain.client.ts', // Disabled - using middleware instead
  ],
  modules: ["@pinia/nuxt"],
});
