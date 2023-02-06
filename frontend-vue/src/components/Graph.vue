<template>
  <div class="card">
    <div class="card-header">
      <div class="d-flex d-flex justify-content-between">
        <div>
          {{ `Graph ${label}` }}
          <i
            class="spinner-border spinner-border-sm mr-1 ml-1"
            v-if="isBusy"
          ></i>
        </div>
        <div>
          <div class="app-label text-center">{{ selectedText }}</div>
          <div
            class="rounded app-gradient"
            :style="`background-image: linear-gradient(to right,${lowColor},${midColor},${highColor})`"
          ></div>
          <div class="d-flex justify-content-between">
            <div class="app-label">{{ lowLabel }}</div>
            <div class="app-label">{{ midLabel }}</div>
            <div class="app-label">{{ highLabel }}</div>
          </div>
        </div>
        <div class="py-2 pl-2">
          <a role="button" alt="graph settings" v-b-modal="`graph-modal-${label}`">
            <i class="cil-cog app-icon-hover text-primary c-icon"></i>
          </a>
        </div>
      </div>
    </div>
    <div class="card-body" ref="chartContainer">
      <highcharts
        class="hc"
        :options="graphOptions"
        v-if="showChart"
      ></highcharts>
    </div>
    <b-modal :id="`graph-modal-${label}`" :title="`Graph ${label} Options`" @ok="setConfig">
      <div class="form-group">
        <label>Color Graph Nodes By</label>
        <b-form-select
          v-model="modal.color"
          :options="colorOptions"
          :disabled="isBusy"
          size="sm"
        ></b-form-select>
      </div>
      <div class="form-group">
        <label>Graph Color Style</label>
        <b-form-radio
          :disabled="isBusy"
          v-model="modal.style"
          value="redToGreen"
        >
          <div class="d-flex justify-content-between">
            <div class="app-label">Red</div>
            <div class="app-label">to</div>
            <div class="app-label">Green</div>
          </div>
          <div
            class="rounded app-gradient mb-3"
            :style="`background-image: linear-gradient(to right,${modal.red},${modal.yellow},${modal.green})`"
          ></div>
        </b-form-radio>
        <b-form-radio
          :disabled="isBusy"
          v-model="modal.style"
          value="greenToRed"
        >
          <div class="d-flex justify-content-between">
            <div class="app-label">Green</div>
            <div class="app-label">to</div>
            <div class="app-label">Red</div>
          </div>
          <div
            class="rounded app-gradient mb-3"
            :style="`background-image: linear-gradient(to right,${modal.green},${modal.yellow},${modal.red})`"
          ></div>
        </b-form-radio>
        <b-form-radio
          :disabled="isBusy"
          v-model="modal.style"
          value="whiteToGreen"
        >
          <div class="d-flex justify-content-between">
            <div class="app-label">White</div>
            <div class="app-label">to</div>
            <div class="app-label">Green</div>
          </div>
          <div
            class="rounded app-gradient mb-3"
            :style="`background-image: linear-gradient(to right,${modal.white},${modal.midGreen},${modal.darkGreen})`"
          ></div>
        </b-form-radio>
        <b-form-radio
          :disabled="isBusy"
          v-model="modal.style"
          value="greenToWhite"
        >
          <div class="d-flex justify-content-between">
            <div class="app-label">Green</div>
            <div class="app-label">to</div>
            <div class="app-label">White</div>
          </div>
          <div
            class="rounded app-gradient mb-3"
            :style="`background-image: linear-gradient(to right,${modal.darkGreen},${modal.midGreen},${modal.white})`"
          ></div>
        </b-form-radio>
      </div>
      <div class="form-group">
        <label>Graph Layout</label>
        <b-form-radio
          :disabled="isBusy"
          v-model="modal.layout"
          value="simplified"
          >Simple</b-form-radio
        >
        <b-form-radio :disabled="isBusy" v-model="modal.layout" value="detailed"
          >Detailed</b-form-radio
        >
      </div>
    </b-modal>
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
  computed: mapState(['filterId', 'colorOptions', 'colors', 'doRedraw']),
  mixins: [msgMixin],
  props: {
    label: {
      type: Number,
      default: 1
    }
  },
  data() {
    return {
      data: [],
      isBusy: false,
      simplified: true,
      showChart: true,
      modal: {
        color: '',
        style: '',
        layout: 'simplified',
        green: '',
        yellow: '',
        red: '',
        white: '#ffffff',
        midGreen: '#9ef8c0',
        darkGreen: '#3a9462'
      },
      selectedColor: '',
      selectedText: '',
      colorScale: null,
      highColor: '',
      highLabel: '--',
      midColor: '',
      midLabel: '--',
      lowColor: '',
      lowLabel: '--',
      chartWidth: 0,
      graphOptions: {
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
              enableSimulation: false,
              maxIterations: 2
            },
            dataLabels: {
              enabled: false
            },
            name: 'networkgraph',
            point: {
              events: {
                click: (e) => {
                  if (e.point.groupId > 0) {
                    this.$store.commit('setGroup', e.point.groupId)
                  } else {
                    console.warn(
                      `node: { id: ${e.point.id} }, { groupId: ${e.point.groupId}}`
                    )
                  }
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
  watch: {
    selectedColor(newValue, oldValue) {
      if (newValue !== oldValue) {
        const option = this.colorOptions.find(
          (option) => option.value === newValue
        )
        this.selectedText = option.text
      }
    },
    filterId() {
      this.getGraph()
    },
    doRedraw(label) {
      if (this.doRedraw && this.label === label) {
        this.showChart = false
        setTimeout(() => {
          this.showChart = true
          this.$store.commit('noRedraw')
        }, 10)
      }
    }
  },
  methods: {
    getGraph() {
      this.isBusy = true
      this.graphOptions.series[0].nodes = []
      this.graphOptions.series[0].data = []
      this.highLabel = '--'
      this.midLabel = '--'
      this.lowLabel = '--'

      const url = '/api/graph'
      const body = {
        color_name: this.selectedColor,
        simplified: this.simplified,
        chart_width: this.$refs.chartContainer.offsetWidth - 10
      }
      if (this.filterId > 0) {
        body.filter_id = this.filterId
      }

      axios
        .post(url, body)
        .then((res) => {
          // set labels for color scale
          this.highLabel = res.data.color_controls.color_high
          this.midLabel = res.data.color_controls.color_middle
          this.lowLabel = res.data.color_controls.color_low

          let nodes = res.data.nodes
          nodes.forEach((node) => {
            node.marker.fillColor = this.colorScale(node.colorScale).toString()
            node.marker.lineWidth = 1
            node.marker.lineColor = '#3c4b64'
          })
          this.graphOptions.series[0].nodes = nodes
          this.graphOptions.series[0].data = res.data.data
        })
        .catch((err) => {
          console.error(err)
          this.errorMsg(err.message)
        })
        .finally(() => {
          this.isBusy = false
        })
    },
    setConfig() {
      if (this.modal.layout === 'detailed') {
        this.simplified = false
      } else {
        this.simplified = true
      }

      this.selectedColor = this.modal.color

      switch (this.modal.style) {
        case 'redToGreen':
          this.lowColor = this.modal.red
          this.midColor = this.modal.yellow
          this.highColor = this.modal.green
          break
        case 'greenToRed':
          this.lowColor = this.modal.green
          this.midColor = this.modal.yellow
          this.highColor = this.modal.red
          break
        case 'greenToWhite':
          this.lowColor = this.modal.darkGreen
          this.midColor = this.modal.midGreen
          this.highColor = this.modal.white
          break
        case 'whiteToGreen':
          this.lowColor = this.modal.white
          this.midColor = this.modal.midGreen
          this.highColor = this.modal.darkGreen
          break
      }

      this.colorScale = chroma.scale([
        this.lowColor,
        this.midColor,
        this.highColor
      ])

      // load graph
      this.getGraph()
    }
  },
  mounted() {
    this.modal.green = chroma(this.colors.success)
    this.modal.yellow = chroma(this.colors.warning)
    this.modal.red = chroma(this.colors.danger).darken(0.6)

    this.modal.style = 'redToGreen'

    this.modal.color = this.colorOptions[this.label - 1].value

    this.setConfig()
  }
}
</script>
<style>
.app-label {
  font-size: 0.8em;
}
.app-gradient {
  min-width: 146px;
  height: 10px;
}
.app-icon-hover:hover {
  font-weight: bold;
}
</style>
