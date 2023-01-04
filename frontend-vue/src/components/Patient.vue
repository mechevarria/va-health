<template>
  <div class="card-deck mb-3">
    <div class="card">
      <div class="card-header">
        <i class="spinner-border spinner-border-sm mr-1" v-if="isBusy"></i>
        Patients
      </div>
      <div class="card-body">
        <div class="card-text">
          <p>
            Displaying {{ (currentPage - 1) * perPage + 1 }} to
            {{ currentPage * perPage }} of
            <strong>{{ this.totalRows }}</strong>
            total patients
          </p>
          <b-table
            striped
            :items="data"
            :fields="fields"
            :current-page="currentPage"
            :per-page="perPage"
            :primary-key="'ID'"
            :tbody-tr-class="'app-pointer'"
            :no-provider-paging="true"
            :no-provider-sorting="true"
            responsive
            bordered
            ref="table"
            @row-clicked="onRowClick"
          ></b-table>
          <div class="d-flex">
            <b-pagination
              v-model="currentPage"
              :total-rows="totalRows"
              :per-page="perPage"
              :disabled="isBusy"
            ></b-pagination>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import msgMixin from '../mixins/msg-mixin'

export default {
  name: 'AppPatient',
  mixins: [msgMixin],
  data() {
    return {
      data: [],
      totalRows: 0,
      currentPage: 1,
      perPage: 10,
      isBusy: false,
      fields: [
        {
          key: 'ID',
          label: 'ID',
          sortable: true
        },
        {
          key: 'Age',
          label: 'Age',
          sortable: true
        },
        {
          key: 'Gender',
          label: 'Gender',
          sortable: true
        },
        {
          key: 'Ethnicity',
          label: 'Ethnicity',
          sortable: true
        },
        {
          key: 'Race',
          label: 'Race',
          sortable: true
        },
        {
          key: 'Vaccination_Status',
          label: 'Vaccination Status',
          sortable: true
        }
      ]
    }
  },
  methods: {
    onRowClick(row) {
      this.$router.push(`/home/patient/${row.ID}`)
    },
    getData() {
      this.isBusy = true

      const url = '/api/patient'
      axios
        .get(url)
        .then((res) => {
          this.data = res.data
          this.totalRows = this.data.length
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
    this.getData()
  }
}
</script>
<style scoped>
.app-pointer {
  cursor: pointer;
}
</style>
