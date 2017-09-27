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

    <vue-recaptcha
      class="recaptcha"
      :sitekey="'6LdMWS8UAAAAAMDHdkp0_sP2qYLdRUBgKSLPyPuX'"
      @verify="verifyRecaptcha"
      @expired="expireRecaptcha"></vue-recaptcha>
    <div class="input-error">
      <phila-form-error-message
        v-if="$v.recaptcha.$error"
        role="alert"
        :field="'recaptcha'"
        :label="'reCAPTCHA'"></phila-form-error-message>
    </div>

    <phila-button @click="validateAndSubmit()">Submit</phila-button>
  </div>
</template>

<script>
  import { validationMixin, withParams } from 'vuelidate'
  import { required, maxLength } from 'vuelidate/lib/validators'
  import VueRecaptcha from 'vue-recaptcha'

  import PhilaTextField from './phila/PhilaTextField.vue'
  import PhilaButton from './phila/PhilaButton.vue'
  import validation from './phila/utils/validation'

  export default {
    mixins: [validationMixin, validation],

    components: {
      PhilaTextField,
      PhilaButton,
      VueRecaptcha
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
        recaptcha: null
      }
    },

    validations: {
      email: {
        required,
        maxLength: maxLength(128)
      },
      recaptcha: {
        required
      }
    },

    methods: {
      verifyRecaptcha (response) {
        this.recaptcha = response
      },
      expireRecaptcha () {
        this.recaptcha = null
      },
      validateAndSubmit () {
        this.$v.$touch()
        if (!this.$v.$error)
          this.onSubmit({
            email: this.email,
            recaptcha: this.recaptcha
          })
      }
    }
  }
</script>

<style lang="css">
  .recaptcha {
    margin: 10px 0;
  }

  .recaptcha > div {
    margin: 0 auto;
  }
</style>
