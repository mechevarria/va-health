<template>
  <div class="container">
    <div class="card-deck mb-4">
      <div class="card">
        <div class="card-body">
          <div class="row">
            <div class="col-sm-3">
              <img
                src="../assets/patient-icon.png"
                alt="avatar"
                class="img-fluid"
                style="width: 150px"
              />
            </div>
            <div class="col-sm-9 align-self-center">
              <h5 class="my-3">
                Patient Physical
                <i
                  class="spinner-border spinner-border-sm ml-1"
                  v-if="isBusy"
                ></i>
              </h5>
            </div>
          </div>

          <div class="row ml-3">
            <div class="col-sm-5">
              <p class="mb-0">ID</p>
            </div>
            <div class="col-sm-7">
              <p class="text-muted mb-0">{{ id }}</p>
            </div>
          </div>
          <div
            class="row ml-3"
            v-for="([key, value], index) in Object.entries(data.physical)"
            :key="index"
          >
            <div class="col-sm-5">
              <p class="mb-0">{{ key }}</p>
            </div>
            <div class="col-sm-7">
              <p class="text-muted mb-0">
                <span
                  v-if="value === 'Yes'"
                  class="badge rounded-pill bg-danger text-white"
                >
                  {{ value }}
                </span>
                <span v-else>
                  {{ value }}
                </span>
              </p>
            </div>
          </div>
        </div>
      </div>
      <div class="card">
        <div class="card-body">
          <p class="card-text">
            <strong class="mb-2">Demographics</strong>
            <i class="spinner-border spinner-border-sm ml-1" v-if="isBusy"></i>
          </p>
          <span
            v-for="([key, value], index) in Object.entries(data.demographics)"
            :key="index"
          >
            <div class="row">
              <div class="col-sm-3">
                <p class="mb-0 ml-2">{{ key }}</p>
              </div>
              <div class="col-sm-9">
                <p class="text-muted mb-0">{{ value }}</p>
              </div>
            </div>
            <hr class="ml-2" />
          </span>
        </div>
      </div>
    </div>
    <div class="card-deck mb-4">
      <div class="card">
        <div class="card-body">
          <p class="card-text">
            <strong class="mb-2">Risk Scores</strong>
            <i class="spinner-border spinner-border-sm ml-1" v-if="isBusy"></i>
          </p>
          <div class="row">
            <div class="col-md-5">
              <div
                class="c-callout"
                :class="getClassName(data.risk_scores.a1c_increase_risk)"
              >
                <small class="text-muted">A1C Increase Risk</small><br />
                <strong class="h4">{{
                  data.risk_scores.a1c_increase_risk
                }}</strong>
              </div>
            </div>
            <!--/.col-->
            <div class="col-md-7">
              <div
                class="c-callout"
                :class="getClassName(data.risk_scores.engagement_decrease_risk)"
              >
                <small class="text-muted">Engagement Decrease Risk</small><br />
                <strong class="h4">{{
                  data.risk_scores.engagement_decrease_risk
                }}</strong>
              </div>
            </div>
            <!--/.col-->
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <p class="card-text">
            <strong class="mb-2">Comorbidities</strong>
            <i class="spinner-border spinner-border-sm ml-1" v-if="isBusy"></i>
            <br />
            <span
              class="badge rounded-pill bg-danger text-white m-2"
              v-for="(key, index) in Object.keys(data.comorbidities)"
              :key="index"
              >{{ key }}</span
            >
          </p>
        </div>
      </div>
    </div>
    <div class="card">
      <div class="card-body">
        <strong class="mb-2">Medicines</strong>
        <pre>{{ data.carepath.meds }}</pre>
      </div>
    </div>
    <div class="card">
      <div class="card-body">
        <strong class="mb-2">Visits</strong>
        <pre>{{ data.carepath.visits }}</pre>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios'
import msgMixin from '../mixins/msg-mixin'

export default {
  name: 'AppPatientDetail',
  mixins: [msgMixin],
  data() {
    return {
      id: 0,
      data: {
        physical: {},
        demographics: {},
        risk_scores: {},
        comorbidities: {},
        raw: {}
      },
      isBusy: true
    }
  },
  methods: {
    getClassName(score) {
      switch (true) {
        case score < 0.333:
          return 'c-callout-success'
        case score > 0.333 && score < 0.666:
          return 'c-callout-warning'
        case score > 0.666:
          return 'c-callout-danger'
        default:
          return 'c-callout-info'
      }
    },
    getDetails() {
      this.isBusy = true
      const url = `/api/patient/${this.id}`
      axios
        .get(url)
        .then((res) => {
          this.data = res.data
        })
        .catch((err) => {
          console.error(err)
          this.errorMsg(err.message)
        })
        .finally(() => {
          this.isBusy = false
        })
    }
  },
  created() {
    this.$root.$on('bg::checkbox::change', (id, values) => {
      console.log('id:', id)
      console.log('values:', values)
    })
    this.id = this.$route.params.id
    this.getDetails()
  }
}
</script>
