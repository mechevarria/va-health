<template>
  <span>
    <h4 class="d-flex justify-content-between align-items-center">
      Clinical Dashboard
      <span>
        <button
          class="btn btn-danger mr-2"
          @click="doClear()"
          v-if="filterId > 0"
        >
          <i class="cil-x-circle btn-icon mr-1"></i>Clear
        </button>
        <button
          class="btn btn-primary"
          v-b-modal.filter-modal
          :disabled="isBusy"
        >
          <i class="cil-filter btn-icon mr-1" v-if="!isBusy"></i>
          <i
            class="spinner-border spinner-border-sm btn-icon mr-1"
            v-if="isBusy"
          ></i>
          Filter
        </button>
      </span>
    </h4>
    <div class="card" v-if="filterId > 0">
      <div class="d-flex flex-row">
        <span v-for="(filter, index) in filters" :key="index">
          <div v-if="filter.enabled" class="ml-4">
            <div class="c-callout" :class="getClass(index)">
              <i class="cil-filter ml-1"></i>
              <small class="text-muted">{{ filter.label }}</small
              ><br />
              <strong class="h6" v-if="filter.categorical"
                >{{ filter.value }}, is equal: {{ filter.is_equal }}</strong
              >
              <strong class="h6" v-else
                >{{ filter.label }}, min: {{ filter.min }}, max: {{ filter.max }}</strong
              >
            </div>
          </div>
        </span>
      </div>
    </div>

    <AppKpi />
    <b-form-checkbox id="graph-compare" v-model="compare" class="mb-2 ml-1">
      Graph Comparison View
    </b-form-checkbox>
    <div class="row">
      <div :class="compare ? 'col-md-6' : 'col-md-12'">
        <AppGraph :label="1" />
      </div>
      <div class="col-md-6" v-if="compare">
        <AppGraph :label="2" />
      </div>
    </div>
    <div class="row">
      <div class="col-md-6" v-if="compare">
        <AppGraph :label="3" />
      </div>
      <div class="col-md-6" v-if="compare">
        <AppGraph :label="4" />
      </div>
    </div>
    <AppExplain />
    <AppExplainDetail :show-secondary="false" />
    <b-modal
      id="filter-modal"
      title="Dashboard Filter"
      @ok="doFilter"
      :ok-only="true"
      ok-title="Filter"
    >
      <span v-for="(filter, index) in filters" :key="index">
        <div class="form-row" v-if="filter.categorical">
          <div class="form-group col-md-5">
            <label>{{ filter.label }}</label>
            <b-form-select
              v-model="filter.value"
              :options="filter.valueOptions"
              :disabled="!filter.enabled"
            ></b-form-select>
          </div>
          <div class="form-group col-md-5">
            <label v-if="filter.boolOptions">Is Equal</label>
            <b-form-select
              v-if="filter.boolOptions"
              v-model="filter.is_equal"
              :options="filter.boolOptions"
              :disabled="!filter.enabled"
            ></b-form-select>
          </div>
          <div class="form-group col-md-2">
            <label v-if="index == 0">Enabled</label>
            <label v-else>&nbsp;</label>
            <b-form-checkbox
              :id="`filter-enabled-${index}`"
              v-model="filter.enabled"
            ></b-form-checkbox>
          </div>
        </div>
        <div class="form-row" v-else>
          <div class="form-group col-md-5">
            <label>{{ filter.label }} Min</label>
            <b-form-spinbutton
              v-model="filter.min"
              :min="filter.inputMin"
              :max="filter.inputMax"
              :disabled="!filter.enabled"
            ></b-form-spinbutton>
          </div>
          <div class="form-group col-md-5">
            <label>{{ filter.label }} Max</label>
            <b-form-spinbutton
              v-model="filter.max"
              :min="filter.inputMin"
              :max="filter.inputMax"
              :disabled="!filter.enabled"
            ></b-form-spinbutton>
          </div>
          <div class="form-group col-md-2">
            <label v-if="index == 0">Enabled</label>
            <label v-else>&nbsp;</label>
            <b-form-checkbox
              :id="`filter-enabled-${index}`"
              v-model="filter.enabled"
            ></b-form-checkbox>
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
    return {
      compare: false,
      isBusy: false
    }
  },
  methods: {
    getClass(index) {
      let className = ''
      switch (true) {
        case index === 0 || index === 6:
          className = 'c-callout-info'
          break
        case index === 1 || index === 7:
          className = 'c-callout-danger'
          break
        case index === 2 || index === 8:
          className = 'c-callout-warning'
          break
        case index === 3 || index === 9:
          className = 'c-callout-success'
          break
        case index === 4 || index === 10:
          className = 'c-callout-secondary'
          break
        case index === 5 || index === 11:
          className = 'c-callout-primary'
          break
      }
      return className
    },
    doFilter() {
      this.isBusy = true
      this.$bvModal.hide('filter-modal')
      this.$store.commit('setFilters', this.filters)
      this.infoMsg('Creating dashboard filter, please wait')

      const url = '/api/filter'
      const postFilters = []
      this.filters.forEach((filter) => {
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
          this.isBusy = false
          if (res.data.id > 0) {
            this.successMsg(`Updating Dashboard with Filter ${res.data.id}`)
            this.$store.commit('setFilterId', res.data.id)
          } else {
            this.warningMsg(res.data.msg)
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
