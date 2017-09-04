import Mustache from 'Mustache'

const defaultValidationMessages = {
  required: '{{label}} is required',
  minLength: '{{label}} needs to be at least {{$params.minLength.min}} characters',
  maxLength: '{{label}} cannot be more than {{$params.minLength.max}} characters',
  email: '{{label}} needs to be a valid email address',
  notDisposableEmail: '{{label}} cannot be a disposable email address'
}

// TODO: turn this into a component? It could use vue templating

export default {
  methods: {
    getValidationMessage (field, label, validationMessages) {
      const $localV = this.$v[field]
      const messages = Object.assign(
        {},
        defaultValidationMessages,
        validationMessages || {})
      const params = {
        $params: $localV.$params,
        field: field,
        label: label || field
      }

      for (var errorType in messages) {
        if ($localV[errorType] === false)
          return Mustache.render(messages[errorType], params)
      }

      return (label || field) + ' is invalid' // failover is validation message is not defined
    }
  }
}
