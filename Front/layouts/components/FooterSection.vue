<template>
  <footer class="footer">
    <div class="footer-container">
      <!-- Columns -->
      <div class="footer-columns">
        <!-- Column 1 -->
        <div class="footer-column">
          <h3 class="footer-title">مهارت‌آموزان</h3>
          <ul>
            <li v-for="page in learnersPages" :key="page.id">
              <nuxt-link
                :to="`/content/${page.slug}`"
                class="footer-link"
                @click="scrollToTop"
              >
                {{ page.title }}
              </nuxt-link>
            </li>
            <li v-if="!learnersPages.length">
              <span class="footer-link text-muted">در حال بارگذاری...</span>
            </li>
          </ul>
        </div>

        <!-- Column 2 -->
        <div class="footer-column">
          <h3 class="footer-title">آموزشگاه‌ها</h3>
          <ul>
            <li v-for="page in schoolsPages" :key="page.id">
              <nuxt-link
                :to="`/content/${page.slug}`"
                class="footer-link"
                @click="scrollToTop"
              >
                {{ page.title }}
              </nuxt-link>
            </li>
            <li v-if="!schoolsPages.length">
              <span class="footer-link text-muted">در حال بارگذاری...</span>
            </li>
          </ul>
        </div>

        <!-- Column 3 -->
        <div class="footer-column">
          <h3 class="footer-title">آنشو</h3>
          <ul>
            <li v-for="page in aboutPages" :key="page.id">
              <nuxt-link
                :to="`/content/${page.slug}`"
                class="footer-link"
                @click="scrollToTop"
              >
                {{ page.title }}
              </nuxt-link>
            </li>
            <li v-if="!aboutPages.length">
              <span class="footer-link text-muted">در حال بارگذاری...</span>
            </li>
          </ul>
        </div>
      </div>

      <!-- Bottom Section -->
      <div class="footer-bottom">
        <div class="social-icons">
          <a
            href="https://www.linkedin.com/in/onsho24/"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="LinkedIn"
            class="social-link"
            title="LinkedIn"
          >
            <i class="fab fa-linkedin"></i>
          </a>
          <a
            href="https://ble.ir/onsho24"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Bale"
            class="social-link"
            title="Bale"
          >
            <img
              src="/bale logo.png"
              alt="Bale"
              style="width: 20px; height: 20px; object-fit: contain"
            />
          </a>
          <a
            href="https://eitaa.com/onsho24"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Eitaa"
            class="social-link"
            title="Eitaa"
          >
            <img
              src="/eitaa logo.png"
              alt="Eitaa"
              style="width: 20px; height: 20px; object-fit: contain"
            />
          </a>
          <a
            href="https://t.me/onsho24"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Telegram"
            class="social-link"
            title="Telegram"
          >
            <i class="fab fa-telegram"></i>
          </a>
          <a
            href="https://www.instagram.com/onsho24?utm_source=qr&igsh=NDE0cTJuemY5dTQ4"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Instagram"
            class="social-link"
            title="Instagram"
          >
            <i class="fab fa-instagram"></i>
          </a>
          <a
            href="https://www.youtube.com/@Onsho24"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="YouTube"
            class="social-link"
            title="YouTube"
          >
            <i class="fab fa-youtube"></i>
          </a>
          <a
            href="https://x.com/onsho24"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="X (Twitter)"
            class="social-link"
            title="X (Twitter)"
          >
            <i class="fab fa-x-twitter"></i>
          </a>
        </div>
        <div class="trust-logos">
          <a
            referrerpolicy="origin"
            target="_blank"
            href="https://trustseal.enamad.ir/?id=5341364&Code=KN08WFNL5m1G0G0KrX7vM1yaXMTdIuYY"
          >
            <img
              referrerpolicy="origin"
              src="https://trustseal.enamad.ir/logo.aspx?id=5341364&Code=KN08WFNL5m1G0G0KrX7vM1yaXMTdIuYY"
              alt="نماد اعتماد الکترونیک"
              style="cursor: pointer"
              code="KN08WFNL5m1G0G0KrX7vM1yaXMTdIuYY"
            />
          </a>
          <a
            referrerpolicy="origin"
            target="_blank"
            href="https://trustseal.enamad.ir/?id=5341364&Code=KN08WFNL5m1G0G0KrX7vM1yaXMTdIuYY"
          >
            <img
              referrerpolicy="origin"
              src="https://trustseal.enamad.ir/logo.aspx?id=5341364&Code=KN08WFNL5m1G0G0KrX7vM1yaXMTdIuYY"
              alt=""
              style="cursor: pointer"
              code="KN08WFNL5m1G0G0KrX7vM1yaXMTdIuYY"
            />
          </a>
          <img
            referrerpolicy="origin"
            id="rgvjsizpfukzrgvjfukzjzpe"
            style="cursor: pointer"
            onclick="
              window.open(
                'https://logo.samandehi.ir/Verify.aspx?id=396367&p=xlaopfvlgvkaxlaogvkajyoe',
                'Popup',
                'toolbar=no, scrollbars=no, location=no, statusbar=no, menubar=no, resizable=0, width=450, height=630, top=30',
              )
            "
            alt="logo-samandehi"
            src="https://logo.samandehi.ir/logo.aspx?id=396367&p=qftibsiywlbqqftiwlbqyndt"
          />
        </div>
        <p class="copy">© 2025 آنشو | تمامی حقوق محفوظ است.</p>
      </div>
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
const learnersPages = computed(() =>
  allStaticPages.value.filter((page) => page.category_value === "learners"),
);

const schoolsPages = computed(() =>
  allStaticPages.value.filter((page) => page.category_value === "institutes"),
);

const aboutPages = computed(() =>
  allStaticPages.value.filter((page) => page.category_value === "onsho"),
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
  flex: 1 1 250px;
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
  font-size: 0.9rem;
  color: #bbb;
}

.copy {
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: #888;
}

.social-icons {
  display: grid !important;
  grid-template-columns: repeat(4, 1fr);
  justify-items: center;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

.social-link {
  color: #ccc;
  font-size: 1.5rem;
  transition: color 0.3s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  text-decoration: none;
}

.social-link:hover {
  color: #ffc107;
  transform: scale(1.1);
}

.social-link i {
  display: inline-block !important;
  line-height: 1 !important;
}

.social-link i.fab {
  font-family: "Font Awesome 6 Brands" !important;
  font-weight: 400 !important;
}

.social-link i.fas {
  font-family: "Font Awesome 6 Free" !important;
  font-weight: 900 !important;
}

.trust-logos {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin: 1rem 0;
  flex-wrap: wrap;
}

.trust-logos a {
  display: inline-block;
  text-decoration: none;
}

.trust-logos img {
  max-width: 120px;
  height: auto;
  display: block;
}

/* Responsive */
@media (max-width: 768px) {
  .footer-columns {
    flex-direction: column;
    align-items: center;
  }

  .footer-column {
    text-align: center;
  }

  .trust-logos {
    flex-wrap: nowrap;
    gap: 0.5rem;
  }

  .trust-logos img {
    max-width: 80px;
  }
}
</style>
