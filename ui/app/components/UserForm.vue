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

    <!-- TODO: phone number validation -->
    <phila-text-field
      :type="'tel'"
      :name="'mobile_phone'"
      v-model="mobile_phone"
      :label="'Mobile Phone'"
      @blur="$v.mobile_phone.$touch()"
      :has-error="$v.mobile_phone.$error"
      :error-message-label="'Mobile phone'"/>

    <phila-button v-on:click="validateAndSave()">Save</phila-button>
  </div>
</template>

<script>
  import { validationMixin, withParams } from 'vuelidate'
  import { required, minLength, maxLength, email, sameAs } from 'vuelidate/lib/validators'
  import MailChecker from 'mailchecker'

  import PhilaTextField from './phila/PhilaTextField.vue'
  import PhilaButton from './phila/PhilaButton.vue'
  import PhilaFormErrorMessage from './phila/PhilaFormErrorMessage.vue'
  import validation from './phila/utils/validation' // TODO: change to validation messages?

  const notDisposableEmail = withParams({type: 'notDisposableEmail'}, value => {
    return MailChecker.isValid(value)
  })

  export default {
    mixins: [validationMixin, validation],
    components: {
      PhilaTextField,
      PhilaButton,
      PhilaFormErrorMessage
    },
    props: {
      onSave: {
        type: Function,
        required: true
      }
    },
    data () {
      return {
        first_name: '',
        last_name: '',
        email: '',
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
      mobile_phone: {
        minLength: minLength(4),
        maxLength: maxLength(128)
      }
    },
    methods: {
      verifyRecaptcha (response) {
        this.recaptcha = response
      },
      expireRecaptcha () {
        this.recaptcha = null
      },
      validateAndSave () {
        this.$v.$touch()
        if (!this.$v.$error)
          this.onSave({
            user: {
              first_name: this.first_name,
              last_name: this.last_name,
              email: this.email,
              mobile_phone: this.mobile_phone
            }
          })
      }
    }
  }
</script>
