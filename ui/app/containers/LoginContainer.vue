<template>
  <div class="row">
    <div class="columns medium-8 login">
      <h1 class="contrast">Login</h1>
      <phila-alert :success="success">Login successful!</phila-alert>
      <phila-alert :error="error">{{ error }}</phila-alert>
      <login-form :onSubmit="submitLogin"></login-form>
      Don't have a login? <router-link to="/registration">Register</router-link>
    </div>
  </div>
</template>

<script>
  import { mapState, mapActions } from 'vuex'

  import PhilaAlert from '../components/phila/PhilaAlert.vue'
  import LoginForm from '../components/LoginForm.vue';

  export default {
    components: {
      PhilaAlert,
      LoginForm
    },
    computed: mapState('login', {
      error: state => state.error,
      success: state => state.success
    }),
    methods: mapActions('login', [
      'submitLogin'
    ])
  }
</script>

<style lang="css">
  .login {
    margin: 2rem auto;
    float: none;
  }
</style>