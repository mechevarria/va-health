<template>
  <div class="card">
    <div class="card-header">
      Patient Segments <i class="spinner-border spinner-border-sm mr-1" v-if="isBusy"></i>
    </div>
    <div class="card-body">
      <div class="card-text">
        <highcharts class="hc" v-if="!isBusy" :options="chartOptions" :highcharts="hcInstance"></highcharts>
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
      hcInstance: Highcharts,
      data: [],
      isBusy: false,
      chartOptions: {
        chart: {
          type: 'networkgraph',
          height: '300px'
        },
        title: {
          text: ''
        },
        series: [{
          colorByPoint: true,
          name: 'networkgraph',
          marker: {
            radius: 15
          },
          data: [],
          nodes: []
        }]
      }
    }
  },
  methods: {
    getGraph() {
      this.isBusy = true
      const url = '/api/graph'
      axios
        .post(url, {
          //filter_id: 18310991,
          color_name: 'species_color'
        })
        .then((res) => {
          this.chartOptions.series[0].data = res.data.data
          this.chartOptions.series[0].nodes = res.data.nodes
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
<style>
.highcharts-color-0 {
  fill: #321fdb;
}

.hightcharts-color-1 {
  fill: #2eb85c;
}

.hightcharts-color-2 {
  fill: #e55353;
}

.hightcharts-color-3 {
  fill: #f9b115;
}

.hightcharts-color-4 {
  fill: #3399ff;
}
</style>