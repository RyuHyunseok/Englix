<template>
  <nav class="navigation-links-nav" v-bind:class="rootClassName">
    <span class="navbar-link">{{ text }}</span>
    <span class="navigation-links-text2 navbar-link">{{ text1 }}</span>
    <span class="navigation-links-text3 navbar-link">{{ text2 }}</span>
    <span class="navigation-links-text4 navbar-link">{{ text3 }}</span>
    <span class="navigation-links-text5 navbar-link">{{ text4 }}</span>
  </nav>
</template>

<script>
export default {
  name: 'NavigationLinks',
  props: {
    text2: {
      type: String,
      default: 'Features',
    },
    text3: {
      type: String,
      default: 'Blog',
    },
    rootClassName: String,
    text4: {
      type: String,
      default: 'Pricing',
    },
    text: {
      type: String,
      default: 'Home',
    },
    text1: {
      type: String,
      default: 'About',
    },
  },
}
</script>

<style scoped>
.navigation-links-nav {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  flex-direction: row;
}
.navigation-links-text2 {
  margin-left: var(--dl-space-space-twounits);
}
.navigation-links-text3 {
  margin-left: var(--dl-space-space-twounits);
}
.navigation-links-text4 {
  margin-left: var(--dl-space-space-twounits);
}
.navigation-links-text5 {
  margin-left: var(--dl-space-space-twounits);
}








@media(max-width: 767px) {
  .navigation-links-nav {
    align-items: flex-start;
    flex-direction: column;
  }
  .navigation-links-text2 {
    margin-left: 0;
    margin-bottom: var(--dl-space-space-unit);
  }
  .navigation-links-text3 {
    margin-left: 0;
    margin-bottom: var(--dl-space-space-unit);
  }
  .navigation-links-text4 {
    margin-left: 0;
    margin-bottom: var(--dl-space-space-unit);
  }
  .navigation-links-text5 {
    margin-left: 0;
    margin-bottom: var(--dl-space-space-unit);
  }
}
</style>
