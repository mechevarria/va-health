<template>
  <span>
    <h4 class="d-flex justify-content-between align-items-center">Clinical Dashboard
      <button class="btn btn-primary" v-b-modal.filter-modal><i class="cil-filter btn-icon mr-1"></i>Filter</button>
    </h4>
    <div class="d-flex justify-content-between align-items-center" v-if="isFiltered">
      <ul class="list-group list-group-horizontal bg-white mb-1 mt-1">
        <li class="list-group-item">{{ filters[0].name }}: {{ filters[0].value }}, is equal: {{ filters[0].is_equal }}</li>
        <li class="list-group-item">{{ filters[1].name }}, min: {{ filters[1].min }}, max: {{ filters[1].max }}</li>
        <li class="list-group-item">{{ filters[2].name }}, min: {{ filters[2].min }}, max: {{ filters[2].max }}</li>
      </ul>
      <button class="btn btn-danger ml-2" @click="doClear()"><i class="cil-x-circle btn-icon mr-1"></i>Clear</button>
    </div>

    <AppKpi />
    <AppNetwork />
    <AppGroup />
    <AppGroupDetails />
    <b-modal id="filter-modal" title="Dashboard Filter" @ok="doFilter" :ok-only=true ok-title="Filter">
      <form @submit.prevent="doFilter">
        <div class="form-row">
          <div class="form-group col-md-6">
            <label>Race</label>
            <b-form-select v-model="filters[0].value" :options="raceOptions"></b-form-select>
          </div>
          <div class="form-group col-md-6">
            <label>Is Equal</label>
            <b-form-select v-model="filters[0].is_equal" :options="boolOptions"></b-form-select>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group col-md-6">
            <label>Age Min</label>
            <b-form-spinbutton v-model="filters[1].min" min="0" max="100"></b-form-spinbutton>
          </div>
          <div class="form-group col-md-6">
            <label>Age Max</label>
            <b-form-spinbutton v-model="filters[1].max" min="0" max="100"></b-form-spinbutton>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group col-md-6">
            <label>A1C Min</label>
            <b-form-spinbutton v-model="filters[2].min" min="0" max="20"></b-form-spinbutton>
          </div>
          <div class="form-group col-md-6">
            <label>A1C Max</label>
            <b-form-spinbutton v-model="filters[2].max" min="0" max="20"></b-form-spinbutton>
          </div>
        </div>
      </form>
    </b-modal>
    <router-view></router-view>
  </span>
</template>

<script>
import AppKpi from './Kpi.vue'
import AppNetwork from './Network.vue'
import AppGroup from './Group.vue'
import AppGroupDetails from './GroupDetails.vue'
import msgMixin from '../mixins/msg-mixin'

export default {
  name: 'AppDashboard',
  components: {
    AppKpi,
    AppNetwork,
    AppGroup,
    AppGroupDetails
  },
  mixins: [msgMixin],
  data() {
    return {
      isFiltered: false,
      raceOptions: [{
        value: null, text: 'No Filter'
      }, {
        value: 'Race_White', text: 'White'
      }, {
        value: 'Race_Black or African American', text: 'African American'
      }, {
        value: 'Ethnicity_HISPANIC OR LATINO', text: 'Hispanic or Latino'
      }, {
        value: 'Race_Asian', text: 'Asian'
      }, {
        value: 'Race_American Indian or Alaska Native', text: 'American Indian or Alaska Native'
      }],
      boolOptions: [{
        value: true, text: 'Yes'
      }, {
        value: false, text: 'No'
      }],
      filters: [
        {
          name: 'race',
          categorical: true,
          value: null,
          is_equal: true
        },
        {
          name: 'AgeAtIndexDate',
          categorical: false,
          min: 0,
          max: 55
        },
        {
          name: 'A1C_last_period4_2021-03-01_2022-03-01',
          categorical: false,
          min: 0,
          max: 20
        }
      ]
    }
  },
  methods: {
    doFilter() {
      this.$bvModal.hide('filter-modal')
      this.isFiltered = true
      console.log(this.filters)
    },
    doClear() {
      this.isFiltered = false
      this.filters[0].value = null
      this.filters[0].is_equal = true
      this.filters[1].min = 0
      this.filters[1].max = 100
      this.filters[2].min = 0
      this.filters[2].max = 20
    }
  }
}
</script>