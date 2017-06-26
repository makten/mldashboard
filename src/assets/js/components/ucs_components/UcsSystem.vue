<script>
	import vSelect from 'vue-select';    
	import { Validator } from 'vee-validate';
	// import UcsQueries from '../../../mixins/UcsQueries';
	import GaugeCreator from '../../../mixins/GaugeCreator';


	export default {
		mixins: [GaugeCreator],

		components: {            
			vSelect,
			Bar,
			LineChart,            
			Validator			
		},

		data() {
			return {				
				ucs_info: [],
				eq_powerstats: null,
				equipment: [],
				cpus: 0,
				dimms: 0,
				disks: 0,
				adaptors: 0,
				storage: 0,

				ucsActive: true,
				predicted_faults: [],
				minors:[],
				warnings:[],
				criticals:[],
				majors:[],
				gauges_container: [
				{id: 'ucs_availability', label: 'Availability', minVal: 0, maxVal: 100},
				{id: 'ucs_network', label: 'Network', minVal: 0, maxVal: 200},
				{id: 'ucs_memory', label: 'Memory', minVal: 0, maxVal: 7000},
				{id: 'swtapus1', label: 'SwA-P-1', minVal: 0, maxVal: 300},
				{id: 'swtapus2', label: 'SwA-P-2', minVal: 0, maxVal: 300},

				],

				barData: {
					labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
					datasets: [{
						label: 'Power Usage Per Month kW',
						backgroundColor: '#FD442B',

						color: '#A11D1D',

						data: [800, 1300, 900, 800, 1400, 1000, 0, 0, 0, 0, 0, 0]
					}]
				},
				options: {responsive: false, maintainAspectRatio: false},

			}
		},

		mounted() {
			this.$nextTick(function(){

				this.getUcsInfo();
				this.getPowerStats();
				this.predictFaults();
				this.createGauges(this.gauges_container);



				setInterval(() => {
					this.updateGauges('ucs_memory', (Math.floor(Math.random() * (50 - 5 + 1)) + 8), 7000);

					this.barData.datasets[0].data = _.drop(this.barData.datasets[0].data)
					this.barData.datasets[0].data.push(Math.floor(Math.random() * (50 - 5 + 1)) + 5)
					this.barData = this.barData;

				}, 10000);

				setInterval(() => {
					this.updateGauges('ucs_availability', (Math.floor(Math.random() * (50 - 5 + 1)) + 5), 100)
				}, 30000);

				setInterval(() => {
					this.updateGauges('ucs_network', (Math.floor(Math.random() * (50 - 5 + 1)) + 8), 200)

				}, 90000);

				setInterval(()=>{
					this.getPowerStats();
				}, 10000)


			});
		},

		methods: {

			getUcsInfo() {

				axios.get('/api/get_ucsinfo')
				.then(response => {

					this.equipment = JSON.parse(response.data)[0];
					this.ucs_info = JSON.parse(response.data)[1];

					let vm = this;
					_.each(this.equipment, (eq) => { 
						vm.cpus += parseInt(eq.num_of_cpu); 
						vm.disks += parseInt(eq.num_of_local_disk); 
						vm.dimms += parseInt(eq.num_of_dimm);
						vm.adaptors += parseInt(eq.num_ofadaptor);
						vm.storage += parseInt(eq.num_of_storage_controller);
					});	
				})
				.catch(errors => { });
			},

			getPowerStats() {

				axios.get('/api/getPowerStats')
				.then(response => {

					this.eq_powerstats = JSON.parse(response.data);
					console.log(this.eq_powerstats[0])

					this.updateGauges('swtapus1', this.eq_powerstats[3].current, this.eq_powerstats[3].power)
					this.updateGauges('swtapus2', this.eq_powerstats[2].current, this.eq_powerstats[2].power)
					// this.updateGauges('pus2', )
					// this.updateGauges('pus3', )
					// this.updateGauges('pus4', )


				})
				.catch(errors => { });
			},


			predictFaults() {

				axios.get('/api/predictfaults')
				.then(response => {
					this.predicted_faults = JSON.parse(response.data)
            		this.warnings = _.filter(this.predicted_faults, (f)=>{return f != 'F0185'})//F0185
            		this.criticals = _.filter(this.predicted_faults, (f)=>{return f != 'F0184'})//F0184
            		this.majors = _.filter(this.predicted_faults, (f)=>{return f != 'F0844'})//F0844 disabled
            	})
				.catch(errors => { })
			}					
		}

	}
</script>

<template>
	<div>		 

		<div class="table-responsive">					
			{{equipment}}

			{{eq_powerstats}}
			<table class="table">
				<tbody>
					<tr>				
						<td width="30%">

							<div class="widget" style="margin-left: 0px; padding: 0px;">

								<div class="title">UCS information</div>

								<table class="table table-borderless">                       

									<tbody>
										<tr>
											<td width="30%" align="left">
												<span>Name</span>
											</td>
											<td width="5%" align="center">:</td>

											<td align="left">
												<span> {{ ucs_info.name }} </span>
											</td>       
										</tr>

										<tr>
											<td width="30%" align="left">
												<span>Status</span>
											</td>
											<td width="5%" align="center">:</td>

											<td align="left">
												<span><i class="material-icons text-success" style="font-size: 12px;">fiber_manual_record</i> {{ ucs_info.status }} Clear</span>
											</td>       
										</tr>

										<tr>
											<td width="30%" align="left">
												<span>IP Address</span>
											</td>
											<td width="5%" align="center">:</td>

											<td align="left">
												<span> {{ ucs_info.address }}</span>
											</td>       
										</tr>

										<tr>
											<td width="30%" align="left">
												<span>System up time</span>
											</td>
											<td width="5%" align="center">:</td>

											<td align="left">
												<span> {{ ucs_info.system_up_time }}</span>
											</td>       
										</tr>

										<tr>
											<td width="30%" align="left">
												<span>Mode</span>
											</td>
											<td width="5%" align="center">:</td>

											<td align="left">
												<span> {{ ucs_info.mode }}</span>
											</td>       
										</tr>
									</tbody>
								</table>
							</div>


							<div class="widget" style="margin-left: 0px; padding: 0px;">

								<div class="title">Alerts</div>									

								<ul class="list list-group faults">
									<li class=" list-group-item">
										<span class="text-info"><i class="fa fa-exclamation-circle"></i></span> 
										{{ warnings.length }}  <span class="label label-info"> Warning</span> faults affecting 2 devices
									</li>
									<li class=" list-group-item">
										<span class="text-warning"><i class="fa fa-exclamation-triangle"></i></span>
										{{ majors.length }} <span class="label label-warning">Major</span> faults affecting 6 devices  
									</li>

									<li class=" list-group-item">
										<span>
											<i class="fa fa-warning text-danger"></i>
											{{ criticals.length }} <span class="label label-danger">Critical</span> faults affecting 3 devices
										</span>  
									</li>

									<li class=" list-group-item">Power consumption</li>										
									<li class=" list-group-item">Availabity</li>										
									<li class=" list-group-item">Packets</li>
									<li class=" list-group-item">Service Profiles</li>
								</ul>

							</div>

						</td>

						<td width="1%"></td>

						<td width="69%">

							<div class="widget" style="margin-left: 0px; padding: 0px;">

								<div class="title">Miscellaneous</div> 

								<div class="chart">
									<div class="chart">

											<!-- <div class="panel panel-default">
											<div class="panel-heading">Statistics</div>
											<div class="panel-body"> -->												
												<div class="row">
													<div class="col-xs-4">
														<span id="ucs_availabilityGaugeContainer"></span>

													</div>

													<div class="col-xs-4">
														<span id="ucs_networkGaugeContainer"></span>
													</div>

													<div class="col-xs-4">
														<span id="ucs_memoryGaugeContainer"></span>
													</div>
												</div>

												<!-- </div>
											</div> -->

											<hr/>


											<div class="row">
												<div class="col-md-3">
													<div class="well usc_components">
														<h3 class="well-center boldered text-primary" > 9 <i class="fa fa-server"></i></h3>
														<h4 class="text-muted">R-Mount</h4>
													</div> 
												</div>
												<div class="col-md-3">
													<div class="well usc_components">
														<h3 class="well-center boldered text-primary" > 13 <i class="fa fa-server"></i></h3>
														<h4 class="text-muted">Chassis</h4>
													</div> 
												</div>
												<div class="col-md-3">
													<div class="well usc_components">
														<h3 class="well-center boldered text-primary" > 9 <i class="fa fa-tasks"></i></h3>
														<h4 class="text-muted">Ch-Server</h4>
													</div> 
												</div>
												<div class="col-md-3">
													<div class="well usc_components">
														<h3 class="well-center boldered text-primary" > 48 <i class="fa fa-sitemap"></i></h3>
														<h4 class="text-muted">Net Ports</h4>
													</div> 
												</div>
											</div>	

											<hr/>

											<div class="row">
												<div class="col-md-12">
													<bar :chart-data="barData" :options="{responsive: false, maintainAspectRatio: true}" :width="450" :height="250"> </bar>
												</div>
											</div>	

											<div class="row">

												<div class="col-md-12">
													
													<div class="col-xs-3">
														<!-- <span id="ucs_availabilityGaugeContainer"></span> -->

													</div>

													<div class="col-xs-3">
														<span id="swtapus1GaugeContainer"></span>
													</div>

													<div class="col-xs-3">
														<span id="swtapus2GaugeContainer"></span>
													</div>
													
												</div>
											</div>																	


										</div>										

									</div>
								</div>
							</td>
						</tr>
					</tbody>
				</table>
			</div>



			<!-- <div class='col-md-6 col-md-offset-3'>
			<div class="alert alert-dismissible alert-warning">
				<button type="button" class="close" data-dismiss="alert">&times</button>
				<strong>Oh snap!!</strong>
				Please select a UCS system from the UCS tab or Add a new UCS sytem
			</div>
		</div> -->
		

	</div>
</template>


<style lang="sass">
	#exTab3 .nav-pills > li > a {
		border-radius: 4px 4px 0 0 ;
	}

	#exTab3 .tab-content {
		color : #3a3a3a;
		background-color: #f0f5fb;
		padding : 5px 15px;
	}


	.well-center {								
		font-weight: 600;
	}


	h3.boldered {

		font-family: 'Arvo', serif;
		font-size: 45px;				
		line-height: 1.1px;
		vertical-align: text-bottom;
		overflow: hidden;				
	}

	h3.boldered-small {

		font-family: 'Arvo', serif;
		font-size: 20px;				
		line-height: 1.1px;
		vertical-align: text-bottom;
		overflow: hidden;				
	}

	.title {
		background: #e4e4e4 !important;
	}

	.faults li {
		padding: 6px !important;
		font-family: serif;
		font-size: 12px; 
	}

	.usc_components {
		color: lightgrey;
		text-align: center;		
		background: #1797F9 !important;
	}

	.usc_components h3 {
		color: #F4F4F4;
		text-align: center;
		font-size: 35px !important;		
	}

	.usc_components h4 {
		color: #DAD7D7;
		text-align: center;	
	}
</style>