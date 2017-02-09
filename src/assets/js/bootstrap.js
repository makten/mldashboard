window._ = require('lodash');

window.$ = window.jQuery = require('jquery');


require('bootstrap-sass');
require('bootstrap');


window.axios = require('axios')

window.Vue = require('vue');
require('vue-resource');

import Form from '../core/Form.js';
import Errors from '../core/Errors.js';
import Moment from 'moment';
import ChartJs from 'chart.js'
window.Chartjs = ChartJs;


window.Form = Form;
window.Errors = Errors;
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