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
            <div class="d-flex justify-content-between">
              <div>{{ key }}</div>
              <div class="text-muted">{{ value }}</div>
            </div>
            <hr />
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
              class="badge bg-danger text-white m-2"
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
          <div class="table-responsive">
            <table class="table table-sm table-striped">
              <tr>
                <th>Medicine</th>
                <th>Post</th>
                <th>Pre</th>
              </tr>
              <tbody>
                <tr
                  v-for="(key, index) in Object.keys(data.carepath.meds)"
                  :key="index"
                >
                  <td>{{ key }}</td>
                  <td
                    v-for="(entry, index) in Object.entries(
                      data.carepath.meds[key]
                    )"
                    :key="index"
                  >
                    <i
                      class="cil-check-circle text-primary"
                      v-if="entry[1] == 1"
                    ></i>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <div class="card">
        <div class="card-body">
          <p class="card-text">
            <strong class="mb-2">Diabetic Medicines</strong>
            <i class="spinner-border spinner-border-sm ml-1" v-if="isBusy"></i>
          </p>
          <div class="table-responsive">
            <table class="table table-sm table-striped">
              <tr>
                <th>Medicine</th>
                <th>Period 1 - 2</th>
                <th>Period 3</th>
              </tr>
              <tbody>
                <tr
                  v-for="(key, index) in Object.keys(
                    data.carepath.diabetic_meds
                  )"
                  :key="index"
                >
                  <td>{{ key }}</td>
                  <td
                    v-for="(entry, index) in Object.entries(
                      data.carepath.diabetic_meds[key]
                    )"
                    :key="index"
                  >
                    <i
                      class="cil-check-circle text-primary"
                      v-if="entry[1] == 1"
                    ></i>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <div class="card">
        <div class="card-body">
          <p class="card-text">
            <strong class="mb-2">Visits</strong>
            <i class="spinner-border spinner-border-sm ml-1" v-if="isBusy"></i>
          </p>
          <div class="table-responsive">
            <table class="table table-sm table-striped">
              <tr>
                <th>Visit Type</th>
                <th>Period 1</th>
                <th>Period 2</th>
                <th>Period 3</th>
              </tr>
              <tbody>
                <tr
                  v-for="(key, index) in Object.keys(data.carepath.visits)"
                  :key="index"
                >
                  <td>{{ key }}</td>
                  <td
                    v-for="(entry, index) in Object.entries(
                      data.carepath.visits[key]
                    )"
                    :key="index"
                  >
                    {{ entry[1] }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    <hr />
    <div class="form-row align-items-center mb-4">
      <div class="col-auto">
        <label for="selected-criteria" class="pt-1"
          >Cohort Criteria for Carepaths</label
        >
        <br />
        <b-form-radio-group
          id="selected-criteria"
          v-model="selectedCriteria"
          :options="criteriaOptions"
          value-field="item"
          text-field="name"
          :disabled="isBusy"
          button-variant="outline-secondary"
          buttons
        ></b-form-radio-group>
        <a
          role="button"
          class="ml-2 mt-1"
          v-b-tooltip.hover
          title="Medicines includes Conditions and Demographics. Visits includes Demographics"
        >
          <i class="c-icon cil-info text-secondary app-icon-hover"></i>
        </a>
      </div>
      <div class="col-auto ml-4">
        <label for="medicine-threshold"
          >Medicine Threshold <strong>{{ medicineThreshold }}</strong></label
        >
        <b-form-input
          id="medicine-threshold"
          v-model="medicineThreshold"
          type="range"
          min="0"
          max="100"
          :disabled="isBusy"
        ></b-form-input>
      </div>
      <div class="col-auto ml-4 mt-3">
        <button
          type="button"
          class="btn btn-primary"
          @click="postDetails(false)"
          :disabled="isBusy"
        >
          <i class="cil-reload btn-icon mr-1" v-if="!isBusy"></i>
          <i
            class="spinner-border spinner-border-sm btn-icon mr-1"
            v-if="isBusy"
          ></i>
          Update
        </button>
      </div>
    </div>
    <h5>Consensus Carepath</h5>
    <div class="card-deck mb-4">
      <div class="card">
        <div class="card-body">
          <p class="card-text">
            <strong class="mb-2">Medicines</strong>
            <i class="spinner-border spinner-border-sm ml-1" v-if="isBusy"></i>
          </p>
          <div class="table-responsive">
            <table class="table table-sm table-striped">
              <tr>
                <th>Medicine</th>
                <th>Post</th>
                <th>Pre</th>
              </tr>
              <tbody>
                <tr
                  v-for="(key, index) in Object.keys(
                    data.carepath_consensus.meds
                  )"
                  :key="index"
                >
                  <td>{{ key }}</td>
                  <td
                    v-for="(entry, index) in Object.entries(
                      data.carepath_consensus.meds[key]
                    )"
                    :key="index"
                  >
                    <b-progress
                      show-value
                      :precision="2"
                      :value="entry[1]"
                      variant="primary"
                      :max="1"
                      v-b-tooltip
                      :title="entry[0]"
                    ></b-progress>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <div class="card">
        <div class="card-body">
          <strong>Diabetic Medicines</strong>
          <i class="spinner-border spinner-border-sm ml-1" v-if="isBusy"></i>
          <div class="d-flex flex-row">
            <div>
              <div
                class="c-callout"
                :class="getA1cClass(prescribedA1cConsensus)"
              >
                <small class="text-muted">Prescribed A1C Change</small><br />
                <strong class="h4">{{ prescribedA1cConsensus }}</strong>
              </div>
            </div>
            <div>
              <div
                class="c-callout"
                :class="getA1cClass(data.carepath_consensus.average_a1c_change)"
              >
                <small class="text-muted">Average A1C Change</small><br />
                <strong class="h4">{{
                  data.carepath_consensus.average_a1c_change
                }}</strong>
              </div>
            </div>
            <div class="align-self-center">
              <button
                type="button"
                class="btn btn-sm btn-primary"
                @click="postA1cChange"
                :disabled="isA1cBusy"
              >
                <i class="cil-sync" v-if="!isA1cBusy"></i>
                <i
                  class="spinner-border spinner-border-sm"
                  v-if="isA1cBusy"
                ></i>
              </button>
            </div>
          </div>
          <div class="table-responsive">
            <table class="table table-sm table-striped">
              <tr>
                <th>Prescribed</th>
                <th>Medicine</th>
                <th>Period 1 - 2</th>
                <th>Period 3</th>
              </tr>
              <tbody>
                <tr
                  v-for="(key, index) in Object.keys(
                    data.carepath_consensus.diabetic_meds
                  )"
                  :key="index"
                >
                  <td>
                    <b-form-checkbox
                      v-model="selectedMeds"
                      :value="`${key}`"
                    ></b-form-checkbox>
                  </td>
                  <td>{{ key }}</td>
                  <td
                    v-for="(entry, index) in Object.entries(
                      data.carepath_consensus.diabetic_meds[key]
                    )"
                    :key="index"
                  >
                    <b-progress
                      show-value
                      :precision="2"
                      :value="entry[1]"
                      variant="primary"
                      :max="1"
                      v-b-tooltip
                      :title="entry[0]"
                    ></b-progress>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <div class="card">
        <div class="card-body">
          <p class="card-text">
            <strong class="mb-2">Visits</strong>
            <i class="spinner-border spinner-border-sm ml-1" v-if="isBusy"></i>
          </p>
          <div class="table-responsive">
            <table class="table table-sm table-striped">
              <tr>
                <th>Visit Type</th>
                <th>Period 1</th>
                <th>Period 2</th>
                <th>Period 3</th>
              </tr>
              <tbody>
                <tr
                  v-for="(key, index) in Object.keys(
                    data.carepath_consensus.visits
                  )"
                  :key="index"
                >
                  <td>{{ key }}</td>
                  <td
                    v-for="(entry, index) in Object.entries(
                      data.carepath_consensus.visits[key]
                    )"
                    :key="index"
                  >
                    <b-progress
                      show-value
                      :precision="2"
                      :value="entry[1]"
                      variant="primary"
                      :max="1"
                      v-b-tooltip
                      :title="entry[0]"
                    ></b-progress>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    <h5>Recommended Carepath</h5>
    <div class="card-deck mb-4">
      <div class="card">
        <div class="card-body">
          <p class="card-text">
            <strong class="mb-2">Medicines</strong>
            <i class="spinner-border spinner-border-sm ml-1" v-if="isBusy"></i>
          </p>
          <div class="table-responsive">
            <table class="table table-sm table-striped">
              <tr>
                <th>Medicine</th>
                <th>Post</th>
                <th>Pre</th>
              </tr>
              <tbody>
                <tr
                  v-for="(key, index) in Object.keys(
                    data.carepath_recommended.meds
                  )"
                  :key="index"
                >
                  <td>{{ key }}</td>
                  <td
                    v-for="(entry, index) in Object.entries(
                      data.carepath_recommended.meds[key]
                    )"
                    :key="index"
                  >
                    <b-progress
                      show-value
                      :precision="2"
                      :value="entry[1]"
                      variant="primary"
                      :max="1"
                      v-b-tooltip
                      :title="entry[0]"
                    ></b-progress>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <div class="card">
        <div class="card-body">
          <strong>Diabetic Medicines</strong>
          <i class="spinner-border spinner-border-sm ml-1" v-if="isBusy"></i>
          <div class="d-flex flex-row">
            <div>
              <div
                class="c-callout"
                :class="getA1cClass(prescribedA1cRecommend)"
              >
                <small class="text-muted">Prescribed A1C Change</small><br />
                <strong class="h4">{{ prescribedA1cRecommend }}</strong>
              </div>
            </div>
            <div>
              <div
                class="c-callout"
                :class="
                  getA1cClass(data.carepath_recommended.average_a1c_change)
                "
              >
                <small class="text-muted">Average A1C Change</small><br />
                <strong class="h4">{{
                  data.carepath_recommended.average_a1c_change
                }}</strong>
              </div>
            </div>
            <div class="align-self-center">
              <button
                type="button"
                class="btn btn-sm btn-primary"
                @click="postA1cChange"
                :disabled="isA1cBusy"
              >
                <i class="cil-sync" v-if="!isA1cBusy"></i>
                <i
                  class="spinner-border spinner-border-sm"
                  v-if="isA1cBusy"
                ></i>
              </button>
            </div>
          </div>
          <div class="table-responsive">
            <table class="table table-sm table-striped">
              <tr>
                <th>Prescribed</th>
                <th>Medicine</th>
                <th>Period 1 - 2</th>
                <th>Period 3</th>
              </tr>
              <tbody>
                <tr
                  v-for="(key, index) in Object.keys(
                    data.carepath_recommended.diabetic_meds
                  )"
                  :key="index"
                >
                  <td>
                    <b-form-checkbox
                      v-model="selectedMeds"
                      :value="`${key}`"
                    ></b-form-checkbox>
                  </td>
                  <td>{{ key }}</td>
                  <td
                    v-for="(entry, index) in Object.entries(
                      data.carepath_recommended.diabetic_meds[key]
                    )"
                    :key="index"
                  >
                    <b-progress
                      show-value
                      :precision="2"
                      :value="entry[1]"
                      variant="primary"
                      :max="1"
                      v-b-tooltip
                      :title="entry[0]"
                    ></b-progress>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <div class="card">
        <div class="card-body">
          <p class="card-text">
            <strong class="mb-2">Visits</strong>
            <i class="spinner-border spinner-border-sm ml-1" v-if="isBusy"></i>
          </p>
          <div class="table-responsive">
            <table class="table table-sm table-striped">
              <tr>
                <th>Visit Type</th>
                <th>Period 1</th>
                <th>Period 2</th>
                <th>Period 3</th>
              </tr>
              <tbody>
                <tr
                  v-for="(key, index) in Object.keys(
                    data.carepath_recommended.visits
                  )"
                  :key="index"
                >
                  <td>{{ key }}</td>
                  <td
                    v-for="(entry, index) in Object.entries(
                      data.carepath_recommended.visits[key]
                    )"
                    :key="index"
                  >
                    <b-progress
                      show-value
                      :precision="2"
                      :value="entry[1]"
                      variant="primary"
                      :max="1"
                      v-b-tooltip
                      :title="entry[0]"
                    ></b-progress>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    <!-- <pre>selectedMeds: {{ selectedMeds }}</pre> -->
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
      selectedMeds: [],
      selectedCriteria: 'meds',
      prescribedA1cConsensus: '0',
      prescribedA1cRecommend: '0',
      criteriaOptions: [
        { item: 'meds', name: 'Medicines' },
        { item: 'visits', name: 'Visits' }
      ],
      medicineThreshold: 70,
      data: {},
      isBusy: true,
      isA1cBusy: true
    }
  },
  methods: {
    clearData() {
      this.data = {
        physical: {},
        demographics: {},
        risk_scores: {},
        comorbidities: {},
        raw: {},
        carepath: {
          diabetic_meds: {},
          meds: {},
          visits: {}
        },
        carepath_consensus: {
          average_a1c_change: '0',
          diabetic_meds: {},
          meds: {},
          visits: {}
        },
        carepath_recommended: {
          average_a1c_change: '0',
          diabetic_meds: {},
          meds: {},
          visits: {}
        }
      }
    },
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
    getA1cClass(strScore) {
      const score = parseFloat(strScore)
      if (score > 0) {
        return 'c-callout-danger'
      } else if (score < 0) {
        return 'c-callout-success'
      } else {
        return 'c-callout-info'
      }
    },
    postA1cChange() {
      this.isA1cBusy = true
      this.prescribedA1cConsensus = '0'
      this.prescribedA1cRecommend = '0'

      const url = '/api/patient/prescribed'
      const body = {
        patient_id: this.id,
        neighbor_criteria: this.selectedCriteria,
        medicines: this.selectedMeds
      }
      axios
        .post(url, body)
        .then((res) => {
          this.prescribedA1cConsensus = res.data.consensus_prescribed_a1c_change
          this.prescribedA1cRecommend =
            res.data.recommended_prescribed_a1c_change
        })
        .catch((err) => {
          console.error(err)
          this.errorMsg(err.message)
        })
        .finally(() => {
          this.isA1cBusy = false
        })
    },
    postDetails(doA1c) {
      this.clearData()
      this.isBusy = true
      const url = '/api/patient'
      const body = {
        patient_id: this.id,
        neighbor_criteria: this.selectedCriteria,
        medicine_threshold: this.medicineThreshold
      }
      axios
        .post(url, body)
        .then((res) => {
          this.data = res.data

          // set default selectedMeds based on carepath
          const meds = this.data.carepath.diabetic_meds
          for (const key of Object.keys(meds)) {
            if (meds[key]._period3 === 1) {
              this.selectedMeds.push(key)
            }
          }
        })
        .catch((err) => {
          console.error(err)
          this.errorMsg(err.message)
        })
        .finally(() => {
          this.isBusy = false
          this.isA1cBusy = false
          
          if(doA1c) {
            this.postA1cChange()
          }
        })
    }
  },
  created() {
    this.id = this.$route.params.id
    this.postDetails(true)
  }
}
</script>
<style>
.app-icon-hover:hover {
  font-weight: bold;
}
</style>
