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
        colorOptions: [{
            value: 'A1Clast_period2_to_4_change',
            text: 'Change in A1C'
        }, {
            value: 'visits_count_permonth_period2_to_4_change',
            text: 'Change in Engagement'
        }, {
            value: 'Is_increase_A1Clast_period2_to_4_change',
            text: 'Predicted A1C Increase'
        }, {
            value: 'Is_decrease_visits_count_permonth_period2_to_4_change',
            text: 'Predicted Change in Engagement'
        }],
        filters: [{
            name: 'race',
            label: 'Race',
            categorical: true,
            value: 'African American',
            valueOptions: [{
                value: 'White', text: 'White'
            }, {
                value: 'African American', text: 'African American'
            }, {
                value: 'Asian', text: 'Asian'
            }],
            boolOptions: [{
                value: true, text: 'Yes'
            }, {
                value: false, text: 'No'
            }],
            is_equal: false
        }, {
            name: 'AgeAtIndexDate',
            label: 'Age',
            categorical: false,
            min: 25,
            inputMin: 25,
            max: 55,
            inputMax: 90
        }, {
            name: 'A1C_last_period4_2021-03-01_2022-03-01',
            label: 'A1C',
            categorical: false,
            min: 7,
            inputMin: 5,
            max: 12,
            inputMax: 15
        }, {
            label: 'Vaccination Status',
            name: 'TotalSeriesCount',
            categorical: false,
            min: 0,
            inputMin: 0,
            max: 3,
            inputMax: 3
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