<template>
  <div data-type="slide" class="slide-slide slide" v-bind:class="rootClassName">
    <div class="slide-max-width max-content-container">
      <div class="slide-left-side">
        <div class="slide-decorations-container">
          <img alt="image" src="/union-200h.png" class="slide-dots" />
          <div class="slide-squares-container">
            <div class="slide-light-green"></div>
            <div class="slide-orange"></div>
          </div>
        </div>
        <div class="slide-image-container">
          <img :alt="imageAlt" :src="imageSrc" class="slide-image" />
          <div class="slide-slider-controls">
            <div data-action="previousSlide" class="slide-go-left">
              <svg viewBox="0 0 1024 1024" class="slide-icon1">
                <path
                  d="M854 470v84h-520l238 240-60 60-342-342 342-342 60 60-238 240h520z"
                ></path>
              </svg>
            </div>
            <div data-action="nextSlide" class="slide-go-right">
              <svg viewBox="0 0 1024 1024" class="slide-icon3">
                <path
                  d="M512 170l342 342-342 342-60-60 238-240h-520v-84h520l-238-240z"
                ></path>
              </svg>
            </div>
          </div>
        </div>
      </div>
      <div class="slide-right-side"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Slide',
  props: {
    rootClassName: String,
    imageSrc: {
      type: String,
      default:
        'https://images.unsplash.com/photo-1508002366005-75a695ee2d17?ixid=Mnw5MTMyMXwwfDF8c2VhcmNofDUxfHxzbWlsZXxlbnwwfHx8fDE2NDM0MDc4MTE&ixlib=rb-1.2.1&w=700',
    },
    imageAlt: {
      type: String,
      default: 'image',
    },
  },
}
</script>

<style scoped>
.slide-slide {
  align-items: stretch;
  flex-direction: row;
  justify-content: center;
  background-color: var(--dl-color-backgrounds-darkblue);
}
.slide-max-width {
  align-items: stretch;
  flex-direction: row;
  justify-content: space-between;
}
.slide-left-side {
  width: 50%;
  display: flex;
  align-items: stretch;
  padding-right: var(--dl-space-space-fiveunits);
  flex-direction: row;
  justify-content: space-between;
}
.slide-decorations-container {
  flex: 1;
  display: flex;
  align-items: flex-end;
  flex-direction: column;
  justify-content: space-between;
}
.slide-dots {
  width: 126px;
  height: 126px;
  margin-top: 21px;
  object-fit: cover;
  margin-right: 21px;
}
.slide-squares-container {
  flex: 0 0 auto;
  display: flex;
  align-items: flex-end;
  flex-direction: column;
}
.slide-light-green {
  flex: 0 0 auto;
  width: 54px;
  height: 54px;
  display: flex;
  align-items: flex-start;
  flex-direction: column;
  background-color: var(--dl-color-backgrounds-lightgreen);
}
.slide-orange {
  flex: 0 0 auto;
  width: 108px;
  height: 108px;
  display: flex;
  align-items: flex-start;
  flex-direction: column;
  background-color: var(--dl-color-backgrounds-primary);
}
.slide-image-container {
  display: flex;
  align-items: stretch;
  flex-direction: column;
  justify-content: space-between;
}
.slide-image {
  width: 100%;
  height: 485px;
  object-fit: cover;
}
.slide-slider-controls {
  flex: 0 0 auto;
  width: 100%;
  display: flex;
  align-items: stretch;
  flex-direction: row;
  justify-content: flex-end;
}
.slide-go-left {
  flex: 0 0 auto;
  width: 100%;
  height: 108px;
  display: flex;
  max-width: 108px;
  max-height: 108px;
  transition: 0.3s;
  align-items: center;
  flex-direction: column;
  justify-content: center;
}
.slide-go-left:hover {
  cursor: pointer;
  background-color: rgba(229, 229, 229, 0.2);
}
.slide-icon1 {
  fill: var(--dl-color-grays-white100);
  width: 42px;
  height: 42px;
}
.slide-go-right {
  flex: 0 0 auto;
  width: 100%;
  height: 108px;
  display: flex;
  max-width: 108px;
  max-height: 108px;
  transition: 0.3s;
  align-items: center;
  flex-direction: column;
  justify-content: center;
}
.slide-go-right:hover {
  cursor: pointer;
  background-color: rgba(229, 229, 229, 0.2);
}
.slide-icon3 {
  fill: var(--dl-color-grays-white100);
  width: 42px;
  height: 42px;
}
.slide-right-side {
  flex: 0 0 auto;
  width: 50%;
  border: 2px dashed rgba(120, 120, 120, 0.4);
  display: flex;
  align-items: flex-start;
  padding-top: var(--dl-space-space-twounits);
  flex-direction: column;
  padding-bottom: var(--dl-space-space-twounits);
  justify-content: center;
}
@media(max-width: 991px) {
  .slide-left-side {
    padding-right: var(--dl-space-space-oneandhalfunits);
  }
}
@media(max-width: 767px) {
  .slide-max-width {
    flex-direction: column;
  }
  .slide-left-side {
    width: 100%;
    padding-right: 0px;
  }
  .slide-image {
    max-width: 700px;
  }
  .slide-right-side {
    width: 100%;
  }
}
@media(max-width: 479px) {
  .slide-dots {
    width: 60px;
    height: 60px;
  }
  .slide-light-green {
    width: 36px;
    height: 36px;
  }
  .slide-orange {
    width: 75px;
    height: 75px;
  }
  .slide-go-left {
    height: 75px;
    max-width: 75px;
    max-height: 75px;
  }
  .slide-go-right {
    height: 75px;
    max-width: 75px;
    max-height: 75px;
  }
}
</style>
