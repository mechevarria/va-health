<template>
  <div class="card">
    <div class="card-header">
      <div class="d-flex">
        <div class="mr-auto mt-1">
          {{ `Graph ${label}` }}
          <i
            class="spinner-border spinner-border-sm mr-1 ml-1"
            v-if="isBusy"
          ></i>
        </div>
        <div class="mr-3 mt-2">
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
        <div class="mr-3">
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
        </div>
        <div class="mt-2">
          <b-form-checkbox
            v-model="simplified"
            :id="`simplified-${label}`"
            :disabled="isBusy"
            >Simplified</b-form-checkbox
          >
        </div>
      </div>
    </div>
    <div class="card-body">
      <div class="card-text" ref="chartContainer">
        <highcharts
          class="hc"
          :options="graphOptions"
          v-if="showChart"
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
  methods: {
    changeColor(option) {
      this.selectedColor = option.value
      this.selectedText = option.text
      this.getGraph()
    },
    getGraph() {
      this.isBusy = true
      this.graphOptions.series[0].nodes = []
      this.graphOptions.series[0].data = []

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
            node.color = this.colorScale(node.colorScale).toString()
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
    }
  },
  watch: {
    filterId() {
      this.getGraph()
    },
    simplified() {
      this.getGraph()
    },
    doRedraw() {
      if (this.doRedraw && this.label === 1) {
        this.showChart = false
        setTimeout(() => {
          this.showChart = true
          this.$store.commit('noRedraw')
        }, 10)
      }
    }
  },
  mounted() {
    if (this.label > 1) {
      this.simplified = false
    }
    this.lowColor = chroma(this.colors.danger).darken(0.6)
    this.midColor = chroma(this.colors.warning)
    this.highColor = chroma(this.colors.success)

    this.colorScale = chroma.scale([this.lowColor, this.midColor, this.highColor])

    this.selectedColor = this.colorOptions[this.label - 1].value
    this.selectedText = this.colorOptions[this.label - 1].text
    this.getGraph()
  }
}
</script>
<style>
.app-label {
  font-size: 0.8em;
}
.app-gradient {
  width: 146px;
  height: 14px;
}
</style>