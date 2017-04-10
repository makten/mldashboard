/**
*	This component handles all chassis server api calls
*
*/
<script>

	export default {

		// props: {ucs: {required: true}},


		data() {

			return {
				
				showStats: false, 
				chassis_servers: [],
				blade_cpustats: [],
                faults: [],
				chassisServerColumns: [
				'equipment', 'model', 'serial', 'num_of_cpus', 'num_of_cores', 
				'enabled_cpu_cores', 'total_memory', 'available_memory', 'NICs', 
				'power', 'serial', 'presence', 'assocState', 'stats', 'faults'
				],

				chassisServerOptions: {
                    // see the options API
                    templates: {

                        // faults: function (h, row) {                        
                        //     return <a href="javascript:void(0)" > <span class="material-icons text-danger" style="font-size:15px;">error</span></a>
                        // }
                    }
                },

            };
        },


        mounted() {
        	this.$nextTick(function(){

        		this.getBlades();

        		console.log('testing chassis server component')

        	});
        },


        methods: {        	

        	getBlades() {

        		axios.get('/api/get_blades')
        		.then(response => {
        			
        			this.chassis_servers = JSON.parse(response.data)

        		})
        		.catch(errors => { })
        	},


        	loadStats(cpustats, dn) {

        		let len = cpustats.length;
        		let sm = 0;

        		_.each(cpustats, (val, key) => { sm += parseInt(val.input_current) });
        		
        		// this.createGauge('singlecpu', 'CPU', 0, sm)

        		this.blade_cpustats = cpustats;
        		this.getBladeFaults(dn)

        	},

        	getBladeFaults(dn) {
        		let str_dn = dn.split('/')
        		let chs = str_dn[1]
        		let bld = str_dn[2]

        		axios.get(`/api/get_bladefaults/${chs}/${bld}`)
        		.then(response => {
        			this.faults = [];
        			this.faults = JSON.parse(response.data);

        		})
        		.catch(errors => { })
        	},
        	
        },

        computed() {

        }



    }

</script>


<template>

	<div>

		<div id="ChassisServers">

			<v-client-table :data="chassis_servers" :columns="chassisServerColumns" :options="chassisServerOptions">

				<template slot="stats" scope="props">
					<div>
						<a href="javascript:void(0)" @click="loadStats(props.row.cpu_stats, props.row.dn)">
							<span class="material-icons text-success icon-small">poll</span>
						</a>
					</div>
				</template>

				<template slot="faults" scope="props">
					<div>
						<a href="javascript:void(0)" @click="getBladeFaults(props.row.dn)">
							<span class="material-icons text-danger icon-small">error</span>
						</a>

					</div>
				</template>

			</v-client-table>


			<div v-if="blade_cpustats.length >= 1">
				<ul class="list-group" v-for="stats in blade_cpustats">

					<li class="list-group-item">
						{{ stats.dn }} {{stats}}
					</li>

				</ul>

				<ul class="list-group" v-for="fault in faults">

					<li class="list-group-item">
						{{ fault.code }} {{ fault.cause }} {{ fault.descr }} {{ fault.severity }} {{ fault.created }} {{fault}}
					</li>

				</ul>

			</div>

		</div>

		
	</div>

</template>

<style lang="sass">
	

</style>