<template>
    <div class="loader-container">
      <div class="rocket-wrapper">
        <div class="rocket-container">
          <img ref="rocketShadow" src="/images/rocket/rocket_shadow.png" class="rocket-part shadow_1" />
          <img ref="personShadow" src="/images/rocket/rocket_shadow.png" class="rocket-part shadow_2" />
          <img ref="rocketTower" src="/images/rocket/tower.png" class="rocket-part tower" />
          <img ref="rocketPerson" src="/images/rocket/character.png" class="rocket-part person" />
          <div class="rocket">
            <img ref="rocketBase" src="/images/rocket/rocket_base.png" class="rocket-part base" />
            <img ref="rocketBody1" src="/images/rocket/rocket_body1.png" class="rocket-part body1" />
            <img ref="rocketBody2" src="/images/rocket/rocket_body2.png" class="rocket-part body2" />
            <img ref="rocketTop" src="/images/rocket/rocket_top.png" class="rocket-part top" />
            <img ref="rocketBooster" src="/images/rocket/rocket_booster.png" class="rocket-part booster" />
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted } from 'vue';
  
  onMounted(() => {
    setTimeout(() => {
      document.querySelector('.base').classList.add('move-base');
      document.querySelector('.body1').classList.add('move-body1');
      document.querySelector('.body2').classList.add('move-body2');
      document.querySelector('.top').classList.add('move-top');
      document.querySelector('.booster').classList.add('move-booster');
    }, 500);
  });
  </script>
  
  <style scoped>
  .loader-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 90vw;
    height: 100vh;
    background-color: white;
  }
  
  .rocket-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    position: fixed;
    right: 100px;
    top: 100px;
  }
  
  .rocket-container {
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    width: 500px;
    height: 500px;
  }
  
  .rocket {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .rocket-part {
    width: 100px;
    position: absolute;
    transition: transform 1s ease-in-out;
  }
  .base {
    width: 70px !important;
  }
  
  .tower {
    width: 120px;
    position: absolute;
    right: 80px;
    top: 0;
  }

  .person {
    width: 150px;
    position: absolute;
    right: -150px;
    top: -25px;
  }

  .shadow_1 {
    width: 150px;
    position: absolute;
    bottom: 100px;
    opacity: 0.5;
    z-index: -1;
  }

  .shadow_2 {
    width: 180px;
    position: absolute;
    right: -170px;
    bottom: 100px;
    opacity: 0.5;
    z-index: -1;
  }
  
  /* موقعیت اولیه قطعات برای نمایش یک موشک کامل */
  .body1 { transform: translateY(-100px); }
  .body2 { transform: translateY(-150px); }
  .top { transform: translateY(-220px); }
  .booster { transform: translateY(-300px); }
  
  /* حرکت جداگانه برای هر قطعه */
  .move-base { transform: translateY(20px); }
  .move-body1 { transform: translateY(-120px); }
  .move-body2 { transform: translateY(-200px); }
  .move-top { transform: translateY(-300px); }
  .move-booster { transform: translateY(-420px); }

  /* تغییر اندازه برای موبایل */
  @media (max-width: 768px) {
    .rocket-container {
      width: 400px;
      height: 400px;
    }
    .rocket-part {
      width: 75px;
    }
    .base {
      width: 60px !important;
    }
    .tower {
      width: 90px;
      right: 40px;
    }
    .person {
      width: 120px;
      right: -100px;
      top: 0;
    }
    .shadow_1, .shadow_2 {
      width: 100px;
      bottom: 60px;
    }
    .shadow_2 {
      right: -110px;
    }
  }
  </style>