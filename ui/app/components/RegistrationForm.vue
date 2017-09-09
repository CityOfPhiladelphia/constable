<template>
  <div>
    <phila-text-field
      :name="'first_name'"
      v-model="first_name"
      :label="'First Name'"
      :required="true"
      @blur="$v.first_name.$touch()"
      :has-error="$v.first_name.$error"
      :error-message-label="'First name'" />

    <phila-text-field
      :name="'last_name'"
      v-model="last_name"
      :label="'Last Name'"
      :required="true"
      @blur="$v.last_name.$touch()"
      :has-error="$v.last_name.$error"
      :error-message-label="'Last name'" />

    <phila-text-field
      :name="'email'"
      v-model="email"
      :label="'Email'"
      :required="true"
      @blur="$v.email.$touch()"
      :has-error="$v.email.$error"
      :error-message-label="'Email'" />

    <password-strength
      :name="'password'"
      v-model="password"
      :label="'Create a password'"
      :required="true"
      @blur="$v.password.$touch()"
      :has-error="$v.password.$error"
      :error-message-label="'Password'"
      :user-inputs="[first_name,last_name,email]"
      ref="password" />

    <phila-text-field
      :type="'password'"
      :name="'confirm_password'"
      v-model="confirm_password"
      :label="'Confirm your password'"
      :required="true"
      @blur="$v.confirm_password.$touch()"
      :has-error="$v.confirm_password.$error"
      :error-message-label="'Confirm password'"
      :validation-messages="{
        sameAsPassword: 'Passwords do not match'
      }"
      ref="confirmPassword" />

    <!-- TODO: phone number validation -->
    <phila-text-field
      :type="'tel'"
      :name="'mobile_phone'"
      v-model="mobile_phone"
      :label="'Mobile Phone'"
      @blur="$v.mobile_phone.$touch()"
      :has-error="$v.mobile_phone.$error"
      :error-message-label="'Mobile phone'"/>

    <!-- TODO: reCAPCHA -->

<!--     <vue-recaptcha
      :sitekey="'6LdLWy8UAAAAAFNsqcjzbMKqBiBL4vQokrfkHE3b'"
      :badge="'inline'"
      @verify="verifyRecaptcha">
      <phila-button v-on:click="validateAndSubmit()">Submit</phila-button>
    </vue-recaptcha> -->

     <vue-recaptcha
      :sitekey="'6LdMWS8UAAAAAMDHdkp0_sP2qYLdRUBgKSLPyPuX'"
      @verify="verifyRecaptcha" class="recapcha"></vue-recaptcha>

    <phila-button v-on:click="validateAndSubmit()">Submit</phila-button>

    <div class="registration-error" v-if="error">
      {{ error }}
    </div>
  </div>
</template>

<script>
  import { validationMixin, withParams } from 'vuelidate'
  import { required, minLength, maxLength, email, sameAs } from 'vuelidate/lib/validators'
  import MailChecker from 'mailchecker'
  import VueRecaptcha from 'vue-recaptcha'

  import PhilaTextField from './phila/PhilaTextField.vue'
  import PhilaButton from './phila/PhilaButton.vue'
  import PasswordStrength from './PasswordStrength.vue'
  import validation from './phila/utils/validation' // TODO: change to validation messages?

  const notDisposableEmail = withParams({type: 'notDisposableEmail'}, value => {
    return MailChecker.isValid(value)
  })

  const passwordStrengthValidation = withParams({type: 'passwordStrength'}, (value, vm) => {
    return vm.$refs.password && vm.$refs.password.strength > 2
  })

  export default {
    mixins: [validationMixin, validation],
    components: {
      PhilaTextField,
      PhilaButton,
      PasswordStrength,
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
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        confirm_password: '',
        mobile_phone: '' // TODO: valid phone. Maybe have country drop down?
      }
    },
    validations: {
      first_name: {
        required,
        minLength: minLength(2),
        maxLength: maxLength(128)
      },
      last_name: {
        required,
        minLength: minLength(2),
        maxLength: maxLength(128)
      },
      email: {
        required,
        email,
        notDisposableEmail,
        maxLength: maxLength(128)
      },
      password: {
        required,
        passwordStrengthValidation,
        minLength: minLength(8),
        maxLength: maxLength(128)
      },
      confirm_password: {
        required,
        sameAsPassword: sameAs('password')
      },
      mobile_phone: {
        minLength: minLength(4),
        maxLength: maxLength(128)
      }
    },
    computed: {
      error () {
        return this.$store.state.registration.error // TODO: component accessing state. Should this be a prop?
      }
    },
    methods: {
      verifyRecaptcha (response) {
        console.log(response)
      },
      validateAndSubmit () {
        this.$v.$touch()
      }
    }
  }
</script>

<style lang="css">
  .registration-error {
    background: #fed0d0;
    padding: 1em;
    margin: .5em 0;
    text-align: center;
  }

  .VuePassword__Input {
    margin-bottom: .75em;
  }

/*  .VuePassword__Toggle__Icon {
    color: #0f4d90;
  }*/

  .VuePassword__Meter {
    color: #f0f0f0;
  }

  .recapcha {
    margin: 10px 0;
  }

  .recapcha > div {
    margin: 0 auto;
  }
</style>