/**
*	This component handles all chassis server api calls
*
*/
<script>

	import vSelect from 'vue-select';    
	import { Validator } from 'vee-validate';
	import modal from '../../../core/modal.vue';
	import linechart from '../../../core/linechart.vue';

	export default {
		
		components: {            
			vSelect,
			Bar,
			// LineChart,            
			Validator,
			modal,
			linechart
		},


		data() {

			return {

				showStats: false,
				gauges: [],
				chassis_servers: [],
				blade_cpustats: [],
				loadedStats: '',
				faultDetails: [],
				modalset: false,

				faults: '',      
				warnings: [],
				minors: [],
				majors: [],
				criticals: [],

				chassisServerColumns: [
				'equipment', 'model', 'serial', 'num_of_cpus', 'num_of_cores', 
				'enabled_cpu_cores', 'total_memory', 'available_memory', 'NICs', 
				'power', 'serial', 'presence', 'assocState', 'stats', 'faults'
				],

				chassisServerOptions: {

					templates: {


					}
				},

				faultDetailsColumns: ['created', 'code', 'type', 'severity', 'descr', 'rule'],
				faultDetailsOptions: {
				},
				datacollection: {
					labels: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'I', 'J', 'K', 'L'],
					datasets: [
					{
						label: 'CPU  1',
						backgroundColor: '#B2AD65',
						data: [2, 3, 4, 9, 5, 4, 2, 2, 1, 3, 1]
					}, {
						label: 'CPU 2',
						backgroundColor: '#BFCB05',
						data: [3, 4, 6, 3, 4, 4, 3, 1, 3, 5,]
					}
					]
				},

				chartdata: {
					labels: [Moment().add(Math.random(1, 10), 'hours').format('HH:mm:ss a'), Moment().add(Math.random(1, 10), 'hours').format('HH:mm:ss a'), Moment().add(Math.random(1, 10), 'hours').format('HH:mm:ss a'), Moment().add(Math.random(1, 10), 'hours').format('HH:mm:ss a'), Moment().add(Math.random(1, 10), 'hours').format('HH:mm:ss a'), Moment().add(Math.random(1, 10), 'hours').format('HH:mm:ss a'), Moment().add(Math.random(1, 10), 'hours').format('HH:mm:ss a'), Moment().add(Math.random(1, 10), 'hours').format('HH:mm:ss a'), Moment().add(Math.random(1, 10), 'hours').format('HH:mm:ss a'), Moment().add(Math.random(1, 10), 'hours').format('HH:mm:ss a'), Moment().add(Math.random(1, 10), 'hours').format('HH:mm:ss a'), Moment().add(Math.random(1, 10), 'hours').format('HH:mm:ss a')],

					datasets : [
					{
						label: "CPU 1",
						fill: true,
						lineTension: 0.11,
						backgroundColor: "rgba(75,192,192,0.4)",
						borderColor: "rgba(75,192,192,1)",
						borderCapStyle: 'butt',
						borderDash: [],
						borderDashOffset: 0.9,
						borderJoinStyle: 'miter',
						pointBorderColor: "rgba(75,192,192,1)",
						pointBackgroundColor: "#fff",
						pointBorderWidth: 1,
						pointHoverRadius: 5,
						pointHoverBackgroundColor: "rgba(75,192,192,1)",
						pointHoverBorderColor: "rgba(220,220,220,1)",
						pointHoverBorderWidth: 2,
						pointRadius: 1,
						pointHitRadius: 1,
						data : [65,59,90,81,56,45,30,20,3,99],
						
					},
					{
						label: "CPU 2",
						fill: true,
						lineTension: 0.11,
						backgroundColor: "rgba(215, 112, 120, 0.9)",
						borderColor: "rgba(75,192,192,1)",
						borderCapStyle: 'butt',
						borderDash: [],
						borderDashOffset: 0.9,
						borderJoinStyle: 'miter',
						pointBorderColor: "rgba(75,192,192,1)",
						pointBackgroundColor: "#fff",
						pointBorderWidth: 1,
						pointHoverRadius: 5,
						pointHoverBackgroundColor: "rgba(75,192,192,1)",
						pointHoverBorderColor: "rgba(220,220,220,1)",
						pointHoverBorderWidth: 2,
						pointRadius: 1,
						pointHitRadius: 1,						
						data : [28,48,40,19,96,87,66,97,92,85]
					}
					]
				},

				chartOption: {
					
					animation: {
						duration: 0,              
						scaleOverride : true,             
						scaleSteps : 10,             
						scaleStepWidth : 10,              
						scaleStartValue : 0
					},

					elements: {
						line: {
							borderWidth: 1,
						},
						point: {
							radius: 2,
						},
					},

					scales: {
						xAxes: [{
							// type: "time",
							// time: {
							// 	format: "HH:mm:s a",
							// 	tooltipFormat: "HH:mm:ss a",
							// },
					// 		scaleLabel: {
					// 			display: true,
					// 			labelString: "Date",
					// 		},
				}],
				yAxes: [{
					// 		stacked: true,
					// 		scaleLabel: {
					// 			display: true,
					// 		},
				}],
			},

		},
	}
},


mounted() {
	this.$nextTick(function(){

				// this.getBlades();
			})
},


methods: {     

	updateData(oldData) {
		var labels = oldData["labels"];
		var dataSetA = oldData["datasets"][0]["data"];
		var dataSetB = oldData["datasets"][1]["data"];

		labels.shift();
		this.count++;
		labels.push(this.count.toString());
		var newDataA = dataSetA[9] + (20 - Math.floor(Math.random() * (41)));
		var newDataB = dataSetB[9] + (20 - Math.floor(Math.random() * (41)));
		dataSetA.push(newDataA);
		dataSetB.push(newDataB);
		dataSetA.shift();
		dataSetB.shift();
	},   	

	getBlades() {

		axios.get('/api/get_blades')
		.then(response => {

			this.chassis_servers = JSON.parse(response.data)

		})
		.catch(errors => { })
	},		


	loadStats(blade) {


		this.blade_cpustats = blade.cpu_stats



		this.loadedStats = blade   

		if (Object.keys(this.gauges).length > 0){


			for (var key in this.gauges) {  

				if(key == 'memory') {    			
					this.updateGauges()
				}
			}

		}
		else {
			this.createGauge("memory", "Memory", 0, 100);

			this.updateGauges();
		}    

		this.getBladeFaults(blade.dn)
		this.showStats = true;

	},

	showFaults(faults) {

		if(faults.length > 0){ 
			this.faultDetails = faults 
			this.modalset = true;		 
		}
	},

	getBladeFaults(dn) {

		let str_dn = dn.split('/')
		let chs = str_dn[1]
		let bld = str_dn[2]

		this.minors = []; 
		this.warnings = [];
		this.criticals = [];
		this.majors = [];

		axios.get(`/api/get_bladefaults/${chs}/${bld}`)
		.then(response => {
			this.faults = JSON.parse(response.data);		

			this.minors = _.filter(this.faults, ['severity', 'minor'])
			this.warnings = _.filter(this.faults, ['severity', 'warning'])
			this.criticals = _.filter(this.faults, ['severity', 'critical'])
			this.majors = _.filter(this.faults, ['severity', 'major'])            

		})
		.catch(errors => { })
	},         


	createGauge(name, label, min, max) {

		var config = {
			size: 150,
			label: label,
			min: undefined != min ? min : 0,
			max: undefined != max ? max : 100,
			minorTicks: 5
		}

		var range = config.max - config.min;
		config.yellowZones = [{
			from: config.min + range * 0.75,
			to: config.min + range * 0.9
		}];

		config.redZones = [{
			from: config.min + range * 0.9,
			to: config.max
		}];

		this.gauges[name] = new Gauge(name + "GaugeContainer", config);
		this.gauges[name].render();
	},

	createGauges() {

		this.createGauge("memory", "Memory", 0, 8400);
		this.createGauge("cpu", "CPU", 0, 100);
		this.createGauge("network", "Network");
		this.createGauge("test", "Test", 1254, 3200);
	},


	updateGauges() {

		for (var key in this.gauges) {


			if(key == 'memory') {
				this.gauges[key].redraw( 60 * Math.random());
						// this.gauges[key].redraw( 100 - (41000 /  this.loadedStats.total_memory * 100));
    					// this.gauges[key].redraw( 100 - (this.loadedStats.available_memory /  this.loadedStats.total_memory * 100));
    				}

    			}
    		},

    		initialize() {
    			this.createGauges();	
    		}

    	}

    }

</script>


<template>

	<div>
		<div class="well" style="border: 1px solid #DBDBDB; width: 600px !important; height: 350px !important;">

			<linechart chartid="cpu_charts" :dataset="chartdata" :options="chartOption" :width='600' :height='250' ></linechart>
		</div>

		<div id="ChassisServers">			

			<v-client-table :data="chassis_servers" :columns="chassisServerColumns" :options="chassisServerOptions">

				<template slot="stats" scope="props">
					<div>
						<a href="javascript:void(0)" @click="loadStats(props.row)">
							<span class="material-icons text-success icon-small">poll</span>
						</a>
					</div>
				</template>

				<template slot="faults" scope="props">
					<div>
						<a href="javascript:void(0)" @click="getBladeFaults(props.row.dn)">
							<span class="material-icons text-danger icon-small">error</span>
						</a>

					</div>
				</template>

			</v-client-table>
			

		</div>

		<modal :isDashboard="true" modalname='modal-stats-data' v-if='showStats' @closeModal="showStats = false"> 
			
			<template slot="title">
				<h3>Blade Statistics</h3>
			</template>

			<template slot="body">			
				<!-- <div class="widget"> -->
				<!-- <div class="chart"> -->
				<div class="row">


					<div class="col-xs-3">                        

						<div class="well smallchart">
							<h3 class="well-center boldered text-primary" > {{ blade_cpustats.length }} <i class="fa fa-tachometer"></i></h3>
							<h3 class="text-muted">Total CPUs</h3>
						</div> 

						<div class="well smallchart">
							<h3 class="well-center boldered text-info" > {{ loadedStats.num_cpu_cores }} <i class="fa fa-tachometer"></i></h3>
							<h3 class="text-muted">CPUs Cores</h3>
						</div>

						<div class="well smallchart">
							<h3 class="well-center boldered text-success" > {{ loadedStats.NICs }} <i class="fa fa-sitemap"></i></h3>
							<h3 class="text-muted">NICs</h3>
						</div> 

					</div>


					<div class="col-xs-9">

						<div class="table-responsive">

							<table class="table table-borderless">                                    

								<tbody>
									<tr>
										<td width="2%">
											<div class="well smallchart">
												<a href="javascript:void(0)" style="text-decoration: none;" @click="showFaults(warnings)">
													<h3 class="well-center-small boldered-small text-info"> {{warnings.length}} <i class="fa fa-exclamation-triangle" aria-hidden="true"></i></h3>
													<h4 class="text-muted">Warnings</h4>
												</a>
											</div> 

										</td>

										<td width="2%">

											<div class="well smallchart">
												<a href="javascript:void(0)" style="text-decoration: none;" @click="showFaults(minors)">
													<h3 class="well-center-small boldered-small text-muted" > {{minors.length}} <i class="fa fa-exclamation-triangle" aria-hidden="true"></i></h3>
													<h4 class="text-muted">Minor</h4>
												</a>
											</div> 

										</td>

										<td width="2%">

											<div class="well smallchart">
												<a href="javascript:void(0)" style="text-decoration: none;" @click="showFaults(majors)">
													<h3 class="well-center boldered-small text-warning" > {{majors.length}} <i class="fa fa-exclamation-triangle" aria-hidden="true"></i></h3>
													<h4 class="text-muted">Major</h4>
												</a>
											</div>

										</td>

										<td width="2%">

											<div class="well smallchart">
												<a href="javascript:void(0)" style="text-decoration: none;" @click="showFaults(criticals)">
													<h3 class="well-center boldered-small" style="color: #F01212;" > {{criticals.length}} <i class="fa fa-exclamation-triangle" aria-hidden="true"></i></h3>
													<h4 class="text-muted">Critical</h4>
												</a>
											</div>

										</td>
										<td width="15%"></td>

									</tr>

									<tr>
										<td>
											<span id="memoryGaugeContainer"></span>
										</td>

										<td>
											<span id="cpu1GaugeContainer"></span>
										</td>

										<td>
											<span id="cpu2GaugeContainer"></span>
										</td>
									</tr>

									<tr>
										<td width="50%" colspan="3">

											<div class="well smallchart" style="border: 1px solid #DBDBDB; width: 600px !important; height: 250px !important;">

												<linechart chartid="cpu_charts" :dataset="chartdata" :options="chartOption" :width='600' :height='250' ></linechart>													
												<!-- <line-chart :chart-data="chartdata" :width='600' :height='250'></line-chart>	 -->

											</div>
										</td>
									</tr>

								</tbody>
							</table>
						</div> 

					</div>

				</div>

				<!-- </div> -->
				<!-- </div> -->
			</template>

		</modal>

		<modal modalname='modal-fault-details' v-if='modalset' @closeModal="modalset = false"> 
			<template slot="title">
				<h3>Faults Details</h3>
			</template>

			<template slot="body">
				
				<v-client-table :data="faultDetails" :columns="faultDetailsColumns" :options="faultDetailsOptions">

					<!-- <template slot="stats" scope="props">
						<div>
							<a href="javascript:void(0)" @click="loadStats(props.row)">
								<span class="material-icons text-success icon-small">poll</span>
							</a>
						</div>
					</template>

					<template slot="faults" scope="props">
						<div>
							<a href="javascript:void(0)" @click="getBladeFaults(props.row.dn)">
								<span class="material-icons text-danger icon-small">error</span>
							</a>

						</div>
					</template> -->

				</v-client-table>
			</template>

		</modal>
		
	</div>
	


</div>

</template>

<style lang="sass">

	.small {
		max-width: 350px;
		max-heigth: 90px;
	}

	.well a:hover {
		text-decoration: none !important;
	}

	.smallchart {
		color: #4a667a;
		/*text-align: left;
		position: relative;
		height: auto;*/
		background-color: #1e2730;
		/*display: inline-block;
		float: left;
		position: relative;
		-moz-box-sizing: border-box;
		-webkit-box-sizing: border-box;
		box-sizing: border-box;
		margin: 10px;
		padding: 15px 20px 65px 20px;*/
	}


</style>