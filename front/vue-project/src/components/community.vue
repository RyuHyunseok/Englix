<template>
  <div
    class="community-container1 thq-section-padding"
    v-bind:class="rootClassName"
  >
    <div class="community-max-width thq-section-max-width">
      <div class="community-container2 thq-flex-column">
        <div v-if="isTermsVisible" class="community-container3">
          <ul class="community-ul1 thq-flex-column">
            <li class="community-li10 thq-flex-column list-item">
              <h2 class="community-heading7 thq-heading-2">
                <slot name="heading7">
                  <!--Default content for heading7-->
                  <div class="community-fragment26">
                    <span class="community-text34">Community</span>
                  </div>
                </slot>
              </h2>
              <p class="thq-body-small">
                <slot name="content7">
                  <!--Default content for content7-->
                  <div class="community-fragment11">
                    <span class="community-text19">
                      Never miss important updates or breaking news with Feedbox.
                    </span>
                  </div>
                </slot>
              </p>
              <ul class="community-ul2 thq-flex-column">
                <li class="list-item">
                  <h3 class="thq-heading-3">
                    <slot name="heading8">
                      <!--Default content for heading8-->
                      <div class="community-fragment37">
                        <span class="community-text45">Title</span>
                      </div>
                    </slot>
                  </h3>
                  <p class="thq-body-small">
                    <slot name="content2">
                      <!--Default content for content2-->
                      <div><span>content</span></div>
                    </slot>
                  </p>
                </li>
                <li class="list-item">
                  <h3 class="thq-heading-3">
                    <slot name="heading9">
                      <!--Default content for heading9-->
                      <div class="community-fragment13">
                        <span class="community-text21">Title</span>
                      </div>
                    </slot>
                  </h3>
                  <p class="thq-body-small">
                    <slot name="content9">
                      <!--Default content for content9-->
                      <div class="community-fragment33">
                        <span class="community-text41">content</span>
                      </div>
                    </slot>
                  </p>
                </li>
              </ul>
            </li>
          </ul>
        </div>
        <div v-if="isPrivacyVisible" class="community-container4">
          <ul class="thq-flex-column">
            <li class="community-li13 thq-flex-column list-item">
              <h1 class="community-heading1 thq-heading-2">
                <slot name="heading1">
                  <!--Default content for heading1-->
                  <div class="community-fragment16">
                    <span class="community-text24">Top News</span>
                  </div>
                </slot>
              </h1>
              <span class="thq-body-small">
                <slot name="content1">
                  <!--Default content for content1-->
                  <div class="community-fragment30">
                    <span class="community-text38">
                      Stay updated with the latest news from around the world.
                    </span>
                  </div>
                </slot>
              </span>
              <ul class="community-ul4 thq-flex-column">
                <li class="list-item">
                  <h1 class="thq-heading-3">
                    <slot name="heading2">
                      <!--Default content for heading2-->
                      <div class="community-fragment25">
                        <span class="community-text33">Customized Feeds</span>
                      </div>
                    </slot>
                  </h1>
                  <p class="thq-body-small">
                    <slot name="content2">
                      <!--Default content for content2-->
                      <div class="community-fragment10">
                        <span class="community-text18">content</span>
                      </div>
                    </slot>
                  </p>
                </li>
                <li class="list-item">
                  <h1 class="thq-heading-3">
                    <slot name="heading3">
                      <!--Default content for heading3-->
                      <div class="community-fragment19">
                        <span class="community-text27">Email Integration</span>
                      </div>
                    </slot>
                  </h1>
                  <span class="thq-body-small">
                    <slot name="content3">
                      <!--Default content for content3-->
                      <div class="community-fragment28">
                        <span class="community-text36">
                          Manage all your email accounts within the app for
                          convenience.
                        </span>
                      </div>
                    </slot>
                  </span>
                </li>
                <li class="list-item">
                  <h1 class="thq-heading-3">
                    <slot name="heading4">
                      <!--Default content for heading4-->
                      <div class="community-fragment14">
                        <span class="community-text22">Sleek Design</span>
                      </div>
                    </slot>
                  </h1>
                  <span class="thq-body-small">
                    <slot name="content4">
                      <!--Default content for content4-->
                      <div class="community-fragment29">
                        <span class="community-text37">
                          Enjoy a modern and intuitive user interface for a
                          seamless reading experience.
                        </span>
                      </div>
                    </slot>
                  </span>
                </li>
                <li class="list-item">
                  <h1 class="thq-heading-3">
                    <slot name="heading5">
                      <!--Default content for heading5-->
                      <div class="community-fragment15">
                        <span class="community-text23">Handpicked Content</span>
                      </div>
                    </slot>
                  </h1>
                  <span class="thq-body-small">
                    <slot name="content5">
                      <!--Default content for content5-->
                      <div class="community-fragment32">
                        <span class="community-text40">
                          Access curated content selected for its quality and
                          relevance.
                        </span>
                      </div>
                    </slot>
                  </span>
                </li>
                <li class="list-item">
                  <h1 class="thq-heading-3">
                    <slot name="heading6">
                      <!--Default content for heading6-->
                      <div class="community-fragment12">
                        <span class="community-text20">
                          Cross-Platform Support
                        </span>
                      </div>
                    </slot>
                  </h1>
                  <span class="thq-body-small">
                    <slot name="content6">
                      <!--Default content for content6-->
                      <div class="community-fragment31">
                        <span class="community-text39">
                          Use Feedbox on both iOS and Android devices for
                          flexibility.
                        </span>
                      </div>
                    </slot>
                  </span>
                </li>
              </ul>
            </li>
          </ul>
        </div>
        <div v-if="isRefundVisible" class="community-container5">
          <ul class="community-ul5 thq-flex-column">
            <li class="community-li19 thq-flex-column list-item">
              <h1 class="community-heading10 thq-heading-2">
                <slot name="heading10">
                  <!--Default content for heading10-->
                  <div class="community-fragment35">
                    <span class="community-text43">Notification Alerts</span>
                  </div>
                </slot>
              </h1>
              <span class="thq-body-small">
                <slot name="content10">
                  <!--Default content for content10-->
                  <div class="community-fragment22">
                    <span class="community-text30">
                      Receive notifications for new content or important news
                      updates.
                    </span>
                  </div>
                </slot>
              </span>
              <ul class="community-ul6 thq-flex-column">
                <li class="list-item">
                  <h1 class="thq-heading-3">
                    <slot name="heading11">
                      <!--Default content for heading11-->
                      <div class="community-fragment39">
                        <span class="community-text47">
                          Social Media Integration
                        </span>
                      </div>
                    </slot>
                  </h1>
                  <span class="thq-body-small">
                    <slot name="content11">
                      <!--Default content for content11-->
                      <div class="community-fragment38">
                        <span class="community-text46">
                          Share interesting articles directly from Feedbox to your
                          social media accounts.
                        </span>
                      </div>
                    </slot>
                  </span>
                </li>
                <li class="list-item">
                  <h1 class="thq-heading-3">
                    <slot name="heading12">
                      <!--Default content for heading12-->
                      <div class="community-fragment27">
                        <span class="community-text35">Night Mode</span>
                      </div>
                    </slot>
                  </h1>
                  <span class="thq-body-small">
                    <slot name="content12">
                      <!--Default content for content12-->
                      <div class="community-fragment18">
                        <span class="community-text26">
                          Switch to a darker theme for comfortable reading in
                          low-light environments.
                        </span>
                      </div>
                    </slot>
                  </span>
                </li>
                <li class="list-item">
                  <h1 class="thq-heading-3">
                    <slot name="heading13">
                      <!--Default content for heading13-->
                      <div class="community-fragment36">
                        <span class="community-text44">Offline Reading</span>
                      </div>
                    </slot>
                  </h1>
                  <span class="thq-body-small">
                    <slot name="content13">
                      <!--Default content for content13-->
                      <div class="community-fragment34">
                        <span class="community-text42">
                          Access your saved content even without an internet
                          connection.
                        </span>
                      </div>
                    </slot>
                  </span>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
      <div class="community-container6 thq-flex-column">
        <button
          @click="handleButtonClick"
          v-if="isTermsVisible"
          class="thq-button-filled"
        >
          <span>
            <slot name="button">
              <!--Default content for button-->
              <div><span>Study</span></div>
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
              <div class="community-fragment23">
                <span class="community-text31">Study</span>
              </div>
            </slot>
          </span>
        </button>
        <button
          @click="handleButtonClick"
          v-if="!isPrivacyVisible"
          class="thq-button-outline"
        >
          <span>
            <slot name="button1">
              <!--Default content for button1-->
              <div><span>Q&amp;A</span></div>
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
              <div class="community-fragment17">
                <span class="community-text25">Q&amp;A</span>
              </div>
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
              <div><span>challenge</span></div>
            </slot>
          </span>
        </button>
        <button class="thq-button-outline">
          <span>
            <slot name="button21">
              <!--Default content for button21-->
              <div class="community-fragment24">
                <span class="community-text32">materials</span>
              </div>
            </slot>
          </span>
        </button>
        <button class="thq-button-outline">
          <span>
            <slot name="button211">
              <!--Default content for button211-->
              <div class="community-fragment20">
                <span class="community-text28">chatting</span>
              </div>
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
              <div class="community-fragment21">
                <span class="community-text29">challenge</span>
              </div>
            </slot>
          </span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Community',
  props: {
    rootClassName: String,
  },
  data() {
    return {
      isRefundVisible: false,
      isPrivacyVisible: false,
      isTermsVisible: true,
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
.community-container1 {
  width: 100%;
  height: 1287px;
  display: flex;
  position: relative;
  align-items: center;
  flex-direction: column;
}
.community-max-width {
  width: 1194px;
  height: 1164px;
  display: flex;
  position: relative;
  max-width: var(--dl-size-size-maxwidth);
  align-items: flex-start;
  flex-direction: row;
  justify-content: flex-start;
}
.community-container2 {
  top: 0px;
  left: 279px;
  width: auto;
  bottom: 0px;
  height: 1195px;
  margin: auto;
  padding: var(--dl-space-space-twounits);
  position: absolute;
  align-items: flex-start;
}
.community-container3 {
  align-self: stretch;
  align-items: flex-start;
}
.community-ul1 {
  align-items: flex-start;
}
.community-li10 {
  align-items: flex-start;
}
.community-heading7 {
  align-self: center;
  text-align: center;
}
.community-ul2 {
  align-items: flex-start;
  padding-left: var(--dl-space-space-fiveunits);
}
.community-container4 {
  align-self: stretch;
  align-items: flex-start;
}
.community-li13 {
  align-items: flex-start;
}
.community-heading1 {
  align-self: center;
  text-align: center;
}
.community-ul4 {
  align-items: flex-start;
  padding-left: var(--dl-space-space-fiveunits);
}
.community-container5 {
  align-self: stretch;
  align-items: flex-start;
}
.community-ul5 {
  align-items: flex-start;
}
.community-li19 {
  align-items: flex-start;
}
.community-heading10 {
  align-self: center;
  text-align: center;
}
.community-ul6 {
  align-items: flex-start;
  padding-left: var(--dl-space-space-fiveunits);
}
.community-container6 {
  flex: 0 0 auto;
  width: auto;
  height: 445px;
  display: flex;
  align-items: stretch;
  padding-top: var(--dl-space-space-threeunits);
  flex-direction: column;
  justify-content: center;
}
.community-fragment10 {
  display: contents;
}
.community-text18 {
  display: inline-block;
}
.community-fragment11 {
  display: contents;
}
.community-text19 {
  display: inline-block;
}
.community-fragment12 {
  display: contents;
}
.community-text20 {
  display: inline-block;
}
.community-fragment13 {
  display: contents;
}
.community-text21 {
  display: inline-block;
}
.community-fragment14 {
  display: contents;
}
.community-text22 {
  display: inline-block;
}
.community-fragment15 {
  display: contents;
}
.community-text23 {
  display: inline-block;
}
.community-fragment16 {
  display: contents;
}
.community-text24 {
  display: inline-block;
}
.community-fragment17 {
  display: contents;
}
.community-text25 {
  display: inline-block;
}
.community-fragment18 {
  display: contents;
}
.community-text26 {
  display: inline-block;
}
.community-fragment19 {
  display: contents;
}
.community-text27 {
  display: inline-block;
}
.community-fragment20 {
  display: contents;
}
.community-text28 {
  display: inline-block;
}
.community-fragment21 {
  display: contents;
}
.community-text29 {
  display: inline-block;
}
.community-fragment22 {
  display: contents;
}
.community-text30 {
  display: inline-block;
}
.community-fragment23 {
  display: contents;
}
.community-text31 {
  display: inline-block;
}
.community-fragment24 {
  display: contents;
}
.community-text32 {
  display: inline-block;
}
.community-fragment25 {
  display: contents;
}
.community-text33 {
  display: inline-block;
}
.community-fragment26 {
  display: contents;
}
.community-text34 {
  display: inline-block;
}
.community-fragment27 {
  display: contents;
}
.community-text35 {
  display: inline-block;
}
.community-fragment28 {
  display: contents;
}
.community-text36 {
  display: inline-block;
}
.community-fragment29 {
  display: contents;
}
.community-text37 {
  display: inline-block;
}
.community-fragment30 {
  display: contents;
}
.community-text38 {
  display: inline-block;
}
.community-fragment31 {
  display: contents;
}
.community-text39 {
  display: inline-block;
}
.community-fragment32 {
  display: contents;
}
.community-text40 {
  display: inline-block;
}
.community-fragment33 {
  display: contents;
}
.community-text41 {
  display: inline-block;
}
.community-fragment34 {
  display: contents;
}
.community-text42 {
  display: inline-block;
}
.community-fragment35 {
  display: contents;
}
.community-text43 {
  display: inline-block;
}
.community-fragment36 {
  display: contents;
}
.community-text44 {
  display: inline-block;
}
.community-fragment37 {
  display: contents;
}
.community-text45 {
  display: inline-block;
}
.community-fragment38 {
  display: contents;
}
.community-text46 {
  display: inline-block;
}
.community-fragment39 {
  display: contents;
}
.community-text47 {
  display: inline-block;
}

@media(max-width: 767px) {
  .community-max-width {
    align-items: center;
    flex-direction: column;
  }
  .community-container2 {
    padding-left: 0px;
    padding-right: 0px;
  }
  .community-ul2 {
    padding-left: var(--dl-space-space-threeunits);
  }
  .community-ul4 {
    padding-left: var(--dl-space-space-threeunits);
  }
  .community-ul6 {
    padding-left: var(--dl-space-space-threeunits);
  }
  .community-container6 {
    align-self: center;
  }
}
@media(max-width: 479px) {
  .community-max-width {
    flex-direction: column;
  }
  .community-ul2 {
    padding-left: var(--dl-space-space-oneandhalfunits);
  }
  .community-ul4 {
    padding-left: var(--dl-space-space-oneandhalfunits);
  }
  .community-ul6 {
    padding-left: var(--dl-space-space-oneandhalfunits);
  }
  .community-container6 {
    align-self: center;
  }
}
</style>
