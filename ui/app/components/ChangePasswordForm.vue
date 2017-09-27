<template>
  <div>
    <phila-text-field
      :type="'password'"
      :name="'current_password'"
      v-model="current_password"
      :label="'Your current password'"
      :required="true"
      @blur="$v.current_password.$touch()"
      :has-error="$v.current_password.$error"
      ref="currentPassword" />

    <!-- TODO: :user-inputs="[first_name,last_name,email]" -->
    <password-strength
      :name="'new_password'"
      v-model="new_password"
      :label="'Create a new password'"
      :required="true"
      @blur="$v.new_password.$touch()"
      :has-error="$v.new_password.$error"
      :error-message-label="'New Password'"
      ref="newPassword" />

    <phila-text-field
      :type="'password'"
      :name="'confirm_new_password'"
      v-model="confirm_new_password"
      :label="'Confirm your new password'"
      :required="true"
      @blur="$v.confirm_new_password.$touch()"
      :has-error="$v.confirm_new_password.$error"
      :error-message-label="'Confirm new password'"
      :validation-messages="{
        sameAsPassword: 'Passwords do not match'
      }"
      ref="confirmNewPassword" />

    <phila-button v-on:click="validateAndSubmit()">Change Password</phila-button>
  </div>
</template>

<script>
  import { validationMixin, withParams } from 'vuelidate'
  import { required, minLength, maxLength, email, sameAs } from 'vuelidate/lib/validators'

  import PhilaTextField from './phila/PhilaTextField.vue'
  import PhilaButton from './phila/PhilaButton.vue'
  import PhilaFormErrorMessage from './phila/PhilaFormErrorMessage.vue'
  import PasswordStrength from './PasswordStrength.vue'
  import validation from './phila/utils/validation' // TODO: change to validation messages?

  const passwordStrengthValidation = withParams({type: 'passwordStrength'}, (value, vm) => {
    return vm.$refs.newPassword && vm.$refs.newPassword.strength > 2
  })

  export default {
    mixins: [validationMixin, validation],
    components: {
      PhilaTextField,
      PhilaButton,
      PhilaFormErrorMessage,
      PasswordStrength
    },
    props: {
      onChangePassword: {
        type: Function,
        required: true
      }
    },
    data () {
      return {
        current_password: '',
        new_password: '',
        confirm_new_password: ''
      }
    },
    validations: {
      current_password: {
        required,
        maxLength: maxLength(128)
      },
      new_password: {
        required,
        passwordStrengthValidation,
        minLength: minLength(8),
        maxLength: maxLength(128)
      },
      confirm_new_password: {
        required,
        sameAsPassword: sameAs('password')
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
          this.onChangePassword({
            current_password: this.current_password,
            new_password: this.new_password
          })
      }
    }
  }
</script>

<style lang="css">
  .VuePassword__Input {
    margin-bottom: .75em;
  }

  .VuePassword__Meter {
    color: #f0f0f0;
  }
</style>
