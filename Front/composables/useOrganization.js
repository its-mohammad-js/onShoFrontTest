export const useOrganization = () => {
  const { $api } = useNuxtApp()
  const authStore = useAuthStore()

  const organization = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const fetchOrganization = async () => {
    const token = useCookie("token").value
    if (!token) {
      return null
    }

    loading.value = true
    error.value = null

    try {
      // First try to get current user's organization using the detail endpoint
      const response = await $api.post('/course/organization/detail', {}, {
        headers: {
          Authorization: "Bearer " + token,
        },
      })

      if (response.data.status && response.data.data) {
        organization.value = response.data.data
        return response.data.data
      }
    } catch (error) {
      console.error('Error fetching organization:', error)
      error.value = error.message
    } finally {
      loading.value = false
    }

    return null
  }

  const isOrganizationActive = computed(() => {
    return organization.value?.is_active === true
  })

  const isOrganizationVerified = computed(() => {
    return organization.value?.is_verified === true
  })

  const canCreateCourse = computed(() => {
    return isOrganizationActive.value && isOrganizationVerified.value
  })

  const canCreateTask = computed(() => {
    return isOrganizationActive.value && isOrganizationVerified.value
  })

  const organizationStatusMessage = computed(() => {
    if (!organization.value) {
      return 'سازمانی یافت نشد'
    }
    
    if (!isOrganizationActive.value) {
      return 'سازمان شما غیرفعال است'
    }
    
    if (!isOrganizationVerified.value) {
      return 'سازمان شما در انتظار تأیید است'
    }
    
    return null
  })

  return {
    organization: readonly(organization),
    loading: readonly(loading),
    error: readonly(error),
    isOrganizationActive,
    isOrganizationVerified,
    canCreateCourse,
    canCreateTask,
    organizationStatusMessage,
    fetchOrganization
  }
}
