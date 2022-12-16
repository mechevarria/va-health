<template>
  <div class="card">
    <div class="card-header">
      <span>Patient Segments <i class="spinner-border spinner-border-sm mr-1" v-if="isBusy"></i></span>

      <b-dropdown class="float-right" id="color-dropdown" right text="Right align">
        <template #button-content>
          <i class="cil-contrast mr-2 mb-1"></i>Change Color
        </template>
        <b-dropdown-item-button v-for="(option, index) in colorOptions" :key="index" @click="changeColor(option)">
          {{ option.text }}
        </b-dropdown-item-button>
      </b-dropdown>
      <b-form-checkbox class="float-right mr-3 mt-2" id="simplified" v-model="simplified">Simplifiied
        View</b-form-checkbox>
    </div>
    <div class="card-body">
      <div class="card-text">
        <highcharts class="hc" v-if="!isBusy" :options="chartOptions" ref="chart"></highcharts>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Highcharts from 'highcharts'
import Networkgraph from 'highcharts/modules/networkgraph'
import axios from 'axios'
import msgMixin from '../mixins/msg-mixin'

Networkgraph(Highcharts)

export default {
  name: 'AppGraph',
  computed: mapState(['filterId', 'colorOptions']),
  mixins: [msgMixin],
  data() {
    return {
      data: [],
      isBusy: false,
      simplified: true,
      selectedColor: '',
      chartOptions: {
        credits: {
          enabled: false
        },
        chart: {
          type: 'networkgraph',
          height: '300'
        },
        title: {
          text: ''
        },
        series: [{
          colorByPoint: true,
          enableMouseTracking: false,
          layoutAlgorithm: {
            enableSimulation: true,
            initialPositions: 'circle'
          },
          dataLabels: {
            enabled: false
          },
          name: 'networkgraph',
          data: [],
          nodes: []
        }]
      }
    }
  },
  methods: {
    changeColor(option) {
      this.selectedColor = option.value
      this.infoMsg(`Coloring graph by ${option.text}`)
      this.getGraph()
    },
    getGraph() {
      this.isBusy = true
      this.chartOptions.series[0].data = []
      this.chartOptions.series[0].nodes = []
      const url = '/api/graph'
      const body = {
        color_name: this.selectedColor,
        simplified: this.simplified
      }
      if (this.filterId > 0) {
        body.filter_id = this.filterId
      }

      axios
        .post(url, body)
        .then((res) => {
          let data = res.data.data
          // fix for ids coming back as ints
          data.forEach(point => {
            point[0] = point[0].toString()
            point[1] = point[1].toString()
          })
          let nodes = res.data.nodes
          nodes.forEach(node => {
            node.marker = {
              radius: node.radius
            }
          })
          this.chartOptions.series[0].nodes = nodes
          this.chartOptions.series[0].data = data
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
      this.getGraph()
    },
    simplified() {
      this.getGraph()
    }
  },
  created() {
    this.selectedColor = this.colorOptions[0].value
    this.getGraph()
  }
}
</script>