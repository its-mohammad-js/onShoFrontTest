// import {useAuthStore} from "~/stores/auth";

// export default defineNuxtRouteMiddleware((to, from) => {
//     const auth = useAuthStore()

//    setTimeout(() => {
//        if (auth.token) {
//            // @ts-ignore
//            if(auth.user.role != 'student') {
//                return navigateTo('/teacheraccount')
//            }
//        }
//    },1000)
// })