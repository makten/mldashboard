<script>

	import vSelect from 'vue-select'

	export default {

		components: { vSelect },

		data () {

			return {

				savedSearches: '',
				
				tableData: {},
				features: [],
				coltypes: [],
				modifiedFeatures: [],
				rowCount: 0,
				syncedVal: '',
				
				deliveries: [
				{name:"Normal Levering", value: 0}, 
				{name:"Next-day", value: 1}, 
				{name:"Express Levering", value: 2}				
				],

				form: new Form({

					target: '',					
					
					features: '',

					portal: 0,					

					channel: 0,

					delivery: 0,

					client: 0,

					category: 0,					

				}),


				api_response: [],
				uploadedFile: '',

				departments: [],

				predictions: [],
				predicted: '',

				monthsBag: [],

			}
		},

		mounted () {

			this.$nextTick( function(){

				
				// this.getSavedSearches();

				// axios.get('api/departments')
				// .then(response => {

				// 	this.departments = JSON.parse(response.data)
				// })
			});




		},

		methods: {

			createFeatures(val){
				this.modifiedFeatures = _.reject(this.features, function(f){return f == val})
				this.form.features = _.reject(this.form.features, function(f){return f == val})
			},

			createFeatureTypes() {
				
				for(let i = 0; i < this.features.length; i++)
				{					
					let x = this.tableData[i][i]
					console.log(x)
					this.coltypes.push({'feature': this.features[i], 'type': x})
				}
				
			},

			getSavedSearches () {

				axios.post('api/getSavedSearches')
				.then(response => {

					this.savedSearches = response.data
					console.log(response.data)

				//this.onSuccess(response);

			})
				.catch(errors => {})
			},

			onSubmit() {

				console.log(this.form)

				// axios.get('/api/departments/add', this.form)
				// .then( response => {	

				// 	this.onSuccess(response.data);

				// })
				// .catch(response => {				

				// });			

			},

			makePrediction () {		
				// console.log(this.form)				

				// axios.get('api/predictOplage', this.form)
				// .then(response => {

				// 	this.onSuccess(response);

				// })
				// .catch(errors => {})
			},


			onSuccess(response) {

				// if(!_.isEmpty(response.error))
				// {

				// 	this.form.errors.record(response.error)

				// }
				// else{


				// 	this.form.reset()
				// 	this.form.errors.clear()				

				// 	this.predicted = response.data					
				// }
			},



			onFileChange(e) {	

				var files = e.target.files || e.dataTransfer.files;
				if (!files.length)
					return;
				this.createCSV(files);



				// let fd = new FormData($('#photo')[0])				

				// this.$http.post('api/sendForm', fd)
				// .then(response => {
				// 	console.log(response.data.result)
				// 	this.api_response = response.data.result					
				// })

				// var files = e.target.files || e.dataTransfer.files;
				// if (!files.length)
				// 	return;
				// this.createImage(files[0]);


			},

			createImage(file) {
				var image = new Image();
				var reader = new FileReader();
				var vm = this;

				reader.onload = (e) => {
					vm.uploadedFile = e.target.result;
				};
				reader.readAsDataURL(file);

				console.log()
			},

			createCSV(files) {

				this.features = [];
				this.coltypes = [];
				this.modifiedFeatures = [];
				this.form.features = '';
				this.form.target = '';
				this.target = '';
				
				let vm = this;
				
				Papa.parse(files[0],{

					// header: true,
					dynamicTyping: true,	
					
					complete: function(results)
					{
						vm.tableData = _.drop(results.data, 1)

						if(typeof results.data[0][0] == 'number')
						{
							for(let i = 0; i < results.data[0].length; i++)
							{
								let row = i + 1
								vm.features.push('Row ' + row)
							}

							vm.createFeatureTypes()
							
						}
						else {

							vm.features = results.data[0]
							vm.createFeatureTypes()

						}


						
						// console.log(typeof results.data[0][0])

						// vm.uploading = False;									
					},

					// step: function(results, parser) {

					// 	vm.rowCount += 1					

					// 	console.log("Row data:", results.data);
					// 	// console.log("Row errors:", results.errors);
					// }
				})

				// var extension = filename.replace(/^.*\./, '');

			 //        // Iff there is no dot anywhere in filename, we would have extension == filename,
			 //        // so we account for this possibility now
			 //        if (extension == filename) {
			 //        	extension = '';
			 //        } else {
			 //            // if there is an extension, we convert to lower case
			 //            // (N.B. this conversion will not effect the value of the extension
			 //            // on the file upload.)
			 //            extension = extension.toLowerCase();
			 //        }		


			},

			removeImage: function (e) {
				this.uploadedFile = '';
			},

			sortAsc(items) {
				return _.sortBy(items, [(i) => {return i.name;}]);
			},

			setSearch() {
				alert('b')
			}
		},

		computed: {

		}


	}


</script>


<template>


	<div class="main">	

		<div class="widget">

			<div class="title">Campaign Prediction</div>

			<div class="chart">

				<div id="csvtable"></div>


				<form class="bs-customizer" role="form" method="POST" @submit.prevent="onSubmit" 
				@keydown="form.errors.clear($event.target.name)">


				<fieldset>

					<!-- <legend>Enter Campaign Details</legend> -->

					<div class="row">


						<div class="col-md-6">
							<span class="label-success">{{ rowCount }}</span>


							<div class="form-group">
								<label for="uploadCsv" class="col-md-2 control-label">File</label>

								<div class="col-md-10">
									<input type="text" readonly="" class="form-control" placeholder="Browse...">
									<input type="file" id="uploadCsv" multiple="False" @change="onFileChange">
								</div>
							</div>
						</div>
						

					</div>

					<div class="row">


						<div class="col-md-4">						
							
							<div class="form-group">
								<label for="search" class="col-md-12 control-label">Target</label>

								<v-select :on-change="createFeatures" v-model="form.target" :options="features"></v-select>
								

								<span class="help is-danger" v-if="form.errors.has('search')" v-text="form.errors.get('search')"></span>
								
							</div>

						</div>


						<div class="col-md-6">
							<div class="form-group" v-if='modifiedFeatures.length > 0'>
								<label for="search" class="col-md-12 control-label">Saved Searches</label>

								<v-select multiple v-model="form.features" :options="modifiedFeatures" transition='expand'></v-select>

								<span class="help is-danger" v-if="form.errors.has('search')" v-text="form.errors.get('search')"></span>
								
							</div>
						</div>


					</div>

					
					<div class="form-group">		
						<table class="table table-bordered table-hover">
							<tr >
								<th v-for="head in coltypes">
									{{ head.feature }} {{ typeof head.type}}
								</th>						
							</tr>

						</table>			
						<!-- <label for="usr">Query</label> -->
						<!-- <input type="text" class="form-control" id="usr" v-model="form.month.search"> -->
					</div>
					



					<div class="form-group">

						{{tableData }}
						<div class="col-md-8 col-md-offset-4">
							<button type="button" class="btn btn-default btn-xs">Reset</button>
							<button type="submit" class="btn btn-primary btn-xs">Predict</button>
						</div>
					</div>

				</fieldset>
			</form>	




			<div class="col-md-8 col-md-offset-2" v-if="predicted.length > 0">
				<span class="text-success" style="font-weight: bolder; font-size: 18px;">{{ Math.ceil(predicted[0][0]) * 1000 }}</span>
			</div>



			<ul class="list-group list-inline" v-for="prediction in predictions">

				<li class="list-group-item">

					{{ Math.ceil(prediction[0]) }}

				</li>

			</ul>


		</div>

	</div>

	<div class="widget">
		<div class="title">Departments Table</div>

		<div class="chart" >

			<form method="POST" @submit.prevent="onSubmit" @keydown="form.errors.clear($event.target.name)">

				<div class="control">

					<label for="name" class="label">Name</label>

					<input type="text" class="input" name="name" v-model="form.name" >
					<span class="help is-danger" v-if="form.errors.has('name')" v-text="form.errors.get('name')"></span>


					<input type="text" class="input" name="description" v-model="form.description" >
					<span class="help is-danger" v-if="form.errors.has('description')" v-text="form.errors.get('description')"></span>					



				</div>

				<button type="submit" >Predict</button>

			</form>

			<table class="table table-striped table-bordered">
				<thead>
					<tr>
						<th width="15%"> Name </th>
						<th width="40%"> Description </th>
						<th width="15%"> Employee Count </th>
						<th width="15%"> Edit </th>
						<th width="15%"> Delete </th>
					</tr>
				</thead>
				<tbody>
					<!-- {% for department in departments %} -->
					<tr v-for="department in departments">
						<td>

							{{ department.name }} 

						</td>
						<td>

							{{ department.description }} 

						</td>

						<td>
							<!-- {{department.employees.length}} -->

						</td>
						<td>
							<a href="#">
								<i class="fa fa-pencil"></i> Edit 
							</a>
						</td>
						<td>
							<a href="#">
								<i class="fa fa-trash"></i> Delete 
							</a>
						</td>
					</tr>
					<!-- {% endfor %} -->
				</tbody>
			</table>

			<!-- <h2 v-if="departments.length > 0">{{ api_response[0][0] }}</h2> -->
				<!-- <ul class="list-group" v-for="item in departments">
					<li class="list-item">
						{{ item.name }}
					</li>
				</ul> -->


				
				

			</div>
		</div>	

		

	</div>

	
</template>

<style>	



</style>