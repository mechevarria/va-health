<template>
  <div class="card-deck mb-3">
    <div class="card">
      <div class="card-header">
        <i class="spinner-border spinner-border-sm mr-1" v-if="isBusy"></i>
        Detail
      </div>
      <div class="card-body">
        <p class="card-text"><pre>Selected ID {{ id }}</pre></p>
      </div>
    </div>
  </div>
</template>
<script>
import msgMixin from '../mixins/msg-mixin'

export default {
  name: 'AppPatientDetail',
  mixins: [msgMixin],
  data() {
    return {
      id: 0
    }
  },
  
  created() {
      this.id = this.$route.params.id
  }
}
</script>
