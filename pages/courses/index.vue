<template>
  <section class="py-3">
    <div class="container">
      <div>
        <div class="row">
          <div class="d-lg-none mb-3">
            <button
              class="btn btn-danger d-flex align-items-center text-center justify-content-center"
              @click="showFilterModal = true"
            >
              <h5 class="fw-bold mt-1 ms-2">فیلتر</h5>
              <i class="icon icon-filled-filter fs-3"></i>
            </button>
          </div>
          <!-- مودال فیلترها برای موبایل -->
          <div
            v-if="showFilterModal"
            class="filter-modal"
            @click.self="showFilterModal = false"
          >
            <div class="filter-modal-content">
              <div class="modal-header">
                <h5 class="fw-bold">فیلترها</h5>
                <button class="btn-close" @click="showFilterModal = false">
                  ×
                </button>
              </div>
              <div class="modal-body">
                <div class="card-body">
                  <!-- فیلترها داخل مودال -->
                  <div class="mb-4">
                    <div class="input-group">
                      <span
                        class="input-group-text bg-white rounded-0 border-0 rounded-end cursor-pointer"
                      >
                        <i class="icon icon-regular-search text-muted"></i>
                      </span>
                      <input
                        type="text"
                        class="form-control border-light rounded-0 border-0 rounded-start shadow-none"
                        placeholder="جستجو در نتایج"
                        v-model="filters.search"
                      />
                    </div>
                  </div>

                  <!-- فیلتر برگزارکننده -->
                  <div class="mb-4">
                    <h6
                      class="fw-bold text-dark mb-3 d-flex align-items-center gap-2"
                    >
                      <i class="icon icon-regular-building"></i>
                      <span>برگزارکننده دوره</span>
                    </h6>
                    <div
                      class="form-check mb-2 d-flex align-items-center justify-content-start"
                      v-for="organizer in organizers"
                      :key="organizer.id"
                    >
                      <input
                        class="form-check-input custom-checkbox"
                        type="checkbox"
                        :id="'organizer' + organizer.id"
                        v-model="filters.organizers"
                        :value="organizer.id"
                      />
                      <label
                        class="form-check-label text-muted"
                        :for="'organizer' + organizer.id"
                      >
                        {{ organizer.name }}
                      </label>
                    </div>
                  </div>
                  <div>
                    <h6
                      class="fw-bold text-dark mb-3 d-flex align-items-center gap-2"
                    >
                      <i class="icon icon-regular-globe"></i
                      ><span> انتخاب زبان</span>
                    </h6>
                    <div
                      class="form-check mb-2 d-flex align-items-center justify-content-start"
                      v-for="language in languages"
                      :key="language.id"
                    >
                      <input
                        class="form-check-input custom-checkbox"
                        type="checkbox"
                        :id="'lang' + language.id"
                        v-model="filters.languages"
                        :value="language.name"
                      />
                      <label
                        class="form-check-label text-muted"
                        :for="'lang' + language.id"
                      >
                        {{ language.name }}
                      </label>
                    </div>
                  </div>
                  <!-- فیلتر نوع دوره -->
                  <div class="mb-4">
                    <h6
                      class="fw-bold text-dark mb-3 d-flex align-items-center gap-2"
                    >
                      <i class="icon icon-regular-calendar"></i
                      ><span>نوع دوره</span>
                    </h6>
                    <div
                      class="form-check mb-2 d-flex align-items-center justify-content-start"
                      v-for="(type, index) in courseTypes"
                      :key="index"
                    >
                      <input
                        class="form-check-input custom-checkbox"
                        type="checkbox"
                        :id="'type' + index"
                        v-model="filters.types"
                        :value="type"
                      />
                      <label
                        class="form-check-label text-muted"
                        :for="'type' + index"
                      >
                        {{ type }}
                      </label>
                    </div>
                  </div>
                  <!-- فیلتر قیمت -->
                  <div class="price-filter">
                    <h6 class="fw-bold mb-4 d-flex align-items-center gap-2">
                      <i class="icon icon-regular-dollar-circle"></i>
                      <span>بازه قیمتی</span>
                    </h6>
                    <div class="row my-4 gap-3">
                      <div class="col-12">
                        <label class="form-label text-muted small"
                          >حداقل قیمت (تومان)</label
                        >
                        <input
                          type="number"
                          class="form-control text-end py-2"
                          v-model.number="filters.minPrice"
                        />
                      </div>
                      <div class="col-12">
                        <label class="form-label text-muted small"
                          >حداکثر قیمت (تومان)</label
                        >
                        <input
                          type="number"
                          class="form-control text-end py-2"
                          v-model.number="filters.maxPrice"
                        />
                      </div>
                    </div>
                  </div>

                  <!-- دکمه‌های اعمال و حذف فیلتر -->
                  <div class="col-sm-12 my-3">
                    <button
                      class="btn btn-danger w-100"
                      @click="
                        applyFilters();
                        showFilterModal = false;
                      "
                    >
                      اعمال فیلتر
                    </button>
                  </div>
                  <div class="col-sm-12">
                    <button
                      class="btn btn-outline-secondary w-100"
                      @click="
                        resetFilters();
                        showFilterModal = false;
                      "
                    >
                      حذف فیلترها
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="col-lg-3 d-none d-lg-block">
            <div
              class="d-flex justify-content-start align-items-center mb-2 mt-3"
            >
              <h5 class="fw-bold text-dark mt-1 ms-2">فیلتر</h5>
              <i class="icon icon-filled-filter fs-3"></i>
            </div>
            <div class="card border-0 p-3 bg-light rounded filter-sticky">
              <div class="card-body">
                <!-- Search Box -->
                <div class="mb-4">
                  <div class="input-group">
                    <span
                      class="input-group-text bg-white rounded-0 border-0 rounded-end cursor-pointer"
                    >
                      <i class="icon icon-regular-search text-muted"></i>
                    </span>
                    <input
                      type="text"
                      class="form-control border-light rounded-0 border-0 rounded-start shadow-none border-none border-0 outline-none"
                      placeholder="جستجو در نتایج"
                      v-model="filters.search"
                    />
                  </div>
                </div>

                <!-- Organizer Filter -->
                <div class="mb-4">
                  <h6
                    class="fw-bold text-dark mb-3 d-flex align-items-center gap-2"
                  >
                    <i class="icon icon-regular-building"></i>
                    <span>برگزارکننده دوره</span>
                  </h6>
                  <div
                    class="form-check mb-2 d-flex align-items-center justify-content-start"
                    v-for="organizer in organizers"
                    :key="organizer.id"
                  >
                    <input
                      class="form-check-input custom-checkbox"
                      type="checkbox"
                      :id="'organizer' + organizer.id"
                      v-model="filters.organizers"
                      :value="organizer.id"
                    />
                    <label
                      class="form-check-label text-muted"
                      :for="'organizer' + organizer.id"
                    >
                      {{ organizer.name }}
                    </label>
                  </div>
                </div>

                <!-- Price Range -->
                <div class="price-filter">
                  <h6 class="fw-bold mb-4 d-flex align-items-center gap-2">
                    <i class="icon icon-regular-dollar-circle"></i>
                    <span> بازه قیمتی:</span>
                  </h6>
                  <div class="row my-4 gap-3">
                    <div class="col-12">
                      <label
                        class="form-label text-muted small d-flex align-items-center justify-content-between"
                        ><span>حداقل قیمت </span> <span>تومان</span></label
                      >
                      <div class="input-group">
                        <input
                          type="text"
                          class="form-control text-end py-2"
                          placeholder="۵۰۰,۰۰۰"
                          v-model.number="filters.minPrice"
                        />
                      </div>
                    </div>
                    <div class="col-12">
                      <label
                        class="form-label text-muted small d-flex align-items-center justify-content-between"
                        ><span>حداکثر قیمت </span> <span>تومان</span></label
                      >
                      <div class="input-group">
                        <input
                          type="text"
                          class="form-control text-end py-2"
                          placeholder="۲۵۰۰,۰۰۰"
                          v-model.number="filters.maxPrice"
                        />
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Language Selection -->
                <!-- <div class="mb-4">
                  <h6
                    class="fw-bold text-dark mb-3 d-flex align-items-center gap-2"
                  >
                    <i class="icon icon-regular-globe"></i
                    ><span> انتخاب زبان</span>
                  </h6>
                  <div
                    class="form-check mb-2 d-flex align-items-center justify-content-start"
                    v-for="language in languages"
                    :key="language.id"
                  >
                    <input
                      class="form-check-input custom-checkbox"
                      type="checkbox"
                      :id="'lang' + language.id"
                      v-model="filters.languages"
                      :value="language.name"
                    />
                    <label
                      class="form-check-label text-muted"
                      :for="'lang' + language.id"
                    >
                      {{ language.name }}
                    </label>
                  </div>
                </div> -->
                <!-- Course Type Filter -->
                <div>
                  <h6
                    class="fw-bold text-dark mb-3 d-flex align-items-center gap-2"
                  >
                    <i class="icon icon-regular-calendar"></i
                    ><span>نوع دوره</span>
                  </h6>
                  <div
                    class="form-check mb-2 d-flex align-items-center justify-content-start"
                    v-for="(type, index) in courseTypes"
                    :key="index"
                  >
                    <input
                      class="form-check-input custom-checkbox"
                      type="checkbox"
                      :id="'type' + index"
                      v-model="filters.types"
                      :value="type"
                    />
                    <label
                      class="form-check-label text-muted"
                      :for="'type' + index"
                    >
                      {{ type }}
                    </label>
                  </div>
                </div>
                <div class="col-sm-12 my-3">
                  <button class="btn btn-danger w-100" @click="applyFilters">
                    اعمال فیلتر
                  </button>
                </div>
                <div class="col-sm-12">
                  <button
                    class="btn btn-outline-secondary w-100"
                    @click="resetFilters"
                  >
                    حذف فیلترها
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div class="col-lg-9">
            <div
              class="d-flex justify-content-start flex-column rounded-3 py-3"
            >
              <!-- دکمه بازگشت اگر در صفحه children هستیم -->

              <a
                v-if="data.selectedCategory"
                class="mt-1 mb-3 cursor-pointer d-block text-danger1"
                @click="resetCategories"
              >
                <i class="icon icon-regular-angle-right"></i>
                {{ getParentCategoryTitle() }}
              </a>

              <!-- نمایش دسته‌بندی‌های فیلتر شده (اصلی یا children) -->
              <div v-if="filteredCategories.length > 0" class="nav-custom">
                <!-- <a
                  class="cursor-pointer"
                  :class="{ active: data.selectedCategory === null }"
                  @click="resetCategories"
                >
                  همه
                </a> -->
                <!-- <a href="javascript:;" :class="{ active: data.selectedCategory === null }" @click="resetCategories"> همه </a> -->

                <a
                  v-if="!data.parentCategory"
                  class="cursor-pointer"
                  :class="{ active: data.selectedCategory === null }"
                  @click="resetCategories"
                >
                  همه
                  <!-- خوشه ها -->
                </a>

                <a
                  v-else
                  class="cursor-pointer"
                  :class="{ active: data.selectedCategory === null }"
                  @click="resetToMainCategory"
                >
                  همه
                  <!-- دسته بندی ها -->
                </a>

                <a
                  v-for="(category, index) in filteredCategories"
                  :key="index"
                  class="cursor-pointer"
                  :class="{ active: data.selectedCategory === category.id }"
                  @click="selectCategory(category)"
                >
                  <img :src="category.logo" alt="" class="w-20-px" />
                  {{ category.title }}
                </a>
              </div>
            </div>

            <div v-if="!data.loaded" class="text-center py-5">
              <div class="spinner-grow text-danger1" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
              <p class="text-muted mt-3">در حال بارگزاری...</p>
            </div>
            <div v-else class="bg-light p-4 rounded">
              <div v-if="courses.data.length === 0" class="text-center py-5">
                <img
                  src="/images/no.gif"
                  alt="No Courses Found"
                  class=""
                  style="width: 300px; height: auto"
                />
                <p class="text-muted">دوره‌ای یافت نشد.</p>
              </div>
              <div v-else class="row">
                <div
                  class="col-sm-6 mb-3"
                  v-for="(course, index) in courses.data"
                  :key="index"
                >
                  <course :course="course" />
                </div>
              </div>

              <!-- Pagination -->
              <div
                v-if="data.totalPages > 1"
                class="d-flex justify-content-center mt-4"
              >
                <nav aria-label="Page navigation">
                  <ul class="pagination">
                    <!-- Previous Button -->
                    <li
                      class="page-item"
                      :class="{ disabled: data.currentPage === 1 }"
                    >
                      <button
                        class="page-link"
                        @click="prevPage()"
                        :disabled="data.currentPage === 1"
                        aria-label="Previous"
                      >
                        <span aria-hidden="true">&laquo;</span>
                      </button>
                    </li>

                    <!-- First Page -->
                    <li v-if="getPageNumbers()[0] > 1" class="page-item">
                      <button class="page-link" @click="goToPage(1)">1</button>
                    </li>
                    <li
                      v-if="getPageNumbers()[0] > 2"
                      class="page-item disabled"
                    >
                      <span class="page-link">...</span>
                    </li>

                    <!-- Page Numbers -->
                    <li
                      v-for="page in getPageNumbers()"
                      :key="page"
                      class="page-item"
                      :class="{ active: page === data.currentPage }"
                    >
                      <button class="page-link" @click="goToPage(page)">
                        {{ page }}
                      </button>
                    </li>

                    <!-- Last Page -->
                    <li
                      v-if="
                        getPageNumbers()[getPageNumbers().length - 1] <
                        data.totalPages - 1
                      "
                      class="page-item disabled"
                    >
                      <span class="page-link">...</span>
                    </li>
                    <li
                      v-if="
                        getPageNumbers()[getPageNumbers().length - 1] <
                        data.totalPages
                      "
                      class="page-item"
                    >
                      <button
                        class="page-link"
                        @click="goToPage(data.totalPages)"
                      >
                        {{ data.totalPages }}
                      </button>
                    </li>

                    <!-- Next Button -->
                    <li
                      class="page-item"
                      :class="{
                        disabled: data.currentPage === data.totalPages,
                      }"
                    >
                      <button
                        class="page-link"
                        @click="nextPage()"
                        :disabled="data.currentPage === data.totalPages"
                        aria-label="Next"
                      >
                        <span aria-hidden="true">&raquo;</span>
                      </button>
                    </li>
                  </ul>
                </nav>
              </div>

              <!-- Pagination Info -->
              <div v-if="data.totalCount > 0" class="text-center mt-3">
                <small class="text-muted">
                  نمایش {{ (data.currentPage - 1) * data.pageSize + 1 }} تا
                  {{
                    Math.min(data.currentPage * data.pageSize, data.totalCount)
                  }}
                  از {{ data.totalCount }} دوره
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useCurrentOrganization } from "@/composables/useCurrentOrganization";

// Dynamic data from backend
const categories = ref([]);
const organizers = ref([]);
const languages = ref([
  { id: "lang1", name: "انگلیسی" },
  { id: "lang2", name: "ترکی" },
  { id: "lang3", name: "فارسی" },
  { id: "lang4", name: "آلمانی" },
]);

const courseTypes = ref(["آفلاین", "آنلاین", "پیش ثبت نام حضوری"]);

const allCourses = ref({
  data: [],
  count: 0,
  next: null,
  previous: null,
});

const route = useRoute();
const router = useRouter();
const { $api, $sweetalert } = useNuxtApp();
const { currentOrganizationId } = useCurrentOrganization();

const data = reactive({
  loaded: false,
  selectedCategory: ref(route.query.category || null),
  parentCategory: null,
  currentPage: 1,
  totalPages: 1,
  totalCount: 0,
  pageSize: 12,
});

const courses = ref({ data: [] });
const showFilterModal = ref(false);

const filters = reactive({
  search: "",
  organizers: [],
  minPrice: "",
  maxPrice: "",
  languages: [],
  types: [],
});

// Load categories from backend
const loadCategories = async () => {
  try {
    const response = await $api.post("/course/category/list", {});
    if (response.data.status) {
      categories.value = response.data.data;
    }
  } catch (error) {
    console.error("Error loading categories:", error);
    $sweetalert.error("خطا در بارگذاری دسته‌بندی‌ها");
  }
};

// Load organizers from backend
const loadOrganizers = async () => {
  try {
    const response = await $api.post("/course/organization/list", {});
    if (response.data.status) {
      organizers.value = response.data.data.data;
    }
  } catch (error) {
    console.error("Error loading organizers:", error);
    $sweetalert.error("خطا در بارگذاری برگزارکنندگان");
  }
};

// Load courses from backend with filters
const loadCourses = async (page = 1) => {
  data.loaded = false;
  try {
    // اگر سرچ داریم، از API مخصوص سرچ استفاده کن
    let response;

    if (filters.search && filters.search.trim() !== "") {
      const searchPayload = {
        search: filters.search.trim(),
        page: page,
        page_size: data.pageSize,
      };

      // اگر در صفحه آموزشگاه هستیم، organization_id را اضافه کن
      if (currentOrganizationId.value) {
        searchPayload.organization_id = currentOrganizationId.value;
      }

      console.log("🔍 Loading courses from /course/search ...", searchPayload);
      response = await $api.post("/course/search", searchPayload);
    } else {
      const requestData = {
        search: null,
        category_id: data.selectedCategory || null,
        organizer_id:
          filters.organizers.length > 0 ? filters.organizers[0] : null,
        min_price: filters.minPrice || null,
        max_price: filters.maxPrice || null,
        type: filters.types.length > 0 ? filters.types : null,
        ordering: "-create_date",
        page: page,
        page_size: data.pageSize,
      };

      console.log("📚 Loading courses from /course/list ...", requestData);
      response = await $api.post("/course/list", requestData);
    }

    console.log("📡 API Response:", response.data);

    if (response.data.status) {
      // اگر سرچ داریم، ساختار پاسخ متفاوت است
      if (
        filters.search &&
        filters.search.trim() !== "" &&
        response.data.data?.courses
      ) {
        const coursesData = response.data.data.courses;

        allCourses.value = {
          data: coursesData.results || [],
          count: coursesData.count || 0,
          next: coursesData.next || null,
          previous: coursesData.previous || null,
        };
        courses.value.data = coursesData.results || [];

        // Update pagination data بر اساس پاسخ سرچ
        data.currentPage = coursesData.page || page;
        data.totalCount = coursesData.count || 0;
        data.totalPages = Math.ceil(
          data.totalCount / (coursesData.page_size || data.pageSize),
        );

        console.log(
          "📂 Search categories result:",
          response.data.data.categories,
        );
      } else {
        // حالت معمولی: /course/list
        allCourses.value = response.data.data;
        courses.value.data = response.data.data.data;

        // Update pagination data
        data.currentPage = page;
        data.totalCount = response.data.data.count;
        data.totalPages = Math.ceil(data.totalCount / data.pageSize);
      }

      // Debug: Log first course attributes
      if (courses.value.data.length > 0) {
        const firstCourse = courses.value.data[0];
        console.log("🎯 First course attributes:", firstCourse.attributes);
      }
    }
  } catch (error) {
    console.error("❌ Error loading courses:", error);
    $sweetalert.error("خطا در بارگذاری دوره‌ها");
    courses.value.data = [];
  } finally {
    data.loaded = true;
  }
};

// Filter courses based on selected filters
const filterCourses = () => {
  data.currentPage = 1; // Reset to first page when filtering

  // به‌روزرسانی Query آدرس بر اساس سرچ
  const query = { ...route.query };
  if (filters.search && filters.search.trim() !== "") {
    query.search = filters.search.trim();
  } else {
    delete query.search;
  }

  router.push({ path: "/courses", query });
  loadCourses(1);
};

// Select category
const selectCategory = (category) => {
  data.selectedCategory = category.id;
  router.push({ path: "/courses", query: { category: category.id } });
  data.parentCategory = category.children?.length ? category : null;
  filterCourses();
};

// Compute filtered categories
const filteredCategories = computed(() => {
  if (data.parentCategory?.children?.length) {
    return data.parentCategory.children;
  }
  return data.selectedCategory ? [] : categories.value;
});

const getParentCategoryTitle = () => {
  const parentCategory = categories.value.find((category) =>
    category.children?.some((child) => child.id === data.selectedCategory),
  );
  return parentCategory ? `بازگشت به ${parentCategory.title}` : "بازگشت";
};

const resetCategories = () => {
  if (data.selectedCategory) {
    const parentCategory = categories.value.find((category) =>
      category.children?.some((child) => child.id === data.selectedCategory),
    );
    if (parentCategory) {
      data.selectedCategory = parentCategory.id;
      data.parentCategory = parentCategory;
      router.push({ path: "/courses", query: { category: parentCategory.id } });
    } else {
      data.selectedCategory = null;
      data.parentCategory = null;
      router.push("/courses");
    }
  } else {
    data.selectedCategory = null;
    data.parentCategory = null;
    router.push("/courses");
  }
  filterCourses();
};

const resetToMainCategory = () => {
  data.selectedCategory = null;
  // data.parentCategory = null;
  router.push("/courses");
  filterCourses();
};

const applyFilters = () => {
  filterCourses();
};

const resetFilters = () => {
  Object.assign(filters, {
    search: "",
    organizers: [],
    minPrice: "",
    maxPrice: "",
    languages: [],
    types: [],
  });
  data.selectedCategory = null;
  data.parentCategory = null;
  data.currentPage = 1;
  router.push("/courses");
  filterCourses();
};

// Pagination functions
const goToPage = (page) => {
  if (page >= 1 && page <= data.totalPages) {
    loadCourses(page);
    // Scroll to top of courses section
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
};

const nextPage = () => {
  if (data.currentPage < data.totalPages) {
    goToPage(data.currentPage + 1);
  }
};

const prevPage = () => {
  if (data.currentPage > 1) {
    goToPage(data.currentPage - 1);
  }
};

// Generate page numbers for pagination
const getPageNumbers = () => {
  const pages = [];
  const maxVisiblePages = 5;
  let startPage = Math.max(
    1,
    data.currentPage - Math.floor(maxVisiblePages / 2),
  );
  let endPage = Math.min(data.totalPages, startPage + maxVisiblePages - 1);

  if (endPage - startPage + 1 < maxVisiblePages) {
    startPage = Math.max(1, endPage - maxVisiblePages + 1);
  }

  for (let i = startPage; i <= endPage; i++) {
    pages.push(i);
  }

  return pages;
};

onMounted(async () => {
  // همگام‌سازی سرچ اولیه با Query آدرس (برای سرچ از هدر)
  if (route.query.search) {
    filters.search = String(route.query.search);
  }

  await Promise.all([loadCategories(), loadOrganizers(), loadCourses()]);
});

// هر تغییری در Query سرچ → دوباره دوره‌ها را لود کن
watch(
  () => route.query.search,
  (newSearch, oldSearch) => {
    if (newSearch === oldSearch) return;
    filters.search = newSearch ? String(newSearch) : "";
    filterCourses();
  },
);
</script>

<style scoped>
.filter-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

.filter-modal-content {
  background: white;
  width: 90%;
  max-width: 400px;
  padding: 20px;
  border-radius: 10px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-body {
  max-height: 70vh;
  overflow-y: auto;
}

.btn-close {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
}

.custom-checkbox {
  width: 24px !important;
  height: 24px !important;
  margin-left: 10px !important;
}
.custom-checkbox:checked {
  background-color: #ff8c14 !important;
  border-color: #ff8c14 !important;
  box-shadow: none !important;
}
.price-filter .form-range {
  width: 100%;
  height: 6px;
  background: #ff8c14;
  border-radius: 5px;
}

.price-filter .form-range::-webkit-slider-thumb {
  width: 20px;
  height: 20px;
  background: #ff8c14;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid white;
}

.price-filter .form-range::-moz-range-thumb {
  width: 20px;
  height: 20px;
  background: #ff8c14;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid white;
}
.card {
  transform: scale(1);
}
/* استایل چسبنده برای فیلترها */
.filter-sticky {
  position: sticky;
  top: 100px; /* فاصله از بالای صفحه */
  z-index: 10;
}

/* اندازه فیلترها */
.custom-checkbox {
  width: 24px !important;
  height: 24px !important;
  margin-left: 10px !important;
}

/* استایل کلی */
.price-filter .form-range {
  width: 100%;
  height: 6px;
  background: #ff8c14;
  border-radius: 5px;
}

.price-filter .form-range::-webkit-slider-thumb {
  width: 20px;
  height: 20px;
  background: #ff8c14;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid white;
}

/* غیرچسبنده کردن فیلترها در موبایل */
@media (max-width: 768px) {
  .filter-sticky {
    position: relative;
    top: auto;
  }
}

/* Pagination Styles */
.pagination {
  margin-bottom: 0;
}

.page-link {
  color: #ff8c14;
  border: 1px solid #dee2e6;
  padding: 0.5rem 0.75rem;
  margin: 0 2px;
  border-radius: 0.375rem;
  transition: all 0.15s ease-in-out;
}

.page-link:hover {
  color: #fff;
  background-color: #ff8c14;
  border-color: #ff8c14;
}

.page-item.active .page-link {
  background-color: #ff8c14;
  border-color: #ff8c14;
  color: #fff;
}

.page-item.disabled .page-link {
  color: #6c757d;
  background-color: #fff;
  border-color: #dee2e6;
  cursor: not-allowed;
}

.page-item.disabled .page-link:hover {
  color: #6c757d;
  background-color: #fff;
  border-color: #dee2e6;
}
</style>
