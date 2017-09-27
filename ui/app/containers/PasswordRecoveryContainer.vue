<template>
  <div class="row">
    <div class="columns medium-8 float-center">
      <h1 class="contrast">Password Recovery</h1>
      <phila-alert :success="success">Please check your email to complete recovery.</phila-alert>
      <phila-alert :error="error">{{ error }}</phila-alert>
      <password-recovery-form v-if="!success" :onSubmit="submit"></password-recovery-form>
    </div>
  </div>
</template>

<script>
  import { mapState, mapActions } from 'vuex'

  import PhilaAlert from '../components/phila/PhilaAlert.vue'
  import PasswordRecoveryForm from '../components/PasswordRecoveryForm.vue';

  export default {
    components: {
      PhilaAlert,
      PasswordRecoveryForm
    },
    computed: mapState('passwordRecovery', {
      error: state => state.error,
      success: state => state.success
    }),
    methods: mapActions('passwordRecovery', [
      'submit'
    ])
  }
</script>

<style lang="css">
  .float-center {
    margin: 2rem auto;
    float: none;
  }
</style>