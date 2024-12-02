<template>
  <div
    class="blog-post-header11-blog-post-header3 thq-section-padding"
    v-bind:class="rootClassName"
  >
    <div class="blog-post-header11-max-width thq-section-max-width">
      <div class="blog-post-header11-content1 thq-flex-row">
        <img
          :alt="blogPostImageAlt"
          :src="blogPostImageSrc"
          class="blog-post-header11-image1 thq-img-ratio-4-3"
        />
        <div class="blog-post-header11-section-title thq-flex-column">
          <div class="blog-post-header11-content2">
            <h1 class="blog-post-header11-title thq-heading-1">
              <slot name="blogPostTitle">
                <!--Default content for blogPostTitle-->
                <div class="blog-post-header11-fragment4">
                  <span class="blog-post-header11-text7">Movie Title</span>
                </div>
              </slot>
            </h1>
            <div class="blog-post-header11-author">
              <span class="thq-body-small">By</span>
              <span class="thq-body-small">
                <slot name="avatarName">
                  <!--Default content for avatarName-->
                  <div class="blog-post-header11-fragment1">
                    <span class="blog-post-header11-text4">
                      AdventureExplorer
                    </span>
                  </div>
                </slot>
              </span>
            </div>
            <div class="blog-post-header11-time">
              <span class="thq-body-small">
                <slot name="date">
                  <!--Default content for date-->
                  <div class="blog-post-header11-fragment3">
                    <span class="blog-post-header11-text6">
                      September 15, 2022
                    </span>
                  </div>
                </slot>
              </span>
              <span class="thq-body-small">•</span>
              <span class="thq-body-small">
                <slot name="readTime">
                  <!--Default content for readTime-->
                  <div class="blog-post-header11-fragment2">
                    <span class="blog-post-header11-text5">130minutes</span>
                  </div>
                </slot>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BlogPostHeader11',
  props: {
    rootClassName: String,
    blogPostImageSrc: {
      type: String,
      default:
        'https://images.unsplash.com/photo-1485846234645-a62644f84728?ixid=M3w5MTMyMXwwfDF8c2VhcmNofDF8fE1PVklFfGVufDB8fHx8MTczMTkxODA3Mnww&ixlib=rb-4.0.3&w=1200',
    },
    blogPostImageAlt: {
      type: String,
      default: 'Adventure Seekers Travel Destinations',
    },
  },
}
</script>

<style scoped>
.blog-post-header11-blog-post-header3 {
  height: 1717px;
  display: flex;
  position: relative;
  align-items: center;
}
.blog-post-header11-max-width {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  flex-direction: column;
}
.blog-post-header11-content1 {
  width: 100%;
  height: 429px;
  display: flex;
}
.blog-post-header11-image1 {
  flex: 1;
  width: 501px;
  height: 100%;
}
.blog-post-header11-section-title {
  flex: 1;
  width: 50%;
  flex-direction: column;
  justify-content: space-between;
}
.blog-post-header11-content2 {
  gap: var(--dl-space-space-oneandhalfunits);
  display: flex;
  align-items: center;
  flex-direction: column;
}
.blog-post-header11-title {
  text-align: center;
}
.blog-post-header11-author {
  gap: var(--dl-space-space-halfunit);
  display: flex;
}
.blog-post-header11-time {
  gap: var(--dl-space-space-halfunit);
  display: flex;
  align-items: center;
}
.blog-post-header11-fragment1 {
  display: contents;
}
.blog-post-header11-text4 {
  display: inline-block;
}
.blog-post-header11-fragment2 {
  display: contents;
}
.blog-post-header11-text5 {
  display: inline-block;
}
.blog-post-header11-fragment3 {
  display: contents;
}
.blog-post-header11-text6 {
  display: inline-block;
}
.blog-post-header11-fragment4 {
  display: contents;
}
.blog-post-header11-text7 {
  display: inline-block;
}
.blog-post-header11root-class-name {
  background-color: var(--dl-color-theme-neutral-light);
}
@media(max-width: 991px) {
  .blog-post-header11-content1 {
    flex-direction: column;
  }
  .blog-post-header11-image1 {
    width: 100%;
  }
  .blog-post-header11-section-title {
    width: 100%;
  }
}
@media(max-width: 767px) {
  .blog-post-header11-content1 {
    flex-direction: column;
  }
}
@media(max-width: 479px) {
  .blog-post-header11-content2 {
    align-items: center;
  }
}
</style>
