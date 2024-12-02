<template>
  <div
    class="blog-post-header12-blog-post-header3 thq-section-padding"
    v-bind:class="rootClassName"
  >
    <div class="blog-post-header12-max-width thq-section-max-width">
      <div class="blog-post-header12-category thq-flex-column"></div>
      <div class="blog-post-header12-content1 thq-flex-row">
        <div class="blog-post-header12-container">
          <video
            :src="videoSrc"
            loop="true"
            muted="true"
            :poster="videoPoster"
            autoplay="true"
            class="blog-post-header12-video"
          ></video>
        </div>
        <div class="blog-post-header12-section-title thq-flex-column">
          <h1 class="blog-post-header12-title thq-heading-1">
            <slot name="blogPostTitle">
              <!--Default content for blogPostTitle-->
              <div class="blog-post-header12-fragment1">
                <span class="blog-post-header12-text4">Movie Title</span>
              </div>
            </slot>
          </h1>
          <div class="blog-post-header12-content2">
            <div class="blog-post-header12-author">
              <span class="thq-body-small">DETAIL</span>
              <span class="thq-body-small">
                <slot name="avatarName">
                  <!--Default content for avatarName-->
                  <div class="blog-post-header12-fragment2">
                    <span class="blog-post-header12-text5">GENRE</span>
                  </div>
                </slot>
              </span>
            </div>
            <div class="blog-post-header12-time">
              <span class="thq-body-small">
                <slot name="date">
                  <!--Default content for date-->
                  <div class="blog-post-header12-fragment3">
                    <span class="blog-post-header12-text6">
                      September 15, 2022
                    </span>
                  </div>
                </slot>
              </span>
              <span class="thq-body-small">•</span>
              <span class="thq-body-small">
                <slot name="readTime">
                  <!--Default content for readTime-->
                  <div class="blog-post-header12-fragment4">
                    <span class="blog-post-header12-text7">150 minutes</span>
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
  name: 'BlogPostHeader12',
  props: {
    rootClassName: String,
    videoSrc: {
      type: String,
      default:
        'https://videos.pexels.com/video-files/2459029/2459029-hd_1280_720_60fps.mp4',
    },
    videoPoster: {
      type: String,
      default:
        'https://images.pexels.com/videos/2459029/pictures/preview-0.jpg',
    },
  },
}
</script>

<style scoped>
.blog-post-header12-blog-post-header3 {
  display: flex;
  position: relative;
  align-items: center;
}
.blog-post-header12-max-width {
  gap: var(--dl-space-space-oneandhalfunits);
  display: flex;
  align-items: center;
  flex-direction: column;
}
.blog-post-header12-category {
  border: 2px dashed rgba(120, 120, 120, 0.4);
}
.blog-post-header12-content1 {
  gap: var(--dl-space-space-threeunits);
  width: 100%;
}
.blog-post-header12-container {
  flex: 1;
  width: 100%;
  height: 560px;
  display: flex;
  align-self: center;
  align-items: center;
  justify-content: center;
}
.blog-post-header12-video {
  width: 666px;
  height: 400px;
  min-width: 300px;
}
.blog-post-header12-section-title {
  align-items: flex-start;
}
.blog-post-header12-title {
  text-align: center;
}
.blog-post-header12-content2 {
  display: flex;
  align-items: flex-start;
  flex-direction: column;
}
.blog-post-header12-author {
  gap: var(--dl-space-space-halfunit);
  display: flex;
}
.blog-post-header12-time {
  gap: 8px;
  display: flex;
  align-items: center;
}
.blog-post-header12-fragment1 {
  display: contents;
}
.blog-post-header12-text4 {
  display: inline-block;
}
.blog-post-header12-fragment2 {
  display: contents;
}
.blog-post-header12-text5 {
  display: inline-block;
}
.blog-post-header12-fragment3 {
  display: contents;
}
.blog-post-header12-text6 {
  display: inline-block;
}
.blog-post-header12-fragment4 {
  display: contents;
}
.blog-post-header12-text7 {
  display: inline-block;
}
.blog-post-header12root-class-name {
  background-color: #D9D9D9;
}
@media(max-width: 991px) {
  .blog-post-header12-content1 {
    gap: var(--dl-space-space-twounits);
  }
}
@media(max-width: 767px) {
  .blog-post-header12-content1 {
    gap: var(--dl-space-space-unit);
    flex-direction: column;
  }
  .blog-post-header12-container {
    width: 100%;
  }
}
@media(max-width: 479px) {
  .blog-post-header12-section-title {
    align-items: center;
  }
  .blog-post-header12-content2 {
    align-items: center;
  }
}
</style>
