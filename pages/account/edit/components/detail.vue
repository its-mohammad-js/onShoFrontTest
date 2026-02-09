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
                v-model="duration"
                class="form-control py-3 shadow-none"
                placeholder="مدت زمان به ساعت"
              />
            </div>
          </div>
        </div>
        <div class="col-md-12 my-4">
          <form-radio
            v-model="data.attributeValues.level"
            :data="data.attributes.find((item) => item.slug === 'level')"
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
                v-model="typeValue"
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
            v-model="price"
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
            v-model="discount"
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
  import { ref, computed, watch, onMounted } from "vue";
  import { useAuthStore } from "~/stores/auth";
  
  const auth = useAuthStore();
  const props = defineProps({
    modelValue: {
      type: Object,
      required: true,
    },
  });
  const emit = defineEmits(["update:modelValue"]);
  
  // استفاده از computed برای دسترسی مستقیم به props.modelValue
  const data = computed({
    get: () => props.modelValue,
    set: (value) => emit("update:modelValue", value)
  });
  
  // ایجاد ref های جداگانه برای price و discount
  const price = computed({
    get: () => props.modelValue.price || "",
    set: (value) => {
      emit("update:modelValue", { ...props.modelValue, price: value });
    }
  });
  
  const discount = computed({
    get: () => props.modelValue.discount !== null && props.modelValue.discount !== undefined ? props.modelValue.discount : "",
    set: (value) => {
      emit("update:modelValue", { ...props.modelValue, discount: value });
    }
  });
  
  // ایجاد computed برای duration
  const duration = computed({
    get: () => props.modelValue.attributeValues?.duration || "",
    set: (value) => {
      const newAttributeValues = { ...props.modelValue.attributeValues, duration: value };
      emit("update:modelValue", { ...props.modelValue, attributeValues: newAttributeValues });
    }
  });

  // ایجاد computed برای type_value
  const typeValue = computed({
    get: () => props.modelValue.type_value || "",
    set: (value) => {
      emit("update:modelValue", { ...props.modelValue, type_value: value });
    }
  });
  
  const selectedCategory = ref(""); 
  const currentCategories = computed(() => [...(data.value.categories || [])]); 
  
  const selectCategory = (category) => {
    selectedCategory.value = category;
    emit("update:modelValue", { ...props.modelValue, selectedCategory: category });
  };
  
  // Watch for changes in attribute values
  watch(
    () => data.value.attributeValues,
    (newAttributeValues) => {
      emit("update:modelValue", { ...props.modelValue, attributeValues: newAttributeValues });
    },
    { deep: true }
  );
  
  // Watch for changes in category
  watch(
    () => data.value.category,
    (newCategory) => {
      emit("update:modelValue", { ...props.modelValue, category: newCategory });
    }
  );
  
  onMounted(() => {
    console.log("📝 Detail component mounted with data:", data.value);
    console.log("📝 Price:", price.value);
    console.log("📝 Discount:", discount.value);
    console.log("📝 Duration:", duration.value);
    console.log("📝 AttributeValues:", data.value.attributeValues);
  });
  </script>
  
  