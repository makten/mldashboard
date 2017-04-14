/**
*	This component handles all chassis server api calls
*
*/
<script>

	import vSelect from 'vue-select';    
	import { Validator } from 'vee-validate';
	import modal from '../../../core/modal.vue';

	export default {

		// props: {ucs: {required: true}},
		components: {            
			vSelect,
			Bar,
			LineChart,            
			Validator,
			modal
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

          // faults: function (h, row) {                        
          //   return <a href="javascript:void(0)" > <span class="material-icons text-danger" style="font-size:15px;">error</span></a>
          // }
      }
  },

  datacollection: {
  	labels: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'I', 'J', 'K', 'L'],
  	datasets: [
  	{
  		label: 'CPU  1',
  		backgroundColor: '#CD3838',
  		data: [2, 3, 4, 9, 5, 4, 2, 2, 1, 3, 1]
  	}, {
  		label: 'CPU 2',
  		backgroundColor: '#5AF0F2',
  		data: [3, 4, 6, 3, 4, 4, 3, 1, 3, 5,]
  	}
  	]
  }
}
},


mounted() {
	this.$nextTick(function(){

		this.getBlades();


	})
},


methods: {        	

	getBlades() {

		axios.get('/api/get_blades')
		.then(response => {

			this.chassis_servers = JSON.parse(response.data)

		})
		.catch(errors => { })
	},


	loadStats(blade) {

    // let len = cpustats.length;
    // let sm = 0;
    this.blade_cpustats = blade.cpu_stats

    // _.each(blade.cpu_stats, (val, key) => { sm += parseInt(val.input_current) });

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
    	// this.createGauge("cpu1", "CPU 1", 0, 100);
    	// this.createGauge("cpu2", "CPU 2", 0, 100);
    	this.updateGauges();
    }    

    this.getBladeFaults(blade.dn)

},

showFaults(faults) {
	if(faults.length > 0){ 
		this.faultDetails = faults 
		this.modalset = true;
		// $('#modal-fault-details').modal('show'); 
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


    // getRandomValue(gauge) {
    // 	var overflow = 0; 
    // 	return gauge.config.min - overflow + (gauge.config.max - gauge.config.min + overflow * 2) * Math.random();
    // },


    initialize() {
    	this.createGauges();
	// setInterval(this.updateGauges, 5000);
}

},

computed() {

}

}

</script>


<template>

	<div>

		<div id="ChassisServers">

			<div class="widget">
				<div class="chart">


					<div class="row">

						<!-- {{ loadedStats }} -->
						

						<div class="col-xs-3">                        

							<div class="well">
								<h3 class="well-center boldered text-primary" > {{ blade_cpustats.length }} <i class="fa fa-tachometer"></i></h3>
								<h3 class="text-muted">Total CPUs</h3>
							</div> 

							<div class="well">
								<h3 class="well-center boldered text-info" > {{ loadedStats.num_cpu_cores }} <i class="fa fa-tachometer"></i></h3>
								<h3 class="text-muted">CPUs Cores</h3>
							</div>

							<div class="well">
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
												<div class="well">
													<a href="javascript:void(0)" style="text-decoration: none;" @click="showFaults(warnings)">
														<h3 class="well-center-small boldered-small text-info"> {{warnings.length}} <i class="fa fa-exclamation-triangle" aria-hidden="true"></i></h3>
														<h4 class="text-muted">Warnings</h4>
													</a>
												</div> 


											</td>

											<td width="2%">

												<div class="well">
													<a href="javascript:void(0)" style="text-decoration: none;" @click="showFaults(minors)">
														<h3 class="well-center-small boldered-small text-muted" > {{minors.length}} <i class="fa fa-exclamation-triangle" aria-hidden="true"></i></h3>
														<h4 class="text-muted">Minor</h4>
													</a>
												</div> 
												

											</td>

											<td width="2%">

												<div class="well">
													<a href="javascript:void(0)" style="text-decoration: none;" @click="showFaults(majors)">
														<h3 class="well-center boldered-small text-warning" > {{majors.length}} <i class="fa fa-exclamation-triangle" aria-hidden="true"></i></h3>
														<h4 class="text-muted">Major</h4>
													</a>
												</div>

											</td>

											<td width="2%">

												<div class="well">
													<a href="javascript:void(0)" style="text-decoration: none;" @click="showFaults(criticals)">
														<h3 class="well-center boldered-small text-danger" > {{criticals.length}} <i class="fa fa-exclamation-triangle" aria-hidden="true"></i></h3>
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
												<div class="small">
													<line-chart :chart-data="datacollection"></line-chart>
												</div>
											</td>
										</tr>

									</tbody>
								</table>
							</div> 

						</div>

					</div>

				</div>
			</div>

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


			<div v-if="blade_cpustats.length >= 1">
				<ul class="list-group" v-for="stats in blade_cpustats">

					<li class="list-group-item">
						{{ stats.dn }} {{stats}}
					</li>

				</ul>

				<ul class="list-group" v-for="fault in faults">

					<li class="list-group-item">
						{{ fault.code }} {{ fault.cause }} {{ fault.descr }} {{ fault.severity }} {{ fault.created }} {{fault}}
					</li>

				</ul>

			</div>

		</div>

		<modal modalname='modal-fault-details' v-if='modalset' @closeFaultsDetails="modalset = false"> 

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

</style>