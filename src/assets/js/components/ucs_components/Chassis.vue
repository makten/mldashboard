
<script>
	
	export default {

		props: {},

		data() {
			return {
				chassis: [],
				single_chassis: {},
				chassis_stats: [],

				chassisColumns: ['name', 'model', 'status'],
				chassisOptions: {
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

        		this.getChassis();

        	});
        },

        methods: {

        	getChassis() {

        		axios.get('/api/get_chassis/')
        		.then(response => {

        			this.chassis = []
        			this.chassis = JSON.parse(response.data)
        		})
        		.catch(errors => { })
        	},

        	getChassisStats(dn, chassis) {

        		let str_dn = dn.split('/')
        		let chs = str_dn[1]
        		this.single_chassis = chassis

        		axios.get(`/api/getChassisStats/${chs}/`)
        		.then(response => {

        			this.chassis_stats = [];
        			this.chassis_stats = JSON.parse(response.data);

                    // this.createGauge('power', 'power', parseInt(this.chassis_stats.input_power_min), parseInt(this.chassis_stats.input_power))

                    // this.editForm.id = client.id;
                    // this.editForm.name = client.name;
                    // this.editForm.redirect = client.redirect;
                    // $('#modal-edit-client').modal('show');

                    this.showStats = true;

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

		<div id="Chassis">

			<v-client-table :data="chassis" :columns="chassisColumns" :options="chassisOptions">
				<template slot="name" scope="props">

					<div>
						<a href="javascript:void(0)" @click="getChassisStats(props.row.dn, props.row)">
							{{props.row.name}}
						</a>

					</div>
				</template>
			</v-client-table>

		</div>

	</div>
</template>


<style lang="sass">
	
</style>
