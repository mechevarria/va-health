<template>
  <div class="card">
    <div class="card-header d-flex justify-content-between align-items-center">
      <span>Patient Segments <i class="spinner-border spinner-border-sm mr-1" v-if="isBusy"></i></span>
      <b-dropdown id="color-dropdown" right text="Right align">
        <template #button-content>
          <i class="cil-contrast mr-2 mb-1"></i>Change Color
        </template>
        <b-dropdown-item-button v-for="(option, index) in colorOptions" :key="index" @click="changeColor(option)">
          {{ option.text }}
        </b-dropdown-item-button>
      </b-dropdown>
    </div>
    <div class="card-body">
      <div class="card-text">
        <highcharts class="hc" v-if="!isBusy" :options="chartOptions" :highcharts="hcInstance"></highcharts>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
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
  computed: mapState(['filterId']),
  mixins: [msgMixin],
  data() {
    return {
      hcInstance: Highcharts,
      data: [],
      isBusy: false,
      colorOptions: [{
        value: 'A1Clast_period2_to_4_change',
        text: 'Change in A1C'
      }, {
        value: 'visits_count_permonth_period2_to_4_change',
        text: 'Change in Engagement'
      }, {
        value: 'Is_increase_A1Clast_period2_to_4_change',
        text: 'Predicted A1C Increase'
      }, {
        value: 'Is_decrease_visits_count_permonth_period2_to_4_change',
        text: 'Predicted Change in Engagement'
      }],
      selectedColor: '',
      chartOptions: {
        credits: {
          enabled: false
        },
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
      const url = '/api/graph'
      const body = {
        color_name: this.selectedColor
      }
      if (this.filterId > 0) {
        body.filter_id = this.filterId
      }

      axios
        .post(url, body)
        .then((res) => {
          this.chartOptions.series[0].data = res.data.data
          this.chartOptions.series[0].nodes = res.data.nodes
          this.chartOptions.series[0].nodes.forEach(node => {
            node.marker = {
              radius: node.radius
            }
          });
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
    }
  },
  created() {
    this.selectedColor = this.colorOptions[0].value
    this.getGraph()
  }
}
</script>