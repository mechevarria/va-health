<template>
  <span>
    <div class="d-flex justify-content-between align-items-center mb-2">
      <h4>Group Comparison <i class="spinner-border spinner-border-sm mb-1 ml-1 mt-1" v-if="isBusy"></i></h4>
      <button type="button" class="btn btn-primary float-right" @click="doCompare()">
        <i class="cil-blur-linear btn-icon mr-1"></i>Compare
      </button>
    </div>
    <div class="card-deck">
      <div class="card">
        <div class="card-header">
          Group 1
        </div>
        <div class="card-body">
          <div class="form-row">
            <div class="form-group col-md-6">
              <label>{{filters[0].label}}</label>
              <b-form-select v-model="filters[0].value" :options="raceOptions"></b-form-select>
            </div>
            <div class="form-group col-md-6">
              <label>Is Equal</label>
              <b-form-select v-model="filters[0].is_equal" :options="boolOptions"></b-form-select>
            </div>
            <!-- <div class="form-group col-md-2">
            <button type="button" alt="Remove filter" class="btn btn-lg mt-4 pb-0"><i class="cil-x-circle btn-icon mr-1"></i></button>
          </div> -->
          </div>
          <div class="form-row">
            <div class="form-group col-md-6">
              <label>{{filters[1].label}} Min</label>
              <b-form-spinbutton v-model="first[1].min" min="25" max="90"></b-form-spinbutton>
            </div>
            <div class="form-group col-md-6">
              <label>{{filters[1].label}} Max</label>
              <b-form-spinbutton v-model="first[1].max" min="25" max="90"></b-form-spinbutton>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-md-6">
              <label>{{filters[2].label}} Min</label>
              <b-form-spinbutton v-model="first[2].min" min="5" max="15"></b-form-spinbutton>
            </div>
            <div class="form-group col-md-6">
              <label>{{filters[2].label}} Max</label>
              <b-form-spinbutton v-model="first[2].max" min="5" max="15"></b-form-spinbutton>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-md-6">
              <label>{{filters[3].label}} Min</label>
              <b-form-spinbutton v-model="first[3].min" min="0" max="3"></b-form-spinbutton>
            </div>
            <div class="form-group col-md-6">
              <label>{{filters[3].label}} Max</label>
              <b-form-spinbutton v-model="first[3].max" min="0" max="3"></b-form-spinbutton>
            </div>
          </div>
        </div>
      </div>
      <div class="card">
        <div class="card-header">
          Group 2
        </div>
        <div class="card-body">
          <div class="form-row">
            <div class="form-group col-md-12">
              <b-form-checkbox id="compare-rest" v-model="compareRest">
                Compare against the rest of the data?
              </b-form-checkbox>
            </div>
          </div>
          <div class="form-row" v-if="!compareRest">
            <div class="form-group col-md-6">
              <label>{{filters[0].label}}</label>
              <b-form-select v-model="second[0].value" :options="raceOptions"></b-form-select>
            </div>
            <div class="form-group col-md-6">
              <label>Is Equal</label>
              <b-form-select v-model="second[0].is_equal" :options="boolOptions"></b-form-select>
            </div>
            <!-- <div class="form-group col-md-2">
            <button type="button" alt="Remove filter" class="btn btn-lg mt-4 pb-0"><i class="cil-x-circle btn-icon mr-1"></i></button>
          </div> -->
          </div>
          <div class="form-row" v-if="!compareRest">
            <div class="form-group col-md-6">
              <label>{{filters[1].label}} Min</label>
              <b-form-spinbutton v-model="second[1].min" min="25" max="90"></b-form-spinbutton>
            </div>
            <div class="form-group col-md-6">
              <label>{{filters[1].label}} Max</label>
              <b-form-spinbutton v-model="second[1].max" min="25" max="90"></b-form-spinbutton>
            </div>
          </div>
          <div class="form-row" v-if="!compareRest">
            <div class="form-group col-md-6">
              <label>{{filters[2].label}} Min</label>
              <b-form-spinbutton v-model="second[2].min" min="5" max="15"></b-form-spinbutton>
            </div>
            <div class="form-group col-md-6">
              <label>{{filters[2].label}} Max</label>
              <b-form-spinbutton v-model="second[2].max" min="5" max="15"></b-form-spinbutton>
            </div>
          </div>
          <div class="form-row" v-if="!compareRest">
            <div class="form-group col-md-6">
              <label>{{filters[3].label}} Min</label>
              <b-form-spinbutton v-model="second[3].min" min="0" max="3"></b-form-spinbutton>
            </div>
            <div class="form-group col-md-6">
              <label>{{filters[3].label}} Max</label>
              <b-form-spinbutton v-model="second[3].max" min="0" max="3"></b-form-spinbutton>
            </div>
          </div>
        </div>
      </div>
    </div>
  </span>
</template>
<script>
import { mapState } from 'vuex'
//import axios from 'axios'
import msgMixin from '../mixins/msg-mixin'

export default {
  name: 'AppCompare',
  mixins: [msgMixin],
  computed: mapState(['filters', 'raceOptions', 'boolOptions']),
  data() {
    return {
      isBusy: false,
      compareRest: false,
      first: null,
      second: null
    }
  },
  methods: {
    doCompare() {
      this.infoMsg(`Comparing against the rest of the data: ${this.compareRest}`)
    },
    setFilters() {
      this.first = JSON.parse(JSON.stringify(this.filters))
      this.second = JSON.parse(JSON.stringify(this.filters))
    }
  },
  created() {
    this.setFilters()
  }
}
</script>