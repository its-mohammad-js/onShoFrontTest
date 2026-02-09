<template>
  <div v-if="!data.loaded">درحال بارگزاری</div>
  <div v-else>
    <section class="w-100">
      <!-- hero section -->
      <div class="container-fluid">
        <div class="position-relative">
          <img
            v-if="course && course.image"
            :src="courseImageUrl"
            alt="Course Image"
            class="w-100 img-fluid h-600-px object-fit-cover"
          />
          <div
            class="w-100 text-center p-4 bg-light bg-opacity-75 position-absolute bottom-0"
          >
            <div
              class="d-flex justify-content-around align-items-center gap-4 flex-wrap"
            >
              <div>
                <p class="text-muted mb-1">دسته بندی:</p>
                <span
                  class="fw-bold d-flex align-items-center justify-content-center gap-2"
                >
                  <i class="icon icon-regular-grid-square text-danger1"></i>
                  {{ course.category.title }}
                </span>
              </div>
              <div>
                <p class="text-muted mb-1">مدت زمان:</p>
                <span
                  class="fw-bold d-flex align-items-center justify-content-center gap-2"
                >
                  <i class="icon icon-regular-clock text-danger1"></i>
                  {{
                    course.attributes.find(
                      (attribute) => attribute.title === "مدت زمان دوره",
                    )?.value || "نامشخص"
                  }}
                </span>
              </div>
              <div>
                <p class="text-muted mb-1">تعداد موقعیت شغلی:</p>
                <span
                  class="fw-bold d-flex align-items-center justify-content-center gap-2"
                >
                  <i class="icon icon-regular-briefcase text-danger1"></i>
                  {{
                    course.attributes.find(
                      (attribute) => attribute.title === "تعداد موقعیت شغلی",
                    )?.value || "نامشخص"
                  }}
                </span>
              </div>
              <div>
                <p class="text-muted mb-1">تعداد ثبت نام کننده:</p>
                <span
                  class="fw-bold d-flex align-items-center justify-content-center gap-2"
                >
                  <i class="icon icon-regular-user text-danger1"></i>
                  <span>150 نفر</span>
                </span>
              </div>
              <div
                class="cursor-pointer"
                :class="[
                  'm-3 rounded-circle shadow-sm d-flex justify-content-center align-items-center w-50-px h-50-px',
                  isSaved ? 'bg-danger text-white' : 'bg-white text-danger1',
                ]"
                @click.stop="toggleSaveCourse"
              >
                <i
                  :class="[
                    'icon fw-light',
                    isSaved ? 'icon-filled-bookmark' : 'icon-regular-bookmark',
                  ]"
                ></i>
              </div>
              <div class="d-flex justify-content-center">
                <div
                  class="d-flex align-items-center justify-content-center rounded-4 gap-2"
                >
                  <div
                    class="text-danger1 d-flex align-items-center gap-2 rounded-4"
                  >
                    <span class="fw-bold fs-5 text-danger1">{{
                      course.average_rate
                    }}</span>
                    <div>
                      <!-- تولید ستاره‌های پر -->
                      <i
                        v-for="star in Math.floor(course.average_rate)"
                        :key="'full-' + star"
                        class="icon icon-filled-star text-danger1"
                      ></i>
                      <!-- تولید یک ستاره نیمه‌پر اگر مقدار اعشاری باشد -->
                      <i
                        v-if="course.average_rate % 1 !== 0"
                        class="icon icon-filled-star-half text-danger1"
                      ></i>
                      <!-- تولید ستاره‌های خالی -->
                      <i
                        v-for="empty in 5 - Math.ceil(course.average_rate)"
                        :key="'empty-' + empty"
                        class="icon icon-regular-star text-muted"
                      ></i>
                    </div>
                  </div>
                  <p class="text-muted mt-3">
                    از {{ course.comments.length }} نظر
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- video player block -->
      <div class="container">
        <div class="text-center my-5">
          <div
            class="position-relative d-flex align-items-center justify-content-center"
          >
            <!-- Check if the video link is available and valid -->
            <div v-if="getFirstLessonVideo()" class="w-100">
              <video
                class="img-fluid rounded shadow-sm w-100 h-280-px object-fit-cover"
                controls
                crossorigin="anonymous"
                preload="metadata"
              >
                <source :src="getFirstLessonVideo()" type="video/mp4" />
                <source :src="getFirstLessonVideo()" type="video/webm" />
                <source :src="getFirstLessonVideo()" type="video/ogg" />
                مرورگر شما از ویدیو پشتیبانی نمی‌کند.
              </video>
              <div class="position-absolute top-0 start-0 m-3">
                <span class="badge bg-primary">پیش‌نمایش دوره</span>
              </div>
            </div>

            <!-- This block won't show if the video link is falsy -->
            <div v-else class="d-none">
              <!-- Empty block, as we want it to be hidden entirely when the video is unavailable -->
            </div>
          </div>
        </div>
      </div>
    </section>

    <section>
      <div class="container mt-5">
        <div class="row align-items-start">
          <div class="col-sm-12">
            <h1 class="fw-bold display-5 text-end">{{ course.title }}</h1>
          </div>
          <div class="col-md-9 order-md-1 order-2">
            <div class="col-sm-12 my-2">
              <p class="text-muted lh-lg">
                {{ course.excerpt }}
              </p>
            </div>
            <nav class="">
              <ul
                class="nav justify-content-between nav-tabs py-3 border-0"
                id="myTab"
                role="tablist"
                style="overflow-x: auto; white-space: nowrap"
              >
                <li class="nav-item" role="presentation">
                  <button
                    class="nav-link active"
                    id="main-tab"
                    data-bs-toggle="tab"
                    data-bs-target="#main"
                    type="button"
                    role="tab"
                    aria-controls="main"
                    aria-selected="true"
                  >
                    دید کلی
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
                    سرفصل ها
                  </button>
                </li>
                <li class="nav-item" role="presentation">
                  <button
                    class="nav-link"
                    id="comments-tab"
                    data-bs-toggle="tab"
                    data-bs-target="#comments"
                    type="button"
                    role="tab"
                    aria-controls="comments"
                    aria-selected="false"
                  >
                    نظرات
                  </button>
                </li>
              </ul>
            </nav>
            <div class="tab-content pb-5" id="myTabContent">
              <div
                class="tab-pane fade show active bg-light py-3 rounded-4"
                id="main"
                role="tabpanel"
                aria-labelledby="main-tab"
              >
                <div class="bg-light p-3">
                  <p class="text-muted lh-lg">
                    {{ course.description }}
                  </p>
                </div>
              </div>
              <div
                class="tab-pane fade bg-light py-3 rounded-4"
                id="headlines"
                role="tabpanel"
                aria-labelledby="headlines-tab"
              >
                <div class="tab-pane fade show active bg-light p-3 rounded-4">
                  <div class="accordion" id="faqAccordion">
                    <!-- بررسی وجود چپترها -->
                    <div v-if="course.chapters && course.chapters.length > 0">
                      <!-- داینامیک کردن چپترها -->
                      <div
                        v-for="(chapter, index) in course.chapters"
                        :key="chapter.slug"
                        class="accordion-item border border-2 rounded bg-transparent mb-4"
                        :class="{
                          'border border-danger rounded': activeItem === index,
                        }"
                      >
                        <h2
                          class="accordion-header p-3"
                          :id="`heading${index}`"
                        >
                          <button
                            class="accordion-button p-3 bg-transparent d-flex justify-content-between align-items-center fw-bold"
                            type="button"
                            :class="{
                              'text-muted': activeItem !== index,
                              'text-danger1': activeItem === index,
                            }"
                            @click="toggleItem(index)"
                          >
                            <span>{{ chapter.title }}</span>
                            <i
                              :class="[
                                'fa me-2',
                                activeItem === index ? 'fa-minus' : 'fa-plus',
                                activeItem === index
                                  ? 'text-danger1'
                                  : 'text-muted',
                              ]"
                            ></i>
                          </button>
                        </h2>
                        <div
                          :id="`collapse${index}`"
                          class="accordion-collapse collapse"
                          :class="{ show: activeItem === index }"
                          :aria-labelledby="`heading${index}`"
                        >
                          <div class="accordion-body">
                            <div
                              v-for="lesson in chapter.lessons"
                              :key="lesson.slug"
                              class="p-3 border-bottom"
                            >
                              <div
                                class="d-flex justify-content-between align-items-center"
                              >
                                <div class="flex-grow-1">
                                  <h6 class="fw-bold text-danger1 mb-2">
                                    {{ lesson.title }}
                                  </h6>
                                  <p class="text-muted mb-2">
                                    {{ lesson.content }}
                                  </p>
                                  <div
                                    v-if="lesson.video_link"
                                    class="d-flex align-items-center gap-2"
                                  >
                                    <i class="fas fa-video text-primary"></i>
                                    <span class="text-primary small"
                                      >ویدیو موجود</span
                                    >
                                  </div>
                                </div>
                                <div class="ms-3">
                                  <button
                                    v-if="lesson.video_link"
                                    @click="selectLesson(lesson)"
                                    class="btn btn-outline-primary btn-sm"
                                  >
                                    <i class="fas fa-play me-1"></i>
                                    تماشا
                                  </button>
                                  <span v-else class="text-muted small"
                                    >بدون ویدیو</span
                                  >
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <!-- پیام خالی بودن -->
                    <div
                      class="d-flex align-items-center justify-content-center flex-column"
                      v-else
                    >
                      <img
                        src="/images/no.gif"
                        alt="No Courses Found"
                        class=""
                        style="width: 200px; height: auto"
                      />
                      <p class="text-muted">
                        درحال حاضر هیچ سرفصلی برای این دوره وجود ندارد .
                      </p>
                    </div>
                  </div>
                </div>
              </div>
              <div
                class="tab-pane fade bg-light p-3 rounded-4"
                id="comments"
                role="tabpanel"
                aria-labelledby="comments-tab"
              >
                <div class="bg-light p-4 rounded">
                  <div class="d-flex justify-content-center">
                    <div
                      class="d-flex align-items-center justify-content-center p-3 bg-white rounded-4 gap-4"
                    >
                      <div
                        class="text-danger1 d-flex align-items-center gap-3 bg-light p-2 rounded-4"
                      >
                        <span class="fw-bold fs-5 text-danger1">{{
                          course.average_rate
                        }}</span>
                        <div>
                          <!-- تولید ستاره‌های پر -->
                          <i
                            v-for="star in Math.floor(course.average_rate)"
                            :key="'full-' + star"
                            class="icon icon-filled-star text-danger1"
                          ></i>
                          <!-- تولید یک ستاره نیمه‌پر اگر مقدار اعشاری باشد -->
                          <i
                            v-if="course.average_rate % 1 !== 0"
                            class="icon icon-filled-star-half text-danger1"
                          ></i>
                          <!-- تولید ستاره‌های خالی -->
                          <i
                            v-for="empty in 5 - Math.ceil(course.average_rate)"
                            :key="'empty-' + empty"
                            class="icon icon-regular-star text-muted"
                          ></i>
                        </div>
                      </div>
                      <p class="text-muted mt-3">
                        از {{ course.comments.length }} نظر
                      </p>
                    </div>
                  </div>
                  <div
                    class="mb-5"
                    v-for="(comment, index) in course.comments"
                    :key="index"
                  >
                    <div class="mb-4">
                      <div class="d-flex align-items-center">
                        <!-- تصویر کاربر -->
                        <img
                          src="/images/user.png"
                          alt="Reviewer"
                          class="rounded-circle img-fluid ms-3 w-100-px h-100-px object-fit-cover"
                        />
                        <!-- اطلاعات کامنت -->
                        <div class="w-100">
                          <!-- بخش ستاره‌ها -->
                          <div class="d-flex justify-content-start">
                            <div
                              class="d-flex align-items-center justify-content-center rounded-4 gap-2"
                            >
                              <div
                                class="text-danger1 d-flex align-items-center gap-2 rounded-4"
                              >
                                <div>
                                  <!-- تولید ستاره‌های پر -->
                                  <i
                                    v-for="star in Math.floor(comment.rate)"
                                    :key="'full-' + star"
                                    class="icon icon-filled-star text-danger1"
                                  ></i>
                                  <!-- تولید یک ستاره نیمه‌پر اگر مقدار اعشاری باشد -->
                                  <i
                                    v-if="comment.rate % 1 !== 0"
                                    class="icon icon-filled-star-half text-danger1"
                                  ></i>
                                  <!-- تولید ستاره‌های خالی -->
                                  <i
                                    v-for="empty in 5 - Math.ceil(comment.rate)"
                                    :key="'empty-' + empty"
                                    class="icon icon-regular-star text-muted"
                                  ></i>
                                </div>
                              </div>
                            </div>
                          </div>
                          <!-- متن کامنت -->
                          <p class="text-muted">
                            {{ comment.content }}
                          </p>
                        </div>
                      </div>
                      <!-- اطلاعات نویسنده کامنت -->
                      <div class="border-bottom pb-3 me-2">
                        <span class="fw-bold"
                          >{{ comment.user.first_name }}
                          {{ comment.user.last_name }}</span
                        >
                        <p class="text-muted mb-0 fs-6">
                          {{ comment.create_date }}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-3 order-md-2 order-1">
            <div class="card border-0">
              <!-- Price and Button -->
              <div class="text-center mb-4 bg-light p-4 rounded-4">
                <div
                  class="d-flex justify-content-between align-items-center mb-3"
                >
                  <span class="text-muted">قیمت دوره:</span>
                  <span class="text-danger1 fw-bold fs-5">
                    {{ formattedPrice }}
                    تومان</span
                  >
                </div>
                <button class="btn btn-danger w-100 py-2" @click="addToCart">
                  ثبت نام دوره
                </button>
              </div>
              <ul class="list-unstyled bg-light p-4 rounded-4">
                <li
                  class="d-flex justify-content-between align-items-center py-4 border-bottom"
                >
                  <span class="text-muted">
                    <i
                      class="icon icon-regular-video text-body-tertiary fs-4"
                    ></i>
                    تعداد درس‌ها:</span
                  >
                  <span>{{ totalLessons }}</span>
                </li>
                <li
                  class="d-flex justify-content-between align-items-center py-4 border-bottom"
                >
                  <span class="text-muted">
                    <i
                      class="icon icon-regular-layer-group text-body-tertiary fs-4"
                    ></i>
                    سطح دوره:</span
                  >
                  <span>
                    {{
                      course.attributes.find(
                        (attribute) => attribute.title === "سطح دوره",
                      )?.value || "نامشخص"
                    }}
                  </span>
                </li>
                <li
                  class="d-flex justify-content-between align-items-center py-4 border-bottom"
                >
                  <span class="text-muted">
                    <i
                      class="icon icon-regular-book-open text-body-tertiary fs-4"
                    ></i>
                    پیش نیاز:</span
                  >
                  <span>
                    {{
                      course.attributes.find(
                        (attribute) => attribute.slug === "need",
                      )?.value || "نامشخص"
                    }}
                  </span>
                </li>
                <li
                  class="d-flex justify-content-between align-items-center py-4 border-bottom"
                >
                  <span class="text-muted">
                    <i
                      class="icon icon-regular-globe text-body-tertiary fs-4"
                    ></i>
                    زبان:</span
                  >
                  <span>
                    {{
                      course.attributes.find(
                        (attribute) => attribute.slug === "language",
                      )?.value || "نامشخص"
                    }}
                  </span>
                </li>
                <li
                  class="d-flex justify-content-between align-items-center py-4 border-bottom"
                >
                  <span class="text-muted">
                    <i
                      class="icon icon-regular-building text-body-tertiary fs-4"
                    ></i>
                    برگزارکننده:</span
                  >
                  <span class="text-center">{{ course.organizer.name }}</span>
                </li>
                <li
                  class="d-flex justify-content-between align-items-center py-4 border-bottom"
                >
                  <span class="text-muted">
                    <i
                      class="icon icon-regular-desktop text-body-tertiary fs-4"
                    ></i>
                    مدرس:</span
                  >
                  <span
                    >{{ course.modares.first_name }}
                    {{ course.modares.last_name }}</span
                  >
                </li>
                <li
                  class="d-flex justify-content-between align-items-center py-4 border-bottom"
                >
                  <span class="text-muted">
                    <i
                      class="icon icon-regular-headphones text-body-tertiary fs-4"
                    ></i>
                    منتور:</span
                  >
                  <span>
                    {{
                      course.attributes.find(
                        (attribute) => attribute.slug === "mentor",
                      )?.value || "نامشخص"
                    }}
                  </span>
                </li>
                <li
                  class="d-flex justify-content-between align-items-center py-4 border-bottom"
                >
                  <span class="text-muted">
                    <i
                      class="icon icon-regular-graduation-cap text-body-tertiary fs-4"
                    ></i>
                    گواهینامه پایان دوره:</span
                  >
                  <span> دارد </span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>
    <section class="container my-3">
      <h4 class="mb-5 fw-bold text-center">فرصت‌های شغلی مرتبط</h4>
      <div class="row g-4">
        <div class="col-lg-4 col-md-6">
          <div class="card border-0 shadow-sm rounded">
            <div
              class="bg-dark-subtle p-2 rounded-top position-relative h-60-px"
            >
              <img
                src="/images/company/snapp.png"
                alt="Company Logo"
                class="rounded-circle border border-dark border-2 w-60-px h-60-px position-absolute top-50 right-10-px"
              />
            </div>
            <div class="card-body">
              <div class="row mt-4 text-end">
                <div class="col-md-6 mb-3">
                  <h5 class="card-title">استخدام برنامه نویس</h5>
                </div>
                <div class="col-md-6 text-lg-start mb-3">
                  <button class="btn btn-danger">مشاهده صفحه</button>
                </div>
              </div>
              <p class="text-muted mb-3">
                <i class="icon icon-regular-building text-danger1"></i> تپسی
              </p>
              <p class="text-muted mb-3">
                <i class="icon icon-regular-location-pin text-danger1"></i>
                تهران، ایران
              </p>
            </div>
          </div>
        </div>
        <div class="col-lg-4 col-md-6">
          <div class="card border-0 shadow-sm rounded">
            <div
              class="bg-dark-subtle p-2 rounded-top position-relative h-60-px"
            >
              <img
                src="/images/company/snapp.png"
                alt="Company Logo"
                class="rounded-circle border border-dark border-2 w-60-px h-60-px position-absolute top-50 right-10-px"
              />
            </div>
            <div class="card-body">
              <div class="row mt-4 text-end">
                <div class="col-md-6 mb-3">
                  <h5 class="card-title">استخدام برنامه نویس</h5>
                </div>
                <div class="col-md-6 text-lg-start mb-3">
                  <button class="btn btn-danger">مشاهده صفحه</button>
                </div>
              </div>
              <p class="text-muted mb-3">
                <i class="icon icon-regular-building text-danger1"></i> تپسی
              </p>
              <p class="text-muted mb-3">
                <i class="icon icon-regular-location-pin text-danger1"></i>
                تهران، ایران
              </p>
            </div>
          </div>
        </div>
        <div class="col-lg-4 col-md-6">
          <div class="card border-0 shadow-sm rounded">
            <div
              class="bg-dark-subtle p-2 rounded-top position-relative h-60-px"
            >
              <img
                src="/images/company/snapp.png"
                alt="Company Logo"
                class="rounded-circle border border-dark border-2 w-60-px h-60-px position-absolute top-50 right-10-px"
              />
            </div>
            <div class="card-body">
              <div class="row mt-4 text-end">
                <div class="col-md-6 mb-3">
                  <h5 class="card-title">استخدام برنامه نویس</h5>
                </div>
                <div class="col-md-6 text-lg-start mb-3">
                  <button class="btn btn-danger">مشاهده صفحه</button>
                </div>
              </div>
              <p class="text-muted mb-3">
                <i class="icon icon-regular-building text-danger1"></i> تپسی
              </p>
              <p class="text-muted mb-3">
                <i class="icon icon-regular-location-pin text-danger1"></i>
                تهران، ایران
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Video Player Modal -->
    <div
      v-if="showVideoPlayer && selectedLesson"
      class="modal fade show d-block"
      tabindex="-1"
      style="background-color: rgba(0, 0, 0, 0.8)"
    >
      <div class="modal-dialog modal-xl modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ selectedLesson.title }}</h5>
            <button
              type="button"
              class="btn-close"
              @click="closeVideoPlayer"
            ></button>
          </div>
          <div class="modal-body p-0">
            <div class="ratio ratio-16x9">
              <!-- اگر ویدیو از Aparat است، از iframe استفاده کن -->
              <iframe
                v-if="
                  selectedLesson.video_link &&
                  isEmbedUrl(getVideoUrl(selectedLesson.video_link))
                "
                :src="getVideoUrl(selectedLesson.video_link)"
                class="w-100 h-100"
                frameborder="0"
                allow="
                  accelerometer;
                  autoplay;
                  clipboard-write;
                  encrypted-media;
                  gyroscope;
                  picture-in-picture;
                "
                allowfullscreen
              ></iframe>
              <!-- در غیر این صورت از video tag استفاده کن -->
              <video
                v-else-if="selectedLesson.video_link"
                controls
                class="w-100 h-100"
                crossorigin="anonymous"
                preload="metadata"
              >
                <source
                  :src="getVideoUrl(selectedLesson.video_link)"
                  type="video/mp4"
                />
                <source
                  :src="getVideoUrl(selectedLesson.video_link)"
                  type="video/webm"
                />
                <source
                  :src="getVideoUrl(selectedLesson.video_link)"
                  type="video/ogg"
                />
                مرورگر شما از ویدیو پشتیبانی نمی‌کند.
              </video>
            </div>
          </div>
          <div class="modal-footer">
            <p class="text-muted mb-0">{{ selectedLesson.content }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, reactive } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useCartStore } from "~/stores/cart";
import { formatNumber } from "~/assets/commons/helpers";

const data = reactive({
  loaded: false,
});
const course = ref({});
const route = useRoute();
const router = useRouter();
const slug = ref(route.params.slug);
const isSaved = ref(false);
const activeItem = ref(null);
const selectedLesson = ref(null);
const showVideoPlayer = ref(false);
const { $api, $sweetalert } = useNuxtApp();
const { getMediaUrl, getVideoUrl, isEmbedUrl } = useMediaUrl();

// تبدیل آدرس تصویر به آدرس با /api
const courseImageUrl = computed(() => getMediaUrl(course.value?.image));

// Mock cart store
const cartItems = ref([]);

const toggleItem = (id) => {
  activeItem.value = activeItem.value === id ? null : id;
};

const selectLesson = (lesson) => {
  selectedLesson.value = lesson;
  showVideoPlayer.value = true;
};

const closeVideoPlayer = () => {
  showVideoPlayer.value = false;
  selectedLesson.value = null;
};

const formattedPrice = computed(() => formatNumber(course.value.price));

const getFirstLessonVideo = () => {
  if (course.value.chapters && course.value.chapters.length > 0) {
    for (const chapter of course.value.chapters) {
      if (chapter.lessons && chapter.lessons.length > 0) {
        for (const lesson of chapter.lessons) {
          if (lesson.video_link) {
            return getVideoUrl(lesson.video_link);
          }
        }
      }
    }
  }
  return null;
};

const totalLessons = computed(() => {
  if (course.value.chapters && Array.isArray(course.value.chapters)) {
    return course.value.chapters.reduce((total, chapter) => {
      return total + (chapter.lessons ? chapter.lessons.length : 0);
    }, 0);
  }
  return 0;
});

// Load course details from backend
const getCourse = async () => {
  data.loaded = false;
  try {
    const response = await $api.post("/course/detail", {
      slug: slug.value,
    });

    if (response.data.status) {
      course.value = response.data.data;
    } else {
      console.error("Course not found for slug:", slug.value);
      course.value = {};
    }
  } catch (error) {
    console.error("Error loading course:", error);
    $sweetalert.error("خطا در بارگذاری اطلاعات دوره");
    course.value = {};
  } finally {
    data.loaded = true;
  }
};

const toggleSaveCourse = async () => {
  const token = useCookie("token").value;

  if (!token) {
    $sweetalert.error("جهت ذخیره دوره لطفاً وارد حساب کاربری خود شوید");
    return;
  }

  try {
    await $api.post(
      "/course/wishlist/create",
      { course_id: course.value.id },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );

    isSaved.value = !isSaved.value;
    $sweetalert.success(
      isSaved.value
        ? "دوره با موفقیت به علاقه‌مندی‌ها اضافه شد"
        : "دوره با موفقیت از علاقه‌مندی‌ها حذف شد",
    );
  } catch (error) {
    console.error("Error toggling save course:", error);
    $sweetalert.error("خطا در ذخیره/حذف دوره");
  }
};

const addToCart = () => {
  const token = useCookie("token").value;

  if (!token) {
    $sweetalert.error("جهت ثبت نام در دوره لطفاً وارد حساب کاربری خود شوید");
    return;
  }

  if (!course.value || !course.value.id) {
    console.error("مشکلی در دریافت اطلاعات دوره وجود دارد!");
    $sweetalert.error("مشکلی در دریافت اطلاعات دوره وجود دارد!");
    return;
  }

  // Check if course is already in cart
  const cartStore = useCartStore();
  const existingItem = cartStore.cartItems.find(
    (item) => item.id === course.value.id,
  );

  if (existingItem) {
    $sweetalert.error("این دوره قبلاً در سبد خرید شما موجود است!");
    return;
  }

  // Add course to cart
  const courseItem = {
    id: course.value.id,
    title: course.value.title,
    price: course.value.price,
    provider: course.value.organizer?.name || "نامشخص",
    image: course.value.image,
  };

  cartStore.addToCart(courseItem);
  $sweetalert.success("دوره با موفقیت به سبد خرید اضافه شد!");

  // Redirect to checkout page
  router.push("/checkout");
};

onMounted(() => {
  getCourse();
});
</script>

<style scoped>
.bg-dark-subtle {
  background-color: rgba(43, 45, 66, 1) !important;
}
</style>
