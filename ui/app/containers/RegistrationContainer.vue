<template>
  <div>
    <div class="row">
      <div class="columns medium-14">
        <i class="fa fa-shield big-icon" aria-hidden="true"></i>

        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. In sed diam ut felis scelerisque rhoncus in sit amet diam. Ut nunc purus, luctus vel nisl quis, mollis tempus neque. Pellentesque eu mauris ut massa convallis porttitor. Integer imperdiet elementum placerat. Curabitur in molestie tortor. Curabitur vestibulum gravida nibh quis congue. Maecenas fringilla ut urna nec eleifend.</p>

        <p>Curabitur gravida ex nisi, non lacinia velit auctor quis:</p>

        <ul>
          <li>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</li>
          <li>Duis a est malesuada, feugiat lacus eget, mollis libero.</li>
          <li>Vestibulum volutpat lacus at mauris rutrum dapibus.</li>
        </ul>
      </div>
      <div class="columns medium-10">
        <h1 class="contrast">Register</h1>
        <phila-alert :success="success">Registration submitted. <br> Please check your email to complete registration.</phila-alert>
        <phila-alert :error="error">{{ error }}</phila-alert>
        <registration-form v-if="!success" :onSubmit="submitRegistration"></registration-form>
      </div>
    </div>
  </div>
</template>

<script>
  import { mapState, mapActions } from 'vuex'

  import PhilaAlert from '../components/phila/PhilaAlert.vue'
  import RegistrationForm from '../components/RegistrationForm.vue'

  export default {
    components: {
      PhilaAlert,
      RegistrationForm
    },
    computed: mapState('registration', {
      error: state => state.error,
      success: state => state.success
    }),
    methods: mapActions('registration', [
      'submitRegistration'
    ]),
    data () {
      return {}
    }
  }
</script>

<style lang="css">
  .big-icon {
    display: block;
    text-align: center;
    color: #000000;
    margin: 1rem 0;
    font-size: 10rem;
  }
</style>
