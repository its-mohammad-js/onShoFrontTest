<template>
  <div class="container py-5">
    <div class="bg-light border border-2 rounded-3 p-4">
      <h6 class="mb-3 fw-bold">ایجاد دوره</h6>
      <div class="row">
        <div class="col-sm-12">
          <!-- Progress Steps -->
          <div class="d-flex align-items-center justify-content-center">
  <!-- اطلاعات کلی دوره -->
  <div class="step-item cursor-pointer"   @click="currentStep = 1" :class="{ 'active': currentStep >= 1 }">
    اطلاعات کلی دوره
    <span class="check-icon">&#10003;</span>
  </div>

  <div class="step-line" :class="{ 'active': currentStep >= 2 }"></div>

  <!-- جزئیات دوره -->
  <div class="step-item cursor-pointer"   @click="currentStep = 2" :class="{ 'active': currentStep >= 2 }">
    جزئیات دوره
    <span class="check-icon">&#10003;</span>
  </div>

  <div class="step-line" :class="{ 'active': currentStep >= 3 }"></div>

  <!-- مدیریت فصل‌ها و درس‌ها -->
  <div class="step-item cursor-pointer"   @click="currentStep = 3" :class="{ 'active': currentStep >= 3 }">
    مدیریت فصل‌ها و درس‌ها
    <span class="check-icon">&#10003;</span>
  </div>
</div>

        </div>
        <div class="col-sm-12">
          <div v-show="currentStep === 1">
            <main-info v-model="data"/>
          </div>
          <div v-show="currentStep === 2">
            <detail v-model="data"/>
          </div>
          <div v-show="currentStep === 3">
            <div v-if="!data.courseId" class="alert alert-warning text-center py-4">
              <i class="fas fa-exclamation-triangle me-2"></i>
              در حال دریافت اطلاعات دوره... لطفاً صبر کنید.
            </div>
            <chapter-lesson-manager v-else v-model="data"/>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-sm-12">
          <div class="row">
            <div class="com-sm-12 mt-5">
              <div class="d-flex align-items-center" :class="[{'justify-content-between': currentStep > 1},{'justify-content-end': currentStep === 1}]">
                <button class="d-flex align-items-center btn btn-danger py-1" v-if="currentStep !== 1" type="button" @click="prevStep">
                  <i class="icon fw-light icon-regular-angle-right fs-5 mx-1 mt-2"></i> <span>مرحله قبل </span>
                </button>
                <button
                    v-if="currentStep === 1"
                    class="d-flex align-items-center btn btn-danger py-1"
                    type="button"
                    @click="nextStep"
                >
                  <span>ثبت و مرحله بعدی</span> <i class="icon fw-light icon-regular-angle-left fs-5 mx-1 mt-2"></i>
                </button>
                <button type="submit" class="btn btn-danger text-white py-3" v-if="currentStep === 2" @click="submitForm">
                  ایجاد دوره
                </button>
                <button type="button" class="btn btn-success text-white py-3" v-if="currentStep === 3" @click="finishCourse">
                  تکمیل و بازگشت
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
import chapterLessonManager from "../edit/components/chapter-lesson-manager.vue";
import { reactive, ref, onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const { $api, $sweetalert } = useNuxtApp();
const { canCreateCourse, organizationStatusMessage, fetchOrganization } = useOrganization()

const data = reactive({
  title: "",
  description: "",
  excerpt : "",
  price: "",
  discount: "",
  category: "",
  photo: "",
  categories: [],
  attributes: [],
  isco_code: "",
  courseId: null,
  chapters: [],
  newChapter: "",
  newLesson: {
    title: "",
    description: "",
    videoLink: "",
  },
  type_value: "", // نوع دوره: online, offline, in_person
  attributeValues: {
    language: "",
    duration: "",
    level: "",
    need:"",
    mentor : "",
  },
});

// دریافت دسته‌بندی‌ها
const getCategories = () => {
  $api
    .post("/course/category/list", {}, {
      headers: {
        Authorization: "Bearer " + useCookie("token").value,
      },
    })
    .then((Value) => {
      data.categories = Value.data.data;
    })
    .catch((error) => {
      console.error("خطا در دریافت دسته‌بندی‌ها:", error);
    });
};

// دریافت اتریبیوت‌ها
const getAttributes = () => {
  $api
    .post("/course/attributes/list", {}, {
      headers: {
        Authorization: "Bearer " + useCookie("token").value,
      },
    })
    .then((Value) => {
      data.attributes = Value.data.data;
      console.log("Attributes:", data.attributes); // بررسی داده‌های attributes
    })
    .catch((error) => {
      console.error("خطا در دریافت اتریبیوت‌ها:", error);
    });
};

const submitForm = () => {
  if (!data.photo) {
    $sweetalert.error("لطفاً یک عکس برای دوره انتخاب کنید.");
    return;
  }
  if (!data.title.trim()) {
    $sweetalert.error("لطفاً عنوان دوره را وارد کنید.");
    return;
  }
  // Check if category is selected (from level 3)
  if (!data.category) {
    $sweetalert.error("لطفاً یک دسته‌بندی برای دوره انتخاب کنید.");
    return;
  }
  if (!data.description.trim()) {
    $sweetalert.error("لطفاً توضیحات دوره را وارد کنید.");
    return;
  }
  if (!data.excerpt.trim()) {
    $sweetalert.error("لطفاً دید کلی دوره را وارد کنید.");
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
    console.log("Attributes Output:", data.attributeValues);
    // بررسی خالی بودن مقدار
    if (attribute && attributeValue) {
      output.push({
        attribute: attribute.id,
        value: attributeValue,
      });
    }
  });

  const formData = new FormData();
  formData.append("title", data.title);
  formData.append("description", data.description);
  formData.append("excerpt", data.excerpt);
  formData.append("price", data.price);
  if (data.discount) {
    formData.append("discount", data.discount);
  }
  if (data.photo) {
    formData.append("image", data.photo);
  }
  // Use category from data (which is set from level 3 in main-info component)
  if (data.category) {
    formData.append("category", data.category);
  }
  if (data.type_value) {
    formData.append("type_value", data.type_value);
  }
  formData.append("attributes", JSON.stringify(output));
  
  // Add isco_code if available
  if (data.isco_code) {
    formData.append("isco_code", data.isco_code);
  }

  $api
    .post("/course/create", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        Authorization: "Bearer " + useCookie("token").value,
      },
    })
    .then((response) => {
      console.log("📡 Response from course/create:", response.data);
      
      if (response.data.status) {
        // دریافت courseId از پاسخ API - بررسی چندین حالت مختلف
        const responseData = response.data.data;
        let courseId = null;
        
        if (responseData) {
          // حالت 1: responseData یک object است
          if (typeof responseData === 'object') {
            courseId = responseData.id || responseData.course_id || responseData.course?.id;
          }
          // حالت 2: responseData یک عدد است (مستقیم courseId)
          else if (typeof responseData === 'number') {
            courseId = responseData;
          }
        }
        
        // اگر courseId پیدا نشد، از response.data مستقیماً بگیر
        if (!courseId) {
          courseId = response.data.id || response.data.course_id || response.data.course?.id;
        }
        
        console.log("🔍 Extracted courseId:", courseId);
        
        if (courseId) {
          data.courseId = courseId;
          console.log("✅ CourseId set successfully:", data.courseId);
          $sweetalert.success("دوره با موفقیت ایجاد شد! حالا می‌توانید فصل‌ها و درس‌ها را اضافه کنید.");
          // رفتن به مرحله 3 برای افزودن فصل و درس
          currentStep.value = 3;
        } else {
          console.error("❌ CourseId not found in response:", response.data);
          $sweetalert.error("دوره ایجاد شد اما شناسه دوره یافت نشد. لطفاً صفحه را رفرش کنید.");
        }
      } else {
        $sweetalert.success("دوره با موفقیت ایجاد شد!");
        router.push("/account/courses");
      }
    })
    .catch((error) => {
      console.error("خطا در ایجاد دوره:", error);
      $sweetalert.error("خطایی در ایجاد دوره رخ داده است.");
    });
};


const currentStep = ref(1);

const nextStep = () => {
  if (currentStep.value < 3) currentStep.value++;
};

const finishCourse = () => {
  $sweetalert.success("دوره شما با موفقیت تکمیل شد!");
  router.push("/account/courses");
};

const prevStep = () => {
  if (currentStep.value > 1) currentStep.value--;
};


// اجرا در زمان لود شدن صفحه
onMounted(async () => {
  // Check organization status first
  await fetchOrganization();
  
  if (!canCreateCourse.value) {
    await $sweetalert.fire({
      title: 'دسترسی محدود',
      text: organizationStatusMessage.value || 'سازمان شما فعال نیست',
      icon: 'warning',
      confirmButtonText: 'متوجه شدم'
    });
    router.push('/account');
    return;
  }
  
  getCategories();
  getAttributes();
});

definePageMeta({
  layout: "account",
  middleware: ['auth']
});
</script>

<style scoped>
.step-item {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 180px;
  height: 50px;
  background: #e0e0e0;
  border-radius: 50px;
  font-weight: bold;
  position: relative;
  color: #555;
}

.step-item.active {
  background: #222; /* رنگ تیره برای مرحله فعال */
  color: #fff;
}

.step-line {
  width: 50px;
  height: 3px;
  background: #e0e0e0;
  margin: 0 10px;
}

.step-line.active {
  background: #222;
}

.step-item.active + .step-line {
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
