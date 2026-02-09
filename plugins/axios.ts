// plugins/axios.ts
import axios from 'axios'
import { defineNuxtPlugin, useRuntimeConfig } from '#app';

// Function to generate random ID
function makeid(length: number) {
    let result = ''
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    const charactersLength = characters.length
    let counter = 0
    while (counter < length) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength))
        counter += 1
    }
    return result
}

// plugins/axios.ts

export default defineNuxtPlugin(() => {
    const config = useRuntimeConfig();
    
    // در production از relative path استفاده کن (برای subdomain)
    // در development از apiBaseUrl استفاده کن
    let baseURL = config.public.apiBaseUrl;
    
    // اگر در production هستیم (نه localhost) و apiBaseUrl به localhost اشاره می‌کند، از relative path استفاده کن
    if (typeof window !== 'undefined') {
      const isProduction = !window.location.hostname.includes('localhost') && 
                          !window.location.hostname.includes('127.0.0.1');
      
      if (isProduction && baseURL.includes('127.0.0.1') || baseURL.includes('localhost')) {
        // در production از relative path استفاده کن که nginx آن را proxy می‌کند
        baseURL = '/api/';
      }
    }
    
    const api = axios.create({
        // @ts-ignore
        baseURL: baseURL,
        // سایر تنظیمات مانند هدرها، تایم‌اوت و غیره
    });
    // Axios Request Interceptor
    api.interceptors.request.use((config) => {
        const imei = useCookie('imei',{ maxAge: 60 * 60 * 24 * 365 }) // Access Nuxt 3 cookies
        const token = useCookie('token') // Access Nuxt 3 cookies

        if (typeof imei.value === 'undefined') {
            // @ts-ignore
            imei.value = makeid(32); // Set IMEI for 1 year
        }

        // Set the IMEI and Authorization headers from cookies

        // config.headers['IMEI'] = imei.value;

        // if (typeof token.value === 'undefined') {
        //     // @ts-ignore
        //     config.headers['Authorization'] = 'Bearer ' + token.value
        // }

        return config
    }, (error) => {
        return Promise.reject(error)
    })

    // Axios Response Error Interceptor
    api.interceptors.response.use((response) => {
        return response
    }, (error) => {
        // if (error.response.status === 401) {
        //     window.location.replace("/auth/login/code");
        // }

        if (error.response.status === 500) {
            console.error('Server Error:', error.response.data)
        }

        return Promise.reject(error)
    })


    return {
        provide: {
            api,
        },
    };
});
