<template>
	<div>

		<button @click="predictFaults" class="btn btn-danger btn-sm">Get Predictions</button>

		<div class="row">
			<div class="col-md-3">
				<ul class="list-group" v-for="pred in predicted_faults">
					
					<li :class="isMatched(pred)" class="list-group-item">						
						<span class="col-md-2" style="padding: 5px; margin-right: 10px;">{{pred[0]}}</span>  <span class="col-md-2" style="padding: 5px; margin-left: 20px;">{{pred[1]}}</span>
					</li>	
					
				</ul>
			</div>
			
		</div>
		
	</div>
</template>

<style lang="sass">
	.matched {
		color: black;
		font-weight: bolder;
		background: #88FFDC !important;
	}

	.notmatched {
		color: white;
		background: #FA9999 !important;
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
            		this.warnings = _.filter(this.predicted_faults, (f)=>{return f[0] != 'F0185'})//F0185
            		this.criticals = _.filter(this.predicted_faults, (f)=>{return f[0] != 'F0184'})//F0184
            		this.majors = _.filter(this.predicted_faults, (f)=>{return f[0] != 'F0844'})//F0844 disabled     		


            	})
				.catch(errors => { })
			},

			isMatched (pred) {

				return pred[0] == pred[1] ? "matched list-group-item" : "notmatched list-group-item";
			}
		}
	}
	
</script>



