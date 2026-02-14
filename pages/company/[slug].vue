<template>
  <div>
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">در حال بارگذاری...</span>
      </div>
      <p class="text-muted mt-3">در حال بارگذاری اطلاعات آموزشگاه...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="container py-5">
      <div class="text-center">
        <i
          class="icon icon-filled-exclamation-triangle text-warning"
          style="font-size: 4rem"
        ></i>
        <h4 class="text-muted mt-3">آموزشگاه یافت نشد</h4>
        <p class="text-muted">{{ error }}</p>
        <nuxt-link to="/" class="btn btn-primary"
          >بازگشت به صفحه اصلی</nuxt-link
        >
      </div>
    </div>

    <!-- Organization Profile -->
    <div v-else-if="organization">
      <!-- Header Section -->
      <section
        class="bg-dark-subtle text-white py-5 header d-flex align-items-center"
        :style="{
          backgroundImage:
            organizationLogoUrl && organizationLogoUrl !== '/images/user.png'
              ? `linear-gradient(rgba(43, 45, 66, 0.85), rgba(43, 45, 66, 0.85)), url(${organizationLogoUrl})`
              : 'none',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundRepeat: 'no-repeat',
        }"
      >
        <div class="container mt-0">
          <div class="d-flex justify-content-start gap-3 align-items-start">
            <div>
              <h1 class="fw-bold">{{ organization.name }}</h1>
              <p v-if="organization.website_url" class="text-white">
                <a
                  :href="organization.website_url"
                  target="_blank"
                  class="text-white text-decoration-none"
                >
                  {{ organization.website_url }}
                </a>
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- Organization Details Section -->
      <section class="container py-5">
        <div class="row">
          <!-- Organization Info Card -->
          <div class="col-lg-12 mb-5">
            <div class="card border-0 shadow-sm">
              <div class="card-header bg-light border-0 py-3">
                <h5 class="mb-0 text-dark">
                  <i class="icon icon-filled-info-circle text-primary me-2"></i>
                  درباره {{ organization.name }}
                </h5>
              </div>
              <div class="card-body">
                <p class="text-muted lh-lg" v-if="organization.description">
                  {{ organization.description }}
                </p>
                <p class="text-muted lh-lg" v-else>
                  توضیحاتی برای این آموزشگاه ثبت نشده است.
                </p>

                <div v-if="organization.website_url" class="mt-3">
                  <a
                    :href="organization.website_url"
                    target="_blank"
                    class="btn btn-outline-primary"
                  >
                    <i class="icon icon-filled-external-link me-2"></i>
                    مشاهده وب‌سایت
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>

        <CategoryMenu
          :categories="categories"
          :selectedCategoryId="selectedCategoryId"
          :getMediaUrl="getMediaUrl"
          @selectCategory="selectCategory"
          @clearCategoryFilter="clearCategoryFilter"
        />

        <!-- Organization Courses -->
        <CourseList
          :organization="organization"
          :courses="courses"
          :coursesLoading="coursesLoading"
          :visibleCourses="visibleCourses"
          :filteredCourses="filteredCourses"
          :visibleCount="visibleCount"
          :hasMoreCourses="hasMoreCourses"
          :getMediaUrl="getMediaUrl"
          :getCourseTypeBadgeClass="getCourseTypeBadgeClass"
          :getCourseTypeIcon="getCourseTypeIcon"
          :formatPrice="formatPrice"
          :loadMoreCourses="loadMoreCourses"
        />
      </section>
    </div>
  </div>
</template>

<script setup>
import {
  ref,
  onMounted,
  onBeforeUnmount,
  computed,
  watch,
  nextTick,
} from "vue";
import CategoryMenu from "./components/CategoryMenu.vue";
import CourseList from "./components/CourseList.vue";

// Get route params
const route = useRoute();
const { $api } = useNuxtApp();
const { getMediaUrl } = useMediaUrl();
const { setCompanyLogo, clearCompanyLogo } = useCompanyLogo();
const { setCurrentOrganizationId, clearCurrentOrganizationId } =
  useCurrentOrganization();
const categoryTree = ref([]);

// Reactive data
const loading = ref(true);
const coursesLoading = ref(false);
const organization = ref(null);
const courses = ref([]);
const categories = ref([]);
const selectedCategoryId = ref(null);
const error = ref("");
const currentPage = ref(1);
const hasMoreCourses = ref(true);
const renderStep = 6;
const visibleCount = ref(renderStep);

// Organization stats (mock data for now)
const organizationStats = ref({
  courses: 0,
  students: 0,
  teachers: 0,
  rating: 0,
});

const level2Categories = computed(() => {
  if (!categoryTree.value.length || !allCourses.value.length) return [];

  const level3Ids = new Set(
    allCourses.value.map((course) => course.category?.id).filter(Boolean),
  );

  const result = [];

  categoryTree.value.forEach((level1) => {
    level1.children?.forEach((level2) => {
      const hasMatchingLevel3 = level2.children?.some((level3) =>
        level3Ids.has(level3.id),
      );

      if (hasMatchingLevel3) {
        result.push(level2);
      }
    });
  });

  return result;
});

// تبدیل آدرس logo به آدرس با /api
const organizationLogoUrl = computed(() => {
  const defaultUrl = "/images/user.png";
  const url = organization.value?.logo || defaultUrl;
  return getMediaUrl(url);
});

// Fetch organization data
const fetchOrganization = async () => {
  try {
    // Check if we're on a subdomain
    let org = null;
    if (process.client) {
      const host = window.location.hostname;
      const subdomainMatch = host.match(/^([a-z0-9-]+)\.onsho24\.ir$/);

      if (subdomainMatch) {
        // We're on a subdomain, fetch organization by subdomain
        const subdomain = subdomainMatch[1];
        try {
          const domainResponse = await $api.post(
            "/course/organization/check-domain",
            {
              subdomain: subdomain, // API از subdomain استفاده می‌کند
            },
          );

          // بررسی ساختار پاسخ API
          if (domainResponse.data.status && domainResponse.data.data) {
            // اگر subdomain اشغال است (available: false)، organizer وجود دارد
            if (
              domainResponse.data.data.available === false &&
              domainResponse.data.data.organizer_id
            ) {
              // اگر organizer کامل در پاسخ وجود دارد، از آن استفاده کن
              if (
                domainResponse.data.data.slug &&
                domainResponse.data.data.name
              ) {
                org = {
                  id: domainResponse.data.data.organizer_id,
                  slug: domainResponse.data.data.slug,
                  name: domainResponse.data.data.name,
                  logo: domainResponse.data.data.logo,
                  description: domainResponse.data.data.description,
                  website_url: domainResponse.data.data.website_url,
                  is_active: domainResponse.data.data.is_active,
                  is_verified: domainResponse.data.data.is_verified,
                };
              } else {
                // اگر organizer کامل نیست، از API list استفاده می‌کنیم (fallback)
                const listResponse = await $api.post(
                  "/course/organization/list",
                  {},
                );

                if (listResponse.data.status && listResponse.data.data.data) {
                  // پیدا کردن organizer با ID
                  org = listResponse.data.data.data.find(
                    (o) => o.id === domainResponse.data.data.organizer_id,
                  );
                }
              }
            }
          }
        } catch (err) {
          console.error("خطا در بررسی زیردامنه:", err);
        }
      }
    }

    // If not found by subdomain, fetch organization by slug
    if (!org) {
      const response = await $api.post("/course/organization/by-slug", {
        slug: route.params.slug,
      });
      // API returns { status, data: { count, page, data: [organization] } }
      if (response.data.status && response.data.data?.data?.length) {
        org = response.data.data.data[0];
      }
    }

    if (org) {
      organization.value = org;
      // Set organization_id for search functionality
      setCurrentOrganizationId(org.id);
      await fetchOrganizationCourses();
      await fetchOrganizationStats();
    } else {
      error.value = "آموزشگاه مورد نظر یافت نشد";
    }
  } catch (err) {
    console.error("خطا در دریافت آموزشگاه:", err);
    error.value = "خطا در دریافت اطلاعات آموزشگاه";
  } finally {
    loading.value = false;
  }
};

// Store all courses (unfiltered)
const allCourses = ref([]);

// Fetch organization courses
const fetchOrganizationCourses = async () => {
  if (!organization.value) return;

  coursesLoading.value = true;
  try {
    const response = await $api.post("/course/list", {
      organizer_id: organization.value.id,
      page: currentPage.value,
    });

    if (response.data.status && response.data.data.data) {
      if (currentPage.value === 1) {
        allCourses.value = response.data.data.data;
        courses.value = response.data.data.data;
        // Extract unique categories from courses
        const categoryMap = new Map();
        response.data.data.data.forEach((course) => {
          if (course.category && course.category.id) {
            // Use category id as key to avoid duplicates
            if (!categoryMap.has(course.category.id)) {
              categoryMap.set(course.category.id, course.category);
            }
          }
        });
        categories.value = level2Categories.value;
      } else {
        allCourses.value.push(...response.data.data.data);
        courses.value.push(...response.data.data.data);
        // Update categories with new courses' categories
        const categoryMap = new Map();
        categories.value.forEach((cat) => categoryMap.set(cat.id, cat));
        response.data.data.data.forEach((course) => {
          if (course.category && course.category.id) {
            if (!categoryMap.has(course.category.id)) {
              categoryMap.set(course.category.id, course.category);
            }
          }
        });
        categories.value = level2Categories.value;
      }

      hasMoreCourses.value = response.data.data.next !== null;

      // Apply category filter if one is selected
      if (selectedCategoryId.value) {
        applyCategoryFilter();
      }
    }
  } catch (err) {
    console.error("خطا در دریافت دوره‌ها:", err);
  } finally {
    coursesLoading.value = false;
  }
};

function normalize(items) {
  return (items || []).map((item) => ({
    ...item,
    children: Array.isArray(item.children) ? normalize(item.children) : [],
  }));
}

const fetchCategoryTree = async () => {
  try {
    const res = await $api.post("/course/category/list", {});
    const data = res?.data?.data ?? res?.data ?? [];
    categoryTree.value = normalize(data);
  } catch (err) {
    console.error("خطا در دریافت دسته‌بندی‌ها:", err);
  }
};

// Filter courses by selected category
const filteredCourses = computed(() => {
  if (!selectedCategoryId.value) {
    return courses.value;
  }
  return courses.value.filter(
    (course) => course.category?.parent === selectedCategoryId.value,
  );
});

const visibleCourses = computed(() => {
  return filteredCourses.value.slice(0, visibleCount.value);
});

// Apply category filter to courses
const applyCategoryFilter = () => {
  if (!selectedCategoryId.value) {
    courses.value = allCourses.value;
    return;
  }
  courses.value = allCourses.value.filter(
    (course) => course.category?.parent === selectedCategoryId.value,
  );

  console.log(
    allCourses.value.filter(
      (course) => course.category?.parent === selectedCategoryId.value,
    ),
  );
};

// Select category and filter courses
const selectCategory = (categoryId) => {
  if (selectedCategoryId.value === categoryId) {
    // If clicking the same category, clear the filter
    clearCategoryFilter();
    return;
  }

  selectedCategoryId.value = categoryId;
  applyCategoryFilter();
  visibleCount.value = renderStep;
};

// Clear category filter
const clearCategoryFilter = () => {
  selectedCategoryId.value = null;
  courses.value = allCourses.value;
  visibleCount.value = renderStep;
};

// Fetch organization stats (mock implementation)
const fetchOrganizationStats = async () => {
  // This would typically come from an API endpoint
  // For now, we'll use mock data
  organizationStats.value = {
    courses: courses.value.length,
    students: Math.floor(Math.random() * 1000) + 100,
    teachers: Math.floor(Math.random() * 50) + 5,
    rating: (Math.random() * 2 + 3).toFixed(1), // Random rating between 3.0 and 5.0
  };
};

// Load more courses
const loadMoreCourses = async () => {
  if (visibleCount.value < filteredCourses.value.length) {
    visibleCount.value += renderStep;
    return;
  }

  if (hasMoreCourses.value) {
    currentPage.value++;
    await fetchOrganizationCourses();
  }
};

// Format date
const formatDate = (dateString) => {
  if (!dateString) return "نامشخص";
  const date = new Date(dateString);
  return date.toLocaleDateString("fa-IR");
};

// Format price
const formatPrice = (price) => {
  if (!price) return "رایگان";
  return new Intl.NumberFormat("fa-IR").format(price);
};

watch(
  [categoryTree, allCourses],
  () => {
    categories.value = level2Categories.value;
  },
  { immediate: true },
);

// Get course type badge class
const getCourseTypeBadgeClass = (typeValue) => {
  switch (typeValue) {
    case "online":
      return "bg-success";
    case "offline":
    case "in_person":
      return "bg-info";
    case "hybrid":
      return "bg-warning";
    default:
      return "bg-secondary";
  }
};

// Get course type icon
const getCourseTypeIcon = (typeValue) => {
  switch (typeValue) {
    case "online":
      return "icon icon-filled-monitor";
    case "offline":
    case "in_person":
      return "icon icon-filled-location";
    case "hybrid":
      return "icon icon-filled-swap";
    default:
      return "icon icon-filled-info-circle";
  }
};

// Page meta
definePageMeta({
  layout: "default",
});

// Computed favicon link for useHead
const faviconLink = computed(() => {
  const logoUrl = organizationLogoUrl.value;
  const hasValidLogo =
    logoUrl &&
    logoUrl !== "/images/user.png" &&
    logoUrl !== "/images/logo-fani.png";

  if (!hasValidLogo) return [];

  const timestamp = Date.now();
  return [
    { rel: "icon", type: "image/png", href: `${logoUrl}?t=${timestamp}` },
    {
      rel: "shortcut icon",
      type: "image/png",
      href: `${logoUrl}?t=${timestamp}`,
    },
    { rel: "apple-touch-icon", href: `${logoUrl}?t=${timestamp}` },
  ];
});

// SEO - Dynamic title, meta and favicon
useHead(() => ({
  title: organization.value
    ? `${organization.value.name} - آموزشگاه`
    : "آموزشگاه",
  meta: [
    {
      name: "description",
      content: organization.value?.description || "صفحه آموزشگاه",
    },
  ],
  link: faviconLink.value,
}));

// Function to update favicon
const updateFavicon = (logoUrl) => {
  if (!process.client || !logoUrl) return;

  try {
    // Remove ALL existing favicon links
    const allFaviconSelectors = [
      "link[rel='icon']",
      "link[rel='shortcut icon']",
      "link[rel='shortcut']",
      "link[rel*='icon']",
      "link[rel*='apple-touch-icon']",
    ];

    allFaviconSelectors.forEach((selector) => {
      try {
        const links = document.querySelectorAll(selector);
        links.forEach((link) => {
          if (link && link.parentNode) {
            link.remove();
          }
        });
      } catch (e) {
        console.warn("Error removing favicon links:", e);
      }
    });

    // Create new favicon with timestamp to prevent caching
    const timestamp = Date.now();
    const logoWithTimestamp = `${logoUrl}?t=${timestamp}`;

    // Create and add favicon link (most important - must be first)
    const faviconLink = document.createElement("link");
    faviconLink.rel = "icon";
    faviconLink.type = "image/png";
    faviconLink.href = logoWithTimestamp;
    if (document.head.firstChild) {
      document.head.insertBefore(faviconLink, document.head.firstChild);
    } else {
      document.head.appendChild(faviconLink);
    }

    // Also try to update existing favicon if it exists
    const existingFavicon = document.querySelector("link[rel='icon']");
    if (existingFavicon) {
      existingFavicon.href = logoWithTimestamp;
    }

    // Create and add shortcut icon
    const shortcutLink = document.createElement("link");
    shortcutLink.rel = "shortcut icon";
    shortcutLink.type = "image/png";
    shortcutLink.href = logoWithTimestamp;
    document.head.appendChild(shortcutLink);

    // Create and add apple-touch-icon
    const appleLink = document.createElement("link");
    appleLink.rel = "apple-touch-icon";
    appleLink.href = logoWithTimestamp;
    document.head.appendChild(appleLink);

    // Force browser to reload favicon by updating the href multiple times
    setTimeout(() => {
      const favicon = document.querySelector("link[rel='icon']");
      if (favicon) {
        favicon.href = `${logoUrl}?t=${Date.now()}`;
      }
    }, 100);
  } catch (error) {
    console.error("Error updating favicon:", error);
  }
};

// Watch for organization logo changes and update favicon and header logo
watch(
  organizationLogoUrl,
  (newLogoUrl) => {
    if (process.client) {
      if (
        newLogoUrl &&
        newLogoUrl !== "/images/user.png" &&
        newLogoUrl !== "/images/logo-fani.png"
      ) {
        // Set company logo for header
        setCompanyLogo(newLogoUrl);

        // Update favicon with multiple attempts
        nextTick(() => {
          updateFavicon(newLogoUrl);
        });

        // Retry after delays to ensure it works
        setTimeout(() => updateFavicon(newLogoUrl), 100);
        setTimeout(() => updateFavicon(newLogoUrl), 300);
        setTimeout(() => updateFavicon(newLogoUrl), 600);
        setTimeout(() => updateFavicon(newLogoUrl), 1000);
      } else {
        clearCompanyLogo();
      }
    }
  },
  { immediate: true },
);

// Also watch organization to update favicon when organization loads
watch(
  organization,
  (newOrg) => {
    if (process.client && newOrg && organizationLogoUrl.value) {
      const logoUrl = organizationLogoUrl.value;
      if (
        logoUrl &&
        logoUrl !== "/images/user.png" &&
        logoUrl !== "/images/logo-fani.png"
      ) {
        setTimeout(() => updateFavicon(logoUrl), 500);
        setTimeout(() => updateFavicon(logoUrl), 1500);
      }
    }
  },
  { immediate: true },
);

// Clear company logo when leaving the page
onBeforeUnmount(() => {
  clearCompanyLogo();
  clearCurrentOrganizationId();
});

const loadData = async () => {
  await fetchCategoryTree();
  await fetchOrganization();
};

// Lifecycle
onMounted(() => {
  loadData();

  // If we're on a subdomain, update the URL to show only subdomain (without /company/slug)
  // This keeps the content but changes the URL in address bar
  if (process.client) {
    const host = window.location.hostname;
    const subdomainMatch = host.match(/^([a-z0-9-]+)\.onsho24\.ir$/);

    if (subdomainMatch && route.path.startsWith("/company/")) {
      // We're on a subdomain and in company page
      // Update URL to just subdomain (without /company/slug) using replaceState
      // This doesn't trigger a reload or navigation
      const newUrl = `${window.location.protocol}//${host}${window.location.search || ""}${window.location.hash || ""}`;

      // Use nextTick to ensure the page is fully loaded before changing URL
      nextTick(() => {
        window.history.replaceState({}, "", newUrl);
      });
    }
  }

  // Also update favicon after mount to ensure it works
  if (process.client && organizationLogoUrl.value) {
    const logoUrl = organizationLogoUrl.value;
    if (
      logoUrl &&
      logoUrl !== "/images/user.png" &&
      logoUrl !== "/images/logo-fani.png"
    ) {
      setTimeout(() => updateFavicon(logoUrl), 500);
      setTimeout(() => updateFavicon(logoUrl), 1500);
      setTimeout(() => updateFavicon(logoUrl), 3000);
    }
  }
});
</script>

<style scoped>
/* Header Section */
.header {
  padding-top: 150px !important;
}

.bg-dark-subtle {
  background-color: rgba(43, 45, 66, 1) !important;
}

.text-primary {
  color: #ff6b35 !important;
}

/* Button Styles */
.btn-primary {
  background-color: #ff6b35;
  border-color: #ff6b35;
}

.btn-primary:hover {
  background-color: #ff8c42;
  border-color: #ff7a2e;
}

.btn-outline-primary {
  color: #ff6b35;
  border-color: #ff6b35;
}

.btn-outline-primary:hover {
  background-color: #ff6b35;
  border-color: #ff6b35;
  color: #ffffff !important;
}

.border-primary {
  border-color: #ff6b35 !important;
}

.badge.bg-primary {
  background-color: #ff6b35 !important;
}

/* Card Styles */
.card {
  transition: transform 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-2px);
}

/* Icon Styles */
.icon {
  font-size: 1.1rem;
}

/* Category Styles */
.category-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 15px;
  border-radius: 15px;
  min-width: 120px;
  max-width: 150px;
}

.category-item:hover {
  transform: translateY(-5px);
  background-color: #f8f9fa;
}

.category-item.active {
  background-color: #fff5f0;
  border: 2px solid #ff6b35;
}

.category-icon {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-color: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
  overflow: hidden;
  border: 3px solid #e9ecef;
  transition: all 0.3s ease;
}

.category-item:hover .category-icon {
  border-color: #ff6b35;
  transform: scale(1.05);
}

.category-item.active .category-icon {
  border-color: #ff6b35;
  background-color: #fff;
}

.category-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.category-placeholder-icon {
  font-size: 2.5rem;
  color: #6c757d;
}

.category-item.active .category-placeholder-icon {
  color: #ff6b35;
}

.category-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #495057;
  text-align: center;
  line-height: 1.3;
  margin-top: 5px;
}

.category-item.active .category-label {
  color: #ff6b35;
  font-weight: 700;
}

/* Media Queries for Mobile */
@media (max-width: 768px) {
  .header {
    padding-top: 100px !important;
  }

  .d-flex {
    flex-direction: column;
    text-align: center;
  }

  .d-flex img {
    margin-bottom: 1rem;
  }

  .category-item {
    min-width: 100px;
    max-width: 120px;
    padding: 10px;
  }

  .category-icon {
    width: 80px;
    height: 80px;
  }

  .category-label {
    font-size: 0.8rem;
  }
}

/* Mobile Categories Menu */
.custom-category-menu-container {
  display: flex;
  overflow-x: auto;
  padding: 0.5rem 0;
  gap: 1rem;
  margin-top: -8px;
  margin-bottom: 18px;
}

.custom-category-item {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0.15rem 1.2rem;
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.3s ease;
  max-width: 150px;
  min-width: 120px;
}

.custom-category-item:hover {
  background-color: #f1f1f1;
}

.custom-active {
  background-color: #ff6b35;
  color: white;
}

.custom-category-item:not(.custom-active) {
  background-color: #f8f9fa;
  color: #495057;
}

.custom-category-text {
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  word-wrap: break-word;
  word-break: break-word;
  white-space: normal;
  max-height: 4rem;
}

/* Course Type Badge Styles */
.custom-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  width: fit-content;
  max-width: 100%;
  white-space: nowrap;
}

.custom-badge i {
  margin-right: 0.25rem;
}
</style>
