<template>
  <span>
    <span v-if="groupId.length > 1" class="d-flex justify-content-between align-items-center mb-2">
      <h5>Top Explains for Group {{ groupId }}
        <i class="spinner-border spinner-border-sm mb-1 ml-1" v-if="isBusy"></i>
      </h5>

      <button type="button" class="btn btn-secondary" @click="clearGroup()" :disabled="isBusy" aria-label="clear">
        <span class="cil-x-circle icon mr-1"></span>Clear
      </button>
    </span>

    <div class="card" v-if="groupId.length > 1 && !isBusy">
      <div class="card-body">
        <h6 class="card-subtitle mb-2">{{ data.group_size }} patients in group</h6>
        <p class="card-text">
          <ul class="list-group list-group-flush">
            <li class="list-group-item" v-for="(explain, index) in data.explains" :key="index">
              {{ explain }}
            </li>
          </ul>
        </p>
      </div>
    </div>
    <router-view></router-view>
  </span>
</template>

<script>
import { mapState } from 'vuex'
import axios from 'axios'
import msgMixin from '../mixins/msg-mixin'

export default {
  name: 'AppExplain',
  mixins: [msgMixin],
  computed: mapState(['groupId']),
  data() {
    return {
      isBusy: false,
      data: {}
    }
  },
  methods: {
    clearGroup() {
      this.data = {}
      this.$store.commit('clearGroup')
    },
    getTopExplains(groupId) {
      this.isBusy = true
      this.data = {}
      let url = `/api/explain/${groupId}`
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
  watch: {
    groupId(newValue) {
      if(newValue.length > 1) {
        this.getTopExplains(newValue)
      }
    }
  },
  created() {
    this.clearGroup()
  }
}
</script>
