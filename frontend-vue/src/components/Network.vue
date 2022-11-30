<template>
  <div class="card">
    <div class="card-header">
      Network Graph <i class="spinner-border spinner-border-sm mr-1" v-if="isBusy"></i>
    </div>
    <div class="card-body">
      <div class="card-text">
        <span v-if="!isBusy">
          <highcharts :options="chartOptions"></highcharts>
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart } from 'highcharts-vue'
import Highcharts from 'highcharts'
import Networkgraph from 'highcharts/modules/networkgraph'
import axios from 'axios'
import msgMixin from '../mixins/msg-mixin'

Networkgraph(Highcharts)

export default {
  name: 'AppNetwork',
  components: {
    highcharts: Chart
  },
  mixins: [msgMixin],
  data() {
    return {
      data: [],
      isBusy: false,
      chartOptions: {
        chart: {
          type: 'networkgraph',
          height: '300px'
        },
        plotOptions: {
          networkgraph: {
            keys: ['from', 'to']
          }
        },
        title: {
          text: ''
        },
        series: [{
          name: 'sample',
          data: []
        }]
      }
    }
  },
  methods: {
    getGraph() {
      this.isBusy = true
      const url = '/api/graph'
      axios
        .get(url)
        .then((res) => {
          this.chartOptions.series[0].data = res.data
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
    this.getGraph()
  }
}
</script>