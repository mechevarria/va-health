<template>
  <span>
    <highcharts class="hc" :options="chartOptions" :highcharts="hcInstance"></highcharts>
    <i class="spinner-border spinner-border-sm mb-1 ml-1" v-if="isBusy"></i>
    <span class="d-flex justify-content-between align-items-center mb-2" v-if="groupId > 0 && !isBusy">
      <h5>Group {{ groupId }} Explains:
      </h5>
      <button type="button" class="btn btn-primary" @click="clearGroup()">
        <span class="cil-x-circle icon mr-1"></span>Clear
      </button>
    </span>
    <div class="row row-cols-1 row-cols-md-4">
      <div class="col" v-for="(explain, index) in groupExplains.explains" :key="index">
        <div class="card">
          <div class="card-body" v-if="explain.type == 'categorical'">
            Name: {{ explain.name }}
            <b-progress show-progress :value="explain.primary_group_percent" variant="primary"></b-progress>
          </div>
          <div class="card-body" v-if="explain.type == 'continuous'">
            Name: {{ explain.name }}
            <b-form-input v-model="explain.primary_group_mean" type="range" min="0" max="1" step="0.0005"
              readonly></b-form-input>
          </div>
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
      hcInstance: Highcharts,
      isBusy: false,
      groupExplains: {
        explains: []
      },
      chartOptions: {
        credits: {
            enabled: false
        },
        chart: {
          type: 'boxplot',
          inverted: true,
          backgroundColor: null,
          height: '80',
          width: '200'
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
            medianColor: '#ffffff'
          }
        },
        title: {
          text: null
        },
        series: [{
          name: '',
          data: [
            [760, 801, 848, 895, 965]
          ]
        }]
      }
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
            this.groupExplains = res.data
            this.infoMsg(`Group ${newValue} has ${this.groupExplains.explains.length} explains`)
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
      this.groupExplains.explains = []
      this.$store.commit('clearGroup')
    }
  }
}
</script>
<style>
</style>