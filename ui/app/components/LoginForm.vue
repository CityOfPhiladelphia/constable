<template>
  <div>
    <phila-text-field
      :name="'email'"
      v-model="email"
      :label="'Email'"
      :required="true"
      :has-error="$v.email.$error"
      @blur="$v.email.$touch()"
      @enter="validateAndSubmit()" />

    <phila-text-field
      :type="'password'"
      :name="'password'"
      v-model="password"
      :label="'Password'"
      :required="true"
      :has-error="$v.password.$error"
      @blur="$v.password.$touch()"
      @enter="validateAndSubmit()" />

    <router-link to="/password-recovery">Forgot password?</router-link>

    <phila-button @click="validateAndSubmit()">Login</phila-button>
  </div>
</template>

<script>
  import { validationMixin, withParams } from 'vuelidate'
  import { required, maxLength } from 'vuelidate/lib/validators'

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
        email: null,
        password: null
      }
    },

    validations: {
      email: {
        required,
        maxLength: maxLength(128)
      },
      password: {
        required,
        maxLength: maxLength(128)
      }
    },

    methods: {
      validateAndSubmit () {
        this.$v.$touch()
        if (!this.$v.$error)
          this.onSubmit({
            email: this.email,
            password: this.password
          })
      }
    }
  }
</script>
