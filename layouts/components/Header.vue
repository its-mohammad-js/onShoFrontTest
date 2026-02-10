<template>
  <nav class="navbar navbar-expand-lg bg-white shadow-sm py-md-3 sticky-top">
    <div class="container d-flex align-items-center justify-content-between">
      <!-- 🔹 Logo + Categories Button -->
      <div class="d-flex align-items-center gap-3">
        <!-- Logo -->
        <nuxt-link
          to="/"
          class="navbar-brand d-flex align-items-center logo-size"
        >
          <img :src="headerLogo" alt="فنی و حرفه ای" class="logo-size" />
        </nuxt-link>

        <!-- 🟢 Categories Button (Desktop Only) -->
        <div class="position-relative d-none d-md-block">
          <button
            ref="categoryButtonRef"
            class="btn btn-outline-secondary px-3 py-1 d-flex align-items-center gap-2 category-btn"
            @click="toggleCategories"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="size-6"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
              />
            </svg>

            دسته‌بندی‌ها
          </button>

          <!-- Dropdown Menu Panel -->
          <div
            v-if="isCategoriesOpen"
            ref="menuPanelRef"
            class="category-menu-container position-absolute end-0 mt-2 shadow rounded bg-white"
          >
            <!-- Close Button (Mobile Only) -->
            <button
              class="category-close-btn d-md-none"
              @click="closeCategories"
              aria-label="بستن منو"
            >
              <i class="fa-solid fa-times"></i>
            </button>
            <CategoryMenu @navigate="handleCategoryNavigate" />
          </div>
        </div>

        <!-- Categories Menu Panel (Mobile - Outside navbar-collapse) -->
        <div
          v-if="isCategoriesOpen"
          ref="mobileMenuPanelRef"
          class="category-menu-container position-fixed d-md-none"
        >
          <!-- Close Button (Mobile Only) -->
          <button
            class="category-close-btn d-md-none"
            @click="closeCategories"
            aria-label="بستن منو"
          >
            <i class="fa-solid fa-times"></i>
          </button>
          <CategoryMenu @navigate="handleCategoryNavigate" />
        </div>

        <div
          class="collapse navbar-collapse"
          :class="{ show: isMenuOpen }"
          id="navbarNav"
          ref="menuRef"
        >
          <!-- Logo (Visible only in Mobile Menu) -->
          <!-- Navbar links (Center in Desktop, Full-width in Mobile) -->
          <ul class="navbar-nav mx-auto">
            <!-- Categories Button (Mobile Only) -->
            <li class="nav-item d-md-none">
              <button
                class="nav-link btn btn-outline-secondary w-100 d-flex align-items-center justify-content-start category-btn-mobile"
                @click="toggleCategories"
              >
                <span>دسته‌بندی‌ها</span>
              </button>
            </li>
            <li class="nav-item">
              <nuxt-link
                class="nav-link d-flex align-items-center justify-content-start"
                to="/company"
                @click="closeMenu"
              >
                <span>آموزشگاه‌ها</span>
              </nuxt-link>
            </li>
            <li class="nav-item d-md-none">
              <nuxt-link
                class="nav-link d-flex align-items-center justify-content-start"
                to="/card"
                @click="closeMenu"
              >
                <span>سبد خرید</span>
              </nuxt-link>
            </li>
          </ul>
          <!-- Mobile Auth Buttons -->
          <div class="d-md-none mt-3 px-3">
            <div v-if="!auth.authenticated">
              <nuxt-link
                to="/auth"
                class="btn btn-danger w-100"
                @click="closeMenu"
                >ورود / ثبت نام</nuxt-link
              >
            </div>
            <div v-else>
              <nuxt-link
                class="btn btn-danger w-100"
                to="/account"
                @click="closeMenu"
                >حساب کاربری</nuxt-link
              >
            </div>
          </div>
        </div>

        <!-- Mobile Menu Overlay -->
        <div
          v-if="isMenuOpen"
          class="mobile-menu-overlay d-md-none"
          @click="closeMenu"
        ></div>

        <!-- Categories Menu Overlay (Mobile) -->
        <div
          v-if="isCategoriesOpen"
          class="mobile-menu-overlay d-md-none"
          @click="closeCategories"
          style="z-index: 1055"
        ></div>
      </div>

      <!-- 🔸 Mobile Toggle -->
      <button
        ref="menuButtonRef"
        class="navbar-toggler shadow-none d-md-none"
        type="button"
        @click="toggleMenu"
        :class="{ collapsed: !isMenuOpen }"
        aria-controls="navbarNav"
        aria-expanded="isMenuOpen ? 'true' : 'false'"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- 🔹 Desktop Right Side -->
      <div class="d-none d-md-flex align-items-center gap-3">
        <!-- Search -->
        <div
          class="search-box d-flex align-items-center shadow-sm gap-3 position-relative"
        >
          <input
            v-model="searchTerm"
            type="text"
            class="form-control shadow-none border-0 px-3 py-2"
            placeholder="دوست داری چی یاد بگیری؟"
            @keyup.enter="handleSearch"
          />
          <button class="btn text-white search-btn" @click="handleSearch">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="size-16 p-2 bg-danger rounded-circle"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"
              />
            </svg>
          </button>

          <!-- Live search dropdown -->
          <div
            v-if="showSearchDropdown"
            class="search-dropdown shadow-sm rounded bg-white"
          >
            <div
              v-if="isSearching"
              class="search-loading text-muted small py-2 px-3"
            >
              در حال جستجو...
            </div>

            <template v-else>
              <div
                v-if="!hasSearchResults"
                class="search-empty text-muted small py-2 px-3"
              >
                نتیجه‌ای یافت نشد
              </div>

              <div v-else class="search-results">
                <div v-if="searchResultsCourses.length" class="search-section">
                  <div
                    class="search-section-title px-3 pt-2 pb-1 small text-muted"
                  >
                    دوره‌ها
                  </div>
                  <button
                    v-for="course in searchResultsCourses"
                    :key="`course-${course.id}`"
                    type="button"
                    class="search-item w-100 text-start px-3 py-2"
                    @click="goToCourseFromSearch(course)"
                  >
                    <div class="fw-bold small text-truncate">
                      {{ course.title }}
                    </div>
                    <div
                      v-if="course.organizer?.name"
                      class="text-muted tiny-text mt-1"
                    >
                      برگزارکننده: {{ course.organizer.name }}
                    </div>
                  </button>
                </div>

                <div
                  v-if="searchResultsCategories.length"
                  class="search-section"
                >
                  <div
                    class="search-section-title px-3 pt-2 pb-1 small text-muted border-top"
                  >
                    دسته‌بندی‌ها
                  </div>
                  <button
                    v-for="category in searchResultsCategories"
                    :key="`cat-${category.id}`"
                    type="button"
                    class="search-item w-100 text-start px-3 py-2"
                    @click="goToCategoryFromSearch(category)"
                  >
                    <div class="fw-bold small text-truncate">
                      {{ category.title }}
                    </div>
                  </button>
                </div>
              </div>
            </template>
          </div>
        </div>

        <!-- Cart -->
        <!-- <div class="cart-icon-container position-relative">
          <nuxt-link to="/checkout" class="cart-button">
            <i class="fa-solid fa-shopping-cart" style="font-size: 18px"></i>
            <span v-if="cartStore.cartItems.length" class="cart-badge">
              {{ cartStore.cartItems.length }}
            </span>
          </nuxt-link>
        </div> -->

        <div class="cart-icon-container position-relative">
          <nuxt-link to="/checkout" class="btn btn-danger">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="size-6"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 0 0-16.536-1.84M7.5 14.25 5.106 5.272M6 20.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm12.75 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z"
              />
            </svg>
            <span v-if="cartStore.cartItems.length" class="cart-badge">
              {{ cartStore.cartItems.length }}
            </span>
          </nuxt-link>
        </div>

        <!-- Auth -->
        <span v-if="!auth.authenticated">
          <nuxt-link to="/auth" class="btn btn-danger px-4 me-3"
            >ورود / ثبت نام</nuxt-link
          >
        </span>
        <span v-else>
          <nuxt-link class="btn btn-danger px-3 me-3" to="/account"
            >حساب کاربری</nuxt-link
          >
        </span>
      </div>

      <!-- Mobile Search Box -->
      <div v-if="route.path === '/'" class="d-md-none mt-2">
        <div
          class="search-box-mobile d-flex align-items-center shadow-sm gap-3 position-relative"
        >
          <input
            v-model="searchTerm"
            type="text"
            class="form-control shadow-none border-0 px-3 py-2"
            placeholder="دوست داری چی یاد بگیری؟"
            @keyup.enter="handleSearch"
          />
          <button class="btn text-white search-btn" @click="handleSearch">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="size-16 p-2 bg-danger rounded-circle"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import {
  ref,
  onMounted,
  onBeforeUnmount,
  nextTick,
  computed,
  watch,
} from "vue";
import { useRouter } from "vue-router";
import { useNuxtApp } from "#app";
import CategoryMenu from "@/components/CategoryMenu.vue";
import { useCartStore } from "@/stores/cart";
import { useAuthStore } from "@/stores/auth";
import { useCompanyLogo } from "@/composables/useCompanyLogo";
import { useCurrentOrganization } from "@/composables/useCurrentOrganization";
import { useRoute } from "vue-router";

const route = useRoute();

const isMobileSearchOpen = ref(false);

const toggleMobileSearch = () => {
  isMobileSearchOpen.value = !isMobileSearchOpen.value;
};

const cartStore = useCartStore();
const auth = useAuthStore();
const { companyLogo } = useCompanyLogo();
const { currentOrganizationId } = useCurrentOrganization();
const router = useRouter();
const { $api } = useNuxtApp();

// Use company logo if available, otherwise use default logo
const headerLogo = computed(() => {
  return companyLogo.value || "/images/logo-fani.png";
});

const isMenuOpen = ref(false);
const isCategoriesOpen = ref(false);
const menuButtonRef = ref(null);
const menuPanelRef = ref(null);
const mobileMenuPanelRef = ref(null);
const categoryButtonRef = ref(null);
const searchTerm = ref("");

// Search suggestions state
const isSearching = ref(false);
const searchResultsCourses = ref([]);
const searchResultsCategories = ref([]);
const searchDebounceTimer = ref(null);

const hasSearchResults = computed(
  () =>
    searchResultsCourses.value.length > 0 ||
    searchResultsCategories.value.length > 0,
);

const showSearchDropdown = computed(
  () =>
    searchTerm.value.trim().length > 0 &&
    (isSearching.value || hasSearchResults.value),
);

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

const closeMenu = () => {
  isMenuOpen.value = false;
};

const closeCategories = () => {
  isCategoriesOpen.value = false;
};

// Close category menu when a category is selected and navigation happens
const handleCategoryNavigate = () => {
  isCategoriesOpen.value = false;
  // Close mobile menu if open
  if (isMenuOpen.value) {
    isMenuOpen.value = false;
  }
};

const toggleCategories = () => {
  isCategoriesOpen.value = !isCategoriesOpen.value;

  // On mobile, close the hamburger menu when opening categories
  if (isCategoriesOpen.value && window.innerWidth < 768) {
    isMenuOpen.value = false;
  }

  // On mobile, position the menu full screen
  if (isCategoriesOpen.value && mobileMenuPanelRef.value) {
    nextTick(() => {
      if (window.innerWidth < 768) {
        const navbar = document.querySelector(".navbar");
        const navbarHeight = navbar ? navbar.offsetHeight : 0;
        mobileMenuPanelRef.value.style.top = `${navbarHeight}px`;
      }
    });
  }
};

// Global header search → navigate to courses page with search query
const handleSearch = () => {
  const query = searchTerm.value.trim();
  if (!query) return;

  router.push({
    path: "/courses",
    query: {
      ...router.currentRoute.value.query,
      search: query,
    },
  });
};

// Run typeahead search against /course/search
const runSearch = async () => {
  const query = searchTerm.value.trim();
  if (!query) {
    searchResultsCourses.value = [];
    searchResultsCategories.value = [];
    return;
  }

  isSearching.value = true;

  try {
    const searchPayload = {
      search: query,
      page: 1,
      page_size: 5,
    };

    // اگر در صفحه آموزشگاه هستیم، organization_id را اضافه کن
    if (currentOrganizationId.value) {
      searchPayload.organization_id = currentOrganizationId.value;
    }

    const response = await $api.post("/course/search", searchPayload);

    if (response.data?.status && response.data.data) {
      searchResultsCourses.value = response.data.data.courses?.results || [];
      searchResultsCategories.value =
        response.data.data.categories?.results || [];
    } else {
      searchResultsCourses.value = [];
      searchResultsCategories.value = [];
    }
  } catch (error) {
    console.error("❌ Error in header search:", error);
    searchResultsCourses.value = [];
    searchResultsCategories.value = [];
  } finally {
    isSearching.value = false;
  }
};

// Debounce user typing
watch(
  () => searchTerm.value,
  (val) => {
    if (searchDebounceTimer.value) {
      clearTimeout(searchDebounceTimer.value);
    }

    if (!val || val.trim().length === 0) {
      searchResultsCourses.value = [];
      searchResultsCategories.value = [];
      return;
    }

    searchDebounceTimer.value = setTimeout(() => {
      runSearch();
    }, 400);
  },
);

// Navigate to course detail
const goToCourseFromSearch = (course) => {
  searchTerm.value = "";
  searchResultsCourses.value = [];
  searchResultsCategories.value = [];
  router.push(`/courses/${course.slug}`);
};

// Navigate to courses page filtered by category
const goToCategoryFromSearch = (category) => {
  searchTerm.value = "";
  searchResultsCourses.value = [];
  searchResultsCategories.value = [];
  router.push({
    path: "/courses",
    query: {
      category: category.id,
    },
  });
};

// Close on outside click
const handleClickOutside = (e) => {
  const clickedInsideCategory =
    (menuPanelRef.value &&
      (menuPanelRef.value === e.target ||
        menuPanelRef.value.contains(e.target))) ||
    (mobileMenuPanelRef.value &&
      (mobileMenuPanelRef.value === e.target ||
        mobileMenuPanelRef.value.contains(e.target))) ||
    e.target.closest(".category-btn") ||
    e.target.closest(".category-btn-mobile");

  const clickedInsideLevel2 = e.target.closest(".level-2");

  if (!clickedInsideCategory && !clickedInsideLevel2) {
    isCategoriesOpen.value = false;
  }

  const searchBoxEl = document.querySelector(".search-box");
  if (searchBoxEl && !searchBoxEl.contains(e.target)) {
    searchResultsCourses.value = [];
    searchResultsCategories.value = [];
  }
};

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
});
onBeforeUnmount(() => {
  document.removeEventListener("click", handleClickOutside);
});
</script>

<style scoped>
/* ✅ Match old header proportions */
.logo-size {
  width: 45px;
  height: auto;
}

.navbar {
  direction: rtl;
}

/* Categories button smaller & fits old layout */
.category-btn {
  font-size: 15px;
  color: #333;
  border-color: #ddd;
  background-color: #fff;
  transition: 0.2s;
}
.category-btn:hover {
  background-color: #f8f9fa;
  border-color: #ccc;
}

/* Dropdown container */
.category-menu-container {
  z-index: 1050;
  width: 600px;
  max-height: 400px;
  overflow: hidden;
  border-radius: 8px;
  direction: rtl;
  position: relative;
}

.category-close-btn {
  position: absolute;
  top: 15px;
  left: 15px;
  z-index: 1051;
  background: #ff8c14;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #fff;
  font-size: 18px;
}

.category-close-btn i {
  display: inline-block;
  line-height: 1;
  font-size: 18px;
  color: #fff;
}

.category-close-btn:hover {
  background: #e67a0f;
  transform: scale(1.1);
  color: #fff;
}

.category-close-btn:hover i {
  color: #fff;
}

@media (max-width: 767.98px) {
  .category-menu-container {
    position: fixed !important;
    width: 100vw;
    max-height: 90vh;
    right: 0 !important;
    left: 0 !important;
    top: 0;
    border-radius: 0;
    margin: 0 !important;
    padding: 0 !important;
    z-index: 1060 !important;
  }

  .category-close-btn {
    top: 10px;
    left: 10px;
    background: #ff8c14;
    color: #fff;
  }

  .category-close-btn i {
    display: inline-block;
    line-height: 1;
    font-size: 18px;
    color: #fff;
  }

  .category-close-btn:hover {
    background: #e67a0f;
    color: #fff;
  }

  .category-close-btn:hover i {
    color: #fff;
  }
}
/* Search box, cart, and badge */
.search-box input {
  width: 240px;
  font-size: 14px;
}

.search-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 4px;
  width: 320px;
  max-height: 360px;
  overflow-y: auto;
  z-index: 1100;
  border: 1px solid #eee;
}

.search-item {
  background: white;
  border: none;
  outline: none;
  cursor: pointer;
  font-size: 13px;
}

.search-item:hover {
  background: #f8f9fa;
}

.tiny-text {
  font-size: 11px;
}

.search-btn .bg-danger {
  background-color: #ff8c14 !important;
}

.search-btn:hover .bg-danger {
  background-color: #e67a0f !important;
}

.cart-icon-container {
  position: relative;
}

.cart-badge {
  position: absolute;
  top: -6px;
  right: -10px;
  background-color: #ff8c14;
  color: white;
  font-size: 0.8rem;
  font-weight: bold;
  padding: 0px 7px;
  border-radius: 25%;
}

.navbar-toggler-icon {
  background-image: url("data:image/svg+xml;charset=utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%23333' viewBox='0 0 30 30'%3E%3Cpath stroke='rgba%2833, 37, 41, 1%29' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3E%3C/svg%3E");
}
.navbar-toggler {
  border: none;
}

/* Mobile Menu Styles */
@media (max-width: 767.98px) {
  .navbar-collapse {
    position: fixed;
    top: 0;
    right: 0;
    width: 280px;
    height: 100vh;
    background: white;
    z-index: 1050;
    padding: 20px;
    box-shadow: -2px 0 10px rgba(0, 0, 0, 0.1);
    transform: translateX(100%);
    transition: transform 0.3s ease-in-out;
    overflow-y: auto;
    direction: rtl;
  }

  .navbar-collapse.show {
    transform: translateX(0);
  }

  .mobile-menu-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.5);
    z-index: 1040;
  }

  .navbar-nav {
    flex-direction: column;
    width: 100%;
    align-items: stretch !important;
    padding: 0 !important;
    margin: 0 !important;
  }

  .navbar-nav.mx-auto {
    margin-left: 0 !important;
    margin-right: 0 !important;
  }

  .navbar-nav .gap-4 {
    gap: 0 !important;
  }

  .nav-item {
    width: 100%;
    margin: 0 !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
    padding: 0 !important;
    text-align: right !important;
  }

  .nav-item.mx-3 {
    margin-left: 0 !important;
    margin-right: 0 !important;
  }

  .nav-link {
    padding: 12px 0 !important;
    padding-right: 0 !important;
    padding-left: 0 !important;
    border-bottom: 1px solid #eee;
    font-size: 14px;
    text-align: right !important;
    direction: rtl !important;
    display: block;
    width: 100%;
    margin: 0 !important;
  }

  /* Smaller font for آموزشگاه‌ها button in mobile menu */
  .nav-item .nav-link {
    font-size: 13px;
    text-align: right !important;
    direction: rtl !important;
    padding: 12px 0 !important;
    padding-right: 0 !important;
    padding-left: 0 !important;
  }

  /* Ensure nav-item links are right-aligned */
  .nav-item a.nav-link {
    text-align: right !important;
    direction: rtl !important;
    padding: 12px 0 !important;
    padding-right: 0 !important;
    padding-left: 0 !important;
  }

  /* Categories button in mobile menu */
  .category-btn-mobile {
    font-size: 15px;
    color: #333;
    border-color: #ddd;
    background-color: #fff;
    transition: 0.2s;
    border: 1px solid #ddd;
    padding-top: 12px !important;
    padding-bottom: 12px !important;
    padding-right: 0 !important;
    padding-left: 0 !important;
    margin: 0 !important;
    margin-bottom: 0 !important;
    text-align: right !important;
    direction: rtl !important;
    width: 100% !important;
  }

  /* Remove gap from category button */
  .category-btn-mobile.gap-2 {
    gap: 0 !important;
  }

  /* Ensure icon and text align properly in category button */
  .category-btn-mobile i {
    margin-left: 8px;
    margin-right: 0;
    flex-shrink: 0;
  }

  .category-btn-mobile span {
    flex: 1;
    text-align: right;
  }

  /* Ensure both items align perfectly - make link text align with button text */
  .nav-item button.category-btn-mobile,
  .nav-item a.nav-link {
    padding-right: 0 !important;
    padding-left: 0 !important;
    margin-right: 0 !important;
    margin-left: 0 !important;
  }

  /* Make sure the link text aligns with button text position */
  .nav-item a.nav-link {
    padding-right: 0 !important;
    padding-left: 0 !important;
    text-indent: 0 !important;
  }

  /* Make link span match button span styling */
  .nav-item a.nav-link span {
    flex: 1;
    text-align: right;
    display: block;
  }

  /* Force both to have same text position - align text content */
  .nav-item button.category-btn-mobile span,
  .nav-item a.nav-link span {
    text-align: right !important;
    padding-right: 0 !important;
    margin-right: 0 !important;
  }

  /* Add invisible spacer to link to match button icon width */
  .nav-item a.nav-link::before {
    content: "";
    width: 24px;
    margin-left: 8px;
    flex-shrink: 0;
    display: inline-block;
  }

  .category-btn-mobile:hover {
    background-color: #f8f9fa;
    border-color: #ccc;
    color: #333;
  }

  /* Mobile auth buttons RTL */
  .d-md-none .btn {
    text-align: right !important;
    direction: rtl !important;
  }
}

.size-6 {
  width: 24px;
  height: 24px;
}

.size-10 {
  width: 30px;
  height: 30px;
}

.size-16 {
  width: 34px;
  height: 34px;
}
</style>
