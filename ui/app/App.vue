<template>
  <div class="row constable-app">
    <login-container></login-container>
  </div>
</template>

<script>
  import LoginContainer from './containers/LoginContainer.vue';

  export default {
    components: {
      LoginContainer
    },
    data () {
      return {}
    }
  }
</script>

<style lang="scss">
  @import 'node_modules/font-awesome/scss/font-awesome.scss';
</style>