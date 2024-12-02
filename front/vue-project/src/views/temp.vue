<template>
    <div class="home-container">
      <div class="home-main1 section-container">
        <div class="home-max-width1 max-content-container">
          <h2 class="home-text10 Heading2">
            <span>JUST</span>
            <span class="home-text12"> FOR you.</span>
          </h2>
          <grid-card rootClassName="grid-cardroot-class-name1">
            <template v-slot:button1>
              <div class="home-fragment10">
                <span class="home-text13">TOEIC</span>
              </div>
            </template>
            <template v-slot:button11>
              <div class="home-fragment11">
                <span class="home-text14">수능</span>
              </div>
            </template>
            <template v-slot:button12>
              <div class="home-fragment12">
                <span class="home-text15">BUSINESS</span>
              </div>
            </template>
          </grid-card>
        </div>
      </div>
      <main class="home-main2">
        <div class="home-section-six section-container">
          <div class="home-max-width2 max-content-container">
            <h2 class="home-text16">
              <span class="Heading2">JUST</span>
              <span class="Heading2"> </span>
              <span class="home-text19">FOR you.</span>
            </h2>
          </div>
          <grid-card text="WHAT'S YOUR LEVEL?" rootClassName="grid-cardroot-class-name2">
            <template v-slot:button1>
              <div class="home-fragment13">
                <span class="home-text20">초급</span>
              </div>
            </template>
            <template v-slot:button11>
              <div class="home-fragment14">
                <span class="home-text21">고급</span>
              </div>
            </template>
            <template v-slot:button12>
              <div class="home-fragment15">
                <span class="home-text22">중급</span>
              </div>
            </template>
          </grid-card>
        </div>
      </main>
      <blog-post-header11 rootClassName="blog-post-header11root-class-name">
        <template v-slot:date>
          <div class="home-fragment16">
            <span class="home-text23">September 15, 2022</span>
          </div>
        </template>
        <template v-slot:readTime>
          <div class="home-fragment17">
            <span class="home-text24">130minutes</span>
          </div>
        </template>
        <template v-slot:avatarName>
          <div class="home-fragment18">
            <span class="home-text25">AdventureExplorer</span>
          </div>
        </template>
        <template v-slot:blogPostTitle>
          <div class="home-fragment19">
            <span class="home-text26">Movie Title</span>
          </div>
        </template>
      </blog-post-header11>
      <blog-post-header12 rootClassName="blog-post-header12root-class-name">
        <template v-slot:date>
          <div class="home-fragment20">
            <span class="home-text27">September 15, 2022</span>
          </div>
        </template>
        <template v-slot:readTime>
          <div class="home-fragment21">
            <span class="home-text28">150 minutes</span>
          </div>
        </template>
        <template v-slot:avatarName>
          <div class="home-fragment22"><span class="home-text29">GENRE</span></div>
        </template>
        <template v-slot:blogPostTitle>
          <div class="home-fragment23">
            <span class="home-text30">Movie Title</span>
          </div>
        </template>
      </blog-post-header12>
    </div>
  </template>
  
  <script setup>
  import gridCard from "@/components/grid-card.vue";
  import blogPostHeader11 from "@/components/blog-post-header11.vue";
  import blogPostHeader12 from "@/components/blog-post-header12.vue";
  </script>
  
  <style scoped>
  .page-container {
    padding: 20px;
  }
  
  .home-container {
    width: 100%;
    display: flex;
    position: relative;
    min-height: 100vh;
    overflow-x: hidden;
    align-items: center;
    flex-direction: column;
    justify-content: flex-start;
    background-color: var(--dl-color-backgrounds-green);
  }
  .home-main1 {
    height: 893px;
    padding-bottom: 0px;
  }
  .home-max-width1 {
    display: flex;
    align-items: center;
    flex-direction: column;
    justify-content: center;
  }
  .home-text10 {
    text-align: center;
    margin-bottom: var(--dl-space-space-threeunits);
  }
  .home-text12 {
    color: var(--dl-color-backgrounds-primary);
  }
  .home-fragment10 {
    display: contents;
  }
  .home-text13 {
    display: inline-block;
  }
  .home-fragment11 {
    display: contents;
  }
  .home-text14 {
    display: inline-block;
  }
  .home-fragment12 {
    display: contents;
  }
  .home-text15 {
    display: inline-block;
  }
  .home-main2 {
    flex: 0 0 auto;
    width: 100%;
    display: flex;
    position: relative;
    align-items: center;
    flex-direction: center;
    justify-content: center;
  }
  .home-section-six {
    height: 914px;
    display: flex;
    align-items: center;
    padding-top: var(--dl-space-space-threeunits);
    flex-direction: flex;
    padding-bottom: 0px;
    justify-content: center;
    background-color: var(--dl-color-backgrounds-primary);
  }
  .home-max-width2 {
    align-items: center;
    justify-content: center;
  }
  .home-text16 {
    font-size: 42px;
    font-style: normal;
    text-align: center;
    font-family: "Lexend";
    font-weight: 600;
    line-height: 1.3;
    margin-bottom: var(--dl-space-space-threeunits);
    text-transform: none;
    text-decoration: none;
  }
  .home-text19 {
    color: var(--dl-color-backgrounds-green);
  }
  .home-fragment13 {
    display: contents;
  }
  .home-text20 {
    display: inline-block;
  }
  .home-fragment14 {
    display: contents;
  }
  .home-text21 {
    display: inline-block;
  }
  .home-fragment15 {
    display: contents;
  }
  .home-text22 {
    display: inline-block;
  }
  .home-fragment16 {
    display: contents;
  }
  .home-text23 {
    display: inline-block;
  }
  .home-fragment17 {
    display: contents;
  }
  .home-text24 {
    display: inline-block;
  }
  .home-fragment18 {
    display: contents;
  }
  .home-text25 {
    display: inline-block;
  }
  .home-fragment19 {
    display: contents;
  }
  .home-text26 {
    display: inline-block;
  }
  .home-fragment20 {
    display: contents;
  }
  .home-text27 {
    display: inline-block;
  }
  .home-fragment21 {
    display: contents;
  }
  .home-text28 {
    display: inline-block;
  }
  .home-fragment22 {
    display: contents;
  }
  .home-text29 {
    display: inline-block;
  }
  .home-fragment23 {
    display: contents;
  }
  .home-text30 {
    display: inline-block;
  }
  @media (max-width: 991px) {
    .home-max-width2 {
      flex-direction: column;
    }
  }
  @media (max-width: 767px) {
    .home-text10 {
      margin-bottom: var(--dl-space-space-twounits);
    }
    .home-text16 {
      margin-bottom: var(--dl-space-space-twounits);
    }
  }
  </style>
  