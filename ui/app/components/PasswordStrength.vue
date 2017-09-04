<template>
  <div class="text-field">
    <label :for="name">{{ label }}<span v-if="required"> *</span></label>
    <vue-password
        :id="name"
        :name="name"
        :class="{ 'input-error': hasError }"
        :value="lazyValue"
        :disabled="disabled"
        :required="required"
        :aria-required="required"
        :aria-invalid="hasError"
        :user-inputs="userInputs"
        @input="onInput"
        ref="password"></vue-password>
    <div class="vue-password-error" :class="{'input-error': hasError}">
      <phila-form-error-message
        v-if="hasError"
        role="alert"
        :field="name"
        :label="errorMessageLabel || label"
        :validation-messages="{
          passwordStrengthValidation: '{{label}} is too weak'
        }"></phila-form-error-message>
    </div>
  </div>
</template>

<script>
  import VuePassword from 'vue-password'

  import PhilaTextField from './phila/PhilaTextField.vue'
  import PhilaFormErrorMessage from './phila/PhilaFormErrorMessage.vue'

  export default {
    name: 'password-strength',

    mixins: [PhilaTextField],

    props: {
      userInputs: {
        type: Array
      }
    },

    components: {
      VuePassword,
      PhilaFormErrorMessage
    },

    computed: {
      strength () {
        return this.$refs.password.strength.score
      }
    },

    mounted () {
      this.$nextTick(() => {
        const passwordInput = document.getElementById(this.name)
        passwordInput.addEventListener('blur', this.onBlur)
        passwordInput.addEventListener('focus', this.onFocus)
      })
    },

    beforeDestroy () {
      const passwordInput = document.getElementById(this.name)
      passwordInput.removeEventListener('blur', this.onBlur)
      passwordInput.removeEventListener('focus', this.onFocus)
    },

    methods: {
      onInput (value) {
        this.inputValue = value
      },
      onBlur (e) {
        this.$emit('blur', e)
      },
      onFocus (e) {
        this.$emit('focus', e)
      }
    }
  }
</script>

<style lang=css>
  .VuePassword__Message {
    height: 1.3rem;
  }

  div.input-error input {
    border: 1px solid #ca310b;
    margin-bottom: 0;
  }

  div.vue-password-error.input-error {
    margin-top: 50px;
  }
</style>
