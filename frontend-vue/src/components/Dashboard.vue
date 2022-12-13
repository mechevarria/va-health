<template>
  <span>
    <h4 class="d-flex justify-content-between align-items-center">Clinical Dashboard
      <button class="btn btn-primary" v-b-modal.filter-modal><i class="cil-filter btn-icon mr-1"></i>Filter</button>
    </h4>
    <div class="d-flex justify-content-between align-items-center border-bottom border-top" v-if="filterId > 0">
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
    <AppNetwork />
    <AppGroup />
    <AppGroupDetails />
    <b-modal id="filter-modal" title="Dashboard Filter" @ok="doFilter" :ok-only=true ok-title="Filter">
      <div class="form-row">
        <div class="form-group col-md-6">
          <label>{{filters[0].label}}</label>
          <b-form-select v-model="filters[0].value" :options="filters[0].valueOptions"></b-form-select>
        </div>
        <div class="form-group col-md-6">
          <label>Is Equal</label>
          <b-form-select v-model="filters[0].is_equal" :options="filters[0].boolOptions"></b-form-select>
        </div>
        <!-- <div class="form-group col-md-2">
            <button type="button" alt="Remove filter" class="btn btn-lg mt-4 pb-0"><i class="cil-x-circle btn-icon mr-1"></i></button>
          </div> -->
      </div>
      <div class="form-row">
        <div class="form-group col-md-6">
          <label>{{filters[1].label}} Min</label>
          <b-form-spinbutton v-model="filters[1].min" :min="filters[1].inputMin" :max="filters[1].inputMax"></b-form-spinbutton>
        </div>
        <div class="form-group col-md-6">
          <label>{{filters[1].label}} Max</label>
          <b-form-spinbutton v-model="filters[1].max" :min="filters[1].inputMin" :max="filters[1].inputMax"></b-form-spinbutton>
        </div>
      </div>
      <div class="form-row">
        <div class="form-group col-md-6">
          <label>{{filters[2].label}} Min</label>
          <b-form-spinbutton v-model="filters[2].min" :min="filters[2].inputMin" :max="filters[2].inputMax"></b-form-spinbutton>
        </div>
        <div class="form-group col-md-6">
          <label>{{filters[2].label}} Max</label>
          <b-form-spinbutton v-model="filters[2].max" :min="filters[2].inputMin" :max="filters[2].inputMax"></b-form-spinbutton>
        </div>
      </div>
      <div class="form-row">
        <div class="form-group col-md-6">
          <label>{{filters[3].label}} Min</label>
          <b-form-spinbutton v-model="filters[3].min" :min="filters[3].inputMin" :max="filters[3].inputMax"></b-form-spinbutton>
        </div>
        <div class="form-group col-md-6">
          <label>{{filters[3].label}} Max</label>
          <b-form-spinbutton v-model="filters[3].max" :min="filters[3].inputMin" :max="filters[3].inputMax"></b-form-spinbutton>
        </div>
      </div>
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
    return {}
  },
  methods: {
    doFilter() {
      const url = '/api/filter'
      let body = {
        filters: JSON.parse(JSON.stringify(this.filters)),
        cohort: true
      }
      body.filters.forEach(filter => {
        delete filter.label
        delete filter.inputMin
        delete filter.inputMax
        delete filter.valueOptions
        delete filter.boolOptions
      });
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