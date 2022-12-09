import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
    state: {
        isSidebarMin: false,
        isSidebarShown: true,
        messages: [],
        groupId: 0,
        filterId: 0,
        filters: [{
            name: 'race',
            categorical: true,
            value: 'African American',
            is_equal: false
        }, {
            name: 'AgeAtIndexDate',
            categorical: false,
            min: 25,
            max: 55
        }, {
            name: 'A1C_last_period4_2021-03-01_2022-03-01',
            categorical: false,
            min: 7,
            max: 12
        }, {
            name: 'TotalSeriesCount',
            categorical: false,
            min: 0,
            max: 3
        }]
    },
    mutations: {
        toggleSidebarMin(state) {
            state.isSidebarMin = !state.isSidebarMin
        },
        sidebarMin(state) {
            state.isSidebarMin = true
        },
        sidebarMax(state) {
            state.isSidebarMin = false
        },
        toggleSidebarShown(state) {
            state.isSidebarShown = !state.isSidebarShown
        },
        sidebarHide(state) {
            state.isSidebarShown = false
        },
        sidebarShow(state) {
            state.isSidebarShown = true
        },
        addMessage(state, msg) {
            state.messages.push(msg)
        },
        clearMessages(state) {
            state.messages = []
        },
        setGroup(state, id) {
            state.groupId = id
        },
        clearGroup(state) {
            state.groupId = 0
        },
        setFilterId(state, id) {
            state.filterId = id
        },
        setFilters(state, filters) {
            state.filters = filters
        },
        clearFilter(state) {
            state.filterId = 0
        }
    }
})

export default store