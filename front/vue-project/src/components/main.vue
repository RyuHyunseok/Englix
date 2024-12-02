<template>
  <div class="main-header5 thq-section-padding">
    <img :alt="props.image1Alt" :src="props.image1Src" class="main-image" />
    <div class="main-container1">
      <div class="main-max-width thq-section-max-width">
        <div class="main-column">
          <div class="main-content">
            <h1 class="thq-heading-1 main-text1">
              <slot name="heading1">
                <div class="main-fragment3">
                  <span class="main-text6">Learn English Through Movies</span>
                </div>
              </slot>
            </h1>
            <p class="thq-body-large main-text2">
              <slot name="content1">
                <div class="main-fragment2">
                  <span class="main-text5">Join our platform to discover personalized movie recommendations, improve your English skills, and connect with fellow movie enthusiasts.</span>
                </div>
              </slot>
            </p>
            <div class="main-actions">
              <div class="main-container2">
                <button class="main-button thq-button-filled">
                  <span class="thq-body-small">
                    <slot name="action1">
                      <div class="main-fragment1">
                        <span class="main-text4">Get Started</span>
                      </div>
                    </slot>
                  </span>
                </button>
              </div>
              <div class="main-container3"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  image1Alt: {
    type: String,
    default: "Movie Buffs Community Image",
  },
  image1Src: {
    type: String,
    default: "https://images.unsplash.com/photo-1705822898715-369170f541cf?ixid=M3w5MTMyMXwwfDF8c2VhcmNofDExOXx8bW92aWVzfGVufDB8fHx8MTczMTk1MDU4M3ww&ixlib=rb-4.0.3&w=1500",
  },
});
</script>

<style scoped>
.main-header5 {
  width: 100%;
  height: 100vh;
  display: flex;
  position: relative;
  align-items: flex-start;
  justify-content: flex-end;
}
.main-image {
  top: 0px;
  left: 0px;
  width: 100%;
  height: 100%;
  position: absolute;
  object-fit: cover;
}
.main-container1 {
  width: 100%;
  height: 865px;
  display: flex;
  align-items: flex-start;
  justify-content: flex-end;
}
.main-max-width {
  display: flex;
  align-self: center;
  align-items: center;
  justify-content: flex-start;
}
.main-column {
  gap: 24px;
  width: auto;
  display: flex;
  z-index: 1;
  max-width: 560px;
  align-items: flex-start;
  flex-shrink: 0;
  flex-direction: column;
}
.main-content {
  gap: var(--dl-space-space-oneandhalfunits);
  display: flex;
  align-self: stretch;
  align-items: flex-start;
  animation-name: fadeInLeftBig;
  flex-direction: column;
  animation-delay: 0s;
  animation-duration: 500ms;
  animation-direction: normal;
  animation-iteration-count: 1;
  animation-timing-function: ease;
}
.main-actions {
  gap: var(--dl-space-space-unit);
  display: flex;
  align-items: flex-start;
}
.main-container2 {
  display: flex;
  align-items: flex-start;
}
.main-button {
  display: flex;
  box-sizing: content-box;
  align-items: center;
  border-color: var(--dl-color-theme-primary1);
  border-style: solid;
  border-width: 1px;
  justify-content: center;
  background-color: var(--dl-color-theme-primary1);
}
.main-container3 {
  border: 2px dashed rgba(120, 120, 120, 0.4);
  display: flex;
  align-items: flex-start;
}
.main-fragment1 {
  display: contents;
}
.main-text4 {
  display: inline-block;
}
.main-fragment2 {
  display: contents;
}
.main-text5 {
  color: #ffcaca;
  display: inline-block;
}
.main-fragment3 {
  display: contents;
}
.main-text6 {
  color: #ffffff;
  display: inline-block;
}
@media (max-width: 767px) {
  .main-header5 {
    justify-content: center;
  }
  .main-max-width {
    justify-content: center;
  }
  .main-column {
    width: 100%;
  }
  .main-text1 {
    text-align: center;
  }
  .main-text2 {
    text-align: center;
  }
  .main-actions {
    width: 100%;
    align-self: flex-start;
    justify-content: center;
  }
}
@media (max-width: 479px) {
  .main-actions {
    flex-direction: column;
  }
  .main-container2 {
    width: 100%;
  }
  .main-button {
    width: 100%;
  }
  .main-container3 {
    width: 100%;
  }
}
</style>
