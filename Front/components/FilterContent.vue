<template>
    <div>
      <!-- جستجو -->
      <div class="mb-4">
        <div class="input-group">
          <span class="input-group-text bg-white cursor-pointer">
            <i class="icon icon-regular-search text-muted"></i>
          </span>
          <input 
            type="text" 
            class="form-control border-light" 
            placeholder="جستجو در نتایج" 
            v-model="filters.search" 
          />
        </div>
      </div>
  
      <!-- برگزارکننده دوره -->
      <div class="mb-4">
        <h6 class="fw-bold text-dark mb-3 d-flex align-items-center gap-2">
          <i class="icon icon-regular-building"></i> <span>برگزارکننده دوره</span>
        </h6>
        <div v-for="(organizer, index) in organizers" :key="index" class="form-check mb-2">
          <input 
            class="form-check-input" 
            type="checkbox" 
            :id="'organizer' + index" 
            v-model="filters.selectedOrganizers" 
            :value="organizer" 
          />
          <label class="form-check-label text-muted" :for="'organizer' + index">{{ organizer }}</label>
        </div>
      </div>
  
      <!-- بازه قیمتی -->
      <div class="price-filter">
        <h6 class="fw-bold mb-4 d-flex align-items-center gap-2">
          <i class="icon icon-regular-dollar-circle"></i>
          <span>بازه قیمتی:</span>
        </h6>
        <div class="row my-4">
          <div class="col-6">
            <label class="form-label text-muted small">حداقل قیمت</label>
            <input type="number" class="form-control text-end py-2" v-model="filters.minPrice" />
          </div>
          <div class="col-6">
            <label class="form-label text-muted small">حداکثر قیمت</label>
            <input type="number" class="form-control text-end py-2" v-model="filters.maxPrice" />
          </div>
        </div>
      </div>
  
      <!-- انتخاب زبان -->
      <div>
        <h6 class="fw-bold text-dark mb-3 d-flex align-items-center gap-2">
          <i class="icon icon-regular-globe"></i><span> انتخاب زبان</span>
        </h6>
        <div v-for="(language, index) in languages" :key="index" class="form-check mb-2">
          <input 
            class="form-check-input" 
            type="checkbox" 
            :id="'lang' + index" 
            v-model="filters.selectedLanguages" 
            :value="language" 
          />
          <label class="form-check-label text-muted" :for="'lang' + index">{{ language }}</label>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  defineProps(["filters"]); // دریافت داده‌ها از کامپوننت والد
  
  const organizers = ["های وب", "دیجی کالا", "دیجی پی"];
  const languages = ["انگلیسی", "ترکی", "فارسی", "آلمانی"];
  </script>
  