<template>
  <footer class="bg-dark text-white py-5">
    <div class="container">
      <div class="row align-items-center">
        <div class="col-md-4 text-center text-md-start order-2 order-md-1">
          <div class="mb-3">
            <div class="d-flex align-items-center justify-content-center justify-content-md-start gap-2">
              <i class="icon icon-regular-phone mt-1"></i>
              <span>09012568188</span>
            </div>
          </div>
          <div>
            <div class="d-flex align-items-center justify-content-center justify-content-md-start gap-2">
              <i class="icon icon-regular-location-pin mt-1"></i>

              <span>تهران، جردن، محل نمایشگاه بین المللی</span>
            </div>
          </div>
        </div>
        <div class="col-md-4 text-center order-1 order-md-2">
          <div class="flex-column d-flex justify-content-center align-items-center gap-2">
            <img src="/images/logo-fani.png" class="logo-size" alt="فنی و حرفه ای" style="object-fit: contain; width: 70px; height: auto;" />
            <p>کانون انجمن‌های صنفی کارفرمایی آموزشگاه‌های آزاد فنی‌و‌حرفه‌ای کشور</p>
          </div>
          <p class="small my-4">
            لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ، و با استفاده از طراحان گرافیک است.
          </p>
          <ul class="list-inline">
            <li class="list-inline-item">
              <nuxt-link to="/cources" class="text-white text-decoration-none">دوره‌ها</nuxt-link>
            </li>
            <li class="list-inline-item mx-3">
              <nuxt-link to="/" class="text-white text-decoration-none">دانشجویان</nuxt-link>
            </li>
            <li class="list-inline-item">
              <nuxt-link to="/events" class="text-white text-decoration-none">رویدادها</nuxt-link>
            </li>
            <li class="list-inline-item mx-3">
              <nuxt-link to="/about" class="text-white text-decoration-none">درباره ما</nuxt-link>
            </li>
          </ul>
        </div>
        <div class="col-md-4 text-center text-md-start mb-4 mb-md-0 order-3 order-md-3">
          <img src="/images/enamad.png" alt="لوگو" class="me-2" />
          <img src="/images/enamad.png" alt="لوگو" />
        </div>
      </div>
      <div class="row border-top border-light pt-3 mt-3">
        <div class="col text-center">
          <p class="mb-0">طراحی و توسعه توسط دلتا ماهورس</p>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.logo-size {
  width: 50px;
}
.bg-dark {
  background-color: #2b2d42 !important;
}
</style>
