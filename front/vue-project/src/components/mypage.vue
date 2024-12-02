<template>
  <div class="thq-section-padding" v-bind:class="rootClassName">
    <h2 class="mypage-heading7 thq-heading-2">
      <slot name="heading71">
        <!--Default content for heading71-->
        <div class="mypage-fragment3">
          <span class="mypage-text20">My Page</span>
        </div>
      </slot>
    </h2>
    <div class="mypage-max-width thq-section-max-width">
      <div class="mypage-container2 thq-flex-column">
        <button class="thq-button-outline">
          <span>
            <slot name="button13">
              <!--Default content for button13-->
              <div class="mypage-fragment4">
                <span class="mypage-text21">내 단어장</span>
              </div>
            </slot>
          </span>
        </button>
        <button class="thq-button-filled">
          <span>
            <slot name="button5">
              <!--Default content for button5-->
              <div class="mypage-fragment7">
                <span class="mypage-text24">찜한 영화</span>
              </div>
            </slot>
          </span>
        </button>
        <button
          @click="handleButtonClick"
          v-if="!isTermsVisible"
          class="thq-button-outline"
        >
          <span>
            <slot name="button">
              <!--Default content for button-->
              <div class="mypage-fragment2"><span>내 단어장</span></div>
            </slot>
          </span>
        </button>
        <button
          @click="handleButtonClick"
          v-if="isPrivacyVisible"
          class="thq-button-filled"
        >
          <span>
            <slot name="button1">
              <!--Default content for button1-->
              <div class="mypage-fragment1"><span>찜한 영화</span></div>
            </slot>
          </span>
        </button>
        <button
          @click="handleButtonClick"
          v-if="!isRefundVisible"
          class="thq-button-outline"
        >
          <span>
            <slot name="button2">
              <!--Default content for button2-->
              <div><span>좋아요한 글</span></div>
            </slot>
          </span>
        </button>
        <button class="thq-button-outline">
          <span>
            <slot name="button21">
              <!--Default content for button21-->
              <div class="mypage-fragment5"><span>내가 쓴 글</span></div>
            </slot>
          </span>
        </button>
        <button class="thq-button-outline">
          <span>
            <slot name="button211">
              <!--Default content for button211-->
              <div class="mypage-fragment8"><span>내가 쓴 댓글</span></div>
            </slot>
          </span>
        </button>
        <button
          @click="handleButtonClick"
          v-if="isRefundVisible"
          class="thq-button-filled"
        >
          <span>
            <slot name="button2">
              <!--Default content for button2-->
              <div class="mypage-fragment6"><span>좋아요한 글</span></div>
            </slot>
          </span>
        </button>
      </div>
      <div class="mypage-container3">
        <app-portofolio
          rootClassName="portofolioroot-class-name"
        ></app-portofolio>
        <div class="mypage-container4 thq-flex-column"></div>
      </div>
    </div>
  </div>
</template>

<script>
import AppPortofolio from './portofolio'

export default {
  name: 'Mypage',
  props: {
    rootClassName: String,
  },
  components: {
    AppPortofolio,
  },
  data() {
    return {
      isTermsVisible: true,
      isRefundVisible: false,
      isPrivacyVisible: false,
    }
  },
  methods: {
    handleButtonClick() {
      this.isRefundVisible = true
      this.isPrivacyVisible = false
      this.isTermsVisible = false
    },
  },
}
</script>

<style scoped>
.mypage-heading7 {
  align-self: center;
  text-align: center;
}
.mypage-max-width {
  width: 1214px;
  height: 1146px;
  display: flex;
  position: relative;
  max-width: var(--dl-size-size-maxwidth);
  align-items: flex-start;
  flex-direction: row;
  justify-content: flex-start;
}
.mypage-container2 {
  flex: 0 0 auto;
  width: auto;
  height: 445px;
  display: flex;
  align-items: stretch;
  padding-top: var(--dl-space-space-threeunits);
  flex-direction: column;
  justify-content: center;
}
.mypage-container3 {
  flex: 0 0 auto;
  width: 1017px;
  height: auto;
  display: flex;
  align-items: flex-start;
  flex-direction: column;
}
.mypage-container4 {
  flex: 0 0 auto;
  width: 1017px;
  border: 2px dashed rgba(120, 120, 120, 0.4);
  height: 1135px;
  display: flex;
  align-items: center;
  padding-top: var(--dl-space-space-threeunits);
  flex-direction: column;
  justify-content: center;
}
.mypage-fragment1 {
  display: contents;
}
.mypage-fragment2 {
  display: contents;
}
.mypage-fragment3 {
  display: contents;
}
.mypage-text20 {
  display: inline-block;
}
.mypage-fragment4 {
  display: contents;
}
.mypage-text21 {
  display: inline-block;
}
.mypage-fragment5 {
  display: contents;
}
.mypage-fragment6 {
  display: contents;
}
.mypage-fragment7 {
  display: contents;
}
.mypage-text24 {
  display: inline-block;
}
.mypage-fragment8 {
  display: contents;
}


@media(max-width: 767px) {
  .mypage-max-width {
    align-items: center;
    flex-direction: column;
  }
  .mypage-container2 {
    align-self: center;
  }
  .mypage-container4 {
    align-self: center;
  }
}
@media(max-width: 479px) {
  .mypage-max-width {
    flex-direction: column;
  }
  .mypage-container2 {
    align-self: center;
  }
  .mypage-container4 {
    align-self: center;
  }
}
</style>
