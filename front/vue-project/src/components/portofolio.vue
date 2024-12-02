<template>
  <div
    class="portofolio-portofolio section-container"
    v-bind:class="rootClassName"
  >
    <div class="portofolio-max-width max-content-container">
      <div class="portofolio-tab-selector-cards-container">
        <portofolio-card
          imageSrc="/external/unsplash_qj15unotnh0-400h-200h.png"
          rootClassName="portofolio-cardroot-class-name"
        ></portofolio-card>
        <portofolio-card
          imageSrc="/external/unsplash_wwqrpsnbpq4-400h-200h.png"
          projectTitle="A brand-new advertising idea"
          rootClassName="portofolio-cardroot-class-name5"
        ></portofolio-card>
        <portofolio-card
          imageSrc="https://images.unsplash.com/photo-1622483767028-3f66f32aef97?ixid=Mnw5MTMyMXwwfDF8c2VhcmNofDEzfHxjb2NhJTIwY29sYXxlbnwwfHx8fDE2NDY5MjYyNTM&amp;ixlib=rb-1.2.1&amp;h=400"
          projectTitle="Coca-Cola Summer Concept Campaign - 2021"
          rootClassName="portofolio-cardroot-class-name4"
        ></portofolio-card>
        <portofolio-card
          imageSrc="https://images.unsplash.com/photo-1519420573924-65fcd45245f8?ixid=Mnw5MTMyMXwwfDF8c2VhcmNofDJ8fG51dGVsbGF8ZW58MHx8fHwxNjQ2OTI2MTky&amp;ixlib=rb-1.2.1&amp;h=400"
          projectTitle="Ad Campaign - I love you as much as I love Nutella"
          rootClassName="portofolio-cardroot-class-name3"
        ></portofolio-card>
        <portofolio-card
          imageSrc="https://images.unsplash.com/photo-1567103472667-6898f3a79cf2?ixid=Mnw5MTMyMXwwfDF8c2VhcmNofDd8fGNvY2ElMjBjb2xhfGVufDB8fHx8MTY0NjkyNjI1Mw&amp;ixlib=rb-1.2.1&amp;h=400"
          projectTitle="Coca-Colla Next Door Campaign - conceptual"
          rootClassName="portofolio-cardroot-class-name2"
        ></portofolio-card>
        <portofolio-card
          imageSrc="https://images.unsplash.com/photo-1545231027-637d2f6210f8?ixid=Mnw5MTMyMXwwfDF8c2VhcmNofDF8fHN0YXJidWNrc3xlbnwwfHx8fDE2NDY5MjYyMzc&amp;ixlib=rb-1.2.1&amp;h=400"
          projectTitle="Starbucks secret is a smile when you get your latte"
          rootClassName="portofolio-cardroot-class-name1"
        ></portofolio-card>
      </div>
    </div>
  </div>
</template>

<script>
import PortofolioCard from './portofolio-card'

export default {
  name: 'Portofolio',
  props: {
    rootClassName: String,
  },
  components: {
    PortofolioCard,
  },
}
</script>

<style scoped>
.portofolio-portofolio {
  height: 1076px;
  position: relative;
}
.portofolio-max-width {
  width: 1002px;
  height: 858px;
  margin-top: var(--dl-space-space-oneandhalfunits);
  flex-direction: column;
}
.portofolio-tab-selector-cards-container {
  width: 100%;
  display: grid;
  grid-row-gap: 40px;
  grid-column-gap: 20px;
  grid-template-rows: repeat(2, 1fr);
  grid-template-columns: repeat(3, 1fr);
}

@media(max-width: 991px) {
  .portofolio-tab-selector-cards-container {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media(max-width: 767px) {
  .portofolio-tab-selector-cards-container {
    grid-template-columns: 1fr;
  }
}
</style>
