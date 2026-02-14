<template>
  <div class="container py-5">
    <div v-if="data.saves.length === 0" class="card mb-4 bg-light">
      <div
        class="card-header border-bottom-0 shadow-none bg-light d-flex align-items-center justify-content-between py-3"
      >
      <h5 class="mb-0 text-dark">
          <i class="icon icon-filled-heart text-dark fs-4"></i> دوره‌های مورد علاقه
        </h5>
      </div>
      <div
        class="card-body min-vh-25 d-flex flex-column justify-content-between"
      >
        <table class="table table-striped">
          <thead class="bg-white rounded">
            <tr class="text-center">
              <th>نام دوره</th>
              <th>عملیات</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td
                colspan="2"
                class="text-center fw-bold shadow-none bg-light border-bottom-0 py-5"
              >
                <span class="d-dlex align-items-center fs-5"
                  ><i class="fa-solid fa-triangle-exclamation ms-2 text-warning fs-3"></i>
                  هنوز دوره‌ای به علاقه‌مندی‌ها اضافه نکرده‌اید.</span
                >
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-else class="card mb-4 bg-light">
      <div
        class="card-header border-bottom-0 shadow-none bg-light d-flex align-items-center justify-content-between py-3"
      >
        <h5 class="mb-0 text-dark">
          <i class="icon icon-filled-heart text-dark fs-4"></i> دوره‌های مورد علاقه
        </h5>
      </div>

      <div class="card-body min-vh-25 d-flex flex-column justify-content-between">
        <table class="table">
          <thead class="bg-white rounded">
            <tr class="text-center">
              <th class="text-end">نام دوره</th>
              <th>عملیات</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(save, index) in data.saves"
              :key="index"
              class="align-middle bg-light"
            >
              <td class="bg-light">
                <div class="d-flex align-items-center py-3">
                  <img
                    :src="getMediaUrl(save.image)"
                    alt="Course Image"
                    class="rounded w-100-px h-75-px object-fit-cover"
                  />
                  <div class="me-3">
                    <div>
                      <span class="text-muted small">برگزار کننده :</span>
                      <span class="text-danger1 small">{{ save.organizer.name }}</span>
                    </div>
                    <h6 class="fw-bold mt-2">{{ save.title }}</h6>
                  </div>
                </div>
              </td>
              <td class="text-center bg-light">
                <button
                  class="btn btn-danger btn-sm"
                  @click="deleteCourse(index)"
                >
                <i class="icon icon-regular-trash"></i>  حذف
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
 
<script setup>
import { reactive, onMounted } from "vue";
import { useNuxtApp } from "#app";

const { $api, $sweetalert } = useNuxtApp();
const { getMediaUrl } = useMediaUrl();
const data = reactive({
  saves: [],
});

const wishlist = async () => {
  await $api.post('/course/wishlist/list', {}, {
    headers: {
      Authorization: 'Bearer ' + useCookie('token').value
    }
  }).then((value) => {
    data.saves = value.data.data || [];
  })
};

const deleteCourse = async (index) => {
  const courseId = data.saves[index].id;

  await $api
    .post(
      "/course/wishlist/create",
      { course_id: courseId },
      {
        headers: {
          Authorization: 'Bearer ' + useCookie('token').value,
        },
      }
    )
    .then(() => {
        data.saves.splice(index, 1);
        $sweetalert.success("دوره با موفقیت از علاقه‌مندی‌ها حذف شد");
    })
    .catch((error) => {
      console.error("Error saving/removing course:", error);
      $sweetalert.error("عملیات با خطا مواجه شد");
    });
};


const isSaved = (index) => {
  return data.saves.some((save) => save.id === data.saves[index].id);
};


onMounted(() => {
  wishlist();
});


definePageMeta({
  layout: "account",
  middleware: ['auth']
});
</script>
