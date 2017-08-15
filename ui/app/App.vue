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

<style lang="css">
  .constable-app {
    margin-top: 20px;
  }
</style>