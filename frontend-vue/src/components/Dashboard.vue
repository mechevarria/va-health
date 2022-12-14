<template>
  <span>
    <h4 class="d-flex justify-content-between align-items-center">Clinical Dashboard
      <button class="btn btn-primary" v-b-modal.filter-modal><i class="cil-filter btn-icon mr-1"></i>Filter</button>
    </h4>
    <div class="d-flex justify-content-between align-items-center border-bottom border-top mb-3" v-if="filterId > 0">
      <ul class="list-group list-group-horizontal list-group-accent" v-for="(filter, index) in filters" :key="index">
        <li class="list-group-item list-group-item-accent-primary" v-if="filter.categorical">
          {{ filter.label }}: {{ filter.value }}, is equal: {{ filter.is_equal }}
        </li>
        <li class="list-group-item list-group-item-accent-info" v-else>
          {{ filter.label }}, min: {{ filter.min }}, max: {{ filter.max }}
        </li>
      </ul>
      <button class="btn btn-danger ml-2" @click="doClear()"><i class="cil-x-circle btn-icon mr-1"></i>Clear</button>
    </div>

    <AppKpi />
    <AppGraph />
    <AppExplain />
    <AppExplainDetail :show-secondary="false" />
    <b-modal id="filter-modal" title="Dashboard Filter" @ok="doFilter" :ok-only=true ok-title="Filter">
      <span v-for="(filter, index) in filters" :key="index">
        <div class="form-row" v-if="filter.categorical">
          <div class="form-group col-md-6">
            <label>{{ filter.label }}</label>
            <b-form-select v-model="filter.value" :options="filter.valueOptions"></b-form-select>
          </div>
          <div class="form-group col-md-6">
            <label>Is Equal</label>
            <b-form-select v-model="filter.is_equal" :options="filter.boolOptions"></b-form-select>
          </div>
        </div>
        <div class="form-row" v-else>
          <div class="form-group col-md-6">
            <label>{{ filter.label }} Min</label>
            <b-form-spinbutton v-model="filter.min" :min="filter.inputMin" :max="filter.inputMax"></b-form-spinbutton>
          </div>
          <div class="form-group col-md-6">
            <label>{{ filter.label }} Max</label>
            <b-form-spinbutton v-model="filter.max" :min="filter.inputMin" :max="filter.inputMax"></b-form-spinbutton>
          </div>
        </div>
      </span>
    </b-modal>
    <router-view></router-view>
  </span>
</template>

<script>
import { mapState } from 'vuex'
import axios from 'axios'
import AppKpi from './Kpi.vue'
import AppGraph from './Graph.vue'
import AppExplain from './Explain.vue'
import AppExplainDetail from './ExplainDetail.vue'
import msgMixin from '../mixins/msg-mixin'

export default {
  name: 'AppDashboard',
  components: {
    AppKpi,
    AppGraph,
    AppExplain,
    AppExplainDetail
  },
  mixins: [msgMixin],
  computed: mapState(['filters', 'filterId']),
  data() {
    return {}
  },
  methods: {
    doFilter() {
      this.$bvModal.hide('filter-modal')
      this.$store.commit('setFilters', this.filters)
      this.infoMsg('Creating dashboard filter, please wait')

      const url = '/api/filter'
      const postFilters = []
      this.filters.forEach(filter => {
        if (filter.enabled) {
          let postFilter = {}
          postFilter.name = filter.name
          postFilter.categorical = filter.categorical

          if (postFilter.categorical) {
            postFilter.value = filter.value
            postFilter.is_equal = filter.is_equal
          } else {
            postFilter.min = filter.min
            postFilter.max = filter.max
          }

          postFilters.push(postFilter)
        }
      })
      const body = {
        filters: postFilters,
        cohort: true
      }
      axios
        .post(url, body)
        .then((res) => {
          this.successMsg(`Updating Dashboard with Filter ${res.data.id}`)
          if (!res.data.msg) {
            this.$store.commit('setFilterId', res.data.id)
          }
        })
        .catch((err) => {
          console.error(err)
          this.errorMsg(err.message)
        })
        .finally(() => {
          this.$bvModal.hide('filter-modal')
        })
    },
    doClear() {
      this.$store.commit('clearFilter')
    }
  }
}
</script>