/**
*
*
*/

<script>

	export default {
		props: ['ucs'],

		data() {
			return {				
				ucs_info: [],
			}
		},


		mounted() {
			this.$nextTick(function(){

				console.log(this.ucs, 'got it')

				this.getUcsInfo();
				

			});
		},


		methods: {

			getUcsInfo() {

				axios.get('/api/get_ucsinfo')
				.then(response => {

					this.ucs_info = JSON.parse(response.data)

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

		<table class="table table-responsive table-responsive">
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
								<span id="powerGaugeContainer"></span>
								<span id="memoryGaugeContainer"></span>
								<span id="cpuGaugeContainer"></span>
								<span id="networkGaugeContainer"></span>
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


</style>