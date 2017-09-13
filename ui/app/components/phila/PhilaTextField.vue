<template>
  <div class="text-field">
    <label :for="name">{{ label }}<span v-if="required" aria-hidden="true"> *</span></label>
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
      @keyup.enter="onEnter"
      @blur="blur"
      @input="onInput"
      @focus="focus"
      ref="input">
    <div class="input-error">
      <phila-form-error-message
        v-if="hasError"
        role="alert"
        :field="name"
        :label="errorMessageLabel || label"
        :validationMessages="validationMessages"></phila-form-error-message>
    </div>
  </div>
</template>

<script>
  import Input from './mixins/input'
  import PhilaFormErrorMessage from './PhilaFormErrorMessage.vue'

  export default {
    name: 'phila-text-field',

    mixins: [Input],

    components: {
      PhilaFormErrorMessage
    },

    inheritAttrs: false,

    props: {
      name: {
        type: String
      },
      label: {
        type: String
      },
      errorMessageLabel: {
        type: String
      },
      validationMessages: {
        type: Object
      },
      type: {
        type: String,
        default: 'text'
      },
      autofocus: {
        type: Boolean
      },
      hasError: {
        type: Boolean,
        default: false
      },
      errorMessage: {
        type: String
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
      // lazyValue () {
      //   !this.validateOnBlur && this.validate()
      // }
    },

    // created () {
    //   console.log('created')
    //   console.log(this)
    //   var $v = null, vnode = this
    //   for (var i = 0; i < 4; i++) {
    //     if ('$v' in vnode) {
    //       $v = vnode.$v
    //       break
    //     } else {
    //       vnode = vnode.$parent
    //     }
    //   }
    //   this.$v = $v
    // },

    // // TODO: remove $v on destroy

    mounted () {
      this.autofocus && this.focus()
    },

    methods: {
      onInput (e) {
        this.inputValue = e.target.value
      },
      onEnter (e) {
        this.$emit('enter')
      },
      blur (e) {
        this.$nextTick(() => {
          this.focused = false
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
