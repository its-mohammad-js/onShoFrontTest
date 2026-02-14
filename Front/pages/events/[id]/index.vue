<template>
  <div v-if="!webinar.title" class="text-center py-5">
    <div class="spinner-border spinner-grow text-danger1" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
    <p class="text-muted mt-3">در حال بارگذاری...</p>
  </div>
  <div v-else>
    <section class="bg-dark-subtle text-white py-5 mb-5 header">
      <div class="container">
        <div
          class="d-flex flex-md-row flex-column justify-content-center justify-content-md-start gap-3 align-items-center align-items-md-start mb-4"
          style="margin-bottom: -200px !important"
        >
          <div class="text-center flex-shrink-0 d-none d-md-flex">
            <img
              :src="webinarImageUrl"
              alt="Webinar Image"
              class="img-fluid rounded-3 border border-dark border-2 w-300-px h-300-px object-fit-cover"
            />
          </div>
          <div class="flex-grow-1 text-center text-md-start">
            <h2 class="fw-bold mb-4 text-center text-md-end">
              {{ webinar.title }}
            </h2>
            <div
              class="d-flex flex-column flex-md-row align-items-center justify-content-center justify-content-md-start gap-3 my-4"
            >
              <p class="text-white d-flex align-items-center justify-content-center gap-3 bg-dark p-3 rounded-3">
                <span>
                  <i class="fa fa-calendar-alt text-danger1 ms-1"></i>
                  {{ webinar.date }}
                </span>
                <span>
                  <i class="icon icon-regular-clock text-danger1"></i>
                  ساعت {{ webinar.start_time }} تا {{ webinar.end_time }}
                </span>
              </p>
              <p class="text-white">سخنران: {{ webinar.speaker }}</p>
            </div>
            <div class="mt-5 d-none d-md-flex align-items-center justify-content-start">
              <button class="btn btn-danger px-5 py-2" @click="registerWebinar">ثبت نام</button>
            </div>
          </div>
          <div class="text-center flex-shrink-0 d-md-none">
            <img
              :src="webinarImageUrl"
              alt="Webinar Image"
              class="img-fluid rounded-3 border border-dark border-2 w-300-px h-300-px object-fit-cover"
            />
          </div>
          <div class="mt-2 d-md-none">
            <button class="btn btn-danger px-5 py-2" @click="registerWebinar">ثبت نام</button>
          </div>
        </div>
      </div>
    </section>

    <section class="my-5 py-5">
      <div class="container mt-5 pt-5">
        <nav>
          <ul
            class="nav justify-content-start gap-3 nav-tabs py-3 border-0"
            id="myTab"
            role="tablist"
            style="overflow-x: auto; white-space: nowrap"
          >
            <li class="nav-item" role="presentation">
              <button
                class="nav-link active"
                id="info-tab"
                data-bs-toggle="tab"
                data-bs-target="#info"
                type="button"
                role="tab"
                aria-controls="info"
                aria-selected="true"
              >
                توضیحات وبینار
              </button>
            </li>
            <li class="nav-item" role="presentation">
              <button
                class="nav-link"
                id="headlines-tab"
                data-bs-toggle="tab"
                data-bs-target="#headlines"
                type="button"
                role="tab"
                aria-controls="headlines"
                aria-selected="false"
              >
                سرفصل‌ها
              </button>
            </li>
          </ul>
        </nav>
        <div class="tab-content pb-5" id="myTabContent">
          <div class="tab-pane fade show active bg-light py-3 rounded-4" id="info" role="tabpanel" aria-labelledby="info-tab">
            <div class="bg-light p-3">
              <p class="text-muted text-center text-md-end lh-lg">
                {{ webinar.description }}
              </p>
            </div>
          </div>

          <div class="tab-pane fade" id="headlines" role="tabpanel" aria-labelledby="headlines-tab">
            <div class="bg-light p-3 rounded-4">
              <div class="accordion" id="faqAccordion">
                <div v-if="webinar.topics && webinar.topics.length > 0">
                  <div
                    v-for="(topic, index) in webinar.topics"
                    :key="index"
                    class="accordion-item border border-2 rounded bg-transparent mb-4"
                    :class="{
                      'border border-danger rounded': activeItem === index,
                    }"
                  >
                    <h2 class="accordion-header p-3" :id="'heading' + index">
                      <button
                        class="accordion-button p-3 bg-transparent d-flex justify-content-between align-items-center fw-bold"
                        type="button"
                        :class="{
                          'text-muted': activeItem !== index,
                          'text-danger1': activeItem === index,
                        }"
                        @click="toggleItem(index)"
                      >
                        <span>{{ topic.title }}</span>
                        <i
                          :class="[
                            'fa me-2',
                            activeItem === index ? 'fa-minus' : 'fa-plus',
                            activeItem === index ? 'text-danger1' : 'text-muted',
                          ]"
                        ></i>
                      </button>
                    </h2>
                    <div
                      :id="'collapse' + index"
                      class="accordion-collapse collapse"
                      :class="{ show: activeItem === index }"
                      :aria-labelledby="'heading' + index"
                    >
                      <div class="accordion-body">{{ topic.content }}</div>
                    </div>
                  </div>
                </div>
                <div v-else class="d-flex align-items-center justify-content-center flex-column">
                  <img src="/images/no.gif" alt="No Topics Found" class="" style="width: 200px; height: auto" />
                  <p class="text-muted">درحال حاضر هیچ سرفصلی برای این رویداد تعریف نشده است !</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";

const router = useRouter();
const activeItem = ref(null);
const { getMediaUrl } = useMediaUrl();

const toggleItem = (id) => {
  activeItem.value = activeItem.value === id ? null : id;
};

// Mock webinar data (standalone, minimal set)
const allWebinars = ref([
  {
    id: "1",
    slug: "intro-to-ai",
    title: "مقدمه‌ای بر هوش مصنوعی",
    speaker: "دکتر حسینی",
    date: "1404/06/01",
    start_time: "17:00",
    end_time: "18:30",
    image: "/images/webinars/1.png",
    is_free: false,
    price: "100,000",
    description: "آشنایی با مفاهیم پایه هوش مصنوعی و کاربردهای آن در زندگی روزمره.",
    topics: [
      {
        title: "مفاهیم اولیه AI",
        content: "تعریف هوش مصنوعی و تاریخچه آن.",
      },
      {
        title: "کاربردهای AI",
        content: "بررسی استفاده از AI در صنایع مختلف.",
      },
    ],
  },
  {
    id: "2",
    slug: "web-development-basics",
    title: "مبانی توسعه وب",
    speaker: "مهندس رضایی",
    date: "1404/06/05",
    start_time: "18:00",
    end_time: "19:30",
    image: "/images/webinars/2.png",
    is_free: true,
    price: "0",
    description: "یادگیری اصول اولیه طراحی و توسعه وب‌سایت با HTML و CSS.",
    topics: [
      {
        title: "معرفی HTML",
        content: "ساختار پایه صفحات وب با HTML.",
      },
      {
        title: "استایل‌دهی با CSS",
        content: "ایجاد ظاهر جذاب برای وب‌سایت‌ها با CSS.",
      },
    ],
  },
  {
    id: "3",
    slug: "data-science-intro",
    title: "آشنایی با علم داده",
    speaker: "خانم محمدی",
    date: "1404/06/10",
    start_time: "16:30",
    end_time: "18:00",
    image: "/images/webinars/1.png",
    is_free: false,
    price: "120,000",
    description: "مقدمه‌ای بر علم داده و ابزارهای مورد استفاده در تحلیل داده‌ها.",
    topics: [
      {
        title: "مفاهیم علم داده",
        content: "تعریف علم داده و نقش آن در تصمیم‌گیری.",
      },
      {
        title: "ابزارهای تحلیل",
        content: "معرفی ابزارهایی مانند Python و R.",
      },
    ],
  },
  {
    id: "4",
    slug: "cybersecurity-essentials",
    title: "اصول امنیت سایبری",
    speaker: "مهندس احمدی",
    date: "1404/06/15",
    start_time: "19:30",
    image: "/images/webinars/2.png",
    is_free: false,
    price: "130,000",
    description: "یادگیری اصول اولیه برای حفاظت از داده‌ها در برابر حملات سایبری.",
    topics: [
      {
        title: "تهدیدات سایبری",
        content: "آشنایی با انواع حملات سایبری.",
      },
      {
        title: "رمزنگری",
        content: "بررسی اصول رمزنگاری و ایمن‌سازی داده‌ها.",
      },
    ],
  },
  {
    id: "5",
    slug: "ux-design-fundamentals",
    title: "مبانی طراحی تجربه کاربری",
    speaker: "خانم صادقی",
    date: "1404/06/20",
    start_time: "17:30",
    end_time: "19:00",
    image: "/images/webinars/1.png",
    is_free: true,
    price: "0",
    description: "آشنایی با اصول طراحی رابط کاربری جذاب و کاربرپسند.",
    topics: [
      {
        title: "اصول UX",
        content: "مفاهیم پایه طراحی تجربه کاربری.",
      },
      {
        title: "ابزارهای طراحی",
        content: "معرفی ابزارهایی مانند Figma.",
      },
    ],
  },
]);

const webinar = reactive({
  id: "",
  slug: "",
  title: "",
  description: "",
  speaker: "",
  date: "",
  start_time: "",
  end_time: "",
  price: "",
  is_free: false,
  image: "",
  topics: [],
});

const route = useRoute();
const slug = ref(route.params.slug);

const getWebinar = () => {
  // Find webinar by slug, or use the first webinar as fallback
  let foundWebinar = allWebinars.value.find((w) => w.slug === slug.value);
  if (!foundWebinar) {
    console.warn(`Webinar not found for slug: ${slug.value}, using fallback`);
    foundWebinar = allWebinars.value[0]; // Fallback to first webinar
  }
  Object.assign(webinar, foundWebinar);
};

// تبدیل آدرس تصویر به آدرس با /api
const webinarImageUrl = computed(() => getMediaUrl(webinar.image));

const registerWebinar = () => {
  if (!webinar.id) {
    console.error("مشکلی در دریافت اطلاعات وبینار وجود دارد!");
    return;
  }
  console.log(`Registered for webinar: ${webinar.title}`);
  router.push("/checkout");
};

onMounted(() => {
  getWebinar();
});
</script>

<style scoped>
.header {
  padding-top: 200px !important;
}

.bg-dark-subtle {
  background-color: rgba(43, 45, 66, 1) !important;
}

.w-300-px {
  width: 300px !important;
}

.h-300-px {
  height: 300px !important;
}

.object-fit-cover {
  object-fit: cover !important;
}

@media (max-width: 768px) {
  .w-300-px {
    width: 100% !important;
    max-width: 600px !important;
    height: auto !important;
  }
  .header {
    padding-top: 150px !important;
  }
}

.spinner-border {
  width: 3rem;
  height: 3rem;
  border-width: 0.3rem;
}
</style>
