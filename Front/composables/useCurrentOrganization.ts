import { ref, readonly } from 'vue'

const currentOrganizationId = ref<number | null>(null)

export const useCurrentOrganization = () => {
  const setCurrentOrganizationId = (id: number | null) => {
    currentOrganizationId.value = id
  }

  const getCurrentOrganizationId = () => {
    return currentOrganizationId.value
  }

  const clearCurrentOrganizationId = () => {
    currentOrganizationId.value = null
  }

  return {
    currentOrganizationId: readonly(currentOrganizationId),
    setCurrentOrganizationId,
    getCurrentOrganizationId,
    clearCurrentOrganizationId
  }
}

