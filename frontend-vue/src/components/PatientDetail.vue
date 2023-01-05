<template>
  <div class="card-deck mb-3">
    <div class="card">
      <div class="card-header">
        Patient Detail
        <i class="spinner-border spinner-border-sm ml-1" v-if="isBusy"></i>
      </div>
      <div class="card-body">
        <p class="card-text"><pre>{{ data }}</pre></p>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios'
import msgMixin from '../mixins/msg-mixin'

export default {
  name: 'AppPatientDetail',
  mixins: [msgMixin],
  data() {
    return {
      id: 0,
      data: {},
      isBusy: false
    }
  },
  methods: {
    getDetails() {
      this.isBusy = true
      const url = `/api/patient/${this.id}`
      axios
        .get(url)
        .then((res) => {
          this.data = res.data
        })
        .catch((err) => {
          console.error(err)
          this.errorMsg(err.message)
        })
        .finally(() => {
          this.isBusy = false
        })
    }
  },
  created() {
      this.id = this.$route.params.id
      this.getDetails()
  }
}
</script>
