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
				toggleToDo: false,	
				newTODO: "",	
				todoList: [
				{name: "Clear all Warning faults on Friday", completed: false},
				{name: "Add Move Gemeente Amsterdam CBS to VM 12", completed:false},
				{name: "Configure Call Home for Blade9", completed:false},
				{name: "Add Service Profile for NS Call center", completed:false},
				],	
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
				{id: 'swtapus1', label: 'SwA-P-1', minVal: 0, maxVal: 270},
				{id: 'swtapus2', label: 'SwA-P-2', minVal: 0, maxVal: 300},
				{id: 'swtbpus1', label: 'SwB-P-1', minVal: 0, maxVal: 300},
				{id: 'swtbpus2', label: 'SwB-P-2', minVal: 0, maxVal: 300},

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

					// this.getPowerStats();				

				}, 5000)


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

					this.predicted_faults = JSON.parse(response.data);					
					
					this.warnings = _.filter(this.predicted_faults, (f)=>{return f[0] == 'F0185'})//F0185
            		this.criticals = _.filter(this.predicted_faults, (f)=>{return f[0] == 'F0184'})//F0184
            		this.majors = _.filter(this.predicted_faults, (f)=>{return f[0] == 'F0844'})//F0844 disabled  

            	})
				.catch(errors => { })
			},

			getPowerStats() {

				axios.get('/api/getPowerStats')
				.then(response => {

					this.eq_powerstats = JSON.parse(response.data);	
					this.updateGauges('swtbpus1', 10, parseInt(this.eq_powerstats[1].power))
					this.updateGauges('swtbpus2', 16, parseInt(this.eq_powerstats[0].power))	
					console.log(this.eq_powerstats)
					// this.updateGauges('swtapus1', this.eq_powerstats[3].current, this.eq_powerstats[3].power)
					// this.updateGauges('swtapus2', this.eq_powerstats[2].current, this.eq_powerstats[2].power)


				})
				.catch(errors => { });
			},

			addNewToDo() {
				
				if(this.newTODO != "")
				{
					let item = {name: this.newTODO, completed: false};
					this.todoList.push(item);
					this.newTODO = "";
				}
			},
			
			removeItem(index) 
			{
				this.todoList.splice(index, 1)
				// this.todoList = _.reject(this.todoList, (i) => { return i.name == item.name })
			}

		}

	}
</script>

<template>
	<div>		 

		<div class="table-responsive">					
			<!-- {{equipment}} -->

			<!-- {{eq_powerstats}} -->
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

								<div class="title">Admin TO DOs</div>
								<form @submit:prevent>
									<div class="form-group">
										<label style="padding: 5px;" for="addToDo" class="text-muted">Add New</label>
										<input @keyup.enter="addNewToDo" v-model="newTODO" type="text" class="form-control" id="addToDo" placeholder="Clear warning faults">
									</div>									
								</form>		

								<div class="todo-list">	

									<ul class="list list-group todolist" v-for="(item, index) in todoList" style="padding: 1px;">
										<li class="list-group-item" style="padding:0px; margin: 1px;">	
											<span @click="removeItem(index)"class="text-danger" style="padding: 4px; font-size: 15px; margin-left: 12px; color: #FF3C00;">&times</span>
											<span :class="{'done': item.completed}" style="padding: 5px;" @click="item.completed = !item.completed">{{ item.name }}</span>
										</li>
									</ul>
								</div>	
							</div>

						</td>

						<td width="1%"></td>

						<td width="69%">

							<div class="widget" style="margin-left: 0px; padding: 0px;">

								<div class="title">Miscellaneous</div> 

								<div class="chart">
									<div class="chart">


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
												<ul class="list list-group faults">
													<li class=" list-group-item">
														<span class="text-info"><i class="fa fa-exclamation-circle"></i></span> 
														There are {{ warnings.length }} faults with severity <span class="label label-info"> Warning</span> affecting 2 devices
													</li>
													<li class=" list-group-item">
														<span class="text-warning"><i class="fa fa-exclamation-triangle"></i></span>
														There are {{ majors.length }} faults with severity <span class="label label-warning">Major</span> affecting 6 devices  
													</li>

													<li class=" list-group-item">
														<span>
															<i class="fa fa-warning text-danger"></i>
															There are {{ criticals.length }} faults with severity <span class="label label-danger">Critical</span> faults affecting 3 devices
														</span>  
													</li>

												</ul>

											</div>
										</div>		
										<hr/>								

										<div class="row">

											<div class="col-md-12">

												<div class="col-xs-3">
													<span id="swtapus1GaugeContainer"></span>
												</div>

												<div class="col-xs-3">
													<span id="swtapus2GaugeContainer"></span>
												</div>

												<div class="col-xs-3">
													<span id="swtbpus1GaugeContainer"></span>
												</div>

												<div class="col-xs-3">
													<span id="swtbpus2GaugeContainer"></span>
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
		font-size: 15px; 
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

	.todolist li span {
		font-size: 12px;		
		background: #F6F6F6;
		border-radius: 5px solid #F6F6F6;
	}

	.todolist li span:hover {
		cursor: pointer;
	}

	.done:hover {
		cursor: pointer;
		color: #666;
	}

	.done {
		background: #B0F6E3;
		text-decoration: line-through;
		color: #09a;
	}
	.done:hover {
		color: #008290;
	}


</style>