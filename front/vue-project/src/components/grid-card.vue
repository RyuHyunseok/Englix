<template>
  <div class="grid-card-grid-card" v-bind:class="rootClassName">
    <img :alt="imageAlt1" :src="imageSrc1" class="grid-card-image" />
    <span class="grid-card-text1">{{ text }}</span>
    <button class="thq-button-outline">
      <span>
        <slot name="button1">
          <!--Default content for button1-->
          <div class="grid-card-fragment3">
            <span class="grid-card-text7">TOEIC</span>
          </div>
        </slot>
      </span>
    </button>
    <button class="thq-button-outline">
      <span>
        <slot name="button12">
          <!--Default content for button12-->
          <div class="grid-card-fragment2">
            <span class="grid-card-text6">BUSINESS</span>
          </div>
        </slot>
      </span>
    </button>
    <button class="thq-button-outline">
      <span>
        <slot name="button11">
          <!--Default content for button11-->
          <div class="grid-card-fragment1">
            <span class="grid-card-text5">수능</span>
          </div>
        </slot>
      </span>
    </button>
  </div>
</template>

<script>
export default {
  name: "GridCard",
  props: {
    imageAlt1: {
      type: String,
      default: "image",
    },
    imageSrc1: {
      type: String,
      default: "https://play.teleporthq.io/static/svg/default-img.svg",
    },
    rootClassName: String,
    text: {
      type: String,
      default: "WHAT'S YOUR GOAL?",
    },
  },
};
</script>

<style scoped>
.grid-card-grid-card {
  gap: 16px;
  flex: 0 0 auto;
  width: 500px;
  height: 619px;
  display: flex;
  padding: 36px;
  align-items: center;
  flex-direction: column;
  justify-content: center;
  background-color: var(--dl-color-grays-white100);
}
.grid-card-image {
  width: 60px;
  height: 60px;
  object-fit: cover;
  margin-bottom: var(--dl-space-space-twounits);
}
.grid-card-text1 {
  font-size: 30px;
  font-style: normal;
  font-weight: 500;
  line-height: 1.3;
  margin-bottom: var(--dl-space-space-halfunit);
}
.grid-card-fragment1 {
  display: contents;
}
.grid-card-text5 {
  display: inline-block;
}
.grid-card-fragment2 {
  display: contents;
}
.grid-card-text6 {
  display: inline-block;
}
.grid-card-fragment3 {
  display: contents;
}
.grid-card-text7 {
  display: inline-block;
}
.grid-cardroot-class-name {
  top: -383px;
  left: 68px;
  position: absolute;
}
</style>
