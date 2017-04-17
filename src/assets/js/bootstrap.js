window._ = require('lodash');

window.$ = window.jQuery = require('jquery');

require('bootstrap-sass');
require('bootstrap');
require('d3')
require('arrive/src/arrive.js');
require('bootstrap-material-design/dist/js/material.js');
require('bootstrap-material-design/dist/js/ripples.js');
require('../mixins/dropdown.js');

window.axios = require('axios');
import VueCharts from 'vue-chartjs';
window.VueCharts = VueCharts;
import { ServerTable, ClientTable, Event } from 'vue-tables-2';
import VeeValidate from 'vee-validate';


window.Vue = require('vue');
Vue.use(ClientTable, {}, false, require('./template.js')('client'))
Vue.use(VeeValidate)

import NProgress from 'nprogress';



window.Validator = require('validatorjs');

Validator.register('multi_required', function(value, requirement, attr){
	console.log(attr)
}, 'test');


require('vue-resource');

import Form from '../core/Form.js';
import Errors from '../core/Errors.js';
// import tabs from '../core/tabs.js';
// import tab from '../core/tab.js';
import Bar from '../charts/Bar.js';
import LineChart from '../charts/Line.js';
import Gauge from '../charts/Guage.js';
import Moment from 'moment';
import ChartJs from 'chart.js';
window.Chartjs = ChartJs;


window.Form = Form;
window.Errors = Errors;
window.Bar = Bar;
window.LineChart = LineChart;
window.Gauge = Gauge;
window.Moment = Moment;
Moment.locale('nl');

require('arrive/src/arrive.js');
require('bootstrap-material-design/dist/js/material.js');
require('bootstrap-material-design/dist/js/ripples.js');
require('selectize');

// axios.defaults.headers.common['X-CSRFToken'] = csrfToken;

axios.interceptors.request.use((request) => {

	request.headers['X-CSRF-TOKEN'] = csrfToken;
	return request;

});


// Vue.http.interceptors.push((request, next) => {

// 	request.headers.set('X-CSRF-TOKEN', csrfToken);

// 	next();

// });