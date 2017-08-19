import Validatable from './validatable'

export default {
  mixins: [Validatable],

  data () {
    return {
      focused: false,
      tabFocused: false,
      internalTabIndex: null,
      lazyValue: this.value
    }
  },

  props: {
    disabled: Boolean,
    label: String,
    required: Boolean,
    tabindex: {
      default: 0
    },
    value: {
      required: false
    }
  },

  computed: {
    isDirty () {
      return !!this.inputValue
    }
  }
}