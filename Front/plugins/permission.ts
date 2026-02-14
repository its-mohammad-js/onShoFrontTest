import permissionDirective from "~/directives/permission";

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.directive("permission", permissionDirective);
});
