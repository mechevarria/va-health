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
        </div>
        <div class="card-body">
          <div class="d-flex justify-content-end">
            <div class="badge bg-primary text-white mr-2">{{ primaryName }}</div>
            <div class="badge  bg-info text-white">{{ secondaryName }}</div>
          </div>
          <hr/>
          <span v-for="(explain, index) in contExplains" :key="index">
            <div class="row">
              <div class="col-sm-6">
                {{ explain.name }}
              </div>
              <div class="col-sm-6">
                <highcharts
                  class="hc"
                  :options="explain.chart"
                ></highcharts>
              </div>
            </div>
            <hr />
          </span>
        </div>
      </div>
      <div class="card">
        <div class="card-header">
          Categorial Explains
        </div>
        <div class="card-body">
          <div class="d-flex justify-content-end">
            <div class="badge bg-primary text-white mr-2">{{ primaryName }}</div>
            <div class="badge  bg-info text-white">{{ secondaryName }}</div>
          </div>
          <hr/>
          <span v-for="(explain, index) in catExplains" :key="index">
            <div class="row">
              <div class="col-sm-6">
                {{ explain.name }}
              </div>
              <div class="col-sm-6">
                <div>
                  <b-progress
                    show-progress
                    :value="explain.primary_group_percent"
                    variant="primary"
                  ></b-progress>
                </div>
                <div>
                  <b-progress
                    show-progress
                    :value="explain.secondary_group_percent"
                    variant="info"
                  ></b-progress>
                </div>
              </div>
            </div>
            <hr />
          </span>
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
    clearOnCreate: Boolean
  },
  data() {
    return {
      isBusy: false,
      primaryName: '--',
      secondaryName: '--',
      catExplains: [],
      contExplains: [],
      defaultOptions: {}
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
          this.primaryName = res.data.primary_name
          this.secondaryName = res.data.secondary_name
          res.data.explains.forEach((explain) => {
            if (explain.type == 'categorical') {
              this.catExplains.push(explain)
            } else {
              explain.chart = JSON.parse(
                JSON.stringify(this.defaultOptions)
              )
              // set boxplot data primary
              explain.chart.series[0].data[0].low = explain.primary_group_quartiles[0]
              explain.chart.series[0].data[0].q1 = explain.primary_group_quartiles[1]
              explain.chart.series[0].data[0].median = explain.primary_group_quartiles[2]
              explain.chart.series[0].data[0].q3 = explain.primary_group_quartiles[3]
              explain.chart.series[0].data[0].high = explain.primary_group_quartiles[4]

              // set boxplot data secondary
              explain.chart.series[0].data[1].low = explain.secondary_group_quartiles[0]
              explain.chart.series[0].data[1].q1 = explain.secondary_group_quartiles[1]
              explain.chart.series[0].data[1].median = explain.secondary_group_quartiles[2]
              explain.chart.series[0].data[1].q3 = explain.secondary_group_quartiles[3]
              explain.chart.series[0].data[1].high = explain.secondary_group_quartiles[4]

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
    },
    setDefaultOptions() {
      this.defaultOptions = {
        credits: {
          enabled: false
        },
        chart: {
          type: 'boxplot',
          height: '60',
          inverted: true,
          backgroundColor: null,
          spacingleft: 0,
          spacingBottom: 0,
          spacingTop: 0,
          spacingRight: 0
        },
        legend: {
          enabled: false
        },
        xAxis: {
          visible: false,
          minPadding: 0,
          maxPadding: 0
        },
        yAxis: {
          visible: true,
          title: null,
          minPadding: 0,
          maxPadding: 0
        },
        title: {
          text: null
        },
        tooltip: {
          outside: true
        },
        series: [
          {
            data: [
              {
                low: 0,
                q1: 0,
                median: 0,
                q3: 0,
                high: 0,
                name: 'Primary',
                color: this.colors.primary,
                fillColor: this.colors.primary,
                medianColor: '#ffffff'
              },
              {
                low: 0,
                q1: 0,
                median: 0,
                q3: 0,
                high: 0,
                name: 'Secondary',
                color: this.colors.info,
                fillColor: this.colors.info,
                medianColor: '#ffffff'
              }
            ]
          }
        ]
      }
    }
  },
  created() {
    this.setDefaultOptions()
    this.clearGroup()
  }
}
</script>
