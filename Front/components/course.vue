<template>
  <div
    class="card h-100 rounded-4 border-0"
    :class="{ 'course-small': size === 'small' }"
  >
    <nuxt-link :to="`/courses/${course.slug}`">
      <div
        class="d-flex align-items-center justify-content-between py-3 px-2 pb-0 mb-0"
        :class="{ 'py-2': size === 'small' }"
      >
        <p
          class="text-muted small text-end"
          :class="{ smaller: size === 'small' }"
        >
          برگزار کننده :
        </p>
        <p
          class="text-danger1 small text-end"
          :class="{ smaller: size === 'small' }"
        >
          {{ course.organizer.name }}
        </p>
      </div>
    </nuxt-link>
    <div class="position-relative">
      <nuxt-link :to="`/courses/${course.slug}`">
        <div
          class="course-image position-relative rounded-0 object-fit-cover"
          :class="size === 'small' ? 'h-180-px' : 'h-270-px'"
          :style="{ backgroundImage: `url(${courseImageUrl})` }"
          :alt="course.title"
        ></div>
      </nuxt-link>
      <div
        class="cursor-pointer position-absolute rounded-circle shadow-sm d-flex justify-content-center align-items-center"
        :class="[
          size === 'small'
            ? 'top-155-px left-8-px w-35-px h-35-px'
            : 'top-245-px left-10-px w-45-px h-45-px',
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
      <nuxt-link :to="`/courses/${course.slug}`" class="text-dark text-end">
        <h5
          class="card-title fw-bold text-dark mt-2"
          :class="{ 'fs-6': size === 'small' }"
        >
          {{ course.title }}
        </h5>
        <div class="d-flex align-items-center justify-content-between py-1">
          <p class="text-muted" :class="{ small: size === 'small' }">
            {{ course.category.title }}
          </p>
        </div>
        <div
          class="row mb-3 justify-content-between"
          :class="{ 'mb-2': size === 'small' }"
        >
          <div
            class="col-5 text-center bg-light rounded-3 me-2"
            :class="size === 'small' ? 'p-1' : 'p-2'"
          >
            <div class="d-flex align-items-center justify-content-center gap-1">
              <i
                class="icon icon-regular-clock text-danger1"
                :class="size === 'small' ? 'smaller' : 'small'"
              ></i>
              <span :class="size === 'small' ? 'smaller' : 'small'">
                {{
                  course.attributes.find(
                    (attribute) => attribute.title === "مدت زمان دوره",
                  )?.value || "نامشخص"
                }}
              </span>
            </div>
          </div>
        </div>
        <div
          class="d-flex justify-content-start gap-2 mb-3"
          :class="{ 'mb-2': size === 'small' }"
        >
          <span
            class="badge bg-danger-subtle text-danger1 border"
            :class="size === 'small' ? 'py-1 smaller' : 'py-2 small'"
          >
            {{
              course.attributes.find(
                (attribute) => attribute.slug === "language",
              )?.value || "نامشخص"
            }}
          </span>
        </div>
        <div class="d-flex justify-content-between align-items-center">
          <span class="text-muted" :class="{ smaller: size === 'small' }"
            >قیمت دوره:</span
          >
          <span
            class="fw-bold text-danger1"
            :class="size === 'small' ? 'fs-6' : 'fs-6'"
          >
            {{ formattedPrice }}
            <span
              class="small text-muted"
              :class="{ smaller: size === 'small' }"
              >تومان</span
            >
          </span>
        </div>
      </nuxt-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useNuxtApp } from "#app";
import { formatNumber } from "~/assets/commons/helpers";

const formattedPrice = computed(() => {
  if (props.course && props.course.price) {
    return formatNumber(props.course.price);
  }
  return "";
});

const props = defineProps({
  course: {
    type: Object,
    required: true,
  },
  size: {
    type: String,
    default: "normal", // 'normal' or 'small'
  },
});

const isSaved = ref(false);
const { $api, $sweetalert } = useNuxtApp();
const { getMediaUrl } = useMediaUrl();

// تبدیل آدرس تصویر به آدرس با /api
const courseImageUrl = computed(() => getMediaUrl(props.course?.image));

// Debug: Log course data when component mounts
onMounted(() => {
  // console.log("🎓 Course component mounted with data:", props.course);
  // console.log("📋 Course attributes:", props.course.attributes);

  // Test attribute finding
  const duration = props.course.attributes?.find(
    (attribute) => attribute.title === "مدت زمان دوره",
  );
  const jobPositions = props.course.attributes?.find(
    (attribute) => attribute.title === "تعداد موقعیت شغلی",
  );
  const language = props.course.attributes?.find(
    (attribute) => attribute.slug === "language",
  );

  // console.log("⏱️ Duration found:", duration);
  // console.log("💼 Job positions found:", jobPositions);
  // console.log("💻 Language found:", language);
});

const toggleSaveCourse = async () => {
  const token = useCookie("token").value;

  if (!token) {
    $sweetalert.error("جهت ذخیره دوره لطفاً وارد حساب کاربری خود شوید");
    return;
  }
  if (isSaved.value) {
    await $api
      .post(
        "/course/wishlist/create",
        { course_id: props.course.id },
        {
          headers: {
            Authorization: `Bearer ${useCookie("token").value}`,
          },
        },
      )
      .then(() => {
        isSaved.value = false;
        $sweetalert.success("دوره با موفقیت از علاقه‌مندی‌ها حذف شد");
      })
      .catch((error) => {
        console.error("Error removing course:", error);
        $sweetalert.error("حذف دوره با خطا مواجه شد");
      });
  } else {
    await $api
      .post(
        "/course/wishlist/create",
        { course_id: props.course.id },
        {
          headers: {
            Authorization: `Bearer ${useCookie("token").value}`,
          },
        },
      )
      .then(() => {
        isSaved.value = true;
        $sweetalert.success("دوره با موفقیت به علاقه‌مندی‌ها اضافه شد");
      })
      .catch((error) => {
        console.error("Error saving course:", error);
        $sweetalert.error("ذخیره دوره با خطا مواجه شد");
      });
  }
};
</script>

<style scoped>
.card {
  transition: transform 0.3s ease-in-out;
}

.card:hover {
  transform: scale(1.02);
}

.text-danger1 {
  color: #ff8c14 !important;
}

.course-image {
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

/* Small size styles */
.course-small .card-body {
  padding: 0.75rem;
}

.course-small .smaller {
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
