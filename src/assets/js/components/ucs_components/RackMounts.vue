
<script>
	export default {
		props: {
			// ucs: {required: true},
		},

		data() {
			return {
				ucsActive: true
			};
		},


		mounted() {
			this.$nextTick(function(){

				// if(this.ucs != ''){
				// 	// this.getChassis();
				// }
				// else {
				// 	this.ucsActive = false
				// }

			});
		},

		methods: {

		},

		computed: {

		}
	}
</script>

<template>

	<div>
		<div id='Rackmount' v-if="ucsActive">
		
		</div>
		
		<div class='col-md-6 col-md-offset-3'>
			<div class="alert alert-dismissible alert-warning">
				<button type="button" class="close" data-dismiss="alert">&times</button>
				<strong>Oh snap!!</strong>
				There are currently no rack units available
			</div>		
		</div>

	</div>
	
</template>

<style lang="sass">
	
</style>