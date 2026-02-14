<template>
      <div class="card mb-5 h-100 rounded-5 border-0 bg-light" :class="{ 'webinar-small': size === 'small' }">
          <div class="position-relative">
      <nuxt-link :to="`/events/${webinar.id}`">
        <div
          class="course-image position-relative rounded-top-5 object-fit-cover"
          :class="size === 'small' ? 'h-180-px' : 'h-270-px'"
          :style="{ backgroundImage: `url(${webinarImageUrl})` }"
          :alt="webinar.title"
        ></div>
      </nuxt-link>
      <div
        class="cursor-pointer position-absolute rounded-circle shadow-sm d-flex justify-content-center align-items-center"
        :class="[
          size === 'small' ? 'top-155-px left-8-px w-35-px h-35-px' : 'top-245-px left-10-px w-45-px h-45-px',
          isSaved ? 'bg-danger text-white' : 'bg-white text-danger1',
        ]"
        @click.stop="toggleSaveCourse"
      >
        <i
          :class="[ 
            'icon fw-light mt-1',
            size === 'small' ? 'fs-5' : 'fs-4',
            isSaved ? 'icon-filled-bookmark' : 'icon-regular-bookmark',
          ]"
        ></i>
      </div>
    </div>
        <div class="card-body" :class="{ 'p-2': size === 'small' }">
          <h5 class="card-title fw-bold text-dark text-end my-3" :class="{ 'fs-6 my-2': size === 'small' }">
            {{ webinar.title }}
          </h5>
          <p class="text-muted text-end mt-2" :class="{ 'small mt-1': size === 'small' }">سخنران: {{ webinar.speaker }}</p>
          <div class="row mb-3 px-2" :class="{ 'mb-2 px-1': size === 'small' }">
            <div class="col-6 text-center bg-white rounded-3" :class="size === 'small' ? 'p-1' : 'p-2'">
              <div class="d-flex align-items-center justify-content-center gap-2">
                <i class="icon icon-regular-calendar text-danger1" :class="size === 'small' ? 'smaller' : ''"></i>
                <span :class="size === 'small' ? 'smaller' : ''">{{ webinar.date }}</span>
              </div>
            </div>
            <div class="col-6 text-center bg-white rounded-3" :class="size === 'small' ? 'p-1' : 'p-2'">
              <div class="d-flex align-items-center justify-content-center gap-2">
                <i class="icon icon-regular-clock text-danger1" :class="size === 'small' ? 'smaller' : ''"></i>
                <span :class="size === 'small' ? 'smaller' : ''">{{ webinar.start_time }}</span>
              </div>
            </div>
          </div>
          <div class="d-flex justify-content-between align-items-center">
            <button class="btn btn-danger" :class="size === 'small' ? 'px-3 py-1 smaller' : 'px-4 py-2'">ثبت نام وبینار</button>
            <span class="text-muted" :class="{ 'smaller': size === 'small' }">
              {{ webinar.is_free ? "رایگان" : webinar.price }}
            </span>
          </div>
        </div>

      </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue';
  
  const props = defineProps({
    webinar: {
      type: Object,
      required: true,
    },
    size: {
      type: String,
      default: 'normal', // 'normal' or 'small'
    },
  });

const isSaved = ref(false);
const { $api, $sweetalert } = useNuxtApp();
const { getMediaUrl } = useMediaUrl();

// تبدیل آدرس تصویر به آدرس با /api
const webinarImageUrl = computed(() => getMediaUrl(props.webinar?.image));

const toggleSaveCourse = async () => {
  const token = useCookie("token").value;

if (!token) {
  $sweetalert.error("جهت ذخیره وبینار لطفاً وارد حساب کاربری خود شوید");
  return;
}
  if (isSaved.value) {
    await $api
      .post(
        "/course/wishlist/create",
        { course_id: props.webinar.id },
        {
          headers: {
            Authorization: `Bearer ${useCookie("token").value}`,
          },
        }
      )
      .then(() => {
        isSaved.value = false;
        $sweetalert.success("وبینار با موفقیت از علاقه‌مندی‌ها حذف شد");
      })
      .catch((error) => {
        console.error("Error removing webinar:", error);
        $sweetalert.error("حذف وبینار با خطا مواجه شد");
      });
  } else {
    await $api
      .post(
        "/course/wishlist/create",
        { course_id: props.webinar.id },
        {
          headers: {
            Authorization: `Bearer ${useCookie("token").value}`,
          },
        }
      )
      .then(() => {
        isSaved.value = true;
        $sweetalert.success("وبینار با موفقیت به علاقه‌مندی‌ها اضافه شد");
      })
      .catch((error) => {
        console.error("Error saving webinar:", error);
        $sweetalert.error("ذخیره وبینار با خطا مواجه شد");
      });
  }
};
  </script>

  <style scoped>

.course-image {
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

/* Small size styles */
.webinar-small .card-body {
  padding: 0.75rem;
}

.webinar-small .smaller {
  font-size: 0.75rem;
}

.h-180-px {
  height: 180px;
}

.h-270-px {
  height: 270px;
}

.top-155-px {
  top: 155px;
}

.top-245-px {
  top: 245px;
}

.left-8-px {
  left: 8px;
}

.left-10-px {
  left: 10px;
}

.w-35-px {
  width: 35px;
}

.h-35-px {
  height: 35px;
}

.w-45-px {
  width: 45px;
}

.h-45-px {
  height: 45px;
}
</style>
  