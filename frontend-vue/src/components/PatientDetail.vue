<template>
  <span>
    <div class="container">
      <div class="row">
        <div class="col-lg-4">
          <div class="card mb-4">
            <div class="card-body text-center">
              <img
                src="../assets/patient-icon.png"
                alt="avatar"
                class="img-fluid"
                style="width: 150px"
              />
              <h5 class="my-3">Patient Physical</h5>
              <p class="mb-1">
                ID <span class="text-muted">{{ id }}</span>
              </p>
              <i class="spinner-border spinner-border-sm ml-1" v-if="isBusy" ></i>
              <p
                class="mb-1"
                v-for="([key, value], index) in Object.entries(data.physical)"
                :key="index"
              >
                {{ key }} <span class="text-muted">{{ value }}</span>
              </p>
            </div>
          </div>
        </div>
        <div class="col-lg-8">
          <div class="card mb-4">
            <div class="card-body">
              <p class="card-text">
                <strong class="mb-2">Demographics</strong>
                <i
                  class="spinner-border spinner-border-sm ml-1"
                  v-if="isBusy"
                ></i>
              </p>
              <span
                v-for="([key, value], index) in Object.entries(
                  data.demographics
                )"
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
          <div class="row">
            <div class="col-md-6">
              <div class="card mb-4 mb-md-0">
                <div class="card-body">
                  <p class="card-text">
                    <strong class="mb-2">Risk Scores</strong>
                    <i
                      class="spinner-border spinner-border-sm ml-1"
                      v-if="isBusy"
                    ></i>
                  </p>
                  <div class="row">
                    <div class="col-md-5">
                      <div class="c-callout c-callout-danger">
                        <small class="text-muted">A1C Increase Risk</small><br />
                        <strong class="h4">{{ data.risk_scores.a1c_increase_risk }}</strong>
                      </div>
                    </div>
                    <!--/.col-->
                    <div class="col-md-7">
                      <div class="c-callout c-callout-info">
                        <small class="text-muted">Engagement Decrease Risk</small><br />
                        <strong class="h4">{{ data.risk_scores.engagement_decrease_risk }}</strong>
                      </div>
                    </div>
                    <!--/.col-->
                  </div>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="card mb-4 mb-md-0">
                <div class="card-body">
                  <p class="card-text">
                    <strong class="mb-2">Comorbidities</strong>
                    <i
                      class="spinner-border spinner-border-sm ml-1"
                      v-if="isBusy"
                    ></i>
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
          </div>
        </div>
      </div>
    </div>
  </span>
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
