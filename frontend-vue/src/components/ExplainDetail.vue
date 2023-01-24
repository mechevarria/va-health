<template>
  <span>
    <span class="mb-2" v-if="groupId.length > 1">
      <h5>
        All Explains for Group {{ groupId }}:
        <i class="spinner-border spinner-border-sm mb-1 ml-1" v-if="isBusy"></i>
      </h5>
    </span>
    <div class="card-deck mb-2" v-if="groupId.length > 1 && !isBusy">
      <div class="card">
        <div class="card-header">
          Continuous Explains
          <i
            class="spinner-border spinner-border-sm mb-1 ml-1"
            v-if="isBusy"
          ></i>
        </div>
        <div class="card-body">
          <table class="table table-sm">
            <tbody>
              <tr v-for="(explain, index) in contExplains" :key="index">
                <td class="app-explain">
                  {{ explain.name }}
                </td>
                <td>
                  <highcharts
                    class="hc"
                    :options="explain.primaryChart"
                  ></highcharts>
                  <highcharts
                    v-if="showSecondary"
                    class="hc"
                    :options="explain.secondaryChart"
                  ></highcharts>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="card">
        <div class="card-header">
          Categorial Explains
          <i
            class="spinner-border spinner-border-sm mb-1 ml-1"
            v-if="isBusy"
          ></i>
        </div>
        <div class="card-body">
          <table class="table table-sm">
            <tr v-for="(explain, index) in catExplains" :key="index">
              <td class="app-explain">
                {{ explain.name }}
              </td>
              <td>
                <b-progress
                  show-progress
                  :value="explain.primary_group_percent"
                  variant="primary"
                ></b-progress>
                <b-progress
                  v-if="showSecondary"
                  show-progress
                  :value="explain.secondary_group_percent"
                  variant="info"
                ></b-progress>
              </td>
            </tr>
          </table>
        </div>
      </div>
    </div>

    <router-view></router-view>
  </span>
</template>

<script>
import { mapState } from 'vuex'
import axios from 'axios'
import { Chart } from 'highcharts-vue'
import Highcharts from 'highcharts'
import highchartsMore from 'highcharts/highcharts-more'
import msgMixin from '../mixins/msg-mixin'

highchartsMore(Highcharts)

export default {
  name: 'AppExplainDetail',
  components: {
    highcharts: Chart
  },
  mixins: [msgMixin],
  computed: mapState(['groupId', 'colors', 'filterId']),
  props: {
    showSecondary: Boolean,
    clearOnCreate: Boolean
  },
  data() {
    return {
      isBusy: false,
      catExplains: [],
      contExplains: [],
      defaultOptions: {
        credits: {
          enabled: false
        },
        chart: {
          type: 'boxplot',
          inverted: true,
          backgroundColor: null,
          height: '40',
          spacingleft: 0,
          spacingBottom: 0,
          spacingTop: 0,
          spacingRight: 0
        },
        tooltip: {
          outside: true
        },
        legend: {
          enabled: false
        },
        xAxis: {
          visible: false
        },
        yAxis: {
          visible: false
        },
        plotOptions: {
          boxplot: {
            fillColor: '',
            stemColor: '',
            whiskerColor: '',
            medianColor: '#ffffff',
            series: {
              animation: false
            }
          }
        },
        title: {
          text: null
        },
        series: [
          {
            name: '',
            data: []
          }
        ]
      }
    }
  },
  watch: {
    filterId() {
      this.clearGroup()
    },
    groupId(newValue) {
      if (newValue.length > 1) {
        this.getExplainDetail(newValue)
      }
    }
  },
  methods: {
    getExplainDetail(groupId) {
      this.isBusy = true
      this.catExplains = []
      this.contExplains = []
      const url = `/api/group/${groupId}`
      axios
        .get(url)
        .then((res) => {
          res.data.explains.forEach((explain) => {
            if (explain.type == 'categorical') {
              this.catExplains.push(explain)
            } else {
              explain.primaryChart = JSON.parse(
                JSON.stringify(this.defaultOptions)
              )
              explain.primaryChart.series[0].name = explain.name
              explain.primaryChart.series[0].data = [
                explain.primary_group_quartiles
              ]
              explain.primaryChart.plotOptions.boxplot.fillColor =
                this.colors.primary
              explain.primaryChart.plotOptions.boxplot.stemColor =
                this.colors.primary
              explain.primaryChart.plotOptions.boxplot.whiskerColor =
                this.colors.primary

              if (this.showSecondary) {
                explain.secondaryChart = JSON.parse(
                  JSON.stringify(this.defaultOptions)
                )
                explain.secondaryChart.series[0].name = explain.name
                explain.secondaryChart.series[0].data = [
                  explain.secondary_group_quartiles
                ]
                explain.secondaryChart.plotOptions.boxplot.fillColor =
                  this.colors.info
                explain.secondaryChart.plotOptions.boxplot.stemColor =
                  this.colors.info
                explain.secondaryChart.plotOptions.boxplot.whiskerColor =
                  this.colors.info
              }

              this.contExplains.push(explain)
            }
          })
        })
        .catch((err) => {
          console.error(err)
          this.errorMsg(err.message)
        })
        .finally(() => {
          this.isBusy = false
        })
    },
    clearGroup() {
      this.contExplains = []
      this.catExplains = []
      this.$store.commit('clearGroup')
    }
  },
  created() {
    this.clearGroup()
  }
}
</script>
<style>
.app-explain {
  width: 50%;
}
</style>
