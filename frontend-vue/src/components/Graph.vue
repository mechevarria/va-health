<template>
  <div class="card">
    <div class="card-header">
      <span
        >Patient Segments
        <i class="spinner-border spinner-border-sm mr-1" v-if="isBusy"></i
      ></span>

      <b-dropdown
        class="float-right"
        id="color-dropdown"
        right
        text="Right align"
        :disabled="isBusy"
      >
        <template #button-content>
          <i class="cil-contrast mr-2 mb-1"></i>{{ selectedText }}
        </template>
        <b-dropdown-item-button
          v-for="(option, index) in colorOptions"
          :key="index"
          @click="changeColor(option)"
        >
          {{ option.text }}
        </b-dropdown-item-button>
      </b-dropdown>
      <b-form-checkbox
        class="float-right mr-3 mt-2"
        id="simplified"
        v-model="simplified"
        :disabled="isBusy"
        >Simplifiied View</b-form-checkbox
      >
    </div>
    <div class="card-body">
      <div class="card-text">
        <highcharts
          class="hc"
          :options="chartOptions"
          :updateArgs="[true, true]"
          ref="chart"
        ></highcharts>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Highcharts from 'highcharts'
import Networkgraph from 'highcharts/modules/networkgraph'
import axios from 'axios'
import chroma from 'chroma-js'
import msgMixin from '../mixins/msg-mixin'

Networkgraph(Highcharts)

export default {
  name: 'AppGraph',
  computed: mapState(['filterId', 'colorOptions', 'colors']),
  mixins: [msgMixin],
  data() {
    return {
      data: [],
      isBusy: false,
      simplified: true,
      selectedColor: '',
      selectedText: '',
      colorScale: null,
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
        series: [
          {
            enableMouseTracking: true,
            layoutAlgorithm: {
              enableSimulation: true,
              initialPositions: 'circle'
            },
            dataLabels: {
              enabled: false
            },
            name: 'networkgraph',
            point: {
              events: {
                click: (e) => {
                  this.$store.commit('setGroup', e.point.id)
                }
              }
            },
            data: [],
            nodes: []
          }
        ]
      }
    }
  },
  methods: {
    changeColor(option) {
      this.selectedColor = option.value
      this.selectedText = option.text
      this.getGraph()
    },
    getGraph() {
      this.isBusy = true
      this.chartOptions.series[0].nodes = []
      this.chartOptions.series[0].data = []

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
          let nodes = res.data.nodes
          nodes.forEach((node) => {
            node.color = this.colorScale(node.colorScale).toString()
            //console.log(`node: ${node.id}, color: ${node.color}, colorScale: ${node.colorScale}`)
          })
          this.chartOptions.series[0].nodes = nodes
          this.chartOptions.series[0].data = res.data.data
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
    this.colorScale = chroma.scale([this.colors.first, this.colors.second, this.colors.third])
    this.selectedColor = this.colorOptions[0].value
    this.selectedText = this.colorOptions[0].text
    this.getGraph()
  }
}
</script>
