<template>
  <div class="row">
    <login
      class="columns medium-8 login"
      :onSubmit="submitLogin"></login>
  </div>
</template>

<script>
  import { mapActions } from 'vuex'

  import Login from '../components/Login.vue';

  export default {
    components: {
      Login
    },
    methods: mapActions([
      'submitLogin'
    ]),
    data () {
      return {}
    }
  }
</script>

<style lang="css">
  .login {
    margin: 0 auto;
    float: none;
  }
</style>