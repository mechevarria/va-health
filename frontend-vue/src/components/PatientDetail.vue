<template>
  <span>
    <div class="row row-cols-1 row-cols-md-3 g-4">
      <div class="col">
        <div class="card">
          <div class="card-header">
            Physical
            <i class="spinner-border spinner-border-sm ml-1" v-if="isBusy"></i>
          </div>
          <div class="card-body">
            <pre>{{ data.physical }}</pre>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-header">
            Demographics
            <i class="spinner-border spinner-border-sm ml-1" v-if="isBusy"></i>
          </div>
          <div class="card-body">
            <pre>{{ data.demographics }}</pre>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-header">
            Comorbidities
            <i class="spinner-border spinner-border-sm ml-1" v-if="isBusy"></i>
          </div>
          <div class="card-body">
            <pre>{{ data.comorbidities }}</pre>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-header">
            Risk Scores
            <i class="spinner-border spinner-border-sm ml-1" v-if="isBusy"></i>
          </div>
          <div class="card-body">
            <pre>{{ data.risk_scores }}</pre>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-header">
            Raw Data
            <i class="spinner-border spinner-border-sm ml-1" v-if="isBusy"></i>
          </div>
          <div class="card-body">
            <pre>{{ data.raw }}</pre>
          </div>
        </div>
      </div>
    </div>
  </span>
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
