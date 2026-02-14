<template>
  <footer class="footer">
    <div class="footer-container">
      <!-- Columns -->
      <div class="footer-columns">
        <!-- Column 1 -->

        <div class="footer-column">
          <h3 class="footer-title">مهارت‌ها</h3>
          <ul>
            <li v-for="page in skillsPages" :key="page.id">
              <nuxt-link
                :to="`/content/${page.slug}`"
                class="footer-link"
                @click="scrollToTop"
              >
                {{ page.title }}
              </nuxt-link>
            </li>
            <li v-if="!skillsPages.length">
              <span class="footer-link text-muted">در حال بارگذاری...</span>
            </li>
          </ul>
        </div>

        <!-- Column 2 -->

        <div class="footer-column">
          <h3 class="footer-title">برنامه‌ها</h3>
          <ul>
            <li v-for="page in programsPages" :key="page.id">
              <nuxt-link
                :to="`/content/${page.slug}`"
                class="footer-link"
                @click="scrollToTop"
              >
                {{ page.title }}
              </nuxt-link>
            </li>
            <li v-if="!programsPages.length">
              <span class="footer-link text-muted">در حال بارگذاری...</span>
            </li>
          </ul>
        </div>

        <!-- Column 3 -->
        <div class="footer-column">
          <h3 class="footer-title">صنایع و حرفه‌ها</h3>
          <ul>
            <li v-for="page in industriesPages" :key="page.id">
              <nuxt-link
                :to="`/content/${page.slug}`"
                class="footer-link"
                @click="scrollToTop"
              >
                {{ page.title }}
              </nuxt-link>
            </li>
            <li v-if="!industriesPages.length">
              <span class="footer-link text-muted">در حال بارگذاری...</span>
            </li>
          </ul>
        </div>

        <!-- Column 4 -->
        <div class="footer-column">
          <h3 class="footer-title">مراکز تخصصی</h3>
          <ul>
            <li v-for="page in centersPages" :key="page.id">
              <nuxt-link
                :to="`/content/${page.slug}`"
                class="footer-link"
                @click="scrollToTop"
              >
                {{ page.title }}
              </nuxt-link>
            </li>
            <li v-if="!centersPages.length">
              <span class="footer-link text-muted">در حال بارگذاری...</span>
            </li>
          </ul>
        </div>
      </div>
      <!-- Bottom -->
    </div>
  </footer>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const allStaticPages = ref([]);

const loadStaticPages = async () => {
  try {
    const { $api } = useNuxtApp();
    const res = await $api.get("/static-content/list");
    const data = res?.data?.data ?? res?.data ?? [];

    // Helper function to generate slug from title
    const generateSlug = (title) => {
      if (!title) return "";
      return title
        .toLowerCase()
        .replace(
          /[^\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFFa-z0-9]+/g,
          "-",
        )
        .replace(/^-+|-+$/g, "");
    };

    // Sort by display_order
    allStaticPages.value = Array.isArray(data)
      ? data
          .map((i) => ({
            id: i.id,
            title: i.title,
            slug: i.slug || generateSlug(i.title),
            category: i.category,
            category_value: i.category_value,
            display_order: i.display_order || 0,
          }))
          .sort((a, b) => (a.display_order || 0) - (b.display_order || 0))
      : [];
  } catch (e) {
    allStaticPages.value = [];
    console.error("Error loading static pages:", e);
  }
};

// Filter pages by category_value
const skillsPages = computed(() =>
  allStaticPages.value.filter((page) => page.category_value === "skills"),
);

const programsPages = computed(() =>
  allStaticPages.value.filter((page) => page.category_value === "programs"),
);

const industriesPages = computed(() =>
  allStaticPages.value.filter((page) => page.category_value === "industries"),
);

const centersPages = computed(() =>
  allStaticPages.value.filter((page) => page.category_value === "centers"),
);

const scrollToTop = () => {
  // Check if we're on mobile
  if (window.innerWidth <= 768) {
    // Use nextTick to ensure navigation is complete
    nextTick(() => {
      setTimeout(() => {
        window.scrollTo({
          top: 0,
          behavior: "smooth",
        });
      }, 100);
    });
  }
};

// Watch for route changes to scroll to top on mobile
watch(
  () => route.path,
  (newPath, oldPath) => {
    if (newPath.startsWith("/content/") && window.innerWidth <= 768) {
      nextTick(() => {
        setTimeout(() => {
          window.scrollTo({
            top: 0,
            behavior: "smooth",
          });
        }, 300);
      });
    }
  },
);

onMounted(loadStaticPages);
</script>

<style scoped>
.footer {
  background-color: #2d4d3d;
  color: #eaeaea;
  padding: 3rem 1rem 1.5rem;
  direction: rtl;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
}

.footer-columns {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
  padding-bottom: 2rem;
}

.footer-column {
  flex: 1 1 240px;
  text-align: center;
}

.footer-column ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #ffc107;
  margin-bottom: 1rem;
}

.footer-link {
  display: block;
  color: #ccc;
  text-decoration: none;
  padding: 0.3rem 0;
  transition: color 0.3s ease;
}

.footer-link:hover {
  color: #fff;
}

.footer-bottom {
  text-align: center;
  margin-top: 2rem;
  font-size: 0.85rem;
  color: #888;
}

/* Responsive */
@media (max-width: 768px) {
  .footer-columns {
    flex-direction: column;
    text-align: center;
    align-items: center;
  }
}
</style>
