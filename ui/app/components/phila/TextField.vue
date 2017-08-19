<template>
  <div class="text-field">
    <label :for="name">{{ label }}<span v-if="required"> *</span></label>
    <input
      :type="type"
      :id="name"
      :name="name"
      :class="{ 'input-error': hasError }"
      :value="lazyValue"
      :disabled="disabled"
      :required="required"
      :autofocus="autofocus"
      :aria-required="required"
      :aria-invalid="hasError"
      :tabindex='tabindex'
      @blur="blur"
      @input="onInput"
      @focus="focus"
      ref="input">
    <div class="input-error">
      <span v-if="hasError" role="alert">{{ validations[0] }}</span>
    </div>
  </div>
</template>

<script>
  import validator from 'validator'
  import MailChecker from 'mailchecker'

  import Input from './mixins/input'

  const validateRequired = (textField, value) => {
    if (textField.required && (value === null || value === undefined || value.length == 0))
      return textField.label + ' is required'
    return true
  }

  const validateLength = (textField, value) => {
    if (value === null || value === undefined || textField.type != 'text')
      return true

    var ln = value.length
    if (ln == 0)
      return true // empty values use `required` validation

    if (ln < textField.min)
      return textField.label + ' needs to be at least ' + textField.min + ' characters'
    if (ln > textField.max)
      return textField.label + ' needs to be under ' + textField.min + ' characters'
    return true
  }

  const textValidation = (textField, value) => {
    if (value === null || value === undefined || !textField.textValidation)
      return true

    for (var validation of textField.textValidation) {
      console.log(validation)
      if (validation == 'email' &&
          !validator.isEmail(value))
        return 'Invalid email'
      else if (validation == 'notDisposableEmail' &&
               !MailChecker.isValid(value))
        return 'Disposable email addresses are not allowed'
    }
    return true
  }

  export default {
    name: 'phila-text-field',

    mixins: [Input],

    inheritAttrs: false,

    props: {
      name: {
        type: String,
        required: true
      },
      type: {
        type: String,
        default: 'text'
      },
      autofocus: {
        type: Boolean
      },
      min: {
        type: Number,
        default: 0
      },
      max: {
        type: Number,
        default: Number.MAX_SAFE_INTEGER
      },
      textValidation: {
        type: Array
      }
    },

    data () {
      return {
        defaultRules: [
          validateRequired,
          validateLength,
          textValidation
        ]
      }
    },

    computed: {
      inputValue: {
        get () {
          return this.lazyValue
        },
        set (val) {
          this.$emit('input', val)
          this.lazyValue = val
        }
      },
      isDirty () {
        return this.lazyValue !== null &&
          typeof this.lazyValue !== 'undefined' &&
          this.lazyValue.toString().length > 0
      }
    },

    watch: {
      focused (val) {
        !val && this.$emit('change', this.lazyValue)
      },
      lazyValue () {
        !this.validateOnBlur && this.validate()
      }
    },

    mounted () {
      this.autofocus && this.focus()
    },

    methods: {
      onInput (e) {
        this.inputValue = e.target.value
      },
      blur (e) {
        this.$nextTick(() => {
          this.focused = false
          this.validate()
        })
        this.$emit('blur', e)
      },
      focus (e) {
        this.focused = true
        this.$refs.input.focus()
        this.$emit('focus', e)
      },
    }
  }
</script>

<style lang="css">
  [type='text'], [type='password'], [type='date'], [type='datetime'], [type='datetime-local'], [type='month'], [type='week'], [type='email'], [type='number'], [type='search'], [type='tel'], [type='time'], [type='url'], [type='color'], textarea {
    margin: 0;
    margin-top: 5px;
  }

  input.input-error {
    border: 1px solid #ca310b;
    margin-bottom: 0;
  }

  div.input-error {
    color: #ca310b;
    height: 20px;
  }

  label {
    margin: 0;
    margin-top: 10px;
  }
</style>
