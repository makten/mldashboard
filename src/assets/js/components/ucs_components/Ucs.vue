/**
*
*
*/

<script>
	import vSelect from 'vue-select';    
	import { Validator } from 'vee-validate';

	export default {
		props: ['ucs'],

		components: {            
			vSelect,
			Bar,
			LineChart,            
			Validator
		},

		data() {
			return {		

				showCredForm: false,		
				ucs_systems: [],

				UcsSystemsColumns: ['id', 'ipAddress', 'subnet', 'owner', 'num_of_cores', 'date_created'],
				UcsSystemsOptions: {

					templates: {

                        // faults: function (h, row) {                        
                        //     return <a href="javascript:void(0)" > <span class="material-icons text-danger" style="font-size:15px;">error</span></a>
                        // }
                    }
                },

                ucs_credentials_form: new Form({

                	ipAddress: '',
                	subnet: '',
                	cred_name: '',
                	cred_username: '',
                	cred_password: '',
                	cred_port: '',
                	cred_protocol: ''

                }),
            }
        },


        mounted() {
        	this.$nextTick(function(){

				// Get blade, rackmounts count,
				// Faults and events

				this.getUcsList();
				

			});
        },


        methods: {

        	getUcsList() {
        		axios.get(`/api/getUcsSystems/`)
        		.then(response => {                 

        			this.ucs_systems = response.data 

        			if (this.ucs_systems.length <= 0) {

        				$('#modal-ucs-list').modal('show');
        			} 




        		})
        		.catch(errors => { })
        	}, 


        	selectUCS(ucs) {    

        		// Broadcast the currently selected tab id to tabs.vue
                eventBroadcaster.$emit('setTab', '#ucs-overview')            
        		// this.ipAddress = ucs.ipAddress
        	},  


        	showAddUcsForm() {
        		$('#modal-ucs-list').modal('show');
        	},


        	showCredentialForm() {

        		this.ucs_credentials_form.cred_name = '';
        		this.ucs_credentials_form.cred_username = '';
        		this.ucs_credentials_form.cred_password = '';
        		this.ucs_credentials_form.cred_port = '';
        		this.ucs_credentials_form.cred_protocol = '';

        		this.showCredForm = true;
        	},


        	validateCredentialsForm(scope) {                                        

        		this.$validator.validateAll(scope).then(result => {
        			if (result) { 

        				alert('Form Submitted!');

        			}
        		});                
        	},


        },


        computed: {

        }
    }

</script>

<template>

	<div>
		
		<a href="javascript:void(0)" @click="showAddUcsForm()" style="text-decoration:none;" class="text-success">
			<i class="material-icons">add_circle</i> Add UCS
		</a>

		<v-client-table :data="ucs_systems" :columns="UcsSystemsColumns" :options="UcsSystemsOptions">

			<template slot="ipAddress" scope="props">
				<div>
					<a href="javascript:void(0)" @click="selectUCS(props.row)">
						{{ props.row.ipAddress }}
					</a>
				</div>
			</template>                       

		</v-client-table>



		<!-- Create UCS System -->
		<div class="modal fade" id="modal-ucs-list" tabindex="-1" role="dialog">

			<div class="modal-dialog">

				<div class="modal-content">

					<div class="modal-header">
						<button type="button " class="close" data-dismiss="modal" aria-hidden="true">&times;</button>

						<h4 class="modal-title"> UCS LIST</h4>
					</div>

					<div class="modal-body">                        


						<form @submit.prevent="validateCredentialsForm('ucs_credentials_form')" class="form-horizontal" > 
							<legend>Add UCS System</legend>

							<div class="form-group">
								<label for="ipAddress" class="col-md-3 control-label">IP Address :</label>

								<div class="col-md-6">
									<input validator="'required|ucs_credentials_form.ipAddress'" type="text" class="form-control" id="ipAddress" placeholder="192.168.1.1" v-model="ucs_credentials_form.ipAddress">

									<p class="help-block text-info">Enter the IP address of the UCS system</p>
									<span v-show="errors.has('ucs_credentials_form.ipAddress')">
										{{ errors.first('ucs_credentials_form.ipAddress') }}</span>
									</div>
								</div>


								<div class="form-group">
									<label for="subnet" class="col-md-3 control-label">Netmask :</label>

									<div class="col-md-6">
										<input validator="'required|ucs_credential_form.subnet|numeric'" type="text" class="form-control" id="subnet" v-model="ucs_credentials_form.subnet">
										<p class="help-block text-info">Enter the subnet of the UCS system</p>
									</div>
								</div>

								<div class="panel panel-primary" v-if="ucs_credentials_form.ipAddress && ucs_credentials_form.subnet">
									<div class="panel-heading">
										<h3 class="panel-title"><span><i class="fa fa-lock fa-lg"></i></span> UCS Login Credentials</h3>
									</div>

									<div class="panel-body">
										
										<div class="table-responsive">
											<table class="table">

												<tr>
													<td width="100%" height="50" colspan="3">
														<a href="javascript:void(0)" @click="showCredentialForm()" style="text-decoration:none;" class="text-success">
															<i class="material-icons">add_circle</i> Add Credentials
														</a>
													</td>
												</tr>

												<tr>
													<td width="30%">
														<ul class="list-group">
															<li class="list-group-item-info">admin</li>
															<li class="list-group-item-danger">user 2</li>
															<li class="list-group-item-warning">admin 3</li>
														</ul>
													</td>

													<td width="5%">                                            
													</td>

													<td width="40%">

														<div class="well" v-if="showCredForm">

															<span class="pull-right close text-danger" style="color: red;" @click="showCredForm = !showCredForm"> 
																&times;
															</span>                                                        

															<div class="form-group label-floating">
																<label class="control-label" for="cred_name"><i class="fa fa-user"></i> Name</label>
																<input class="form-control input-sm" id="cred_name" type="text" v-model="ucs_credentials_form.cred_name">
																<p class="help-block text-info">Enter credential name</p>
															</div>

															<div class="form-group label-floating">
																<label class="control-label" for="username"><i class="fa fa-user"></i> Username</label>
																<input class="form-control input-sm" id="username" type="text" v-model="ucs_credentials_form.cred_username">
																<p class="help-block text-info">UCS Username</p>
															</div>

															<div class="form-group label-floating">
																<label class="control-label" for="password"><i class="fa fa-user-secret" aria-hidden="true"></i> Password</label>
																<input class="form-control input-sm" id="password" type="password" v-model="ucs_credentials_form.cred_password">
																<p class="help-block text-info">UCS password</p>
															</div>

															<div class="form-group label-floating">
																<label class="control-label" for="port">Port</label>
																<input class="form-control input-sm" id="port" type="text" v-model="ucs_credentials_form.cred_port">
																<p class="help-block text-info">UCS Port</p>
															</div>

															<div class="form-group label-floating">
																<label class="control-label" for="protocol"><i class="fa fa-globe"></i> Protocol</label>
																<input class="form-control input-sm" id="protocol" type="text" v-model="ucs_credentials_form.cred_protocol">
																<p class="help-block text-info">UCS Connection protocol</p>
															</div>                                                    

														</div>
													</td>
												</tr>

												<tr>

													<td colspan="3">
														<center>
															<button type="submit" class="btn btn-primary btn-xs">Discover</button>
														</center>
													</td>

												</tr>

											</table>
										</div>
									</div>
								</div>

								
							</form>

						</div>


						<div class="modal-footer">
							<button type="button" class="btn btn-xs btn-default" data-dismiss="modal">Close</button>
						</div>

					</div>
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

		.well {
			text-align: center;
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