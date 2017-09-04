export default {
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
    },
    field: {
      type: String
    }
  },

  computed: {
    isDirty () {
      return !!this.inputValue
    }
  }
}