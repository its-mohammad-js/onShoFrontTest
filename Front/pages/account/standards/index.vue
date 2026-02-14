<template>
  <div class="standards-management">
    <div class="container-fluid">
      <div class="row">
        <div class="col-12">
          <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h4 class="mb-0">مدیریت استانداردها</h4>
              <button 
                class="btn btn-primary" 
                @click="showCreateModal = true"
                v-if="canCreateStandards"
              >
                <i class="fas fa-plus"></i> افزودن استاندارد جدید
              </button>
            </div>
            <div class="card-body">
              <!-- Filters -->
              <div class="row mb-4">
                <div class="col-md-3">
                  <input 
                    type="text" 
                    class="form-control" 
                    placeholder="جستجو در استانداردها..."
                    v-model="searchQuery"
                    @input="searchStandards"
                  >
                </div>
                <div class="col-md-2">
                  <select class="form-control" v-model="selectedCluster" @change="filterStandards">
                    <option value="">همه خوشه‌ها</option>
                    <option v-for="cluster in filterOptions.clusters" :key="cluster" :value="cluster">
                      {{ cluster }}
                    </option>
                  </select>
                </div>
                <div class="col-md-2">
                  <select class="form-control" v-model="selectedGroup" @change="filterStandards">
                    <option value="">همه گروه‌ها</option>
                    <option v-for="group in filterOptions.group_names" :key="group" :value="group">
                      {{ group }}
                    </option>
                  </select>
                </div>
                <div class="col-md-2">
                  <select class="form-control" v-model="selectedType" @change="filterStandards">
                    <option value="">همه انواع</option>
                    <option v-for="type in filterOptions.types" :key="type" :value="type">
                      {{ type }}
                    </option>
                  </select>
                </div>
                <div class="col-md-2">
                  <select class="form-control" v-model="viewMode" @change="changeViewMode">
                    <option value="list">نمایش لیستی</option>
                    <option value="tree">نمایش درختی</option>
                  </select>
                </div>
              </div>

              <!-- Loading -->
              <div v-if="loading" class="text-center">
                <div class="spinner-border" role="status">
                  <span class="sr-only">در حال بارگذاری...</span>
                </div>
              </div>

              <!-- Standards List -->
              <div v-else-if="viewMode === 'list'">
                <div class="table-responsive">
                  <table class="table table-striped">
                    <thead>
                      <tr>
                        <th>شماره</th>
                        <th>نام استاندارد</th>
                        <th>خوشه</th>
                        <th>گروه</th>
                        <th>نوع</th>
                        <th>سطح</th>
                        <th>تاریخ تدوین</th>
                        <th>عملیات</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="standard in filteredStandards" :key="standard.id">
                        <td>{{ standard.number || '-' }}</td>
                        <td>{{ standard.standard_name || '-' }}</td>
                        <td>{{ standard.cluster || '-' }}</td>
                        <td>{{ standard.group_name || '-' }}</td>
                        <td>{{ standard.type || '-' }}</td>
                        <td>{{ standard.level }}</td>
                        <td>{{ formatDate(standard.compilation_date) }}</td>
                        <td>
                          <button 
                            class="btn btn-sm btn-info me-1" 
                            @click="viewStandard(standard)"
                          >
                            <i class="fas fa-eye"></i>
                          </button>
                          <button 
                            class="btn btn-sm btn-warning me-1" 
                            @click="editStandard(standard)"
                            v-if="canCreateStandards"
                          >
                            <i class="fas fa-edit"></i>
                          </button>
                          <button 
                            class="btn btn-sm btn-danger" 
                            @click="deleteStandard(standard)"
                            v-if="canCreateStandards"
                          >
                            <i class="fas fa-trash"></i>
                          </button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <!-- Tree View -->
              <div v-else-if="viewMode === 'tree'">
                <div class="standards-tree">
                  <div v-for="standard in treeStandards" :key="standard.id" class="tree-item">
                    <div 
                      class="tree-node" 
                      :style="{ paddingLeft: (standard.level * 20) + 'px' }"
                    >
                      <i class="fas fa-folder me-2"></i>
                      <span class="fw-bold">{{ standard.standard_name || 'بدون نام' }}</span>
                      <span class="text-muted ms-2">({{ standard.number || 'بدون شماره' }})</span>
                      <div class="tree-actions ms-2">
                        <button 
                          class="btn btn-sm btn-info me-1" 
                          @click="viewStandard(standard)"
                        >
                          <i class="fas fa-eye"></i>
                        </button>
                        <button 
                          class="btn btn-sm btn-warning me-1" 
                          @click="editStandard(standard)"
                          v-if="canCreateStandards"
                        >
                          <i class="fas fa-edit"></i>
                        </button>
                        <button 
                          class="btn btn-sm btn-danger" 
                          @click="deleteStandard(standard)"
                          v-if="canCreateStandards"
                        >
                          <i class="fas fa-trash"></i>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Empty State -->
              <div v-if="!loading && filteredStandards.length === 0" class="text-center py-5">
                <i class="fas fa-clipboard-list fa-3x text-muted mb-3"></i>
                <h5 class="text-muted">هیچ استانداردی یافت نشد</h5>
                <p class="text-muted">برای شروع، استاندارد جدیدی اضافه کنید</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div class="modal fade" :class="{ show: showCreateModal || showEditModal }" :style="{ display: showCreateModal || showEditModal ? 'block' : 'none' }">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              {{ showEditModal ? 'ویرایش استاندارد' : 'افزودن استاندارد جدید' }}
            </h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <StandardsForm 
              :standard="editingStandard"
              :is-edit="showEditModal"
              @saved="onStandardSaved"
              @cancelled="closeModal"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- View Modal -->
    <div class="modal fade" :class="{ show: showViewModal }" :style="{ display: showViewModal ? 'block' : 'none' }">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">جزئیات استاندارد</h5>
            <button type="button" class="btn-close" @click="showViewModal = false"></button>
          </div>
          <div class="modal-body">
            <StandardsDetail :standard="viewingStandard" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '~/stores/auth'
import StandardsForm from '~/components/StandardsForm.vue'
import StandardsDetail from '~/components/StandardsDetail.vue'

// Get runtime config for API base URL
const config = useRuntimeConfig()

// Reactive data
const loading = ref(false)
const standards = ref([])
const treeStandards = ref([])
const filterOptions = ref({
  clusters: [],
  group_names: [],
  types: []
})

// Filters
const searchQuery = ref('')
const selectedCluster = ref('')
const selectedGroup = ref('')
const selectedType = ref('')
const viewMode = ref('list')

// Modals
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showViewModal = ref(false)
const editingStandard = ref(null)
const viewingStandard = ref(null)

// Computed
const authStore = useAuthStore()
const canCreateStandards = computed(() => {
  return authStore.user?.permissions?.includes('standards_manage') || 
         authStore.user?.is_superuser
})

const filteredStandards = computed(() => {
  let filtered = standards.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(standard => 
      standard.standard_name?.toLowerCase().includes(query) ||
      standard.cluster?.toLowerCase().includes(query) ||
      standard.group_name?.toLowerCase().includes(query)
    )
  }

  if (selectedCluster.value) {
    filtered = filtered.filter(standard => standard.cluster === selectedCluster.value)
  }

  if (selectedGroup.value) {
    filtered = filtered.filter(standard => standard.group_name === selectedGroup.value)
  }

  if (selectedType.value) {
    filtered = filtered.filter(standard => standard.type === selectedType.value)
  }

  return filtered
})

// Methods
const loadStandards = async () => {
  loading.value = true
  try {
    const response = await $fetch(`${config.public.apiBaseUrl}course/standards/list`, {
      method: 'POST',
      body: {
        page: 1,
        page_size: 1000
      }
    })
    
    if (response.status) {
      standards.value = response.data
    }
  } catch (error) {
    console.error('Error loading standards:', error)
  } finally {
    loading.value = false
  }
}

const loadTreeStandards = async () => {
  try {
    const response = await $fetch(`${config.public.apiBaseUrl}course/standards/tree`, {
      method: 'POST',
      body: {
        root_only: false
      }
    })
    
    if (response.status) {
      treeStandards.value = response.data
    }
  } catch (error) {
    console.error('Error loading tree standards:', error)
  }
}

const loadFilterOptions = async () => {
  try {
    const response = await $fetch(`${config.public.apiBaseUrl}course/standards/filter-options`)
    if (response.status) {
      filterOptions.value = response.data
    }
  } catch (error) {
    console.error('Error loading filter options:', error)
  }
}

const searchStandards = () => {
  // Search is handled by computed property
}

const filterStandards = () => {
  // Filtering is handled by computed property
}

const changeViewMode = () => {
  if (viewMode.value === 'tree') {
    loadTreeStandards()
  }
}

const viewStandard = (standard) => {
  viewingStandard.value = standard
  showViewModal.value = true
}

const editStandard = (standard) => {
  editingStandard.value = standard
  showEditModal.value = true
}

const deleteStandard = async (standard) => {
  if (confirm('آیا از حذف این استاندارد اطمینان دارید؟')) {
    try {
      const response = await $fetch(`${config.public.apiBaseUrl}course/standards/delete`, {
        method: 'POST',
        body: {
          standard_id: standard.id
        }
      })
      
      if (response.status) {
        await loadStandards()
        if (viewMode.value === 'tree') {
          await loadTreeStandards()
        }
      } else {
        alert('خطا در حذف استاندارد: ' + response.message)
      }
    } catch (error) {
      console.error('Error deleting standard:', error)
      alert('خطا در حذف استاندارد')
    }
  }
}

const onStandardSaved = () => {
  closeModal()
  loadStandards()
  if (viewMode.value === 'tree') {
    loadTreeStandards()
  }
}

const closeModal = () => {
  showCreateModal.value = false
  showEditModal.value = false
  editingStandard.value = null
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('fa-IR')
}

// Lifecycle
onMounted(() => {
  loadStandards()
  loadFilterOptions()
})

// Page configuration
definePageMeta({
  layout: "account",
  middleware: ["auth"],
})
</script>

<style scoped>
.standards-management {
  padding: 20px;
}

.tree-item {
  margin-bottom: 5px;
}

.tree-node {
  display: flex;
  align-items: center;
  padding: 8px;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  background: #f8f9fa;
}

.tree-actions {
  margin-left: auto;
}

.modal.show {
  background-color: rgba(0, 0, 0, 0.5);
}

.table th {
  background-color: #f8f9fa;
  border-top: none;
}
</style>
