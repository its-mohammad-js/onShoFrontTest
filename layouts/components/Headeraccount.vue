<template>
  <nav class="navbar navbar-expand-lg bg-light shadow-sm py-3 sticky-top">
    <div class="container">
      <!-- Toggle button for mobile -->
      <button
        class="navbar-toggler ms-auto"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="d-flex align-items-center d-md-none mt-3">
        <div class="position-relative">
          <button class="btn btn-light p-0 border-0">
            <i class="fa fa-bell fs-5"></i>
            <span
              class="position-absolute top-0 start-100 translate-middle p-1 bg-danger border border-light rounded-circle"
              style="width: 10px; height: 10px"
            ></span>
          </button>
        </div>
        <div class="dropdown position-relative ms-4">
          <button
            class="btn border-0 dropdown-toggle d-flex align-items-center"
            type="button"
            id="profileDropdown"
            data-bs-toggle="dropdown"
            aria-expanded="false"
          >
            <img
              src="/images/user.png"
              alt="Profile"
              class="rounded-circle ms-2"
              style="width: 40px; height: 40px; object-fit: cover"
            />
          </button>
          <ul class="dropdown-menu dropdown-center" aria-labelledby="profileDropdown">
            <li class="text-center">
              <nuxt-link to="/account/profile" class="dropdown-item">پروفایل</nuxt-link>
            </li>
            <li class="text-center">
              <nuxt-link to="/account/password" class="dropdown-item">تغییر رمز عبور</nuxt-link>
            </li>
            <li class="text-center">
              <a href="javascript:;" @click="logout" class="dropdown-item">خروج</a>
            </li>
          </ul>
        </div>
      </div>

      <!-- Navbar links and Logo -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <!-- Logo (Visible only in Mobile Menu) -->
        <div class="d-flex justify-content-center">
          <nuxt-link to="/" class="navbar-brand d-flex align-items-center" href="#">
            <img src="/images/logo-fani.png" alt="فنی و حرفه ای" style="width: 70px; height: auto; object-fit: contain;" />
          </nuxt-link>
        </div>

        <!-- Navbar links (Center in Desktop, Full-width in Mobile) -->
        <ul class="navbar-nav mx-auto gap-4">
          <li class="nav-item">
            <nuxt-link class="nav-link" to="/courses">دوره‌ها</nuxt-link>
          </li>
          <li class="nav-item">
            <nuxt-link class="nav-link" to="/">دانشجویان</nuxt-link>
          </li>
          <li class="nav-item">
            <nuxt-link class="nav-link" to="/events">رویدادها</nuxt-link>
          </li>
          <li class="nav-item">
            <nuxt-link class="nav-link" to="/about">درباره ما</nuxt-link>
          </li>
        </ul>
      </div>

      <div class="d-flex align-items-center gap-3 ms-lg-3 d-none d-md-flex">
        <div class="position-relative">
          <button class="btn btn-light p-0 border-0">
            <i class="fa fa-bell fs-5"></i>
            <span
              class="position-absolute top-0 start-100 translate-middle p-1 bg-danger border border-light rounded-circle"
              style="width: 10px; height: 10px"
            ></span>
          </button>
        </div>
        <div class="dropdown position-relative">
          <button
            class="btn border-0 dropdown-toggle d-flex align-items-center"
            type="button"
            id="profileDropdown"
            data-bs-toggle="dropdown"
            aria-expanded="false"
          >
            <img
              src="/images/user.png"
              alt="Profile"
              class="rounded-circle ms-2"
              style="width: 40px; height: 40px; object-fit: cover"
            />
          </button>
          <ul class="dropdown-menu dropdown-center" aria-labelledby="profileDropdown">
            <li class="text-center">
              <nuxt-link to="/account/profile" class="dropdown-item">پروفایل</nuxt-link>
            </li>
            <li class="text-center">
              <nuxt-link to="/account/password" class="dropdown-item">تغییر رمز عبور</nuxt-link>
            </li>
            <li class="text-center">
              <a href="javascript:;" @click="logout" class="dropdown-item">خروج</a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from "~/stores/auth";
const auth = useAuthStore();
const logout = () => {
  auth.logout();
};
</script>

<style scoped>
.navbar {
  direction: rtl;
}

.nav-link {
  font-size: 16px !important;
  color: #222b29 !important;
  transition: color 0.3s;
}

.nav-link:hover {
  color: #FF8C14;
}

.navbar-toggler-icon {
  background-image: url("data:image/svg+xml;charset=utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%23333' viewBox='0 0 30 30'%3E%3Cpath stroke='rgba%2833, 37, 41, 1%29' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3E%3C/svg%3E");
}

.navbar-toggler {
  border: none;
}

.dropdown-menu {
  left: 50% !important;
  transform: translateX(-50%) !important;
}

@media (max-width: 991.98px) {
  .navbar-brand {
    display: none;
  }

  .d-flex {
    margin-bottom: 10px;
    justify-content: center;
  }

  .navbar-collapse {
    text-align: center;
  }

  .navbar-nav {
    flex-direction: column;
    gap: 15px;
  }
}
</style>
