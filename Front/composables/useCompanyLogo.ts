import { ref, readonly } from 'vue'

const companyLogo = ref<string | null>(null)

export const useCompanyLogo = () => {
  const setCompanyLogo = (logo: string | null) => {
    companyLogo.value = logo
  }

  const getCompanyLogo = () => {
    return companyLogo.value
  }

  const clearCompanyLogo = () => {
    companyLogo.value = null
  }

  return {
    companyLogo: readonly(companyLogo),
    setCompanyLogo,
    getCompanyLogo,
    clearCompanyLogo
  }
}

