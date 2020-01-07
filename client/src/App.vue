<template>
  <div id="app" class="container-fluid">
    <Nav />
    <router-view />
  </div>
</template>
<script>
import Nav from '@/components/Nav.vue';

export default {
  // Application entry point
  name: 'app',
  components: {
    Nav
  },
}
</script>
<style>
</style>
