
export default defineNuxtPlugin((nuxtApp) => {
    const auth = useAuthStore();
    auth.init();
    const province = useProvinceStore();
    province.initProvince();
})
