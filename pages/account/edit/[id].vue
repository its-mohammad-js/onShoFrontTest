<template>
  <div class="container py-5">
    <div class="bg-light border border-2 rounded-3 p-4">
      <h6 class="mb-3 fw-bold">ویرایش دوره</h6>
      <div class="row">
        <div class="col-sm-12">
          <div class="d-flex align-items-center justify-content-center mb-4">
        <!-- مرحله 1 -->
        <div class="step-item cursor-pointer" @click="currentStep = 1" :class="{ 'active': currentStep >= 1 }">
          اطلاعات کلی دوره
          <span class="check-icon" v-if="currentStep > 1">✔</span>
        </div>
        <div class="step-line" :class="{ 'active': currentStep >= 2 }"></div>

        <!-- مرحله 2 -->
        <div class="step-item cursor-pointer" @click="currentStep = 2" :class="{ 'active': currentStep >= 2 }">
          جزئیات دوره
          <span class="check-icon" v-if="currentStep > 2">✔</span>
        </div>
        <div class="step-line" :class="{ 'active': currentStep >= 3 }"></div>

        <!-- مرحله 3 -->
        <div class="step-item cursor-pointer"  @click="currentStep = 3" :class="{ 'active': currentStep >= 3 }">
          مدیریت فصل‌ها و درس‌ها
          <span class="check-icon" v-if="currentStep > 3">✔</span>
        </div>
      </div>

        </div>

        <div class="col-sm-12">
          <!-- Loading State -->
          <div v-if="!data.loaded" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">در حال بارگذاری...</span>
            </div>
            <p class="text-muted mt-3">در حال بارگذاری اطلاعات دوره...</p>
          </div>
          
          <!-- Form Content -->
          <div v-else>
            <div v-show="currentStep === 1">
              <main-info v-model="data" />
            </div>
            <div v-show="currentStep === 2">
              <detail v-model="data" />
            </div>
            <div v-show="currentStep === 3">
              <chapter-lesson-manager v-model="data" />
            </div>
          </div>
        </div>
      </div>

      <div v-if="data.loaded" class="row">
        <div class="col-sm-12">
          <div class="row">
            <div class="col-sm-12 mt-5">
              <div
                class="d-flex align-items-center"
                :class="[
                  { 'justify-content-between': currentStep > 1 },
                  { 'justify-content-end': currentStep === 1 }
                ]"
              >
                <button
                  v-if="currentStep > 1"
                  class="d-flex align-items-center btn btn-danger py-1"
                  type="button"
                  @click="prevStep"
                >
                  <i class="icon fw-light icon-regular-angle-right fs-5 mx-1 mt-2"></i>
                  <span>مرحله قبل </span>
                </button>
                <button
                  v-if="currentStep < 3"
                  class="d-flex align-items-center btn btn-danger py-1"
                  type="button"
                  @click="nextStep"
                >
                  <span>ثبت و مرحله بعدی</span>
                  <i class="icon fw-light icon-regular-angle-left fs-5 mx-1 mt-2"></i>
                </button>
                <button
                  type="submit"
                  class="btn btn-danger text-white py-3"
                  v-if="currentStep === 3"
                  @click="updateCourse"
                >
                  ویرایش دوره
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import mainInfo from "./components/main-info.vue";
import detail from "./components/detail.vue";
import chapterLessonManager from "./components/chapter-lesson-manager.vue";
import { reactive, ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
const router = useRouter();
const route = useRoute();
const { $api, $sweetalert } = useNuxtApp();

const data = reactive({
  loaded: false,
  course: {},
  title: "",
  description: "",
  excerpt: "",
  price: "",
  discount: "",
  category: "",
  photo: "",
  categories: [],
  attributes: [],
  courseId: null,
  chapters: [],
  type_value: "", // نوع دوره: online, offline, in_person
  attributeValues: {
    language: "",
    duration: "",
    level: "",
    need: "",
    mentor: "",
  },
  newChapter: '',
  newLesson: {
    title: "",
    description: "",
    videoLink: "",
  },
});

const currentStep = ref(1);

const getCategories = () => {
$api
  .post("/course/category/list", {}, {
    headers: {
      Authorization: "Bearer " + useCookie("token").value,
    },
  })
  .then((Value) => {
    data.categories = Value.data.data;
    console.log("📝 Categories loaded:", data.categories);
  })
  .catch((error) => {
    console.error("خطا در دریافت دسته‌بندی‌ها:", error);
  });
};

const getAttributes = () => {
$api
  .post("/course/attributes/list", {}, {
    headers: {
      Authorization: "Bearer " + useCookie("token").value,
    },
  })
  .then((value) => {
    data.attributes = value.data.data;
    console.log("📝 Attributes loaded:", data.attributes);
  })
  .catch((error) => {
    console.error("خطا در دریافت اتریبیوت‌ها:", error);
  });
};

const getAttributeItem = (input) => {
  if (!data.course || !data.course.attributes || !Array.isArray(data.course.attributes)) {
    console.log(`❌ No attributes available for ${input}`);
    return "";
  }
  
  // ابتدا سعی می‌کنیم با slug پیدا کنیم
  let item = data.course.attributes.find(item => item.slug == input);
  
  // اگر با slug پیدا نشد، از data.attributes استفاده می‌کنیم تا title را پیدا کنیم
  if (!item && data.attributes && Array.isArray(data.attributes)) {
    const attributeDef = data.attributes.find(attr => attr.slug === input);
    if (attributeDef && attributeDef.title) {
      // حالا با title از course.attributes پیدا می‌کنیم
      item = data.course.attributes.find(courseAttr => courseAttr.title === attributeDef.title);
    }
  }
  
  // اگر هنوز پیدا نشد، مستقیماً با title جستجو می‌کنیم
  if (!item) {
    const titleMap = {
      'duration': 'مدت زمان دوره',
      'level': 'سطح دوره',
      'language': 'زبان دوره',
      'need': 'پیش‌نیاز',
      'mentor': 'مدرس'
    };
    const title = titleMap[input];
    if (title) {
      item = data.course.attributes.find(courseAttr => courseAttr.title === title);
    }
  }
  
  if (item && typeof item !== 'undefined') {
    if (typeof item.value !== 'undefined') {
      if (item.value !== null) {
        console.log(`✅ Found attribute ${input}: ${item.value}`);
        return item?.value || "";
      }
    }
  }

  console.log(`❌ Attribute ${input} not found or has no value`);
  console.log(`📝 Available attributes:`, data.course.attributes);
  return "";
}

const getCurrent = () => {
  $api
    .post(
      "/course/user/detail",
      { course_id: data.courseId },
      {
        headers: {
          Authorization: "Bearer " + useCookie("token").value,
        },
      }
    )
    .then((value) => {
      data.course = value.data.data || {};
      populateFormData();
    })
    .catch((error) => {
      console.error("خطا در دریافت اطلاعات دوره:", error);
      $sweetalert.error("خطایی در دریافت اطلاعات دوره رخ داده است.");
      data.loaded = true; // حتی در صورت خطا، loaded را true کن تا صفحه نمایش داده شود
    });
};

const populateFormData = () => {
  if (data.course && Object.keys(data.course).length > 0) {
    console.log("📝 Populating form with course data:", data.course);
    
    data.title = data.course.title || "";
    data.description = data.course.description || "";
    data.excerpt = data.course.excerpt || "";
    data.chapters = data.course.chapters || [];
    data.photo = data.course.image || "";
    data.category = data.course.category?.id || "";
    data.price = data.course.price || "";
    data.discount = data.course.discount !== null && data.course.discount !== undefined ? data.course.discount : "";
    data.type_value = data.course.type_value || "";
    
    // اطمینان از اینکه chapters دارای lessons است
    if (data.chapters && Array.isArray(data.chapters)) {
      data.chapters = data.chapters.map(chapter => ({
        ...chapter,
        lessons: chapter.lessons || []
      }));
    }
    
    // Populate attribute values
    data.attributeValues.language = getAttributeItem("language");
    data.attributeValues.duration = getAttributeItem("duration");
    data.attributeValues.level = getAttributeItem("level");
    data.attributeValues.need = getAttributeItem("need");
    data.attributeValues.mentor = getAttributeItem("mentor");
    
    console.log("📝 Form data populated:", {
      title: data.title,
      description: data.description,
      category: data.category,
      price: data.price,
      discount: data.discount,
      attributeValues: data.attributeValues
    });
    
    data.loaded = true;
  } else {
    console.log("❌ No course data available to populate form");
  }
};


const updateCourse = () => {
  if (!data.photo) {
    $sweetalert.error("لطفاً یک عکس برای دوره انتخاب کنید.");
    return;
  }
  if (!data.title.trim()) {
    $sweetalert.error("لطفاً عنوان دوره را وارد کنید.");
    return;
  }
  if (!data.description.trim()) {
    $sweetalert.error("لطفاً توضیحات دوره را وارد کنید.");
    return;
  }
  if (!data.price || data.price <= 0) {
    $sweetalert.error("لطفاً قیمت دوره را به درستی وارد کنید.");
    return;
  }
  let output = [];
Object.keys(data.attributeValues).forEach((key) => {
  const attribute = data.attributes.find((item) => item.slug === key);
  const attributeValue = data.attributeValues[key];
  if (attribute && attributeValue) {
    output.push({
      attribute: attribute.id,
      value: attributeValue,
    });
  }
});
console.log("Attributes Output:", output);

const formData = new FormData();
formData.append("course_id", data.courseId);
formData.append("title", data.title);
formData.append("description", data.description);
formData.append("excerpt", data.excerpt);
formData.append("price", data.price);
if (data.discount) {
  formData.append("discount", data.discount);
}
if (data.category) {
  formData.append("category", data.category);
}
if (data.type_value) {
  formData.append("type_value", data.type_value);
}
formData.append("attributes", JSON.stringify(output));

if (data.photo instanceof File) {
  formData.append("image", data.photo);
} else if (typeof data.photo === "string" && data.photo.startsWith("http")) {
  formData.append("image_url", data.photo);
}

  $api
    .post("/course/update", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        Authorization: "Bearer " + useCookie("token").value,
      },
    })
    .then(() => {
      $sweetalert.success("دوره با موفقیت ویرایش شد!");
      router.push("/account");
    })
    .catch((error) => {
      console.error("خطا در ویرایش دوره:", error);
      $sweetalert.error("خطایی در ویرایش دوره رخ داده است.");
    });
};

const nextStep = () => {
  if (currentStep.value < 3) currentStep.value++;
};

const prevStep = () => {
  if (currentStep.value > 1) currentStep.value--;
};


onMounted(() => {
  // Try multiple ways to get the course ID
  const routeId = route.params.id;
  const queryId = route.query.id;
  const courseId = parseInt(routeId) || parseInt(queryId) || 12; // fallback to 12 for testing
  
  data.courseId = courseId;
  console.log("🔍 Route params:", route.params);
  console.log("🔍 Route query:", route.query);
  console.log("🔍 Course ID from route:", routeId, "Parsed:", courseId);
  console.log("🔍 Full data object:", data);
  
  getCategories();
  getAttributes();
  if (data.courseId) {
    getCurrent();
  }
});

definePageMeta({
  layout: "account",
  middleware: ['auth']
});


</script>

<style scoped>
.nav-pills .nav-link {
  cursor: pointer;
}
.nav-pills .nav-link.active {
  background-color: #dc3545;
  color: #fff;
}

.step-item {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 180px;
  height: 50px;
  background: #ddd;
  border-radius: 50px;
  font-weight: bold;
  color: #555;
  position: relative;
}

.step-item.active {
  background: #222;
  color: #fff;
}

.step-line {
  width: 50px;
  height: 3px;
  background: #ddd;
  margin: 0 10px;
}

.step-line.active {
  background: #222;
}

.check-icon {
  position: absolute;
  right: 10px;
  font-size: 14px;
  display: none;
}

.step-item.active .check-icon {
  display: inline;
}
@media (max-width: 768px) {
  .d-flex.align-items-center.justify-content-center {
    flex-direction: column; /* المان‌ها را در موبایل زیر هم قرار می‌دهد */
    align-items: center; /* وسط‌چین کردن در موبایل */
  }

  .step-item {
    width: 100%; /* در موبایل پهنای هر آیتم را تمام صفحه می‌کند */
    max-width: 300px; /* حداکثر عرض هر آیتم */
    height: 45px;
    font-size: 14px; /* متن را کوچکتر می‌کند */
    margin-bottom: 10px; /* فاصله بین مراحل */
  }

  .step-line {
    display: none; /* حذف خط اتصال بین مراحل در موبایل */
  }
}

</style>
