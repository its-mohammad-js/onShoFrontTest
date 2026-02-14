<template>
  <div class="standards-detail">
    <div v-if="standard" class="row">
      <!-- Basic Information -->
      <div class="col-md-6">
        <div class="card mb-3">
          <div class="card-header">
            <h6 class="mb-0">اطلاعات پایه</h6>
          </div>
          <div class="card-body">
            <div class="row mb-2">
              <div class="col-4"><strong>شماره:</strong></div>
              <div class="col-8">{{ standard.number || '-' }}</div>
            </div>
            <div class="row mb-2">
              <div class="col-4"><strong>نام استاندارد:</strong></div>
              <div class="col-8">{{ standard.standard_name || '-' }}</div>
            </div>
            <div class="row mb-2">
              <div class="col-4"><strong>نام لاتین:</strong></div>
              <div class="col-8">{{ standard.standard_name_latin || '-' }}</div>
            </div>
            <div class="row mb-2">
              <div class="col-4"><strong>سطح:</strong></div>
              <div class="col-8">
                <span class="badge bg-info">{{ standard.level }}</span>
              </div>
            </div>
            <div class="row mb-2">
              <div class="col-4"><strong>والد:</strong></div>
              <div class="col-8">
                <span v-if="standard.parent_info">
                  {{ standard.parent_info.standard_name }} ({{ standard.parent_info.number }})
                </span>
                <span v-else class="text-muted">ریشه</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Classification -->
      <div class="col-md-6">
        <div class="card mb-3">
          <div class="card-header">
            <h6 class="mb-0">طبقه‌بندی</h6>
          </div>
          <div class="card-body">
            <div class="row mb-2">
              <div class="col-4"><strong>خوشه:</strong></div>
              <div class="col-8">{{ standard.cluster || '-' }}</div>
            </div>
            <div class="row mb-2">
              <div class="col-4"><strong>گروه:</strong></div>
              <div class="col-8">{{ standard.group_name || '-' }}</div>
            </div>
            <div class="row mb-2">
              <div class="col-4"><strong>نوع:</strong></div>
              <div class="col-8">
                <span class="badge bg-secondary">{{ standard.type || '-' }}</span>
              </div>
            </div>
            <div class="row mb-2">
              <div class="col-4"><strong>کارو دانش:</strong></div>
              <div class="col-8">{{ standard.work_and_knowledge || '-' }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Codes -->
      <div class="col-md-6">
        <div class="card mb-3">
          <div class="card-header">
            <h6 class="mb-0">کدها</h6>
          </div>
          <div class="card-body">
            <div class="row mb-2">
              <div class="col-4"><strong>کد قدیم:</strong></div>
              <div class="col-8">{{ standard.old_standard_code || '-' }}</div>
            </div>
            <div class="row mb-2">
              <div class="col-4"><strong>نسخه:</strong></div>
              <div class="col-8">{{ standard.version || '-' }}</div>
            </div>
            <div class="row mb-2">
              <div class="col-4"><strong>کد شایستگی:</strong></div>
              <div class="col-8">{{ standard.competency_code || '-' }}</div>
            </div>
            <div class="row mb-2">
              <div class="col-4"><strong>کد شغل ISCO:</strong></div>
              <div class="col-8">{{ standard.isco_job_code || '-' }}</div>
            </div>
            <div class="row mb-2">
              <div class="col-4"><strong>کد گروه ISCO:</strong></div>
              <div class="col-8">{{ standard.isco_group_code || '-' }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Education and Hours -->
      <div class="col-md-6">
        <div class="card mb-3">
          <div class="card-header">
            <h6 class="mb-0">تحصیلات و ساعات</h6>
          </div>
          <div class="card-body">
            <div class="row mb-2">
              <div class="col-4"><strong>سطح تحصیلات:</strong></div>
              <div class="col-8">{{ standard.entry_education_level || '-' }}</div>
            </div>
            <div class="row mb-2">
              <div class="col-4"><strong>ساعت نظری:</strong></div>
              <div class="col-8">{{ standard.theoretical_hours || '-' }}</div>
            </div>
            <div class="row mb-2">
              <div class="col-4"><strong>ساعت عملی:</strong></div>
              <div class="col-8">{{ standard.practical_hours || '-' }}</div>
            </div>
            <div class="row mb-2">
              <div class="col-4"><strong>ساعت کارورزی:</strong></div>
              <div class="col-8">{{ standard.internship_hours || '-' }}</div>
            </div>
            <div class="row mb-2">
              <div class="col-4"><strong>ساعت پروژه:</strong></div>
              <div class="col-8">{{ standard.project_hours || '-' }}</div>
            </div>
            <div class="row mb-2">
              <div class="col-4"><strong>ساعت کل:</strong></div>
              <div class="col-8">
                <span class="badge bg-success">{{ standard.total_hours || '-' }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Dates and Statistics -->
      <div class="col-md-6">
        <div class="card mb-3">
          <div class="card-header">
            <h6 class="mb-0">تاریخ‌ها و آمار</h6>
          </div>
          <div class="card-body">
            <div class="row mb-2">
              <div class="col-4"><strong>تاریخ تدوین:</strong></div>
              <div class="col-8">{{ formatDate(standard.compilation_date) }}</div>
            </div>
            <div class="row mb-2">
              <div class="col-4"><strong>تاریخ ایجاد:</strong></div>
              <div class="col-8">{{ formatDateTime(standard.create_date) }}</div>
            </div>
            <div class="row mb-2">
              <div class="col-4"><strong>آخرین به‌روزرسانی:</strong></div>
              <div class="col-8">{{ formatDateTime(standard.update_date) }}</div>
            </div>
            <div class="row mb-2">
              <div class="col-4"><strong>تعداد فرزندان:</strong></div>
              <div class="col-8">
                <span class="badge bg-primary">{{ standard.children_count || 0 }}</span>
              </div>
            </div>
            <div class="row mb-2">
              <div class="col-4"><strong>تعداد هم‌سطح‌ها:</strong></div>
              <div class="col-8">
                <span class="badge bg-warning">{{ standard.siblings_count || 0 }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Ancestors -->
      <div class="col-md-6" v-if="standard.ancestors && standard.ancestors.length > 0">
        <div class="card mb-3">
          <div class="card-header">
            <h6 class="mb-0">اجداد</h6>
          </div>
          <div class="card-body">
            <div v-for="(ancestor, index) in standard.ancestors" :key="ancestor.id" class="mb-2">
              <div class="d-flex align-items-center">
                <span class="badge bg-light text-dark me-2">{{ index + 1 }}</span>
                <span>{{ ancestor.standard_name }} ({{ ancestor.number }})</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-5">
      <i class="fas fa-exclamation-triangle fa-3x text-warning mb-3"></i>
      <h5 class="text-muted">استاندارد یافت نشد</h5>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// Props
const props = defineProps({
  standard: {
    type: Object,
    default: null
  }
})

// Methods
const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('fa-IR')
}

const formatDateTime = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString('fa-IR')
}
</script>

<style scoped>
.standards-detail {
  padding: 0;
}

.card {
  border: 1px solid #e9ecef;
  border-radius: 8px;
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  padding: 0.75rem 1rem;
}

.card-header h6 {
  color: #495057;
  font-weight: 600;
}

.card-body {
  padding: 1rem;
}

.row {
  margin-bottom: 0.5rem;
}

.badge {
  font-size: 0.75em;
}

.text-muted {
  color: #6c757d !important;
}
</style>
