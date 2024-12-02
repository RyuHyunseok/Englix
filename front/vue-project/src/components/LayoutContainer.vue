<template>
  <div class="layout-container">
    <slot></slot>
  </div>
</template>

<style scoped>
.layout-container {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: var(--content-padding);
  width: 100%;
  box-sizing: border-box;
}
</style>