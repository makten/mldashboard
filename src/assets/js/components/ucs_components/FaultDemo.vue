<template>
	<div>

		<button @click="predictFaults" class="btn btn-danger btn-sm">Get Predictions</button>


		<!-- {{ predicted_faults }} -->
		<!-- {{ actual_faults }} -->

		<!-- {{test}} -->

		<div class="row">
			<div class="col-md-4">
				<ul class="list-group fault" v-for="pred in predicted_faults">
					<li :class="isMatched(pred)" class="list-group-item">
						<span style="padding: 5px; ">{{pred[1]}}</span> || <span style="padding: 5px; ">{{pred[1]}}</span>
					</li>
					<!-- <li :class="isMatched(pred)">
						
					</li> -->
				</ul>
			</div>

			<!-- <div class="col-md-2">
				<ul class="list-group" v-for="(act, fake) in actual_faults">
					<li class="list-group-item" v-bind:class="isMatched(fake)">{{ act }}</li>
				</ul>
			</div> -->
		</div>
		
	</div>
</template>

<style lang="sass">
	.matched {
		background: #45A745 !important;
	}

	.notmatched {
		background: #F64F05 !important;
	}
</style>



<script>

	export default {
		data (){
			return {
				predicted: {},
				actual: {},
				predicted_faults: [],
				actual_faults: [],
				minors:[],
				warnings:[],
				criticals:[],
				majors:[],
			}
		},

		mounted() {
			this.$nextTick(function(){

			})
		},

		methods : {
			predictFaults() {

				axios.get('/api/predictfaults')
				.then(response => {					

					this.predicted_faults = JSON.parse(response.data);
					// this.actual_faults = JSON.parse(response.data.actuals);
					// console.log(this.predicted_faults)
            		this.warnings = _.filter(this.predicted_faults, (f)=>{return f != 'F0185'})//F0185
            		this.criticals = _.filter(this.predicted_faults, (f)=>{return f != 'F0184'})//F0184
            		this.majors = _.filter(this.predicted_faults, (f)=>{return f != 'F0844'})//F0844 disabled     		


            	})
				.catch(errors => { })
			},

			isMatched (pred) {

				return pred[0] == pred[1] ? "matched list-group-item" : "notmatched list-group-item";
			}
		}
	}
	
</script>



