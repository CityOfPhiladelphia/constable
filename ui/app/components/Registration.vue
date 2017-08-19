<template>
  <div>
    <text-field
      :name="'first_name'"
      v-model="first_name"
      :label="'First Name'"
      :validateOnBlur="true"
      :required="true"
      :min="1"
      :max="128" />

    <text-field
      :name="'last_name'"
      v-model="last_name"
      :label="'Last Name'"
      :validateOnBlur="true"
      :required="true"
      :min="1"
      :max="128" />

    <text-field
      :name="'email'"
      v-model="email"
      :label="'Email'"
      :validateOnBlur="true"
      :required="true"
      :max="128"
      :text-validation="['email','notDisposableEmail']" />

    <!-- TODO: live username availbility -->
    <text-field
      :name="'username'"
      v-model="username"
      :label="'Choose your username'"
      :validateOnBlur="true"
      :required="true"
      :min="4"
      :max="128" />

    <!-- TODO: password strength validation -->
    <!-- TODO: errors should say Password as the field -->

    <div>
      <label for="password">Create a password *</label>
      <vue-password
        id="password"
        name="password"
        v-model="password"
        :user-inputs="[first_name,last_name,username,email]"
        ref="password">
      </vue-password>
    </div>

    <!-- TODO: confirm it matches password -->
    <text-field
      :type="'password'"
      :name="'confirm_password'"
      v-model="confirm_password"
      :label="'Confirm your password'"
      :validateOnBlur="true"
      :required="true"
      :min="8"
      :max="128"
      :errorMessages="passwordConfirmation(password, confirm_password)"
      ref="confirmPassword" />

    <!-- TODO: phone number validation -->
    <text-field
      :type="'tel'"
      :name="'mobile_phone'"
      v-model="mobile_phone"
      :label="'Mobile Phone (optional)'"
      :validateOnBlur="true"
      :min="8"
      :max="128" />

    <!-- TODO: reCAPCHA -->

    <phila-button v-on:click="validateAndSubmit()">Submit</phila-button>

    <div class="registration-error" v-if="error">
      {{ error }}
    </div>
  </div>
</template>

<script>
  import VuePassword from 'vue-password'

  import TextField from './phila/TextField.vue'
  import Button from './phila/Button.vue'

  export default {
    components: {
      TextField,
      'phila-button': Button,
      VuePassword
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
        last_name: null,
        email: null,
        username: null,  // TODO: check lengeth. lowercase?
        password: null,  // TODO: check length. check strength
        confirm_password: null,  // TODO: check matches
        mobile_phone: null  // TODO: valid phone. Maybe have country drop down?
      }
    },
    computed: {
      error () {
        return this.$store.state.registration.error // TODO: component accessing state. Should this be a prop?
      }
    },
    methods: {
      passwordConfirmation (password, confirmPassword) {
        if (this.$refs.confirmPassword &&
            this.$refs.confirmPassword.shouldValidate &&
            (password && password.length > 0) &&
            (confirmPassword && confirmPassword.length > 0) &&
            password != confirm_password)
          return 'Passwords do not match'
      },

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
  .registration-error {
    background: #fed0d0;
    padding: 1em;
    margin: .5em 0;
    text-align: center;
  }

  .VuePassword__Input {
    margin-bottom: .5em;
  }

/*  .VuePassword__Toggle__Icon {
    color: #0f4d90;
  }*/

  .VuePassword__Meter {
    color: #f0f0f0;
  }
</style>