<template>
  <span>
    <h4 class="d-flex justify-content-between align-items-center">Clinical Dashboard
      <button class="btn btn-primary" v-b-modal.filter-modal><i class="cil-filter btn-icon mr-1"></i>Filter</button>
    </h4>
    <div class="d-flex justify-content-between align-items-center border-bottom border-top" v-if="filterId > 0">
      <ul class="list-group list-group-horizontal list-group-accent">
        <li class="list-group-item list-group-item-accent-primary">{{ filters[0].name }}: {{ filters[0].value }}, is
          equal: {{ filters[0].is_equal }}</li>
      </ul>
      <ul class="list-group list-group-horizontal list-group-accent">
        <li class="list-group-item list-group-item-accent-info">{{ filters[1].name }}, min: {{ filters[1].min }}, max:
          {{ filters[1].max }}</li>
      </ul>
      <ul class="list-group list-group-horizontal list-group-accent">
        <li class="list-group-item list-group-item-accent-success">{{ filters[2].name }}, min: {{ filters[2].min }},
          max: {{ filters[2].max }}</li>
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
            <b-form-spinbutton v-model="filters[1].min" min="25" max="90"></b-form-spinbutton>
          </div>
          <div class="form-group col-md-6">
            <label>Age Max</label>
            <b-form-spinbutton v-model="filters[1].max" min="25" max="90"></b-form-spinbutton>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group col-md-6">
            <label>A1C Min</label>
            <b-form-spinbutton v-model="filters[2].min" min="5" max="15"></b-form-spinbutton>
          </div>
          <div class="form-group col-md-6">
            <label>A1C Max</label>
            <b-form-spinbutton v-model="filters[2].max" min="5" max="15"></b-form-spinbutton>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group col-md-6">
            <label>Vaccination Status Min</label>
            <b-form-spinbutton v-model="filters[3].min" min="0" max="3"></b-form-spinbutton>
          </div>
          <div class="form-group col-md-6">
            <label>Vaccination Status Max</label>
            <b-form-spinbutton v-model="filters[3].max" min="0" max="3"></b-form-spinbutton>
          </div>
        </div>
      </form>
    </b-modal>
    <router-view></router-view>
  </span>
</template>

<script>
import { mapState } from 'vuex'
import axios from 'axios'
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
  computed: mapState(['filters', 'filterId']),
  data() {
    return {
      raceOptions: [{
        value: 'White', text: 'White'
      }, {
        value: 'African American', text: 'African American'
      }, {
        value: 'Asian', text: 'Asian'
      }],
      boolOptions: [{
        value: true, text: 'Yes'
      }, {
        value: false, text: 'No'
      }]
    }
  },
  methods: {
    doFilter() {
      const url = '/api/filter'
      const body = {
        filters: this.filters,
        cohort: true
      }
      this.$bvModal.hide('filter-modal')
      this.$store.commit('setFilters', this.filters)
      this.infoMsg('Creating dashboard filter, please wait')
      axios
        .post(url, body)
        .then((res) => {
          this.successMsg(`Updating Dashboard with Filter ${res.data.id}`)
          this.$store.commit('setFilterId', res.data.id)
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