<template>
  <div>
    <phila-text-field
      :name="'email'"
      v-model="email"
      :label="'Email'"
      :required="true"
      @blur="$v.email.$touch()"
      :has-error="$v.email.$error"
      :error-message-label="'First name'" />

    <phila-text-field
      :type="'password'"
      :name="'password'"
      v-model="password"
      :label="'Password'"
      :required="true"
      @blur="$v.password.$touch()"
      :has-error="$v.password.$error"
      :error-message-label="'First name'" />

    <phila-button v-on:click="validateAndSubmit()">Login</phila-button>

    <div class="login-error" v-if="error">
      {{ error }}
    </div>
  </div>
</template>

<script>
  import { validationMixin, withParams } from 'vuelidate'
  import { required } from 'vuelidate/lib/validators'

  import PhilaTextField from './phila/PhilaTextField.vue'
  import PhilaButton from './phila/PhilaButton.vue'
  import validation from './phila/utils/validation'

  export default {
    mixins: [validationMixin, validation],

    components: {
      PhilaTextField,
      PhilaButton
    },

    props: {
      onSubmit: {
        type: Function,
        required: true
      }
    },

    data () {
      return {
        username: null,
        password: null
      }
    },

    computed: {
      error () {
        return this.$store.state.login.error // TODO: component accessing state. Should this be a prop?
      }
    },

    validations: {
      email: {
        required
      },
      password: {
        required
      }
    },

    methods: {
      validateAndSubmit () {
        this.$validator.validateAll()
        .then((valid) => {
          if (valid)
            this.onSubmit({
              username: this.username,
              password: this.password
            })
        })
      }
    }
  }
</script>

<style lang="css">
  .login-error {
    background: #fed0d0;
    padding: 1em;
    margin: .5em 0;
    text-align: center;
  }
</style>