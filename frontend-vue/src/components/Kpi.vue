<template>
  <span>
    <div class="card-deck">
      <div class="card mb-4 mt-2 text-white bg-danger">
        <div class="card-body">
          <i class="spinner-border spinner-border-sm mb-1 ml-1 mt-1" v-if="isBusy"></i>
          <span v-if=data[0]>
            {{ data[0].name }}
            <h4>{{ data[0].value }}</h4>
          </span>
        </div>
      </div>
      <div class="card mb-4 mt-2 text-white bg-warning">
        <div class="card-body">
          <i class="spinner-border spinner-border-sm mb-1 ml-1 mt-1" v-if="isBusy"></i>
          <span v-if=data[1]>
            {{ data[1].name }}
            <h4>{{ data[1].value }}</h4>
          </span>
        </div>
      </div>
      <div class="card mb-4 mt-2 text-white bg-primary">
        <div class="card-body">
          <i class="spinner-border spinner-border-sm mb-1 ml-1 mt-1" v-if="isBusy"></i>
          <span v-if=data[2]>
            {{ data[2].name }}
            <h4>{{ data[2].value }}</h4>
          </span>
        </div>
      </div>
      <div class="card mb-4 mt-2 text-white bg-success">
        <div class="card-body">
          <i class="spinner-border spinner-border-sm mb-1 ml-1 mt-1" v-if="isBusy"></i>
          <span v-if=data[3]>
            {{ data[3].name }}
            <h4>{{ data[3].value }}</h4>
          </span>
        </div>
      </div>
      <div class="card mb-4 mt-2 text-white bg-info">
        <div class="card-body">
          <i class="spinner-border spinner-border-sm mb-1 ml-1 mt-1" v-if="isBusy"></i>
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
import { mapState } from 'vuex'
import axios from 'axios'
import msgMixin from '../mixins/msg-mixin'

export default {
  name: 'AppKpi',
  computed: mapState(['filterId']),
  mixins: [msgMixin],
  data() {
    return {
      data: [],
      isBusy: true
    }
  },
  methods: {
    getKpi() {
      this.isBusy = true
      this.data = true
      let url = '/api/kpi'
      if (this.filterId > 0) {
        url = url + `/${this.filterId}`
      }
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
  watch: {
    filterId() {
      this.getKpi()
    }
  },
  created() {
    this.getKpi()
  }
}
</script>