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
    import { mapGetters } from 'vuex';

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
                
                ucsSystem: {},
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
                api_response: [],
                uploadedFile: '',
                departments: [],
                predictions: [],
                predicted: '',
                monthsBag: [],
                interval: null,

                barData: {
                    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                    datasets: [{
                        label: 'Power Usage Per Month kW',
                        backgroundColor: '#FD442B',

                        color: '#A11D1D',

                        data: [800, 1300, 900, 800, 1400, 1000, 0, 0, 0, 0, 0, 0]
                    }]
                },

                chartdata: {
                    labels: [Moment().add(Math.random(1, 10), 'hours').format('HH:mm:ss a'), Moment().add(Math.random(1, 10), 'hours').format('HH:mm:ss a'), Moment().add(Math.random(1, 10), 'hours').format('HH:mm:ss a'), Moment().add(Math.random(1, 10), 'hours').format('HH:mm:ss a'), Moment().add(Math.random(1, 10), 'hours').format('HH:mm:ss a'), Moment().add(Math.random(1, 10), 'hours').format('HH:mm:ss a'), Moment().add(Math.random(1, 10), 'hours').format('HH:mm:ss a'), Moment().add(Math.random(1, 10), 'hours').format('HH:mm:ss a'), Moment().add(Math.random(1, 10), 'hours').format('HH:mm:ss a'), Moment().add(Math.random(1, 10), 'hours').format('HH:mm:ss a'), Moment().add(Math.random(1, 10), 'hours').format('HH:mm:ss a'), Moment().add(Math.random(1, 10), 'hours').format('HH:mm:ss a')],

                    datasets : [
                    {
                        label: "Temp Srv. Closet",
                        fill: true,
                        lineTension: 0.11,
                        backgroundColor: "#34DCFA",
                        borderColor: "#1344FC",
                        borderCapStyle: 'butt',
                        borderDash: [],
                        borderDashOffset: 0.9,
                        borderJoinStyle: 'miter',
                        pointBorderColor: "rgba(75,192,192,1)",
                        pointBackgroundColor: "#fff",
                        pointBorderWidth: 1,
                        pointHoverRadius: 5,
                        pointHoverBackgroundColor: "rgba(75,192,192,1)",
                        pointHoverBorderColor: "rgba(220,220,220,1)",
                        pointHoverBorderWidth: 2,
                        pointRadius: 1,
                        pointHitRadius: 1,
                        data : [26,25,23,27,25,26,27,26,25,25]
                    },
                    {
                        label: "Temp Datacenter",
                        fill: true,
                        lineTension: 0.11,
                        backgroundColor: "#FB6161",
                        borderColor: "#FF0000",
                        borderCapStyle: 'butt',
                        borderDash: [],
                        borderDashOffset: 0.9,
                        borderJoinStyle: 'miter',
                        pointBorderColor: "rgba(75,192,192,1)",
                        pointBackgroundColor: "#ffffff",
                        pointBorderWidth: 1,
                        pointHoverRadius: 5,
                        pointHoverBackgroundColor: "rgba(75,192,192,1)",
                        pointHoverBorderColor: "rgba(220,220,220,1)",
                        pointHoverBorderWidth: 2,
                        pointRadius: 1,
                        pointHitRadius: 1,                      
                        data : [35,33,34,35,36,36,35,37,40,39]
                    }
                    ]
                },

                chartOption: {

                    animation: {
                        duration: 0,              
                        scaleOverride : true,             
                        scaleSteps : 10,             
                        scaleStepWidth : 10,              
                        scaleStartValue : 0
                    },

                    elements: {
                        line: {
                            borderWidth: 1,
                        },
                        point: {
                            radius: 2,
                        },
                    },

                    scales: {                        
                    }
                }

            }
        },

        mounted() {

            this.$nextTick(function () {

                // if(window.location.hash){
                //     eventBroadcaster.$emit('setTab', window.location.hash)
                // }
                eventBroadcaster.$on('setUcs', this.setUcsSystem)               

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
                    
                })
                .catch(errors => { })
            },            

            getSavedSearches() {

                axios.post('api/getSavedSearches')
                .then(response => {

                    this.savedSearches = response.data
                    console.log(response.data)
                        // this.onSuccess(response);

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

                    },
                    
                })

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

        computed: {
            //Install - --save-dev babel-preset-stage-2
            ...mapGetters({
                ucs: 'uscsystems'
            }),

        },                   

        beforeDestroy: function () {
            clearInterval(this.interval);
        }

    }
</script>


<template>

    <div class="main">

        <div class="widget col-md-9">

            <div class="chart">

                <tabs>
                    <tab name="UCS" :selected="true" >
                        <h4>UCS Systems</h4>
                        <ucs></ucs>
                    </tab>

                    <tab name="UCS Overview">
                        <h4>UCS overview</h4>
                        <ucs-system></ucs-system>
                    </tab>


                    <tab name="Chassis">
                        <h4>Chassis list</h4>
                        <chassis></chassis>
                    </tab>

                    <tab name="Chassis Servers">
                        <h4>Chassis Servers List</h4>
                        <chassis-server></chassis-server>
                    </tab>

                    <tab name="RackMounts">
                        <h4>RackMount Servers</h4>
                        <rack-mount></rack-mount>
                    </tab>
                </tabs>
            </div>
        </div> 

        <div class="widget col-md-3" style="margin-left: 0px; padding: 0px;">
            <div class="chart">
                <div class="title">Data Center Statistics</div>
                <div class="row">
                    <div class="col-md-12">
                        <bar :chart-data="barData" :options="{responsive: false, maintainAspectRatio: true}" :width="400" :height="250"> </bar>

                        <hr/>

                        <line-chart :chart-data="chartdata" :options="{responsive: false, maintainAspectRatio: true}" :width="400" :height="250"></line-chart>
                    </div>
                    
                </div>
            </div>

        </div>      


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
