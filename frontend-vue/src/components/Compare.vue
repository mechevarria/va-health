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
              <label>{{first[0].label}}</label>
              <b-form-select v-model="first[0].value" :options="first[0].valueOptions"></b-form-select>
            </div>
            <div class="form-group col-md-6">
              <label>Is Equal</label>
              <b-form-select v-model="first[0].is_equal" :options="first[0].boolOptions"></b-form-select>
            </div>
            <!-- <div class="form-group col-md-2">
            <button type="button" alt="Remove filter" class="btn btn-lg mt-4 pb-0"><i class="cil-x-circle btn-icon mr-1"></i></button>
          </div> -->
          </div>
          <div class="form-row">
            <div class="form-group col-md-6">
              <label>{{first[1].label}} Min</label>
              <b-form-spinbutton v-model="first[1].min" :min="first[1].inputMin" :max="first[1].inputMax"></b-form-spinbutton>
            </div>
            <div class="form-group col-md-6">
              <label>{{first[1].label}} Max</label>
              <b-form-spinbutton v-model="first[1].max" :min="first[1].inputMin" :max="first[1].inputMax"></b-form-spinbutton>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-md-6">
              <label>{{first[2].label}} Min</label>
              <b-form-spinbutton v-model="first[2].min" :min="first[2].inputMin" :max="first[2].inputMax"></b-form-spinbutton>
            </div>
            <div class="form-group col-md-6">
              <label>{{first[2].label}} Max</label>
              <b-form-spinbutton v-model="first[2].max" :min="first[2].inputMin" :max="first[2].inputMax"></b-form-spinbutton>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-md-6">
              <label>{{first[3].label}} Min</label>
              <b-form-spinbutton v-model="first[3].min" :min="first[3].inputMin" :max="first[3].inputMax"></b-form-spinbutton>
            </div>
            <div class="form-group col-md-6">
              <label>{{first[3].label}} Max</label>
              <b-form-spinbutton v-model="first[3].max" :min="first[3].inputMin" :max="first[3].inputMax"></b-form-spinbutton>
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
              <label>{{second[0].label}}</label>
              <b-form-select v-model="second[0].value" :options="second[0].valueOptions"></b-form-select>
            </div>
            <div class="form-group col-md-6">
              <label>Is Equal</label>
              <b-form-select v-model="second[0].is_equal" :options="second[0].boolOptions"></b-form-select>
            </div>
            <!-- <div class="form-group col-md-2">
            <button type="button" alt="Remove filter" class="btn btn-lg mt-4 pb-0"><i class="cil-x-circle btn-icon mr-1"></i></button>
          </div> -->
          </div>
          <div class="form-row" v-if="!compareRest">
            <div class="form-group col-md-6">
              <label>{{second[1].label}} Min</label>
              <b-form-spinbutton v-model="second[1].min" :min="second[1].inputMin" :max="second[1].inputMax"></b-form-spinbutton>
            </div>
            <div class="form-group col-md-6">
              <label>{{second[1].label}} Max</label>
              <b-form-spinbutton v-model="second[1].max" :min="second[1].inputMin" :max="second[1].inputMax"></b-form-spinbutton>
            </div>
          </div>
          <div class="form-row" v-if="!compareRest">
            <div class="form-group col-md-6">
              <label>{{second[2].label}} Min</label>
              <b-form-spinbutton v-model="second[2].min" :min="second[2].inputMin" :max="second[2].inputMax"></b-form-spinbutton>
            </div>
            <div class="form-group col-md-6">
              <label>{{second[2].label}} Max</label>
              <b-form-spinbutton v-model="second[2].max" :min="second[2].inputMin" :max="second[2].inputMax"></b-form-spinbutton>
            </div>
          </div>
          <div class="form-row" v-if="!compareRest">
            <div class="form-group col-md-6">
              <label>{{second[3].label}} Min</label>
              <b-form-spinbutton v-model="second[3].min" :min="second[3].inputMin" :max="second[3].inputMax"></b-form-spinbutton>
            </div>
            <div class="form-group col-md-6">
              <label>{{second[3].label}} Max</label>
              <b-form-spinbutton v-model="second[3].max" :min="second[3].inputMin" :max="second[3].inputMax"></b-form-spinbutton>
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
  computed: mapState(['filters']),
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