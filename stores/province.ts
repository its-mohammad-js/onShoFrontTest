import { defineStore } from 'pinia'
import { useCookie } from '#app' // Use Nuxt's cookie composable

export const useProvinceStore = defineStore('province', {
    state: () => ({
        province: '',
    }),

    getters: {
        getProvince: (state) => state.province,
    },

    actions: {
        initProvince() {
            const provinceCookie = useCookie('province',{ maxAge: 60 * 60 * 24 * 365 });
            this.province = provinceCookie.value || '';
        },

        setProvince(province: any) {
            const provinceCookie = useCookie('province',{ maxAge: 60 * 60 * 24 * 365 });

            (province)

            // Set the province in the cookie with 1 year expiry
            provinceCookie.value = province;

            this.province = province;
        },
    },
});
