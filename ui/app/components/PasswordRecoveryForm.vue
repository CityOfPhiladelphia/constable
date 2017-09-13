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

    <phila-button @click="validateAndSubmit()">Submit</phila-button>
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
        email: null
      }
    },

    validations: {
      email: {
        required,
        maxLength: maxLength(128)
      }
    },

    methods: {
      validateAndSubmit () {
        this.$v.$touch()
        if (!this.$v.$error)
          this.onSubmit({
            email: this.email
          })
      }
    }
  }
</script>
