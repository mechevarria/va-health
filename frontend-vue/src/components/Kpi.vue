<template>
  <span>
    <i class="spinner-border spinner-border-sm mb-1" v-if="isBusy"></i>
    <div class="card-deck">
      <div class="card mb-4 mt-2 text-white bg-danger">
        <div class="card-body">
          <span v-if=data[0]>
            {{ data[0].name }}
            <h4>{{ data[0].value }}</h4>
          </span>
        </div>
      </div>
      <div class="card mb-4 mt-2 text-white bg-warning">
        <div class="card-body">
          <span v-if=data[1]>
            {{ data[1].name }}
            <h4>{{ data[1].value }}</h4>
          </span>
        </div>
      </div>
      <div class="card mb-4 mt-2 text-white bg-primary">
        <div class="card-body">
          <span v-if=data[2]>
            {{ data[2].name }}
            <h4>{{ data[2].value }}</h4>
          </span>
        </div>
      </div>
      <div class="card mb-4 mt-2 text-white bg-success">
        <div class="card-body">
          <span v-if=data[3]>
            {{ data[3].name }}
            <h4>{{ data[3].value }}</h4>
          </span>
        </div>
      </div>
      <div class="card mb-4 mt-2 text-white bg-info">
        <div class="card-body">
          <span v-if=data[4]>
            {{ data[4].name }}
            <h4>{{ data[4].value }}</h4>
          </span>
        </div>
      </div>
    </div>
  </span>
</template>

<script>
import axios from 'axios'
import msgMixin from '../mixins/msg-mixin'

export default {
  name: 'AppKpi',
  mixins: [msgMixin],
  data() {
    return {
      data: [],
      isBusy: true
    }
  },
  methods: {
    getKpi() {
      const url = '/api/kpi'
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
    this.getKpi()
  }
}
</script>