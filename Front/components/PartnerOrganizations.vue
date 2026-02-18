<template>
  <section class="partner-orgs-section py-3 py-md-5" dir="rtl">
    <div class="container">
      <!-- Title -->
      <div class="text-center mb-4">
        <h3 class="fw-bold mb-3 partner-title">آموزشگاه‌های همکار</h3>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">در حال بارگذاری...</span>
        </div>
      </div>

      <!-- Organizations List -->
      <div v-else-if="organizations.length > 0" class="organizations-list">
        <div class="row g-4">
          <div
            v-for="org in organizations"
            :key="org.id"
            class="col-12 col-md-6 col-lg-4"
          >
            <div class="org-card">
              <!-- Logo -->
              <div class="org-logo-wrapper">
                <img
                  v-if="org.logo"
                  :src="getMediaUrl(org.logo)"
                  :alt="org.name"
                  class="org-logo"
                />
                <div v-else class="org-logo-placeholder">
                  <i class="bi bi-building"></i>
                </div>
              </div>

              <!-- Content -->
              <div class="org-content">
                <!-- Name -->
                <h5 class="org-name">
                  <a
                    v-if="org.subdomain"
                    :href="`https://${org.subdomain}.onsho24.ir`"
                    class="text-decoration-none text-dark"
                  >
                    {{ org.name }}
                  </a>
                  <nuxt-link
                    v-else-if="org.slug"
                    :to="`/company/${org.slug}`"
                    class="text-decoration-none text-dark"
                  >
                    {{ org.name }}
                  </nuxt-link>
                  <span v-else>{{ org.name }}</span>
                  <span
                    v-if="org.is_verified"
                    class="verified-badge"
                    title="تایید شده"
                  >
                    <i class="bi bi-check-circle-fill"></i>
                  </span>
                </h5>

                <!-- Description -->
                <p v-if="org.description" class="org-description">
                  {{ org.description }}
                </p>

                <!-- Course Types -->
                <div
                  v-if="org.course_types && org.course_types.length > 0"
                  class="course-types"
                >
                  <button
                    v-for="type in org.course_types"
                    :key="type.value"
                    class="course-type-btn"
                    :class="getCourseTypeClass(type.value)"
                  >
                    {{
                      type.label === "آنلاین"
                        ? "برخط"
                        : type.label === "پیش ثبت نام حضوری"
                          ? "پیش ثبت نام حضوری"
                          : "ضبط شده"
                    }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Load More / Browse All -->
        <div class="text-center mt-5">
          <button
            v-if="hasNext"
            @click="loadMore"
            class="btn btn-outline-primary me-3"
            :disabled="loadingMore"
          >
            <span
              v-if="loadingMore"
              class="spinner-border spinner-border-sm me-2"
            ></span>
            نمایش بیشتر
          </button>
          <nuxt-link to="/company" class="btn btn-primary m-2">
            گشتن همه
          </nuxt-link>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-5">
        <p class="text-muted">هیچ آموزشگاهی یافت نشد.</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useMediaUrl } from "~/composables/useMediaUrl";

const { $api } = useNuxtApp();
const { getMediaUrl } = useMediaUrl();

const organizations = ref([]);
const loading = ref(true);
const loadingMore = ref(false);
const currentPage = ref(1);
const pageSize = ref(9);
const hasNext = ref(false);

const fetchOrganizations = async (page = 1, append = false) => {
  try {
    if (page === 1) {
      loading.value = true;
    } else {
      loadingMore.value = true;
    }

    const response = await $api.post("/course/organization/list", {
      page: page,
      page_size: pageSize.value,
    });
    console.log(response);

    if (response?.data?.status && response?.data?.data?.data) {
      const newOrgs = response.data.data.data;

      if (append) {
        organizations.value = [...organizations.value, ...newOrgs];
      } else {
        organizations.value = newOrgs;
      }

      hasNext.value = response.data.data.has_next || false;
      currentPage.value = page;
    }
  } catch (error) {
    console.error("خطا در دریافت آموزشگاه‌ها:", error);
  } finally {
    loading.value = false;
    loadingMore.value = false;
  }
};

const loadMore = () => {
  if (hasNext.value && !loadingMore.value) {
    fetchOrganizations(currentPage.value + 1, true);
  }
};

const getCourseTypeClass = (type) => {
  const typeMap = {
    online: "course-type-online",
    offline: "course-type-offline",
    in_person: "course-type-inperson",
  };
  return typeMap[type] || "";
};

onMounted(() => {
  fetchOrganizations();
});
</script>

<style scoped>
.partner-orgs-section {
  background: linear-gradient(
    to bottom,
    rgba(40, 167, 69, 0.6) 0%,
    rgba(40, 167, 69, 0.5) 30%,
    rgba(255, 140, 20, 0.5) 70%,
    rgba(255, 140, 20, 0.6) 100%
  );
  direction: rtl;
}

.partner-title {
  color: #1b5e20; /* سبز تیره برای تیتر آموزشگاه‌های همکار */
}

.org-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.org-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.org-logo-wrapper {
  width: 80px;
  height: 80px;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  border-radius: 8px;
  overflow: hidden;
}

.org-logo {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 8px;
}

.org-logo-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6c757d;
  font-size: 2rem;
}

.org-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.org-name {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #1b5e20; /* سبز برای نام آموزشگاه */
}

.verified-badge {
  color: #28a745;
  font-size: 1rem;
}

.org-description {
  color: #6c757d;
  font-size: 0.9rem;
  line-height: 1.6;
  margin-bottom: 16px;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.course-types {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: auto;
}

.course-type-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 500;
  color: white;
  cursor: default;
  transition: opacity 0.2s;
}

.course-type-btn:hover {
  opacity: 0.9;
}

.course-type-online {
  background: #ffc813;
}

.course-type-offline {
  background: #178d6e;
}

.course-type-inperson {
  background: #198754;
}

.btn-outline-primary {
  border-color: #2e7d32;
  color: #2e7d32;
}

.btn-outline-primary:hover {
  background-color: #2e7d32;
  border-color: #2e7d32;
  color: white;
}

.btn-primary {
  background-color: #ff8c14;
  border-color: #ff8c14;
}

.btn-primary:hover {
  background-color: #e67e00;
  border-color: #e67e00;
}

/* Responsive */
@media (max-width: 768px) {
  .org-card {
    padding: 16px;
  }

  .org-logo-wrapper {
    width: 60px;
    height: 60px;
  }

  .org-name {
    font-size: 1rem;
  }

  .org-description {
    font-size: 0.85rem;
  }

  .course-type-btn {
    padding: 6px 12px;
    font-size: 0.8rem;
  }

  .btn {
    font-size: 0.9rem;
    padding: 8px 16px;
  }
}
</style>
