/**
*	This component is responsible for all UCS related tasks
*
*/

<script>

	import vSelect from 'vue-select';    
	import { Validator } from 'vee-validate';
	import modal from '../../../core/modal.vue';
	import FormHelper from '../../../mixins/FormHelper';	
	import UcsValidation from '../../../mixins/validationRules';
	import UcsQueries from '../../../mixins/UcsQueries';

	export default {
		mixins: [FormHelper, UcsValidation, UcsQueries],
		props: ['ucs'],

		components: {            
			vSelect,
			Bar,
			LineChart,            
			Validator,
			modal
		},

		data() {
			return {		

				showCredForm: false,
				setUcsModal: false,		
				ucs_systems: [],
				validations: [],
				ucs_credentials: [],

				UcsSystemsColumns: ['id', 'ipAddress', 'subnet', 'owner', 'num_of_cores', 'date_created'],
				UcsSystemsOptions: {

					templates: {

                        // faults: function (h, row) {                        
                        //     return <a href="javascript:void(0)" > <span class="material-icons text-danger" style="font-size:15px;">error</span></a>
                        // }
                    }
                },

                ucs_credentials_form: new Form({

                	section_name: 'add_ucs',
                	ipAddress: '',
                	subnet: '',
                	cred_name: '',
                	cred_username: '',
                	cred_password: '',
                	cred_port: '',
                	cred_protocol: '',
                	cred_timeout: '',
                	errors: [],

                }),
            }
        },


        mounted() {
        	this.$nextTick(function(){

				/**
				*	Add option to deny tab when ucs is not set
				*	Add option to assign ucs to client
				* 
				*/

				// Get blade, rackmounts count,
				// Faults and events

				this.getUcsList();				
				
			});
        },


        methods: {

        	getUcsList() {

				NProgress.start();

        		axios.get(`/api/getUcsSystems/`)
        		.then(response => {
					
					this.ucs_systems = response.data

        			if (this.ucs_systems.length <= 0) {

        				$('#modal-ucs-list').modal('show');
        			}

					NProgress.done();

        		})
        		.catch(errors => { 
					NProgress.done();
				})
        	}, 


        	selectUCS(ucs) {    

        		// Broadcast the currently selected tab id to tabs.vue
        		eventBroadcaster.$emit('setTab', '#ucs-overview')
				// eventBroadcaster.$emit('setUcs', ucs)        		
        	},  


        	showAddUcsForm() {

        		this.getUcsCredentials()
        		this.setUcsModal = true;
        	},


        	getUcsCredentials() {
        		axios.get(`/api/getUcsCredentials`)
        		.then(response => {
        			this.ucs_credentials = response.data

        		})
        		.catch( errors => {})
        	},


        	showCredentialForm() {

        		this.ucs_credentials_form.cred_name = '';
        		this.ucs_credentials_form.cred_username = '';
        		this.ucs_credentials_form.cred_password = '';
        		this.ucs_credentials_form.cred_port = '';
        		this.ucs_credentials_form.cred_protocol = '';

        		this.showCredForm = true;
        	},

        	useCredentials(credential) {
        		
        		this.ucs_credentials_form.cred_name = '',
        		this.ucs_credentials_form.cred_username = '',
        		this.ucs_credentials_form.cred_password = '',
        		this.ucs_credentials_form.cred_port = '',
        		this.ucs_credentials_form.cred_protocol = '',
        		this.ucs_credentials_form.cred_timeout = '',

        		this.ucs_credentials_form.cred_name = credential.cred_name
        		this.ucs_credentials_form.cred_username = credential.cred_username
        		this.ucs_credentials_form.cred_password = credential.cred_password
        		this.ucs_credentials_form.cred_port = credential.cred_port
        		this.ucs_credentials_form.cred_protocol = credential.cred_protocol
        		this.ucs_credentials_form.cred_timeout = credential.cred_timeout  

        		this.showCredForm = true;      		
        	},


        	storeUcsCredentials () {	

        		let validationData = this.ucsValidationRules();				

        		let validation = this.validateForm(this.ucs_credentials_form, validationData.rules, validationData.messages);

        		if(validation.fails()){
        			this.validations = [];
        			this.validations.push(validation.errors.errors);
        		}

        		if (validation.passes()){
        			
        			this.validations = [];
        			this.persistForm('post', '/api/createUcsCredentials/', this.ucs_credentials_form, this.ucs_credentials);
        		}

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


		<modal width="50" :isDashboard="false" modalname='modal-add-ucs' v-if='setUcsModal' @closeModal="setUcsModal = false"> 
			
			<template slot='title'>Add UCS System</template>
			
			<template slot='body'>
				
				<!-- <div class="alert alert-dismissible alert-danger" v-if="ucs_credentials_form.errors.length > 0" style="background-color: #F15959;">
					<p><strong>Whoops!</strong> Iets is mis gegaan!</p>
					<br>
					<ul>
						<li v-for="error in ucs_credentials_form.errors">
							{{ error }}
						</li>
					</ul>
				</div> -->


				<form @submit.prevent="store" class="form-horizontal"> 
					
					
					<div class="form-group">

						<label for="ipAddress" class="col-md-3 control-label">IP Address :</label>

						<div class="col-md-6">
							<input type="text" class="form-control" id="ipAddress" placeholder="192.168.1.1" v-model="ucs_credentials_form.ipAddress">

							<p class="help-block text-info">Enter the IP address of the UCS system</p>	<br>
							<p class="error-block text-danger" v-if="hasErrors()"> {{ validations[0].ipAddress }} </p>						
							
						</div>
						
					</div>


					<div class="form-group" >
						<label for="subnet" class="col-md-3 control-label">Netmask :</label>

						<div class="col-md-6">
							<input type="text" class="form-control" id="subnet" v-model="ucs_credentials_form.subnet" placeholder="255.255.255.0">
							<p class="help-block text-info">Enter the subnet of the UCS system</p>	<br>
							<p class="error-block text-danger" v-if="hasErrors()"> {{ validations[0].subnet }} </p>						
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
											<p class="error-block text-danger" v-if="hasErrors()"> Add UCS Credentials </p>
										</td>
									</tr>

									<tr>
										<td width="30%">

											<div class="table-responsive" v-show="ucs_credentials.length > 0">

												<table class="table table-bordered table-hover">
													<thead>
														<tr>
															<th><span>Select Credentials </span></th>
														</tr>
													</thead>

													<tbody class="finger">
														<tr v-for='credential in ucs_credentials'>
															<td style="padding: 4px; font-weight: 600;">
																<a @click="useCredentials(credential)" href="javascript:void(0)" style="text-decoration: none;"><span><i class="fa fa-lock fa-lg"></i></span> {{ credential.cred_name }} </a>
															</td>
														</tr>
													</tbody>

												</table>

											</div>
											
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
													<input class="form-control input-sm" id="cred_name" type="text" v-model="ucs_credentials_form.cred_name" name="cred_name">												
													<p class="error-block text-danger" v-if="hasErrors()"> {{ validations[0].cred_name }} </p>
												</div>												

												<div class="form-group label-floating">
													<label class="control-label" for="cred_username"><i class="fa fa-user"></i> Username</label>
													<input class="form-control input-sm" id="cred_username" type="text" v-model="ucs_credentials_form.cred_username" name="cred_username">													
													<p class="error-block text-danger" v-if="hasErrors()"> {{ validations[0].cred_username }} </p>
												</div>

												<div class="form-group label-floating">
													<label class="control-label" for="cred_password"><i class="fa fa-user-secret" aria-hidden="true"></i> Password</label>
													<input class="form-control input-sm" id="cred_password" type="password" v-model="ucs_credentials_form.cred_password">													
													<p class="error-block text-danger" v-if="hasErrors()"> {{ validations[0].cred_password }} </p>
												</div>

												<div class="form-group label-floating">
													<label class="control-label" for="port">Port</label>
													<input class="form-control input-sm" id="port" type="text" v-model="ucs_credentials_form.cred_port">													
													<p class="error-block text-danger" v-if="hasErrors()"> {{ validations[0].cred_port }} </p>
												</div>

												<div class="form-group label-floating">
													<label class="control-label" for="protocol"><i class="fa fa-globe"></i> Protocol</label>
													<input class="form-control input-sm" id="protocol" type="text" v-model="ucs_credentials_form.cred_protocol">													
													<p class="error-block text-danger" v-if="hasErrors()"> {{ validations[0].cred_protocol }} </p>
												</div> 

												<div class="form-group label-floating">
													<label class="control-label" for="cred_timeout"><i class="fa fa-globe"></i> Timeout</label>
													<input class="form-control input-sm" id="cred_timeout" type="text" v-model="ucs_credentials_form.cred_timeout">													
													<p class="error-block text-danger" v-if="hasErrors()"> {{ validations[0].cred_timeout }} </p>
												</div>                                                    

											</div>
										</td>
									</tr>

									<tr>

										<td colspan="3">
											<center>
												<button @click.prevent="storeUcsCredentials" type="submit" class="btn btn-primary btn-xs">Discover</button>
											</center>
										</td>

									</tr>

								</table>
							</div>
						</div>
					</div>


				</form>
			</template>

		</modal>

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

	table a {
		text-decoration: none;
	}

	table a:hover {
		text-decoration: none;
	}

	.form-control {
		padding-left: 8px !important;
		maring-bottom: -20px !important;		
	}	

</style>