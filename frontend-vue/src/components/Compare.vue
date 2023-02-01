<template>
  <span>
    <div class="d-flex justify-content-between align-items-center mb-2">
      <h4>
        Group Comparison
      </h4>
      <button
        type="button"
        class="btn btn-primary float-right"
        @click="doCompare()"
        :disabled="isBusy"
      >
        <i class="cil-blur-linear btn-icon mr-1" v-if="!isBusy"></i>
        <i
          class="spinner-border spinner-border-sm btn-icon mr-1"
          v-if="isBusy"
        ></i>
        Compare
      </button>
    </div>
    <div class="card-deck mb-2">
      <div class="card">
        <div
          class="card-header text-primary d-flex justify-content-between align-items-center"
        >
          Group 1
          <button
            type="button"
            class="btn btn-sm"
            @click="showFilters = !showFilters"
          >
            <i v-if="!showFilters" class="cil-chevron-bottom btn-icon"></i>
            <i v-if="showFilters" class="cil-chevron-top btn-icon"></i>
          </button>
        </div>
        <div class="card-body" v-if="showFilters">
          <span v-for="(filter, index) in first" :key="index">
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
                  :id="`group-1-filter-enabled-${index}`"
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
                  :id="`group-1-filter-enabled-${index}`"
                  v-model="filter.enabled"
                ></b-form-checkbox>
              </div>
            </div>
          </span>
        </div>
      </div>
      <div class="card">
        <div
          class="card-header text-info d-flex justify-content-between align-items-center"
        >
          Group 2
          <button
            type="button"
            class="btn btn-sm"
            @click="showFilters = !showFilters"
          >
            <i v-if="!showFilters" class="cil-chevron-bottom btn-icon"></i>
            <i v-if="showFilters" class="cil-chevron-top btn-icon"></i>
          </button>
        </div>
        <div class="card-body" v-if="showFilters">
          <div class="form-row">
            <div class="form-group col-md-12">
              <b-form-checkbox id="compare-rest" v-model="compareRest">
                Compare against the rest of the data?
              </b-form-checkbox>
            </div>
          </div>
          <span v-if="!compareRest">
            <span v-for="(filter, index) in second" :key="index">
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
                    :id="`group-2-filter-enabled-${index}`"
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
                    :id="`group-2-filter-enabled-${index}`"
                    v-model="filter.enabled"
                  ></b-form-checkbox>
                </div>
              </div>
            </span>
          </span>
        </div>
      </div>
    </div>
    <AppExplainDetail clear-on-create show-secondary />
  </span>
</template>
<script>
import { mapState } from 'vuex'
import axios from 'axios'
import AppExplainDetail from './ExplainDetail.vue'
import msgMixin from '../mixins/msg-mixin'

export default {
  name: 'AppCompare',
  components: {
    AppExplainDetail
  },
  mixins: [msgMixin],
  computed: mapState(['filters']),
  data() {
    return {
      showFilters: true,
      isBusy: false,
      compareRest: false,
      first: null,
      second: null,
      firstId: 0,
      secondId: 0
    }
  },
  methods: {
    doCompare() {
      this.isBusy = true
      if (this.compareRest) {
        this.infoMsg('Comparing first group against the rest of the data')
      }

      const url = '/api/filter'
      const firstFilters = []
      this.first.forEach((filter) => {
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

          firstFilters.push(postFilter)
        }
      })
      const firstBody = {
        filters: firstFilters,
        cohort: false
      }
      const secondFilters = []
      let secondBody = {}
      if (!this.compareRest) {
        this.second.forEach((filter) => {
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

            secondFilters.push(postFilter)
          }
        })
        secondBody = {
          filters: secondFilters,
          cohort: false
        }
      }
      axios
        .post(url, firstBody)
        .then((res) => {
          if (res.data.id > 0) {
            this.firstId = res.data.id
            this.successMsg(`First group ID is ${this.firstId}`)
            if (this.compareRest) {
              this.$store.commit('setGroup', this.firstId)
            } else {
              return axios.post(url, secondBody)
            }
          } else {
            this.warningMsg(`Group 1: ${res.data.msg}`)
          }
        })
        .then((res) => {
          if (!this.compareRest) {
            if (res) {
              if (res.data.id > 0) {
                this.secondId = res.data.id
                this.successMsg(`Second group ID is ${this.secondId}`)
                this.$store.commit(
                  'setGroup',
                  `${this.firstId}-${this.secondId}`
                )
              } else {
                this.warningMsg(`Group 2: ${res.data.msg}`)
              }
            }
          }
        })
        .catch((err) => {
          console.error(err)
          this.errorMsg(err.message)
        })
        .finally(() => {
          this.showFilters = false
          this.isBusy = false
        })
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
