<template>
  <span>
    <h5>Groups: <i class="spinner-border spinner-border-sm mr-1" v-if="isBusy"></i></h5>
    <div class="row row-cols-1 row-cols-md-3">
      <div class="col" v-for="(group, index) in groups" v-bind:key="group.id">
        <div class="card">
          <div class="card-header">
            <h5 class="d-flex justify-content-between align-items-center">
              {{ group.id }}
              <button type="button" class="btn btn-sm" @click="toggleExplain(index)">
                <i v-if="!group.visible" class="cil-chevron-bottom btn-icon"></i>
                <i v-if="group.visible" class="cil-chevron-top btn-icon"></i>
              </button>
            </h5>
            <span class="bg-light text-dark">
              <span class="font-weight-bold">Patients:</span> {{ group.group_size }} | <span class="font-weight-bold">Top
                Explainers:</span> {{ group.explains.length }}
            </span>
          </div>
          <div class="card-body" v-if="group.visible">
            <div class="card-text">
              <div class="d-flex justify-content-between align-items-center">
                <b>Top Explainers:</b>
                <button class="btn btn-primary mt-2" @click="getGroupDetails(group.id, index)">
                  <i class="cil-list-rich btn-icon mr-1"></i>All Explainers
                </button>
              </div>
              <li v-for="(explain, index) in group.explains" v-bind:key="index">{{ explain }}</li>
            </div>
          </div>
        </div>
      </div>
    </div>
    <router-view></router-view>
  </span>
</template>

<script>
import axios from 'axios'
import msgMixin from '..//mixins/msg-mixin';

export default {
  name: 'AppGroup',
  mixins: [msgMixin],
  data() {
    return {
      isBusy: false,
      groups: []
    }
  },
  methods: {
    getExplain() {
      this.isBusy = true
      const url = '/api/explain'
      axios
        .get(url)
        .then((res) => {
          this.groups = res.data
          this.groups.forEach(group => {
            group.visible = false
          });
        })
        .catch((err) => {
          console.error(err)
          this.errorMsg(err.message)
        })
        .finally(() => {
          this.isBusy = false
        })
    },
    toggleExplain(index) {
      let group = this.groups[index]
      group.visible = !group.visible
      this.$set(this.groups, index, group)
    },
    getGroupDetails(id, index) {
      console.log('Getting group details', id)
      this.toggleExplain(index)
    }
  },
  created() {
    this.getExplain()
  }
}
</script>