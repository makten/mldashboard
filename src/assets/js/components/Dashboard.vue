<script>
    import vSelect from 'vue-select';
    import tabs from '../../core/tabs.js';
    import tab from '../../core/tab.js';
    import UcsSystem from './ucs_components/UcsSystem.vue';
    import Ucs from './ucs_components/Ucs.vue';
    import Chassis from './ucs_components/Chassis.vue';
    import ChassisServer from './ucs_components/ChassisServer.vue';
    import RackMount from './ucs_components/RackMounts.vue';
    import { Validator } from 'vee-validate';

    export default {

        components: {
            Ucs,
            UcsSystem,
            Chassis,
            ChassisServer,
            RackMount,
            vSelect,
            Bar,
            LineChart,
            tabs,
            tab,
            Validator
        },

        data() {

            return {    

                // errors: null, 

                
                
                ipAddress: '',

                
                
                rackunits: [],                
                

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
                
                // Broadcast the currently selected tab id to tabs.vue

                if(window.location.hash){
                    eventBroadcaster.$emit('setTab', window.location.hash)
                }
                



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

            // this.plotChart(ctx);
            // setInterval(function() {
            //     let a = Math.floor((Math.random() * 50) + 1)
            //     let i = Moment().format()

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
                    // console.log(this.rackunits)
                    
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
            }

        },


        beforeDestroy: function () {
            clearInterval(this.interval);
        }

    }
</script>


<template>

    <div class="main">




        <div class="widget">




            <!-- <div class="chart" style="background: #004080;">
    
                <bar :data="barData"
                     :options="{responsive: false, maintainAspectRatio: false}"
                     :width="400"
                     :height="200">
    
                </bar>
    
            </div> -->

            <!-- <div class="chart">
    
                <bar :data="barData2"
                     :options="{responsive: false, maintainAspectRatio: false}"
                     :width="400"
                     :height="200">
    
                </bar>
    
            </div> -->


            <div class="chart">

                <tabs>

                    <tab name="UCS" :selected="true" >
                        <h3>UCS Systems</h3>
                        
                        <ucs></ucs>
                        
                    </tab>

                    <tab name="UCS Overview">
                        <h3>UCS overview</h3>
                        
                        <ucs-system :ucs="ipAddress"></ucs-system>
                        
                    </tab>


                    <tab name="Chassis">
                        <h3>Chassis list</h3>
                        <chassis></chassis>

                    </tab>

                    <tab name="Chassis Servers">
                        <h1>Chassis Servers List</h1>
                        <chassis-server></chassis-server>
                    </tab>

                    <tab name="RackMounts">
                        <h1>RackMount Servers</h1>
                        <rack-mount ucs=''></rack-mount>
                    </tab>
                </tabs>                

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


    


</div>

</template>



<style lang="sass">

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


    .help-block {
        font-size: 10px !important;
    }

    a {
        text-decoration: none;
    }

    a :hover {
        text-decoration: none;
    }

    .small {
        max-width: 350px;
        max-heigth: 100px;
    }

    .error-block {
        animation: shake 0.82s cubic-bezier(.36,.07,.19,.97) both;
        transform: translate3d(0, 0, 0);
        backface-visibility: hidden;
        perspective: 1000px;
    }


    @keyframes shake {
        10%, 90% {
            transform: translate3d(-1px, 0, 0);
        }

        20%, 80% {
            transform: translate3d(2px, 0, 0);
        }

        30%, 50%, 70% {
            transform: translate3d(-4px, 0, 0);
        }

        40%, 60% {
            transform: translate3d(4px, 0, 0);
        }
    }
</style>
