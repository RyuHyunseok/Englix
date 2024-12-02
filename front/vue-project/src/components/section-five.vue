<template>
  <div class="section-five-section-five section-container">
    <div class="section-five-max-width max-content-container">
      <div class="section-five-cards-container">
        <grid-card
          text="WHAT'S YOUR GOAL?"
          imageSrc="/vector%203-200h.png"
          rootClassName="grid-cardroot-class-name"
        >
          <template v-slot:button1>
            <div class="section-five-fragment1">
              <span class="section-five-text1">TOEIC</span>
            </div>
          </template>
          <template v-slot:button11>
            <div class="section-five-fragment2">
              <span class="section-five-text2">수능</span>
            </div>
          </template>
          <template v-slot:button12>
            <div class="section-five-fragment3">
              <span class="section-five-text3">BUSINESS</span>
            </div>
          </template>
        </grid-card>
      </div>
    </div>
  </div>
</template>

<script>
import GridCard from './grid-card'

export default {
  name: 'SectionFive',
  props: {},
  components: {
    GridCard,
  },
}
</script>

<style scoped>
.section-five-section-five {
  position: relative;
}
.section-five-max-width {
  flex-direction: column;
  justify-content: center;
}
.section-five-cards-container {
  width: 100%;
  display: grid;
  grid-gap: var(--dl-space-space-twounits);
  position: relative;
  grid-template-columns: 1fr 1fr;
}
.section-five-fragment1 {
  display: contents;
}
.section-five-text1 {
  display: inline-block;
}
.section-five-fragment2 {
  display: contents;
}
.section-five-text2 {
  display: inline-block;
}
.section-five-fragment3 {
  display: contents;
}
.section-five-text3 {
  display: inline-block;
}
@media(max-width: 767px) {
  .section-five-cards-container {
    grid-template-columns: 1fr;
  }
}
</style>
