<template>
    <div>
        <div class="row my-4">
          <div class="col-md-12 mb-3">
            <label for="photo" class="form-label">انتخاب عکس:</label>
            <template v-if="previewImage">
              <div class="position-relative w-200-px h-150-px">
                <img
                  :src="previewImage"
                  alt="پیش نمایش عکس"
                  class="img-thumbnail w-200-px h-150-px border-dashed border-dark"
                />
                <button
                  type="button"
                  class="btn btn-danger remove-btn"
                  @click="removePhoto"
                >
                  <i class="icon icon-regular-times font-size-14 mt-1"></i>
                </button>
              </div>
            </template>
            <template v-else>
              <div
                class="photo-box d-flex align-items-center justify-content-center"
                @click="triggerFileInput"
              >
                <i class="icon icon-regular-plus fs-1"></i>
              </div>
              <input
                id="photo"
                type="file"
                class="d-none"
                @change="handleFileUpload"
              />
            </template>
          </div>
        </div>
        <div class="row my-4">
          <div class="col-md-12 mb-3">
            <label for="courseName" class="form-label">نام دوره آموزشی:</label>
            <input
              type="text"
              id="courseName"
              v-model="data.title"
              class="form-control py-3 shadow-none"
              placeholder="عنوان دوره را وارد کنید"
            />
          </div>
        </div>
        <div class="row my-4">
          <div class="col-md-12 mb-3">
            <label for="courseDescription" class="form-label">توضیحات دوره آموزشی:</label>
            <textarea
              id="courseDescription"
              v-model="data.description"
              class="form-control py-3 shadow-none"
              rows="5"
              placeholder="توضیحات دوره را وارد کنید"
            ></textarea>
          </div>
          <div class="col-md-12 mb-3">
            <label for="courseExcerpt" class="form-label">دید کلی دوره:</label>
            <textarea
              id="courseExcerpt"
              v-model="data.excerpt"
              class="form-control py-3 shadow-none"
              rows="5"
              placeholder="دید کلی دوره را وارد کنید"
            ></textarea>
          </div>
        </div>
      <div class="row my-4">
        <div class="col-md-12 mb-3">
          <label for="iscoCode" class="form-label">کد اسیکو (اختیاری):</label>
          <input
            type="text"
            id="iscoCode"
            v-model="iscoCode"
            @blur="searchByIscoCode"
            class="form-control py-3 shadow-none"
            placeholder="کد اسیکو را وارد کنید"
          />
          <small class="form-text text-muted">
            با وارد کردن کد اسیکو، دسته‌بندی و عنوان دوره به صورت خودکار پیشنهاد می‌شود
          </small>
        </div>
      </div>
      <div class="row my-4">
        <div class="col-md-4 mb-3">
          <label for="categoryLevel1" class="form-label">خوشه:</label>
          <select
            id="categoryLevel1"
            v-model="selectedCategoryLevel1"
            @change="onCategoryLevel1Change"
            class="form-control py-3 shadow-none"
          >
            <option value="">انتخاب خوشه</option>
            <option
              v-for="category in level1Categories"
              :key="category.id"
              :value="category.id"
            >
              {{ category.title }}
            </option>
          </select>
        </div>
        <div class="col-md-4 mb-3">
          <label for="categoryLevel2" class="form-label">گروه:</label>
          <select
            id="categoryLevel2"
            v-model="selectedCategoryLevel2"
            @change="onCategoryLevel2Change"
            class="form-control py-3 shadow-none"
            :disabled="!selectedCategoryLevel1"
          >
            <option value="">انتخاب گروه</option>
            <option
              v-for="category in level2Categories"
              :key="category.id"
              :value="category.id"
            >
              {{ category.title }}
            </option>
          </select>
        </div>
        <div class="col-md-4 mb-3">
          <label for="categoryLevel3" class="form-label">دسته‌بندی:</label>
          <select
            id="categoryLevel3"
            v-model="selectedCategoryLevel3"
            @change="onCategoryLevel3Change"
            class="form-control py-3 shadow-none"
            :disabled="!selectedCategoryLevel2"
          >
            <option value="">انتخاب دسته‌بندی</option>
            <option
              v-for="category in level3Categories"
              :key="category.id"
              :value="category.id"
            >
              {{ category.title }}
            </option>
          </select>
        </div>
      </div>
      </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";
import {useAuthStore} from "~/stores/auth";
  
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
const iscoCode = ref('');
const suggestions = ref([]);
const loadingSuggestions = ref(false);

// Category selection states
const selectedCategoryLevel1 = ref('');
const selectedCategoryLevel2 = ref('');
const selectedCategoryLevel3 = ref('');
const level1Categories = ref([]);
const level2Categories = ref([]);
const level3Categories = ref([]);
const allCategories = ref([]);

const previewImage = ref(null);
const { $api, $sweetalert } = useNuxtApp(); 

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    data.value.photo = file; 
    previewImage.value = URL.createObjectURL(file);
  }
};

if(data.value.photo !== '') {
  previewImage.value = data.value.photo;
}


const removePhoto = () => {
  data.value.photo = null; 
  previewImage.value = null;
};

const triggerFileInput = () => {
  document.getElementById("photo").click();
};

// Search by ISCO code using API
const searchByIscoCode = async () => {
  if (!iscoCode.value || !iscoCode.value.trim()) {
    return;
  }

  const code = iscoCode.value.trim();
  loadingSuggestions.value = true;
  suggestions.value = [];

  try {
    const response = await $api.post('/course/category/by-isco-code', {
      isco_code: code
    }, {
      headers: {
        Authorization: "Bearer " + useCookie("token").value,
      },
    });

    // Extract suggestions from response
    // Response structure: { status: true, data: { categories: [{ category: {...}, courses: [] }] } }
    const responseData = response?.data?.data ?? response?.data;
    let suggestionsArray = [];
    
    // Handle different response structures
    if (responseData?.categories && Array.isArray(responseData.categories)) {
      // New API structure: categories array with category object inside
      suggestionsArray = responseData.categories.map(item => item.category || item);
    } else if (Array.isArray(responseData)) {
      suggestionsArray = responseData;
    } else if (responseData?.suggestions && Array.isArray(responseData.suggestions)) {
      suggestionsArray = responseData.suggestions;
    } else if (responseData?.category) {
      // Single category response
      suggestionsArray = [responseData.category];
    }
    
    if (!suggestionsArray || suggestionsArray.length === 0) {
      $sweetalert.fire({
        title: 'پیشنهادی یافت نشد',
        text: 'کد اسیکو وارد شده یافت نشد',
        icon: 'warning',
        confirmButtonText: 'متوجه شدم'
      });
      return;
    }

    // Store suggestions
    suggestions.value = suggestionsArray;

    // If only one suggestion, apply it directly
    if (suggestionsArray.length === 1) {
      applySuggestion(suggestionsArray[0]);
      return;
    }

    // If multiple suggestions, show modal to user
    await showSuggestionsModal();
  } catch (error) {
    console.error('Error fetching suggestions:', error);
    $sweetalert.fire({
      title: 'خطا',
      text: error.response?.data?.message || 'خطایی در دریافت پیشنهادات رخ داد',
      icon: 'error',
      confirmButtonText: 'باشه'
    });
  } finally {
    loadingSuggestions.value = false;
  }
};

// Show suggestions modal
const showSuggestionsModal = async () => {
  if (suggestions.value.length === 0) return;

  // If only one suggestion, apply it directly
  if (suggestions.value.length === 1) {
    const suggestion = suggestions.value[0];
    const categoryTitle = suggestion.title || suggestion.name || suggestion.category_title || suggestion.suggested_category_title || '-';
    
    const result = await $sweetalert.fire({
      title: 'دسته‌بندی یافت شد',
      html: `
        <div class="text-right">
          <p><strong>دسته‌بندی:</strong> ${categoryTitle}</p>
          <p>آیا می‌خواهید این دسته‌بندی اعمال شود؟</p>
        </div>
      `,
      icon: 'question',
      showCancelButton: true,
      confirmButtonText: 'بله، اعمال کن',
      cancelButtonText: 'خیر',
      confirmButtonColor: '#dc3545',
      cancelButtonColor: '#6c757d'
    });

    if (result.isConfirmed) {
      applySuggestion(suggestion);
    }
    return;
  }

  // Multiple suggestions - show list
  let suggestionsHtml = '<div class="text-right" style="max-height: 400px; overflow-y: auto;">';
  
  suggestions.value.forEach((suggestion, index) => {
    const categoryTitle = suggestion.title || suggestion.name || suggestion.category_title || suggestion.suggested_category_title || '-';
    suggestionsHtml += `
      <div style="border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 5px; cursor: pointer; transition: background-color 0.2s;" 
           class="suggestion-item" 
           data-suggestion-index="${index}">
        <p style="margin: 0;"><strong>دسته‌بندی:</strong> ${categoryTitle}</p>
        <p style="margin: 5px 0; color: #dc3545; font-size: 12px;">برای انتخاب این دسته‌بندی کلیک کنید</p>
      </div>
    `;
  });
  
  suggestionsHtml += '</div>';

  const result = await $sweetalert.fire({
    title: 'پیشنهادات یافت شده',
    html: suggestionsHtml,
    icon: 'info',
    showCancelButton: true,
    confirmButtonText: 'انصراف',
    cancelButtonText: 'انصراف',
    confirmButtonColor: '#6c757d',
    cancelButtonColor: '#6c757d',
    showConfirmButton: false,
    didOpen: () => {
      // Add click handlers and hover effects
      document.querySelectorAll('.suggestion-item').forEach((item) => {
        const index = parseInt(item.getAttribute('data-suggestion-index'));
        
        // Hover effects
        item.addEventListener('mouseenter', () => {
          item.style.backgroundColor = '#f0f0f0';
        });
        item.addEventListener('mouseleave', () => {
          item.style.backgroundColor = 'white';
        });
        
        // Click handler
        item.addEventListener('click', () => {
          if (suggestions.value[index]) {
            applySuggestion(suggestions.value[index]);
            // Close modal
            const swal = document.querySelector('.swal2-container');
            if (swal) {
              const cancelButton = swal.querySelector('.swal2-cancel');
              if (cancelButton) cancelButton.click();
            }
          }
        });
      });
    }
  });
};

// Find category in hierarchy recursively
const findCategoryInHierarchy = (categories, targetId) => {
  for (const cat of categories) {
    if (cat.id == targetId) {
      return { category: cat, level: 1, parent1: null, parent2: null };
    }
    if (cat.children && Array.isArray(cat.children)) {
      for (const child of cat.children) {
        if (child.id == targetId) {
          return { category: child, level: 2, parent1: cat, parent2: null };
        }
        if (child.children && Array.isArray(child.children)) {
          for (const grandchild of child.children) {
            if (grandchild.id == targetId) {
              return { category: grandchild, level: 3, parent1: cat, parent2: child };
            }
          }
        }
      }
    }
  }
  return null;
};

// Find parent categories recursively
const findParentPath = (categories, targetId, path = []) => {
  for (const cat of categories) {
    if (cat.id == targetId) {
      return [...path, cat];
    }
    if (cat.children && Array.isArray(cat.children)) {
      const newPath = findParentPath(cat.children, targetId, [...path, cat]);
      if (newPath) return newPath;
    }
  }
  return null;
};

// Apply selected suggestion
const applySuggestion = async (suggestion) => {
  if (!suggestion) return;

  // Store isco_code in data
  data.value.isco_code = iscoCode.value.trim();

  // Get category from suggestion (handle both direct category object and nested structure)
  const category = suggestion.category || suggestion;
  
  // Get category ID
  let categoryId = category.id || suggestion.id || suggestion.category_id;
  
  if (!categoryId) {
    console.error('Category ID not found in suggestion:', suggestion);
    return;
  }

  // Wait for categories to be loaded if not already
  if (allCategories.value.length === 0) {
    await loadCategories();
  }

  if (allCategories.value.length > 0) {
    // Find the category in hierarchy to get its full path
    const found = findCategoryInHierarchy(allCategories.value, categoryId);
    
    if (found) {
      // Always set the found category in level 3 (last level)
      // And set its parents in levels 1 and 2
      if (found.level === 3) {
        // Category is at level 3, set it and its parents
        selectedCategoryLevel1.value = found.parent1.id;
        onCategoryLevel1Change();
        selectedCategoryLevel2.value = found.parent2.id;
        onCategoryLevel2Change();
        selectedCategoryLevel3.value = found.category.id;
        onCategoryLevel3Change();
      } else if (found.level === 2) {
        // Category is at level 2, set parent at level 1, category at level 2, and category at level 3
        selectedCategoryLevel1.value = found.parent1.id;
        onCategoryLevel1Change();
        selectedCategoryLevel2.value = found.category.id;
        onCategoryLevel2Change();
        selectedCategoryLevel3.value = found.category.id;
        onCategoryLevel3Change();
      } else if (found.level === 1) {
        // Category is at level 1, we need to find its children to set level 2 and 3
        selectedCategoryLevel1.value = found.category.id;
        onCategoryLevel1Change();
        if (found.category.children && found.category.children.length > 0) {
          const firstChild = found.category.children[0];
          selectedCategoryLevel2.value = firstChild.id;
          onCategoryLevel2Change();
          if (firstChild.children && firstChild.children.length > 0) {
            // Set first grandchild at level 3
            selectedCategoryLevel3.value = firstChild.children[0].id;
            onCategoryLevel3Change();
          } else {
            // No grandchildren, set child at level 3
            selectedCategoryLevel3.value = firstChild.id;
            onCategoryLevel3Change();
          }
        } else {
          // No children, can't set at level 3, set at level 1 only
          data.value.category = found.category.id;
        }
      }
    } else {
      // Category not found in hierarchy, try to use parent from API response
      if (category.parent) {
        // Find parent in hierarchy
        const parentFound = findCategoryInHierarchy(allCategories.value, category.parent);
        if (parentFound) {
          // Set parent at appropriate level and category at level 3
          if (parentFound.level === 1) {
            // Parent is at level 1, set it at level 1, category at level 2 and 3
            selectedCategoryLevel1.value = parentFound.category.id;
            onCategoryLevel1Change();
            selectedCategoryLevel2.value = categoryId;
            onCategoryLevel2Change();
            selectedCategoryLevel3.value = categoryId;
            onCategoryLevel3Change();
          } else if (parentFound.level === 2) {
            // Parent is at level 2, set grandparent at level 1, parent at level 2, category at level 3
            selectedCategoryLevel1.value = parentFound.parent1.id;
            onCategoryLevel1Change();
            selectedCategoryLevel2.value = parentFound.category.id;
            onCategoryLevel2Change();
            selectedCategoryLevel3.value = categoryId;
            onCategoryLevel3Change();
          } else if (parentFound.level === 3) {
            // Parent is at level 3, set grandparent at level 1, parent's parent at level 2, category at level 3
            selectedCategoryLevel1.value = parentFound.parent1.id;
            onCategoryLevel1Change();
            selectedCategoryLevel2.value = parentFound.parent2.id;
            onCategoryLevel2Change();
            selectedCategoryLevel3.value = categoryId;
            onCategoryLevel3Change();
          }
        } else {
          // Parent not found in hierarchy, try to find it by searching all categories
          const findCategoryById = (categories, id) => {
            for (const cat of categories) {
              if (cat.id == id) return cat;
              if (cat.children) {
                const found = findCategoryById(cat.children, id);
                if (found) return found;
              }
            }
            return null;
          };
          
          const parentCat = findCategoryById(allCategories.value, category.parent);
          if (parentCat) {
            // Found parent, now find its parent
            const grandparentFound = findCategoryInHierarchy(allCategories.value, category.parent);
            if (grandparentFound && grandparentFound.parent1) {
              selectedCategoryLevel1.value = grandparentFound.parent1.id;
              onCategoryLevel1Change();
              selectedCategoryLevel2.value = category.parent;
              onCategoryLevel2Change();
              selectedCategoryLevel3.value = categoryId;
              onCategoryLevel3Change();
            } else {
              // No grandparent, set parent at level 1
              selectedCategoryLevel1.value = category.parent;
              onCategoryLevel1Change();
              selectedCategoryLevel2.value = categoryId;
              onCategoryLevel2Change();
              selectedCategoryLevel3.value = categoryId;
              onCategoryLevel3Change();
            }
          } else {
            // Parent not found, set directly
            data.value.category = categoryId;
          }
        }
      } else {
        // No parent info, set directly
        data.value.category = categoryId;
      }
    }
  } else {
    // Categories not loaded, set directly
    data.value.category = categoryId;
  }

  $sweetalert.fire({
    title: 'موفق',
    text: 'دسته‌بندی با موفقیت اعمال شد',
    icon: 'success',
    confirmButtonText: 'باشه'
  });
};

watch(data, (newValue) => {
  emit("update:modelValue", newValue);
});

// Load categories from API
const loadCategories = async () => {
  try {
    const response = await $api.post('/course/category/list', {}, {
      headers: {
        Authorization: "Bearer " + useCookie("token").value,
      },
    });

    // Handle different response structures
    let categoriesArray = [];
    if (response.data?.status && response.data?.data) {
      categoriesArray = response.data.data;
    } else if (response.data?.data && Array.isArray(response.data.data)) {
      categoriesArray = response.data.data;
    } else if (Array.isArray(response.data)) {
      categoriesArray = response.data;
    }

    allCategories.value = categoriesArray;
    
    // Level 1 categories are parent categories (top level categories with children)
    level1Categories.value = categoriesArray.filter(cat => {
      // Parent categories are those that have children
      return cat.children && Array.isArray(cat.children) && cat.children.length > 0;
    });
  } catch (error) {
    console.error('Error loading categories:', error);
    $sweetalert.fire({
      title: 'خطا',
      text: 'خطایی در دریافت دسته‌بندی‌ها رخ داد',
      icon: 'error',
      confirmButtonText: 'باشه'
    });
  }
};

// Handle level 1 category change (خوشه)
const onCategoryLevel1Change = () => {
  // Reset level 2 and 3
  selectedCategoryLevel2.value = '';
  selectedCategoryLevel3.value = '';
  data.value.category = '';
  level2Categories.value = [];
  level3Categories.value = [];

  if (!selectedCategoryLevel1.value) return;

  // Find selected level 1 category from allCategories
  const level1Cat = allCategories.value.find(cat => cat.id == selectedCategoryLevel1.value);
  if (level1Cat && level1Cat.children && Array.isArray(level1Cat.children)) {
    level2Categories.value = level1Cat.children;
  } else {
    // If no children, this might be a leaf category, set it directly
    data.value.category = selectedCategoryLevel1.value;
  }
};

// Handle level 2 category change
const onCategoryLevel2Change = () => {
  // Reset level 3
  selectedCategoryLevel3.value = '';
  data.value.category = '';
  level3Categories.value = [];

  if (!selectedCategoryLevel2.value) return;

  // Find selected level 2 category
  const level2Cat = level2Categories.value.find(cat => cat.id == selectedCategoryLevel2.value);
  if (level2Cat && level2Cat.children && Array.isArray(level2Cat.children) && level2Cat.children.length > 0) {
    level3Categories.value = level2Cat.children;
  } else {
    // If no children, this is the final category
    data.value.category = selectedCategoryLevel2.value;
  }
};

// Handle level 3 category change
const onCategoryLevel3Change = () => {
  if (selectedCategoryLevel3.value) {
    data.value.category = selectedCategoryLevel3.value;
  }
};

onMounted(() => {
  // Load categories from API
  loadCategories();
});
</script>

<style scoped>
.img-thumbnail {
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  position: relative;
}
.photo-box {
  width: 200px;
  height: 150px;
  border: 2px dashed rgba(220, 53, 69, 0.8);
  border-radius: 8px;
  cursor: pointer;
  color: rgba(220, 53, 69, 0.8);
  transition: background-color 0.3s, color 0.3s;
}

.photo-box:hover {
  background-color: #f8f9fa;
  color: rgba(220, 53, 69, 0.8);
}

.photo-box-plus {
  font-size: 24px;
  font-weight: bold;
}

/* دکمه حذف عکس */
.remove-btn {
  position: absolute;
  top: 10px;
  left: 10px;
  background-color: rgba(220, 53, 69, 0.8);
  border: none;
  border-radius: 50%;
  color: #fff;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  cursor: pointer;
}

.remove-btn:hover {
  background-color: rgba(220, 53, 69, 1);
}
</style>
