<template>
  <span>
    <div class="card-deck">
      <div class="card">
        <div class="card-body">
          <h4 class="card-title">Eureka API Status</h4>
          <div class="card-text">
            <pre>{{ data }}</pre>
          </div>
        </div>
      </div>
      <div class="card">
        <div class="card-body">
          <div class="card-text">
            <span v-if="!isBusy">
              <highcharts :options="chartOptions"></highcharts>
            </span>
          </div>
        </div>
      </div>
    </div>
    <router-view></router-view>
  </span>
</template>

<script>
import { Chart } from 'highcharts-vue'
import Highcharts from 'highcharts'
import Networkgraph from 'highcharts/modules/networkgraph'
import axios from 'axios'
import msgMixin from '../mixins/msg-mixin'

Networkgraph(Highcharts)

export default {
  name: 'AppHome',
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
          text: 'Network Graph'
        },
        series: [{
          name: 'sample',
          data: []
        }]
      }
    }
  },
  methods: {
    getStatus() {
      const url = '/api/status'
      axios
        .get(url)
        .then((res) => {
          this.data = JSON.stringify(res.data, null, 2)
        })
        .catch((err) => {
          console.error(err)
          this.errorMsg(err.message)
        })
    },
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
    this.getStatus()
  }
}
</script>