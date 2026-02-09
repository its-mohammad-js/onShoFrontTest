// import {useAuthStore} from "~/stores/auth";

// export default defineNuxtRouteMiddleware((to, from) => {
//     const auth = useAuthStore()
//     setTimeout(() => {
//         if (auth.token) {
//             // @ts-ignore
//             if (auth.user.role != 'teacher') {
//                 return navigateTo('/account')
//             }
//         }
//     }, 1000);
// })