<template>
  <div class="row">
    <div class="columns medium-8 login">
      <h1 class="contrast">Login</h1>
      <login-form
        :onSubmit="submitLogin"></login-form>
    </div>
  </div>
</template>

<script>
  import { mapActions } from 'vuex'

  import LoginForm from '../components/LoginForm.vue';

  export default {
    components: {
      LoginForm
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
    margin: 2rem auto;
    float: none;
  }
</style>