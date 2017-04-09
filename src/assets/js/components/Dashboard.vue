<script>
    import vSelect from 'vue-select';
    import tabs from '../../core/tabs.js';
    import tab from '../../core/tab.js';
    import UcsSystem from './ucs_components/UcsSystem.vue';
    import Chassis from './ucs_components/Chassis.vue';
    import ChassisServer from './ucs_components/ChassisServer.vue';
    import RackMount from './ucs_components/RackMounts.vue';
    



    export default {

        components: {
            UcsSystem,
            Chassis,
            ChassisServer,
            RackMount,
            vSelect,
            Bar,
            LineChart,
            tabs,
            tab
        },

        data() {

            return {        

                ucs_systems: [],
                ipAddress: '',                     

                datacollection: null,
                
                rackunits: [],                
                faults: [],

                savedSearches: '',

                tableData: {},
                features: [],
                coltypes: [],
                modifiedFeatures: [],
                rowCount: 0,
                syncedVal: '',
                chartLine: null,

                
                

                gauges: [],

                barData: {
                    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                    datasets: [{
                        label: 'Test Data Hafiz',
                        backgroundColor: '#ff8040',

                        color: '#ffffff',

                        data: [40, 20, 12, 39, 10, 40, 39, 80, 40, 20, 12, 11]
                    }]
                },

                barData2: {

                    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],

                    datasets: [{

                        label: 'Test Data 2',

                        backgroundColor: '#ff0000',

                        color: '#ffffff',

                        fillColor: "rgba(220,220,220,0.5)",

                        strokeColor: "rgba(220,220,220,0.8)",

                        highlightFill: "rgba(220,220,220,0.75)",

                        highlightStroke: "rgba(220,220,220,1)",

                        borderColor: "#14B214",

                        data: [100, 60, 12, 100, 10, 40, 1, 80, 2, 20, 12, 11]

                    }]

                },              


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
                interval: null,

            }
        },

        mounted() {

            this.$nextTick(function () {

                this.getUcsList();

                /** Query UCS System
                // If none popup modal to add
                    /**
                    * 1. IP and subnet
                    * 2. Add credentials
                    * 3 Discover and show overview
                    *
                // ELSE show a list of ucs to select from
                * If online one, show it
                */ 

                // this.initialize();
                // this.getUcsInfo();
                // this.fillData();
                
                // this.getRackUnits();
                

            //this.getBladeFaults();

            var ctx = $("#myChart");

            // $('#modal-create-company').on('shown.bs.modal', () => {
            //     $('#create-company-name').focus();
            // });

            // $('#modal-edit-client').on('shown.bs.modal', () => {
            //     $('#edit-client-name').focus();
            // });

            // this.plotChart(ctx);
            // setInterval(function() {
            //     let a = Math.floor((Math.random() * 50) + 1)
            //     let i = Moment().format()
            //     console.log(i)
            //         // add(Math.floor((Math.random() * 6) + 1), 'days').
            //     // this.forecasted = _.drop(this.forecasted, 1)
            //     this.forecasted.push({
            //         y: a,
            //         x: i
            //     })
            //     this.plotChart(ctx)
            //     // this.chartLine.update()
            // }.bind(this), 3000);
            // this.getSavedSearches();
            // axios.get('api/departments')
            // .then(response => {
            // 	this.departments = JSON.parse(response.data)
            // })

        });

        },


        methods: {  

            getUcsList() {
                axios.get(`/api/getUcsSystems/`)
                .then(response => {                 

                    this.ucs_systems = response.data  
                    
                    // this.ipAddress = this.ucs_systems[0].ipAddress                  

                    // $('#modal-ucs-list').modal('show');                    

                })
                .catch(errors => { })
            }, 

            selectUCS(ucs) {
                this.ipAddress = ucs.ipAddress
            },         

            /**
            * Show the form for creating new company.
            */
            showcompanyForm() {
                $('#modal-create-company').modal('show');
            },


            /**
            * Show the form for creating new contact person.
            */
            showcontactpersonForm() {
                $('#modal-create-contactperson').modal('show');
            },

            /**
            * Edit the given client.
            */
            edit(client) {

                this.editForm.id = client.id;
                this.editForm.name = client.name;
                this.editForm.redirect = client.redirect;

                $('#modal-edit-client').modal('show');
            },

            fillData() {
                this.datacollection = {
                    labels: [this.getRandomInt(), this.getRandomInt()],
                    datasets: [{
                        label: 'Data One',
                        backgroundColor: '#f87979',
                        data: [this.getRandomInt(), this.getRandomInt()]
                    }, {
                        label: 'Data One',
                        backgroundColor: '#f87979',
                        data: [this.getRandomInt(), this.getRandomInt()]
                    }]
                }
            },


            getRandomInt() {
                return Math.floor(Math.random() * (50 - 5 + 1)) + 5
            },          


            getRackUnits() {

                axios.get('/api/get_rackunits')
                .then(response => {

                    this.this.rackunits = []
                    this.rackunits = JSON.parse(response.data)
                    console.log(this.rackunits)
                    
                })
                .catch(errors => { })
            },            

            getSavedSearches() {

                axios.post('api/getSavedSearches')
                .then(response => {

                    this.savedSearches = response.data
                    console.log(response.data)

                        //this.onSuccess(response);

                    })
                .catch(errors => { })
            },

            onSubmit() {
                // this.chartLine.update()
                // console.log(this.form)

                // axios.get('/api/departments/add', this.form)
                // .then( response => {	

                // 	this.onSuccess(response.data);

                // })
                // .catch(response => {				

                // });			

            },

            makePrediction() {
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

                Papa.parse(files[0], {

                    // header: true,
                    dynamicTyping: true,

                    complete: function (results) {
                        vm.tableData = _.drop(results.data, 1)

                        if (typeof results.data[0][0] == 'number') {
                            for (let i = 0; i < results.data[0].length; i++) {
                                let row = i + 1
                                vm.features.push('Row ' + row)
                            }

                            vm.createFeatureTypes()

                        } else {

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
                return _.sortBy(items, [(i) => {
                    return i.name;
                }]);
            },


            setSearch() {
                alert('b')
            },


            createGauge(name, label, min, max) {
                var config = {
                    size: 120,
                    label: label,
                    min: undefined != min ? min : 0,
                    max: undefined != max ? max : 100,
                    minorTicks: 5
                }

                var range = config.max - config.min;
                config.yellowZones = [{
                    from: config.min + range * 0.75,
                    to: config.min + range * 0.9
                }];
                config.redZones = [{
                    from: config.min + range * 0.9,
                    to: config.max
                }];

                this.gauges[name] = new Gauge(name + "GaugeContainer", config);
                this.gauges[name].render();
            },


            createGauges() {
                this.createGauge("memory", "Memory");
                this.createGauge("cpu", "CPU");
                // this.createGauge("network", "Network");
                this.createGauge("test", "Test", 1254, 3200);
            },


            updateGauges() {

                for (var key in this.gauges) {
                    console.log(key)
                    var value = this.getRandomValue(this.gauges[key])
                    this.gauges[key].redraw(value);
                    console.log(this.gauges)
                }
            },


            getRandomValue(gauge) {
                var overflow = 0; //10;
                return gauge.config.min - overflow + (gauge.config.max - gauge.config.min + overflow * 2) * Math.random();
            },


            initialize() {
                this.createGauges();
                setInterval(this.updateGauges, 5000);
            },


        // toggleStatsView() {
        //     this.showStats != this.showStats;
        // }

    },


    beforeDestroy: function () {
        clearInterval(this.interval);
    }

}
</script>


<template>

    <div class="main">


        <div class="widget">

            <div class="chart">

                <tabs v-if="ipAddress">

                    <tab name="UCS Overview" :selected="true" >
                        <h1>Here is the content for the UCS overview tab.</h1>
                        
                        <ucs-system :ucs="ipAddress"></ucs-system>
                        
                    </tab>


                    <tab name="Chassis">
                        <h1>Here is the content for the chassis tab.</h1>
                        <chassis></chassis>

                    </tab>

                    <tab name="Chassis Servers">
                        <h1>Here is the content for the chassis servers tab.</h1>
                        <chassis-server></chassis-server>
                    </tab>

                    <tab name="RackMounts">
                        <h1>Here is the content for the about our vision tab.</h1>
                        <rack-mount ucs=''></rack-mount>
                    </tab>
                </tabs>
                <div v-else>
                    <h3>Select UCS System</h3>
                    
                    <ul class="list-group" v-for="ucs in ucs_systems">
                        <li class="list-group-item">
                            <a href="#" @click="selectUCS(ucs)"> {{ ucs.ipAddress }} </a>
                        </li>
                    </ul>
                </div>

            </div>
        </div>


        <!-- <div class="widget">

            <div class="title">Chassis List</div>

            <div class="chart" style="background: #004080;">
                <bar :data="barData" :options="{responsive: false, maintainAspectRatio: false}" :width="400" :height="200"> </bar>
            </div>

            <div class="chart">
                <bar :data="barData2" :options="{responsive: false, maintainAspectRatio: false}" :width="400" :height="200"></bar>
            </div>
        </div> -->


        <!-- Show UCS List Modal -->
        <div class="modal fade" id="modal-ucs-list" tabindex="-1" role="dialog">

            <div class="modal-dialog">

                <div class="modal-content">

                    <div class="modal-header">
                        <button type="button " class="close" data-dismiss="modal" aria-hidden="true">&times;</button>

                        <h4 class="modal-title"> UCS LIST</h4>
                    </div>

                    <div class="modal-body">

                        <h3>body</h3>

                        {{ ucs_systems }}

                    </div>


                    <div class="modal-footer">
                        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                        <!-- <button type="button" class="btn btn-primary" @click="storeCompany"> Opslaan </button> -->
                    </div>

                </div>
            </div>
        </div>


        

    </div>

</template>



<style lang="sass">

    .small {
        max-width: 150;
        margin: 150px auto;
    }


    .VueTables__table tr {
        font-size: 11px !important;
    }

    .icon-small {
        font-size: 15px;
    }

    .nav-pills>li.is-active>a, 
    .nav-pills>li.active>a:focus, 
    .nav-pills>li.active>a:hover {

        color: #3a3a3a;
        background-color: #f0f5fb;

    }

    .table-borderless > tbody > tr > td,
    .table-borderless > tbody > tr > th,
    .table-borderless > tfoot > tr > td,
    .table-borderless > tfoot > tr > th,
    .table-borderless > thead > tr > td,
    .table-borderless > thead > tr > th {
        border: none;
    }

    .title {
        background: #DAD8D8 !important;
    }

</style>