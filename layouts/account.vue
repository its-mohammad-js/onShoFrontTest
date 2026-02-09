<template>
  <div>
    <Headeraccount />
    <main class="main pages bg-white">
    <div class="page-content">
      <div class="container">
        <div class="row">
          <div class="col-lg-12 mx-auto">
            <div class="d-lg-none text-end mt-3  d-flex align-items-center justify-content-center position-sticky sticky-top bg-danger rounded-pill" style="top: 120px;">
  <button class="btn bg-danger px-4 py-2 rounded-pill shadow-sm d-flex align-items-center gap-2"
          @click="showOffcanvas = true">
    <i class="fas fa-user-circle fs-5"></i>
    <span class="fw-bold">منوی حساب کاربری</span>
  </button>
</div>

<div 
  class="col-lg-3 bg-light rounded p-lg-4 p-md-3 mb-3 offcanvas offcanvas-top" 
  :class="{ 'show': showOffcanvas }"
  tabindex="-1"
  @click.self="showOffcanvas = false"
>
  <!-- دکمه بستن در سمت چپ -->
  <div class="offcanvas-header d-lg-none d-flex justify-content-between align-items-center border-bottom p-3">
    <h5 class="fw-bold mb-0">منو</h5>
    <button class="btn btn-light rounded-circle border-0 fs-5 d-flex align-items-center justify-content-center"
            @click="showOffcanvas = false"
            style="width: 36px; height: 36px;">
      <i class="fas fa-times"></i>
    </button>
  </div>

  <!-- محتوای منو -->
  <div class="offcanvas-body">
    <div class="nav flex-column nav-pills">
      <nuxt-link class="nav-link" :class="{'active': route.path === '/account'}" to="/account">
        <i class="icon icon-filled-home fs-4"></i> داشبورد
      </nuxt-link>
      <h4 class="text-muted fs-6 mb-2 mt-4 me-2">
        <i class="icon icon-filled-layer-group fs-3 text-danger1"></i> دوره‌ها
      </h4>
      <nuxt-link class="nav-link" :class="{'active': route.path === '/account/courses'}" to="/account/courses" v-permission="'course_view'">
        دوره‌های من
      </nuxt-link>
      <nuxt-link class="nav-link" :class="{'active': route.path === '/account/tasks'}" to="/account/tasks" v-permission="'task_view'">
        تمرین‌های من
      </nuxt-link>
      <nuxt-link class="nav-link" :class="{'active': route.path === '/account/saved-courses'}" to="/account/saved-courses" v-permission="'course_view'">
        مورد علاقه‌ی من
      </nuxt-link>
      <nuxt-link 
        v-if="canCreateCourse"
        class="nav-link" 
        :class="{'active': route.path === '/account/create'}" 
        to="/account/create" 
        v-permission="'course_create'"
      >
        ساخت دوره
      </nuxt-link>
      <div 
        v-else-if="organizationStatusMessage" 
        class="nav-link text-muted disabled"
        :title="organizationStatusMessage"
      >
        <i class="icon icon-filled-exclamation-triangle me-2"></i>
        ساخت دوره (غیرفعال)
      </div>
      <h4 class="text-muted fs-6 mb-2 mt-4 me-2">
        <i class="icon icon-filled-comments fs-3 text-danger1"></i> بازخورد و بهبود
      </h4>
      <nuxt-link class="nav-link" :class="{'active': route.path === '/account/support'}" to="/account/support">
        سیستم پشتیبانی
      </nuxt-link>
      <nuxt-link class="nav-link" :class="{'active': route.path === '/account/feedback'}" to="/account/feedback">
        بازخورد
      </nuxt-link>
      <nuxt-link class="nav-link" :class="{'active': route.path === '/account/redeem-code'}" to="/account/redeem-code">
        <i class="icon icon-filled-ticket me-2"></i>
        استفاده از کد
      </nuxt-link>
      <nuxt-link class="nav-link" :class="{'active': route.path === '/account/organization'}" to="/account/organization" v-permission="'user_manage'">
        <i class="icon icon-filled-building me-2"></i>
        مدیریت سازمان
      </nuxt-link>
      <nuxt-link class="nav-link" :class="{'active': route.path === '/account/organization/purchase-courses'}" to="/account/organization/purchase-courses" v-permission="'user_manage'">
        <i class="icon icon-filled-shopping-cart me-2"></i>
        خرید دوره برای سازمان
      </nuxt-link>
      <nuxt-link class="nav-link" :class="{'active': route.path === '/account/organization/codes'}" to="/account/organization/codes" v-permission="'user_manage'">
        <i class="icon icon-filled-ticket me-2"></i>
        کدهای دسترسی
      </nuxt-link>
      <nuxt-link class="nav-link" :class="{'active': route.path === '/account/standards'}" to="/account/standards" v-permission="'standards_manage'">
        <i class="icon icon-filled-award me-2"></i>
        مدیریت استانداردها
      </nuxt-link>
      <a href="javascript:;" @click="logout" class="logout text-danger1 me-2">
        <i class="icon icon-filled-arrow-right-from-line fs-4"></i> خروج
      </a>
    </div>
  </div>
</div>


            <div class="row">
              <div class="col-lg-3 bg-light rounded p-lg-4 p-md-3 p-2 mb-3 d-none d-lg-block">
                <div
                  class="nav flex-column nav-pills"
                  role="tablist"
                  aria-orientation="vertical"
                  style="--bs-bg-opacity: 1"
                >
                  <!-- Navigation Items -->
                 
                  <nuxt-link
                    class="nav-link"
                    :class="{'active': route.path === '/account'}"
                    to="/account"
                  >
                  <i class="icon icon-filled-home fs-4"></i>
                  داشبورد
                  </nuxt-link>
                  <!-- <nuxt-link
                    class="nav-link"
                    :class="{'active': route.path === '/account/step-one'}"
                    to="/account/step-one"
                  >
                    چالش استعداد‌یابی
                  </nuxt-link> -->
                  <h4 class="text-muted fs-6 mb-2 mt-4 me-2">
                    <i class="icon icon-filled-layer-group fs-3 text-danger1"></i> دوره‌ها
                  </h4>
                  <nuxt-link
                    class="nav-link"
                    :class="{'active': route.path === '/account/courses'}"
                    to="/account/courses"
                     v-permission="'course_view'"
                   
                  >
                    دوره‌های من
                  </nuxt-link>
                  <nuxt-link
                    class="nav-link"
                    :class="{'active': route.path === '/account/tasks'}"
                    to="/account/tasks"
                    v-permission="'task_view'"
                  >
                    تمرین‌های من
                  </nuxt-link>
                  <nuxt-link
                    class="nav-link"
                    :class="{'active': route.path === '/account/saved-courses'}"
                    to="/account/saved-courses"
                     v-permission="'course_view'"
                    
                  >
                  مورد علاقه ی من
                  </nuxt-link>
                  <nuxt-link
                    v-if="canCreateCourse"
                    class="nav-link"
                    :class="{'active': route.path === '/account/create'}"
                    to="/account/create"
                    v-permission="'course_create'"
                  >
                  ایجاد دوره
                  </nuxt-link>
                  <div 
                    v-else-if="organizationStatusMessage" 
                    class="nav-link text-muted disabled"
                    :title="organizationStatusMessage"
                  >
                    <i class="icon icon-filled-exclamation-triangle me-2"></i>
                    ایجاد دوره (غیرفعال)
                  </div>
                  <nuxt-link
                    v-if="canCreateTask"
                    class="nav-link"
                    :class="{'active': route.path === '/account/create_task'}"
                    to="/account/create_task"
                     v-permission="'task_create'"
                   
                  >
                    ایجاد تمرین
                  </nuxt-link>
                  <div 
                    v-else-if="organizationStatusMessage" 
                    class="nav-link text-muted disabled"
                    :title="organizationStatusMessage"
                  >
                    <i class="icon icon-filled-exclamation-triangle me-2"></i>
                    ایجاد تمرین (غیرفعال)
                  </div>
                  <!-- <nuxt-link
                    class="nav-link"
                    :class="{'active': route.path === '/account/list'}"
                    to="/account/list"
                  >
                   لیست دوره‌های مدرس
                  </nuxt-link> -->
                  <!-- <nuxt-link
                    class="nav-link"
                    :class="{'active': route.path === '/account/teacher-contact'}"
                    to="/account/teacher-contact"
                  >
                    ارتباط با مدرس
                  </nuxt-link> -->

                  <h4 class="text-muted fs-6 mb-2 mt-4 me-2" v-permission="'course_view'">
                    <i class="icon icon-filled-briefcase fs-3 text-danger1"></i> فرصت‌های شغلی
                  </h4>
                  <nuxt-link
                    class="nav-link disabled"
                    :class="{'active': route.path === '/account/suggestions'}"
                    to="/account/suggestions"
                    v-permission="'course_view'"
                  >
                   <span> پیشنهاد شغلی  </span><span class="text-danger1 fw-normal">(به زودی)</span>
                  </nuxt-link>
                  <!-- <nuxt-link
                    class="nav-link"
                    :class="{'active': route.path === '/account/job-publish'}"
                    to="/account/job-publish"
                  >
                    منتشر شغلی
                  </nuxt-link> -->

                  <!-- <h4 class="text-muted fs-6 mb-2 mt-4 me-2">
                    <i class="fas fa-file-alt text-danger1"></i> ارزیابی و گواهینامه
                  </h4>
                  <nuxt-link
                    class="nav-link"
                    :class="{'active': route.path === '/account/exam'}"
                    to="/account/exam"
                  >
                    آزمون نهایی
                  </nuxt-link>
                  <nuxt-link
                    class="nav-link"
                    :class="{'active': route.path === '/account/certificate'}"
                    to="/account/certificate"
                  >
                    صدور گواهینامه
                  </nuxt-link> -->

                  <h4 class="text-muted fs-6 mb-2 mt-4 me-2">
                    <i class="icon icon-filled-users fs-3 text-danger1"></i> رویدادها 
                  </h4>
                  <!-- <nuxt-link
                    class="nav-link"
                    :class="{'active': route.path === '/account/expert-groups'}"
                    to="/account/expert-groups"
                  >
                    گروه‌های تخصصی
                  </nuxt-link> -->
                  <nuxt-link
                    class="nav-link"
                    :class="{'active': route.path === '/account/saved-events'}"
                    to="/account/saved-events"
                    v-permission="'webinar_manage'"
                  >
                    رویدادهای مورد علاقه
                  </nuxt-link>

                  <h4 class="text-muted fs-6 mb-2 mt-4 me-2">
                    <i class="icon icon-filled-comments fs-3 text-danger1"></i> بازخورد و بهبود
                  </h4>
                  <!-- <nuxt-link
                    class="nav-link"
                    :class="{'active': route.path === '/account/support'}"
                    to="/account/support"
                  >
                    سیستم پشتیبانی
                  </nuxt-link> -->
                  <nuxt-link
                    class="nav-link"
                    :class="{'active': route.path === '/account/feedback'}"
                    to="/account/feedback"
                  >
                    بازخورد
                  </nuxt-link>
                  
                  <h4 class="text-muted fs-6 mb-2 mt-4 me-2">
                    <i class="icon icon-filled-ticket fs-3 text-danger1"></i> کدهای دسترسی
                  </h4>
                  <nuxt-link
                    class="nav-link"
                    :class="{'active': route.path === '/account/redeem-code'}"
                    to="/account/redeem-code"
                  >
                    <i class="icon icon-filled-ticket me-2"></i>
                    استفاده از کد
                  </nuxt-link>

                  <h4 class="text-muted fs-6 mb-2 mt-4 me-2" v-permission="'user_manage'">
                    <i class="icon icon-filled-users fs-3 text-danger1"></i> مدیریت سیستم
                  </h4>
                  <nuxt-link
                    class="nav-link"
                    :class="{'active': route.path === '/account/list'}"
                    to="/account/list"
                    v-permission="'user_manage'"
                  >
                    مدیریت کاربران
                  </nuxt-link>
                  <nuxt-link
                    class="nav-link"
                    :class="{'active': route.path === '/account/profile'}"
                    to="/account/profile"
                    v-permission="'user_manage'"
                  >
                    پروفایل کاربری
                  </nuxt-link>
                  <nuxt-link
                    class="nav-link"
                    :class="{'active': route.path === '/account/organization'}"
                    to="/account/organization"
                    v-permission="'user_manage'"
                  >
                    <i class="icon icon-filled-building me-2"></i>
                    مدیریت سازمان
                  </nuxt-link>
                  <nuxt-link
                    class="nav-link"
                    :class="{'active': route.path === '/account/organization/purchase-courses'}"
                    to="/account/organization/purchase-courses"
                    v-permission="'user_manage'"
                  >
                    <i class="icon icon-filled-shopping-cart me-2"></i>
                    خرید دوره برای سازمان
                  </nuxt-link>
                  <nuxt-link
                    class="nav-link"
                    :class="{'active': route.path === '/account/organization/codes'}"
                    to="/account/organization/codes"
                    v-permission="'user_manage'"
                  >
                    <i class="icon icon-filled-ticket me-2"></i>
                    کدهای دسترسی
                  </nuxt-link>
                  <nuxt-link
                    class="nav-link"
                    :class="{'active': route.path === '/account/standards'}"
                    to="/account/standards"
                    v-permission="'standards_manage'"
                  >
                    <i class="icon icon-filled-award me-2"></i>
                    مدیریت استانداردها
                  </nuxt-link>

                  <!-- <h4 class="text-muted fs-6 mb-2 mt-4 me-2">
                    <i class="icon icon-filled-wallet fs-3 text-danger1"></i> مالی
                  </h4>
                  <nuxt-link
                    class="nav-link"
                    :class="{'active': route.path === '/account/payments'}"
                    to="/account/payments"
                  >
                    پرداخت‌ها
                  </nuxt-link> -->
                  <a
                    href="javascript:;"
                    @click="logout"
                    class="logout text-danger1 me-2"
                  >
                  <i class="icon icon-filled-arrow-right-from-line fs-4"></i>  خروج 
                  </a>
                </div>
              </div>
              <div class="col-lg-9">
                <slot></slot>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
  <FirstFooter />
  <FooterSection />
  </div>
</template>

<script setup>
import { useAuthStore } from '~/stores/auth';
import Headeraccount from './components/Headeraccount.vue';
import FooterSection from './components/FooterSection.vue';
import FirstFooter from './components/FirstFooter.vue';
import { ref, watch, provide, onMounted } from "vue";
import { useRoute } from "vue-router";

const auth = useAuthStore();
const route = useRoute();
const showOffcanvas = ref(false);

// Organization status
const { canCreateCourse, canCreateTask, organizationStatusMessage, fetchOrganization } = useOrganization()

// Fetch organization status on mount
onMounted(() => {
  fetchOrganization()
})

// هنگام تغییر صفحه، Offcanvas را ببند
watch(() => route.fullPath, () => {
  showOffcanvas.value = false;
});

const logout = () => {
  auth.logout();
};

provide("showOffcanvas", showOffcanvas); // ارسال متغیر به فرزندها

</script>

<style scoped>
.container {
  margin-bottom: 100px;
}

.nav-pills .nav-link.active,
.nav-pills .show > .nav-link {
  background-color: rgba(251, 241, 242, 1) !important; /* Light background for active */
  color: rgba(193, 18, 31, 1) !important; /* Blue text for active state */
  font-weight: bold !important;
  border: none !important;
  border-right: 5px solid rgba(193, 18, 31, 1) !important;

}

.nav-pills .nav-link {
  color: #6c757d !important; /* Default text color */
  font-size: 16px !important;
  padding: 10px 15px !important;
  font-weight: normal !important;
  border-radius: 0.5rem !important;
  display: flex !important;
  align-items: center !important;
  justify-content: start !important;
}

.nav-pills .nav-link i {

  margin-left: 10px !important; /* Space between icon and text */
}

.nav-link:hover {
  background-color: #f8f9fa;
}

.logout {
  color:rgba(193, 18, 31, 1) !important;
  font-weight: bold !important;
}

.logout:hover {
  color: rgba(193, 18, 31, 1) !important;
}

.nav-pills {
  gap: 10px; /* Add spacing between items */
}

.text-white {
  font-size: 18px;
}
@media (max-width: 992px) {
  .offcanvas {
    width: 100% !important;
    height: 100vh !important;
    background: white !important;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    transition: transform 0.3s ease-in-out;
    transform: translateY(-100%);
    position: fixed;
    top: 0;
    left: 0;
    z-index: 1050;
  }

  .offcanvas.show {
    transform: translateY(0);
  }

  .offcanvas-header {
    padding: 10px;
    background: rgba(251, 241, 242, 1);
  }

  .btn-close {
    font-size: 20px;
    border: none;
    background: none;
    cursor: pointer;
  }

  .offcanvas-body {
    padding: 20px;
    overflow-y: auto;
    max-height: calc(100vh - 50px);
  }
}

</style>
