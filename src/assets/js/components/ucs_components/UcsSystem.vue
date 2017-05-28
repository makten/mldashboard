<script>
	import vSelect from 'vue-select';    
	import { Validator } from 'vee-validate';
	// import UcsQueries from '../../../mixins/UcsQueries';

	export default {
		
		components: {            
			vSelect,
			Bar,
			LineChart,            
			Validator
		},

		data() {
			return {				
				ucs_info: [],
				ucsActive: true,
				predicted_faults: [],
				minors:[],
				warnings:[],
				criticals:[],
				majors:[],
			}
		},


		mounted() {
			this.$nextTick(function(){

				// Get blade, rackmounts count,
				// Faults and events
				// Get General Statistics about UCS System
				// Reject tab if ucs is not set

				// console.log(this.ucs, 'got it')

				/** 
				*	Check if UCS-IP is set, if so proceed to get to all queries
				* 	else, reject and exit back to UCS List
				*/				
				
				// if (this.ucs) {
					
					this.getUcsInfo();
					this.predictFaults();
					
				// }
				// else {
				// 	this.ucsActive = false
				// }				


			});
		},


		methods: {

			setUcsSystem(ucs) {
                // this.ucsSystem = ucs
                
            }, 

            getUcsInfo() {

            	axios.get('/api/get_ucsinfo')
            	.then(response => {

            		this.ucs_info = JSON.parse(response.data)

            	})
            	.catch(errors => { })

            },


            predictFaults() {

            	axios.get('/api/predictfaults')
            	.then(response => {
            		
            		this.predicted_faults = JSON.parse(response.data)

            		// this.minors = _.reject(this.predicted_faults, (f)=>{return f != 'F0185'})
            		
            		this.warnings = _.filter(this.predicted_faults, (f)=>{return f != 'F0185'})//F0185
            		this.criticals = _.filter(this.predicted_faults, (f)=>{return f != 'F0184'})//F0184
            		this.majors = _.filter(this.predicted_faults, (f)=>{return f != 'F0844'})//F0844 disabled 
            		

            	})
            	.catch(errors => { })

            },


        },


        computed: {

        }
    }

</script>

<template>
	<div>
		
		<div class="table-responsive" v-if='ucsActive'>

					
			
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

								<div class="title" style="background: #e4e4e4">UCS Faults</div>

								<ul class="list list-group">
									<li class=" list-group-item text-success">General information</li>
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

						</td>

						<td width="1%"></td>

						<td width="69%">

							<div class="widget" style="margin-left: 0px; padding: 0px;">

								<div class="title">UCS Statistics</div>                       

								<div class="chart">
											<!-- <span id="powerGaugeContainer"></span>
											<span id="memoryGaugeContainer"></span>
											<span id="cpuGaugeContainer"></span>
											<span id="networkGaugeContainer"></span> -->
										</div>


										<div class="chart">
											<ul class="list list-group">
												<li class=" list-group-item text-success">General information</li>
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

		</style>