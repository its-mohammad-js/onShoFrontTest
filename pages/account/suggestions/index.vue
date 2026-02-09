<template>
    <div class="container py-5">
      <h5 class="mb-4">پیشنهادات شغلی براساس دوره‌ای که گذرانده‌اید:</h5>
      <div class="row g-3">
        <div
          class="col-lg-6 col-md-6"
          v-for="(job, index) in jobOffers"
          :key="index"
        >
          <div class="card border-0 shadow-sm rounded">
            <div class="bg-dark-subtle p-2 rounded-top position-relative h-60-px">
              <img
                :src="getMediaUrl(job.companyLogo)"
                alt="Company Logo"
                class="rounded-circle border border-dark border-2 w-60-px h-60-px position-absolute top-50 right-10-px"
              />
            </div>
            <div class="card-body">
              <div class="row mt-4 text-end">
                <div class="col-md-6 mb-3">
                  <h5 class="card-title">{{ job.title }}</h5>
                </div>
                <div class="col-md-6 text-lg-start mb-3">
                  <button class="btn btn-danger" @click="viewCompany(job.companyPage)">
                    مشاهده صفحه
                  </button>
                </div>
              </div>
              <p class="text-muted mb-3">
                <i class="icon icon-regular-building text-danger1"></i> {{ job.companyName }}
              </p>
              <p class="text-muted mb-3">
                <i class="icon icon-regular-location-pin text-danger1"></i>{{ job.location }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  
  const { getMediaUrl } = useMediaUrl();

  const jobOffers = ref([
    {
      title: "استخدام برنامه نویس",
      companyName: "تپسی",
      location: "تهران، ایران",
      companyLogo: "https://via.placeholder.com/60",
      companyPage: "/company/tapsi",
    },
    {
      title: "استخدام برنامه نویس",
      companyName: "اسنپ",
      location: "تهران، ایران",
      companyLogo: "https://via.placeholder.com/60",
      companyPage: "/company/snapp",
    },
    {
      title: "استخدام برنامه نویس",
      companyName: "دیجی کالا",
      location: "تهران، ایران",
      companyLogo: "https://via.placeholder.com/60",
      companyPage: "/company/digikala",
    },
  ]);
  
 
  const viewCompany = (companyPage) => {

    window.location.href = companyPage;
  };
  definePageMeta({
  layout: "account",
  middleware: ['auth']
});
  </script>
  
  <style scoped>
  .h-60-px {
    height: 60px;
  }
  .w-60-px {
    width: 60px;
  }
  .right-10-px {
    right: 10px;
  }
  
  .bg-dark-subtle {
  background-color: rgba(43, 45, 66, 1) !important;
}
  </style>
  