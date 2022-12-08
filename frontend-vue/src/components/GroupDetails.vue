<template>
  <span>
    <i class="spinner-border spinner-border-sm mb-1 ml-1" v-if="isBusy"></i>
    <span class="d-flex justify-content-between align-items-center mb-2" v-if="groupId > 0 && !isBusy">
      <h5>Group {{ groupId }} Explains:
      </h5>
      <button type="button" class="btn btn-primary" @click="clearGroup()">
        <span class="cil-x-circle icon mr-1"></span>Clear
      </button>
    </span>
    <div class="card-deck mb-2" v-if="groupId > 0">
      <div class="card">
        <div class="card-header">
          Continuous Explains
        </div>
        <div class="card-body">
          <table class="table table-sm">
            <tbody>
              <tr v-for="(explain, index) in contExplains" :key="index">
                <td class="app-explain">
                  {{ explain.name }}
                </td>
                <td>
                  <highcharts class="hc" :options="explain.chartOptions"></highcharts>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="card">
        <div class="card-header">
          Categorial Explains
        </div>
        <div class="card-body">
          <table class="table table-sm">
            <tr v-for="(explain, index) in catExplains" :key="index">
              <td class="app-explain">
                {{ explain.name }}
              </td>
              <td>
                <b-progress show-progress :value="explain.primary_group_percent" variant="primary"></b-progress>
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
import msgMixin from '../mixins/msg-mixin';

highchartsMore(Highcharts)

export default {
  name: 'AppGroupDetail',
  components: {
    highcharts: Chart
  },
  mixins: [msgMixin],
  computed: mapState(['groupId']),
  data() {
    return {
      isBusy: false,
      catExplains: [],
      contExplains: []
    }
  },
  watch: {
    groupId(newValue) {
      if (newValue > 0) {
        this.isBusy = true
        const url = `/api/group/${newValue}`
        axios
          .get(url)
          .then((res) => {
            res.data.explains.forEach(explain => {
              if (explain.type == 'categorical') {
                this.catExplains.push(explain)
              } else {
                explain.chartOptions = {
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
                      fillColor: '#1EACFC',
                      stemColor: '#1EACFC',
                      whiskerColor: '#1EACFC',
                      medianColor: '#ffffff',
                      series: {
                        animation: false
                      }
                    }
                  },
                  title: {
                    text: null
                  },
                  series: [{
                    name: explain.name,
                    data: [explain.primary_group_quartiles]
                  }]
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
      }
    }
  },
  methods: {
    clearGroup() {
      this.contExplains = []
      this.catExplains = []
      this.$store.commit('clearGroup')
    }
  }
}
</script>
<style>
.app-explain {
  width: 50%
}
</style>