export default {
  methods: {
    infoMsg(text) {
      const msg = {
        text: text,
        variant: 'info',
        classes: ['bg-info', 'text-white', '.border-0'],
        iconClass: 'cil-info',
        textClass: 'text-info'
      }
      this.renderMsg(msg)
    },
    successMsg(text) {
      const msg = {
        text: text,
        variant: 'success',
        classes: ['bg-success', 'text-white', '.border-0'],
        iconClass: 'cil-check-circle',
        textClass: 'text-success'
      }
      this.renderMsg(msg)
    },
    warningMsg(text) {
      const msg = {
        text: text,
        variant: 'warning',
        classes: ['bg-warning', 'text-white', '.border-0'],
        iconClass: 'cil-warning',
        textClass: 'text-warning'
      }
      this.renderMsg(msg)
    },
    errorMsg(text) {
      const msg = {
        text: text,
        variant: 'danger',
        classes: ['bg-danger', 'text-white', '.border-0'],
        iconClass: 'cil-x-circle',
        textClass: 'text-danger'
      }
      this.renderMsg(msg)
    },
    renderMsg(msg) {
      const vNodesMsg = [
        this.$createElement('i', { class: [msg.iconClass, 'mr-2'] }),
        msg.text
      ]
      this.$bvToast.toast(vNodesMsg, {
        variant: msg.variant,
        solid: true,
        noCloseButton: true,
        toastClass: msg.classes,
        toaster: 'b-toaster-bottom-center mb-2'
      })
      this.$store.commit('addMessage', msg)
    }
  }
}
