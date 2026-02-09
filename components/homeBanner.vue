<template>
  <section
    class="banner position-relative py-4 text-center text-md-start overflow-hidden"
  >
    <!-- Background image -->
    <img
      v-if="imageUrl"
      :src="imageUrl"
      alt="Banner Background"
      class="banner-bg"
    />

    <div class="container position-relative">
      <div class="row align-items-center">
        <div class="col-md-7">
          <h1 class="fw-bold text-dark mb-3">
            <span class="text-danger1">{{ title }}</span>
          </h1>
          <p class="lead text-muted mb-4">{{ subtitle }}</p>

          <nuxt-link
            v-if="buttonText && buttonLink"
            :to="buttonLink"
            class="btn btn-danger px-4 py-2"
          >
            {{ buttonText }}
          </nuxt-link>

          <span v-if="!auth.authenticated">
            <nuxt-link to="/auth" class="btn btn-danger px-4 me-3"
              >ثبت نام</nuxt-link
            >
          </span>
        </div>

        <div class="col-md-5 text-center mt-4 mt-md-0" v-if="illustrationUrl">
          <img
            :src="illustrationUrl"
            alt="Banner Illustration"
            class="img-fluid"
          />
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from "vue";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
const { getMediaUrl } = useMediaUrl();

const props = defineProps({
  title: {
    type: String,
    default: "به دنیای مهارت خوش آمدید!",
  },
  subtitle: {
    type: String,
    default: "با آموزش‌های حرفه‌ای مهارت‌های خود را ارتقا دهید.",
  },
  image: {
    type: String,
    default: "/images/test.jpg",
  },
  illustration: {
    type: String,
    default: "/images/test.jpg",
  },
  buttonText: {
    type: String,
    default: "شروع کنید",
  },
  buttonLink: {
    type: String,
    default: "/courses",
  },
});

// تبدیل آدرس‌های تصویر به آدرس با /api
const imageUrl = computed(() => getMediaUrl(props.image));
const illustrationUrl = computed(() => getMediaUrl(props.illustration));
</script>

<style scoped>
.banner {
  background-color: #fff;
  position: relative;
  min-height: 400px;
}

/* Background image */
.banner-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.15;
}

/* Responsive text tweaks */
@media (max-width: 768px) {
  .banner {
    text-align: center;
  }
}
</style>
