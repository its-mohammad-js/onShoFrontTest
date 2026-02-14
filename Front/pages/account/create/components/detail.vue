<template>
  <div>
    <div class="row p-3 bg-white rounded-4">
      <div class="col-md-12 my-4">
        <div class="row justify-content-between align-items-center">
          <div class="col-12 col-md-3 mb-3 mb-md-0">
            <label for="duration" class="form-label"
              >مدت زمان دوره (ساعت) :</label
            >
          </div>
          <div class="col-12 col-md-6">
            <input
              type="text"
              id="duration"
              v-model="data.attributeValues.duration"
              class="form-control py-3 shadow-none"
              placeholder="مدت زمان به ساعت"
            />
          </div>
        </div>
      </div>
      <div class="col-md-12 my-4">
        <form-radio
  v-model="data.attributeValues.level"
  :data="data.attributes.find((item) => item.slug === 'level') || {}"
/>
      </div>
      <div class="col-md-12 my-4">
        <div class="row justify-content-between align-items-center">
          <div class="col-12 col-md-3 mb-3 mb-md-0">
            <label for="type_value" class="form-label">نوع دوره:</label>
          </div>
          <div class="col-12 col-md-6">
            <select
              id="type_value"
              v-model="data.type_value"
              class="form-control py-3 shadow-none"
            >
              <option value="">انتخاب کنید</option>
              <option value="online">آنلاین</option>
              <option value="offline">آفلاین</option>
              <option value="in_person">حضوری</option>
            </select>
          </div>
        </div>
      </div>
    </div>
    <div class="row p-3 bg-white rounded-4 my-4">
      <div class="col-md-12 my-4">
        <div class="row justify-content-between align-items-center">
          <div class="col-12 col-md-3 mb-3 mb-md-0">
            <label for="price" class="form-label">قیمت دوره:</label>
          </div>
          <div class="col-12 col-md-6">
            <input
          type="number"
          id="price"
          v-model="data.price"
          class="form-control py-3 shadow-none"
          placeholder="قیمت به تومان"
        />
          </div>
        </div>
      </div>
      <div class="col-md-12 my-4">
        <div class="row justify-content-between align-items-center">
          <div class="col-12 col-md-3 mb-3 mb-md-0">
            <label for="discount" class="form-label">درصد تخفیف :</label>
          </div>
          <div class="col-12 col-md-6">
            <input
          type="number"
          id="discount"
          v-model="data.discount"
          class="form-control py-3 shadow-none"
          placeholder="درصد تخفیف"
        />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import { useAuthStore } from "~/stores/auth";

const auth = useAuthStore();
// تعریف props و emit
const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
  },
});
const emit = defineEmits(["update:modelValue"]);

// داده‌ها
const data = ref(props.modelValue);



// مدیریت دسته‌بندی‌ها
const selectedCategory = ref(""); // دسته‌بندی انتخاب‌شده
const currentCategories = ref([...data.value.categories]); // دسته‌بندی فعلی

const selectCategory = (category) => {
  selectedCategory.value = category; // ذخیره در متغیر local
  data.value.selectedCategory = category; // ذخیره در data و به‌روزرسانی modelValue
};

// مشاهده تغییرات در data
watch(data, (newValue) => {
  emit("update:modelValue", newValue);
});
</script>

