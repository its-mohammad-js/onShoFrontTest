<template>
  <div class="container py-5">
    <div class="bg-light border border-2 p-3 rounded-3">
   
      <div
        class="d-flex justify-content-between align-items-center border-bottom pb-3"
      >
        <div class="d-flex align-items-center gap-3">
          <img
            :src="getMediaUrl(instructor.avatar)"
            alt="Instructor Avatar"
            class="rounded-circle border border-light"
            width="60"
            height="60"
          />
          <div>
            <h6 class="mb-1">{{ instructor.name }}</h6>
            <p class="text-muted mb-0 small">{{ instructor.activity }}</p>
          </div>
        </div>
      </div>

    
      <div class="chat-window my-4 border-0 pb-3 border-bottom">
        <div
          v-for="message in messages"
          :key="message.id"
          class="d-flex mb-3"
          :class="
            message.sender === 'me'
              ? 'justify-content-start'
              : 'justify-content-end'
          "
        >
          <div
            class="d-flex align-items-start gap-2"
            :class="message.sender === 'me' ? 'flex-row' : 'flex-row-reverse'"
          >
            <img
              v-if="message.sender === 'them'"
              :src="getMediaUrl(instructor.avatar)"
              alt="User Avatar"
              class="rounded-circle w-40-px h-40-px"
            />
            <div
              class="chat-bubble px-3 py-2"
              :class="
                message.sender === 'me'
                  ? 'bg-dark-subtle text-white'
                  : 'bg-white text-muted'
              "
            >
              <p class="mb-1">{{ message.text }}</p>
              <small
                :class="[
                  'd-block mt-1',
                  message.sender === 'me'
                    ? 'text-white text-start'
                    : 'text-end text-muted',
                ]"
              >
                {{ message.time }}
              </small>
            </div>
          </div>
        </div>
      </div>

   
      <div class="d-flex align-items-center">
        <div class="position-relative">
  <input
    type="file"
    id="fileInput"
    class="d-none"
  />
  <label for="fileInput" class="btn bg-white border rounded-0 rounded-end-3 py-3 border-start-0">
    <i class="fa-solid fa-paperclip"></i>
  </label>
</div>
        <input
          v-model.trim="newMessage"
          type="text"
          class="form-control flex-grow-1 py-3 rounded-0 border-0 border-top border-bottom shadow-none"
          placeholder="پیام خود را وارد کنید"
          @keyup.enter="sendMessage"
        />
        <button class="btn btn-danger text-white border outline-none rounded-0 rounded-start-3 py-3 border-end-0" @click="sendMessage">
          <i class="fa-solid fa-paper-plane"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const { getMediaUrl } = useMediaUrl();

const instructor = ref({
  name: "نام مدرس",
  activity: "حوزه فعالیت",
  avatar: "https://via.placeholder.com/60", 
});


const messages = ref([
  {
    id: 1,
    sender: "them",
    text: "لورم ایپسوم متن ساختگی با تولید سادگی.",
    time: "21:30",
  },
  {
    id: 2,
    sender: "me",
    text: "لورم ایپسوم متن ساختگی با تولید سادگی.",
    time: "22:00",
  },
]);


const newMessage = ref("");


const sendMessage = () => {
  if (newMessage.value.trim() !== "") {
    messages.value.push({
      id: Date.now(),
      sender: "me",
      text: newMessage.value,
      time: "22:00",
    });
    newMessage.value = ""; 
  }
};
definePageMeta({
  layout: "account",
  middleware: ['auth']
});
</script>

<style scoped>
.chat-window {
  background-color: #f9f9f9;
  padding: 20px;
  height: 400px;
  overflow-y: auto;
  border-radius: 10px;
  border: 1px solid #ddd;
}

.chat-bubble {
  max-width: 500px !important;
  border-radius: 15px;
  font-size: 14px;
  line-height: 1.5;
  word-wrap: break-word;
}

.chat-bubble.bg-dark-subtle {
  background-color: #2b2d42 !important;
  color: white;
}

.chat-bubble.bg-light {
  background-color: #f1f1f1 !important;
  color: black;
}
</style>
