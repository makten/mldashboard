/* global $ */

/***
 *	Load dependences*
 */
require('./bootstrap');


/**
 * New up components
 */
Vue.component('dashboard-component', require('./components/Dashboard.vue'));
Vue.component('header-section', require('./components/Header.vue'));
Vue.component('sidebar', require('./components/Sidebar.vue'));

import { store } from "./store.js";

window.eventBroadcaster = new Vue();



window.papa_config = {
    delimiter: ",", // auto-detect
    newline: "", // auto-detect
    quoteChar: '"',
    header: false,
    dynamicTyping: false,
    preview: 0,
    encoding: "",
    worker: false,
    comments: false,
    step: undefined,
    complete: undefined,
    error: undefined,
    download: false,
    skipEmptyLines: false,
    chunk: undefined,
    fastMode: false,
    beforeFirstChunk: undefined,
    withCredentials: undefined
}



const app = new Vue({

    el: "#app",
    store: store,

    mounted() {
        this.$nextTick(function() {


            $.material.init();
            $.material.ripples();
            $.material.input();
            $.material.checkbox();

            $('label.tree-toggler').click(function() {
                $(this).parent().children('ul.tree').toggle(300);
            });

            // $('select').selectize({
            // 	placeholder: 'Select a month',
            // 	// sortField: 'asc',
            // 	create: true,				
            // });



            //Tooltip popups
            $(".top").tooltip({
                placement: "top"
            });

            $(".right").tooltip({
                placement: "right"
            });

            $(".bottom").tooltip({
                placement: "bottom"
            });

            $(".left").tooltip({
                placement: "left"
            });


        })
    }

})