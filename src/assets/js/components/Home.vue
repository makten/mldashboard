<script>


	export default {
		

		data () {
			return {

				persons: [
					{name: 'Hafiz Abass', city: 'Zwolle'},
					{name: 'Hafiz Abass', city: 'Zwolle'}
				]
			}
		},
		mounted () {
			this.$nextTick( function(){
				
				
			});
		}
		
	}

</script>


<template>


	<div class="main">

		<div class="col-md-8 col-md-offset-2" id="bam" style="margin-top: 80px;">

			<h1>

				Something Amazing Is Coming Soon!

			</h1>

			<p class="fadeIn wait-2s">You Will Love it</p>

		</div>	


		<div class="widget">
			<div class="title">Number of views</div>
			<div class="chart" v-for="person in persons">
				<p>{{ person.name }}</p>
				<p>{{ person.city }}</p>
			</div>
		</div>


		<div class="widget">
			<div class="title">Number of likes</div>
			<div class="chart">
			<button class="btn btn-success btn-sm">Buuuuut</button>
			</div>
		</div>
		
		<div class="widget">
			<div class="title">Number of comments</div>
			<div class="chart"></div>
		</div>

	</div>

	
</template>

<style>
	
</style>