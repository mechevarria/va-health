<template>
  <span>
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

      <div class="card">
        <div class="card-body">
          <p class="card-text">
            <strong class="mb-2">Risk Scores</strong>
            <i class="spinner-border spinner-border-sm ml-1" v-if="isBusy"></i>
          </p>
          <div
            class="c-callout mb-4 mt-4"
            :class="getClassName(data.risk_scores.a1c_increase_risk)"
          >
            <small class="text-muted">A1C Increase Risk</small><br />
            <strong class="h4">{{ data.risk_scores.a1c_increase_risk }}</strong>
          </div>
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
    <h5>Carepath</h5>
    <div class="card-deck mb-4">
      <div class="card">
        <div class="card-body">
          <p class="card-text">
            <strong class="mb-2">Medicines</strong>
            <i class="spinner-border spinner-border-sm ml-1" v-if="isBusy"></i>
          </p>
          <table class="table table-striped">
            <tr>
              <th>Medicine</th>
              <th>Period 1 - 2</th>
              <th>Period 3</th>
            </tr>
            <tbody>
              <tr
                v-for="(entry, index) in Object.entries(data.carepath.meds)"
                :key="index"
              >
                <td>{{ entry[0] }}</td>
                <td>{{ entry[1]._period1_2 }}</td>
                <td>{{ entry[1]._period3 }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="card">
        <div class="card-body">
          <p class="card-text">
            <strong class="mb-2">Visits</strong>
            <i class="spinner-border spinner-border-sm ml-1" v-if="isBusy"></i>
          </p>
          <table class="table table-striped">
            <tr>
              <th>Visit Type</th>
              <th>Period 1</th>
              <th>Period 2</th>
              <th>Period 3</th>
            </tr>
            <tbody>
              <tr
                v-for="(entry, index) in Object.entries(data.carepath.visits)"
                :key="index"
              >
                <td>{{ entry[0] }}</td>
                <td>{{ entry[1]._period1 }}</td>
                <td>{{ entry[1]._period2 }}</td>
                <td>{{ entry[1]._period3 }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <b-form-group label="Nearest Neighbor Criteria for Consensus and Recommended Carepaths">
      <b-form-radio-group
        v-model="selectedCriteria"
        :options="criteriaOptions"
        class="mb-3"
        value-field="item"
        text-field="name"
        :disabled="isBusy"
        button-variant="outline-primary"
        buttons
      ></b-form-radio-group>
    </b-form-group>
    <h5>Consensus Carepath</h5>
    <h5>Recommended Carepath</h5>
    <pre>{{ data }}</pre>
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
      selectedCriteria: 'meds',
      criteriaOptions: [
        { item: 'meds', name: 'Medicines' },
        { item: 'visits', name: 'Visits' }
      ],
      data: {
        physical: {},
        demographics: {},
        risk_scores: {},
        comorbidities: {},
        raw: {},
        carepath: {
          meds: {},
          visits: {}
        }
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
    postDetails() {
      this.isBusy = true
      const url = '/api/patient'
      const body = {
        patient_id: this.id,
        neighbor_criteria: this.selectedCriteria
      }
      axios
        .post(url, body)
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
    this.id = this.$route.params.id
    this.postDetails()
  }
}
</script>
