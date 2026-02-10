<template>
  <div>
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">در حال بارگذاری...</span>
      </div>
      <p class="text-muted mt-3">در حال بارگذاری آموزشگاه...</p>
    </div>

    <!-- Organizations List -->
    <div v-else>
      <!-- Header -->
      <section class="header-gradient text-white py-5 mb-5">
        <div class="container">
          <div class="row">
            <div class="col-12 text-center">
              <h1 class="fw-bold mb-3">
                <i class="icon icon-filled-building me-2"></i>
                آموزشگاه‌ها
              </h1>
              <p class="lead">
                با بهترین آموزشگاه‌های فنی و حرفه ای کشور آشنا شوید
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- Organizations Grid -->
      <section class="container py-5">
        <div v-if="allOrganizations.length === 0" class="text-center py-5">
          <i
            class="icon icon-filled-building text-muted"
            style="font-size: 4rem"
          ></i>
          <h4 class="text-muted mt-3">آموزشگاهی یافت نشد</h4>
          <p class="text-muted">هنوز آموزشگاهی ثبت نشده است</p>
        </div>

        <div v-if="visibleOrganizations.length > 0" class="row g-4">
          <div
            v-for="organization in visibleOrganizations"
            :key="organization.id"
            class="col-lg-4 col-md-6"
          >
            <div class="card border-0 shadow-sm h-100 organization-card">
              <div class="card-body text-center p-4">
                <div class="mb-3">
                  <img
                    :src="getMediaUrl(organization.logo) || '/images/user.png'"
                    :alt="organization.name"
                    class="rounded-circle border border-3 border-primary"
                    style="width: 100px; height: 100px; object-fit: cover"
                  />
                </div>
                <h5 class="card-title fw-bold">{{ organization.name }}</h5>
                <p class="card-text text-muted small">
                  {{ organization.description?.substring(0, 120)
                  }}{{ organization.description?.length > 120 ? "..." : "" }}
                </p>
                <div class="mt-3">
                  <nuxt-link
                    :to="`/company/${organization.slug}`"
                    class="btn btn-primary btn-sm"
                  >
                    <i class="icon icon-filled-eye me-1"></i>
                    مشاهده صفحه
                  </nuxt-link>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Load More Button -->
        <div v-if="hasMoreOrganizations" class="text-center mt-5">
          <button
            @click="loadMoreOrganizations"
            class="btn btn-outline-primary"
            :disabled="loadingMore"
          >
            <span
              v-if="loadingMore"
              class="spinner-border spinner-border-sm me-2"
            ></span>
            مشاهده بیشتر
          </button>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const { $api } = useNuxtApp();
const { getMediaUrl } = useMediaUrl();

const RENDER_BATCH_SIZE = 9;

const loading = ref(true);
const loadingMore = ref(false);

const allOrganizations = ref([]);
const visibleOrganizations = ref([]);

const currentPage = ref(1);
const hasMoreOrganizations = ref(true);

const updateVisibleOrganizations = () => {
  visibleOrganizations.value = allOrganizations.value.slice(
    0,
    visibleOrganizations.value.length + RENDER_BATCH_SIZE,
  );
};

const fetchOrganizations = async () => {
  try {
    const response = await $api.post("/course/organization/list", {
      page: currentPage.value,
    });

    if (response.data.status && response.data.data.data) {
      allOrganizations.value.push(...response.data.data.data);
      hasMoreOrganizations.value = response.data.data.next !== null;

      if (visibleOrganizations.value.length === 0) {
        visibleOrganizations.value = allOrganizations.value.slice(
          0,
          RENDER_BATCH_SIZE,
        );
      }
    }
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
    loadingMore.value = false;
  }
};

const loadMoreOrganizations = async () => {
  if (visibleOrganizations.value.length < allOrganizations.value.length) {
    updateVisibleOrganizations();
    return;
  }

  if (hasMoreOrganizations.value) {
    loadingMore.value = true;
    currentPage.value++;
    await fetchOrganizations();
  }
};

definePageMeta({
  layout: "default",
});

useHead({
  title: "آموزشگاه‌های آموزشی",
  meta: [
    {
      name: "description",
      content: "با بهترین آموزشگاه‌های فنی و حرفه ای کشور آشنا شوید",
    },
  ],
});

onMounted(() => {
  fetchOrganizations();
});
</script>

<style scoped>
/* Header gradient - سبز به نارنجی */
.header-gradient {
  background: linear-gradient(
    to left,
    rgba(40, 167, 69, 0.6) 0%,
    rgba(255, 140, 20, 0.6) 100%
  );
  background-image: linear-gradient(
    to left,
    rgba(40, 167, 69, 0.7) 0%,
    rgba(40, 167, 69, 0.5) 30%,
    rgba(255, 140, 20, 0.5) 70%,
    rgba(255, 140, 20, 0.7) 100%
  );
}

.bg-primary {
  background-color: #ff8c14 !important;
}

.text-primary {
  color: #ff8c14 !important;
}

.btn-primary {
  background-color: #ff8c14;
  border-color: #ff8c14;
}

.btn-primary:hover {
  background-color: #e67a0f;
  border-color: #d66a0a;
}

.btn-outline-primary {
  color: #ff8c14;
  border-color: #ff8c14;
}

.btn-outline-primary:hover {
  background-color: #ff8c14;
  border-color: #ff8c14;
}

.border-primary {
  border-color: #ff8c14 !important;
}

.organization-card {
  transition:
    transform 0.2s ease-in-out,
    box-shadow 0.2s ease-in-out;
}

.organization-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15) !important;
}

.icon {
  font-size: 1.1rem;
}

.badge {
  font-size: 0.875rem;
}

@media (max-width: 768px) {
  .lead {
    font-size: 1rem;
  }
}
</style>
