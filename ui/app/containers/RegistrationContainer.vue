<template>
  <div class="row">
    <registration class="columns medium-8" :onSubmit="submitRegistration"></registration>
  </div>
</template>

<script>
  import { mapActions } from 'vuex'

  import Registration from '../components/Registration.vue';

  export default {
    components: {
      Registration
    },
    methods: mapActions([
      'submitRegistration'
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