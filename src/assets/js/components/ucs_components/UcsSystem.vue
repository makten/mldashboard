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
				
				],

			}
		},

		mounted() {
			this.$nextTick(function(){

				this.getUcsInfo();
				this.predictFaults();
				this.createGauges(this.gauges_container);


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
		
		<div class="table-responsive" v-if='ucsActive'>					
			{{equipment}}
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

								<div class="title">UCS Faults</div>	

								<table class="table table-borderless">                       

									<tbody>
										<tr>
											<td width="30%" align="left">
												<span>Chassis</span>
											</td>
											<td width="5%" align="center">:</td>

											<td align="left">
												<span> 4 </span>
											</td>       
										</tr>

										<tr>
											<td width="30%" align="left">
												<span>Blades</span>
											</td>
											<td width="5%" align="center">:</td>

											<td align="left">
												<span> 10 </span>
											</td>       
										</tr>

										<tr>
											<td width="30%" align="left">
												<span>RackUnits</span>
											</td>
											<td width="5%" align="center">:</td>

											<td align="left">
												<span> 0</span>
											</td>       
										</tr>

										
									</tbody>

								</table> 
							</div>

						</td>

						<td width="1%"></td>

						<td width="69%">

							<div class="widget" style="margin-left: 0px; padding: 0px;">

								<div class="title">Miscellaneous</div> 

								<div class="chart">
									<div class="chart">

										<div class="panel panel-default">
											<div class="panel-heading">Statistics</div>
											<div class="panel-body">												

												<div class="col-xs-3">
													<span id="ucs_availabilityGaugeContainer"></span>

												</div>

												<div class="col-xs-3">
													<span id="ucs_networkGaugeContainer"></span>
												</div>

												<div class="col-xs-3">
													<span id="ucs_memoryGaugeContainer"></span>
												</div>

											</div>
										</div>

										<div class="well">
											<div class="row">
												<div class="col-xs-3">
													<div class="well">
														<h3 class="well-center boldered text-primary" > 9 <i class="fa fa-tachometer"></i></h3>
														<h4 class="text-muted">CPUs</h4>
													</div> 
												</div>
												<div class="col-xs-3">
													<div class="well">
														<h3 class="well-center boldered text-primary" > 9 <i class="fa fa-tachometer"></i></h3>
														<h4 class="text-muted">CPUs</h4>
													</div> 
												</div>
												<div class="col-xs-3">
													<div class="well">
														<h3 class="well-center boldered text-primary" > 9 <i class="fa fa-tachometer"></i></h3>
														<h4 class="text-muted">CPUs</h4>
													</div> 
												</div>
											</div>																		
											
										</div>

										<div class="well">
											<h4 class="label label-success">Alerts</h4>
											<ul class="list list-group faults">
												<li class=" list-group-item">
													<span class="text-info"><i class="fa fa-exclamation-circle"></i></span> 
													There are {{ warnings.length }}  alerts with severity <span class="label label-info"> Warning</span> affecting 2 devices
												</li>
												<li class=" list-group-item">
													<span class="text-warning"><i class="fa fa-exclamation-triangle"></i></span>
													There are {{ majors.length }}  alerts with severity <span class="label label-warning">Major</span> affecting 6 devices  
												</li>

												<li class=" list-group-item">
													<span>
														<i class="fa fa-warning text-danger"></i>
														There are {{ criticals.length }}  alerts with severity <span class="label label-danger">Critical</span> affecting 3 devices
													</span>  
												</li>

												<li class=" list-group-item">Number of faults per type</li>
												<li class=" list-group-item">Power consumption</li>
												<li class=" list-group-item">Num of blades</li>
												<li class=" list-group-item" >Num of Chassis</li>
												<li class=" list-group-item">Availabity</li>
												<li class=" list-group-item">Network ports</li>
												<li class=" list-group-item">Packets</li>
												<li class=" list-group-item">Service Profiles</li>
											</ul>
										</div>										

									</div>										

								</div>
							</div>
						</td>
					</tr>
				</tbody>
			</table>
		</div>

		<div class='col-md-6 col-md-offset-3' v-else>
			<div class="alert alert-dismissible alert-warning">
				<button type="button" class="close" data-dismiss="alert">&times</button>
				<strong>Oh snap!!</strong>
				Please select a UCS system from the UCS tab or Add a new UCS sytem
			</div>
		</div>
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
</style>