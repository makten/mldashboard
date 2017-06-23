import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export const store = new Vuex.Store({
    state: {
        ucs: [
            { name: "Hafiz Abass", profession: "Software Engineer", interests: "Technology" },
            { name: "John Doe", profession: "Software Engineer", interests: "Technology" }
        ]
    },

    getters: {
        uscsystems(state) {
            return state.ucs
        }
    },

    mutations: {
        adducs(state) {
            // state.usc.push()
        }
    }
});