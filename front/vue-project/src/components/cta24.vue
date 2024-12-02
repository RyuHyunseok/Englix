<template>
  <div class="cta24-container10 thq-section-padding">
    <div class="cta24-max-width thq-section-max-width">
      <div class="cta24-container11">
        <div class="cta24-content">
          <div v-if="link1Selector" class="cta24-container12">
            <span class="thq-body-small">01</span>
            <h2 class="cta24-text11 thq-heading-2">
              <slot name="link1">
                <!--Default content for link1-->
                <div class="cta24-fragment1">
                  <span class="cta24-text26">Click link one</span>
                </div>
              </slot>
            </h2>
          </div>
          <div
            @click="handleContainerClick"
            v-if="!link1Selector"
            class="cta24-container13"
          >
            <span class="thq-body-small">01</span>
            <h2 class="thq-heading-2">
              <slot name="link11">
                <!--Default content for link11-->
                <div class="cta24-fragment3">
                  <span class="cta24-text28">Click link one</span>
                </div>
              </slot>
            </h2>
          </div>
          <div v-if="link2Selector" class="cta24-container14">
            <span class="thq-body-small">02</span>
            <h2 class="cta24-text15 thq-heading-2">
              <slot name="link2">
                <!--Default content for link2-->
                <div class="cta24-fragment5">
                  <span class="cta24-text30">Click link two</span>
                </div>
              </slot>
            </h2>
          </div>
          <div
            @click="handleContainerClick"
            v-if="!link2Selector"
            class="cta24-container15"
          >
            <span class="thq-body-small">02</span>
            <h2 class="thq-heading-2">
              <slot name="link21">
                <!--Default content for link21-->
                <div class="cta24-fragment4">
                  <span class="cta24-text29">Click link two</span>
                </div>
              </slot>
            </h2>
          </div>
          <div v-if="link3Selector" class="cta24-container16">
            <span class="thq-body-small">03</span>
            <h2 class="cta24-text19 thq-heading-2">
              <slot name="link3">
                <!--Default content for link3-->
                <div class="cta24-fragment6">
                  <span class="cta24-text31">Click link three</span>
                </div>
              </slot>
            </h2>
          </div>
          <div
            @click="handleContainerClick"
            v-if="!link3Selector"
            class="cta24-container17"
          >
            <span class="thq-body-small">03</span>
            <h2 class="thq-heading-2">
              <slot name="link31">
                <!--Default content for link31-->
                <div class="cta24-fragment7">
                  <span class="cta24-text32">Click link three</span>
                </div>
              </slot>
            </h2>
          </div>
          <div v-if="link4Selector" class="cta24-container18">
            <span class="thq-body-small">04</span>
            <h2 class="cta24-text23 thq-heading-2">
              <slot name="link4">
                <!--Default content for link4-->
                <div class="cta24-fragment2">
                  <span class="cta24-text27">Click link four</span>
                </div>
              </slot>
            </h2>
          </div>
          <div
            @click="handleContainerClick"
            v-if="!link4Selector"
            class="cta24-container19"
          >
            <span class="thq-body-small">04</span>
            <h2 class="thq-heading-2">
              <slot name="link41">
                <!--Default content for link41-->
                <div class="cta24-fragment8">
                  <span class="cta24-text33">Click link four</span>
                </div>
              </slot>
            </h2>
          </div>
        </div>
        <img
          :alt="image1Alt"
          :src="image1Src"
          v-if="link1Selector"
          class="cta24-image1 thq-img-ratio-1-1"
        />
        <img
          :alt="image2Alt"
          :src="image2Src"
          v-if="link2Selector"
          class="cta24-image2 thq-img-ratio-1-1"
        />
        <img
          :alt="image3Alt"
          :src="image3Src"
          v-if="link3Selector"
          class="cta24-image3 thq-img-ratio-1-1"
        />
        <img
          :alt="image4Alt"
          :src="image4Src"
          v-if="link4Selector"
          class="cta24-image4 thq-img-ratio-1-1"
        />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CTA24',
  props: {
    image4Alt: {
      type: String,
      default: 'image1Alt',
    },
    image3Src: {
      type: String,
      default:
        'https://images.unsplash.com/photo-1637308755606-266e7f2371d4?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5MTMyMXwwfDF8cmFuZG9tfHx8fHx8fHx8MTczMTkxODUxMXw&ixlib=rb-4.0.3&q=80&w=1080',
    },
    image4Src: {
      type: String,
      default:
        'https://images.unsplash.com/photo-1507209696998-3c532be9b2b5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5MTMyMXwwfDF8cmFuZG9tfHx8fHx8fHx8MTczMTkxODUxMXw&ixlib=rb-4.0.3&q=80&w=1080',
    },
    image2Alt: {
      type: String,
      default: 'image1Alt',
    },
    image3Alt: {
      type: String,
      default: 'image3Alt',
    },
    image2Src: {
      type: String,
      default:
        'https://images.unsplash.com/photo-1523044214787-9caaa5ee4d8e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5MTMyMXwwfDF8cmFuZG9tfHx8fHx8fHx8MTczMTkxODUxMnw&ixlib=rb-4.0.3&q=80&w=1080',
    },
    image1Src: {
      type: String,
      default:
        'https://images.unsplash.com/photo-1691510644964-33748b6cc4d0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w5MTMyMXwwfDF8cmFuZG9tfHx8fHx8fHx8MTczMTkxODUxMXw&ixlib=rb-4.0.3&q=80&w=1080',
    },
    image1Alt: {
      type: String,
      default: 'image1Alt',
    },
  },
  data() {
    return {
      link2Selector: false,
      link3Selector: false,
      link4Selector: false,
      link1Selector: true,
    }
  },
  methods: {
    handleContainerClick() {
      this.link2Selector = false
      this.link3Selector = false
      this.link1Selector = false
      this.link4Selector = true
    },
  },
}
</script>

<style scoped>
.cta24-container10 {
  width: 100%;
  position: relative;
}
.cta24-max-width {
  gap: var(--dl-space-space-fiveunits);
  width: 100%;
  height: auto;
  display: flex;
  overflow: hidden;
  position: relative;
  max-width: var(--dl-size-size-maxwidth);
  align-self: center;
  align-items: flex-start;
  justify-content: flex-start;
}
.cta24-container11 {
  width: 100%;
  display: flex;
  align-items: center;
}
.cta24-content {
  flex: 1;
  width: 100%;
  display: flex;
  align-self: center;
  align-items: flex-start;
  flex-direction: column;
}
.cta24-container12 {
  gap: var(--dl-space-space-twounits);
  cursor: pointer;
  display: flex;
  align-self: stretch;
  align-items: center;
  flex-shrink: 0;
  padding-top: var(--dl-space-space-oneandhalfunits);
  border-color: var(--dl-color-theme-neutral-dark);
  border-style: solid;
  border-width: 1px 0;
  padding-bottom: var(--dl-space-space-oneandhalfunits);
}
.cta24-text11 {
  color: var(--dl-color-theme-accent1);
}
.cta24-container13 {
  gap: var(--dl-space-space-twounits);
  cursor: pointer;
  display: flex;
  align-self: stretch;
  align-items: center;
  flex-shrink: 0;
  padding-top: var(--dl-space-space-oneandhalfunits);
  border-color: var(--dl-color-theme-neutral-dark);
  border-style: solid;
  border-width: 1px 0;
  padding-bottom: var(--dl-space-space-oneandhalfunits);
}
.cta24-container14 {
  gap: var(--dl-space-space-twounits);
  cursor: pointer;
  display: flex;
  align-self: stretch;
  align-items: center;
  flex-shrink: 0;
  padding-top: var(--dl-space-space-oneandhalfunits);
  border-color: var(--dl-color-theme-neutral-dark);
  border-style: solid;
  border-width: 0 0 1px;
  padding-bottom: var(--dl-space-space-oneandhalfunits);
}
.cta24-text15 {
  color: var(--dl-color-theme-accent1);
}
.cta24-container15 {
  gap: var(--dl-space-space-twounits);
  cursor: pointer;
  display: flex;
  align-self: stretch;
  align-items: center;
  flex-shrink: 0;
  padding-top: var(--dl-space-space-oneandhalfunits);
  border-color: var(--dl-color-theme-neutral-dark);
  border-style: solid;
  border-width: 0 0 1px;
  padding-bottom: var(--dl-space-space-oneandhalfunits);
}
.cta24-container16 {
  gap: var(--dl-space-space-twounits);
  cursor: pointer;
  display: flex;
  align-self: stretch;
  align-items: center;
  flex-shrink: 0;
  padding-top: var(--dl-space-space-oneandhalfunits);
  border-color: var(--dl-color-theme-neutral-dark);
  border-style: solid;
  border-width: 0 0 1px;
  padding-bottom: var(--dl-space-space-oneandhalfunits);
}
.cta24-text19 {
  color: var(--dl-color-theme-accent1);
}
.cta24-container17 {
  gap: var(--dl-space-space-twounits);
  cursor: pointer;
  display: flex;
  align-self: stretch;
  align-items: center;
  flex-shrink: 0;
  padding-top: var(--dl-space-space-oneandhalfunits);
  border-color: var(--dl-color-theme-neutral-dark);
  border-style: solid;
  border-width: 0 0 1px;
  padding-bottom: var(--dl-space-space-oneandhalfunits);
}
.cta24-container18 {
  gap: var(--dl-space-space-twounits);
  cursor: pointer;
  display: flex;
  align-self: stretch;
  align-items: center;
  flex-shrink: 0;
  padding-top: var(--dl-space-space-oneandhalfunits);
  border-color: var(--dl-color-theme-neutral-dark);
  border-style: solid;
  border-width: 0 0 1px;
  padding-bottom: var(--dl-space-space-oneandhalfunits);
}
.cta24-text23 {
  color: var(--dl-color-theme-accent1);
}
.cta24-container19 {
  gap: var(--dl-space-space-twounits);
  cursor: pointer;
  display: flex;
  align-self: stretch;
  align-items: center;
  flex-shrink: 0;
  padding-top: var(--dl-space-space-oneandhalfunits);
  border-color: var(--dl-color-theme-neutral-dark);
  border-style: solid;
  border-width: 0 0 1px;
  padding-bottom: var(--dl-space-space-oneandhalfunits);
}
.cta24-image1 {
  max-width: 410px;
}
.cta24-image2 {
  max-width: 410px;
}
.cta24-image3 {
  max-width: 410px;
}
.cta24-image4 {
  max-width: 410px;
}
.cta24-fragment1 {
  display: contents;
}
.cta24-text26 {
  display: inline-block;
}
.cta24-fragment2 {
  display: contents;
}
.cta24-text27 {
  display: inline-block;
}
.cta24-fragment3 {
  display: contents;
}
.cta24-text28 {
  display: inline-block;
}
.cta24-fragment4 {
  display: contents;
}
.cta24-text29 {
  display: inline-block;
}
.cta24-fragment5 {
  display: contents;
}
.cta24-text30 {
  display: inline-block;
}
.cta24-fragment6 {
  display: contents;
}
.cta24-text31 {
  display: inline-block;
}
.cta24-fragment7 {
  display: contents;
}
.cta24-text32 {
  display: inline-block;
}
.cta24-fragment8 {
  display: contents;
}
.cta24-text33 {
  display: inline-block;
}
@media(max-width: 991px) {
  .cta24-max-width {
    flex-direction: row;
  }
  .cta24-container11 {
    flex-direction: column;
  }
  .cta24-image2 {
    width: auto;
  }
  .cta24-image3 {
    width: auto;
  }
  .cta24-image4 {
    width: auto;
  }
}
@media(max-width: 767px) {
  .cta24-image1 {
    width: 100%;
  }
  .cta24-image2 {
    width: 100%;
  }
  .cta24-image3 {
    width: 100%;
  }
  .cta24-image4 {
    width: 100%;
  }
}
</style>
