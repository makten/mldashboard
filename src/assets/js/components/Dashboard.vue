<script>
    import vSelect from 'vue-select';


    export default {

        components: {

            vSelect,
            Bar,
            LineChart,
        },

        data() {

            return {

                showStats: false,

                ucs_info: [],

                datacollection: null,

                chassis: [],
                single_chassis: {},
                chassis_stats: [],

                blades: [],
                rackunits: [],
                blade_cpustats: [],
                faults: [],

                savedSearches: '',

                tableData: {},
                features: [],
                coltypes: [],
                modifiedFeatures: [],
                rowCount: 0,
                syncedVal: '',
                chartLine: null,

                chassisServerColumns: ['equipment', 'model', 'serial', 'num_of_cpus', 'num_of_cores', 'enabled_cpu_cores', 'total_memory', 'available_memory', 'NICs', 'power', 'serial', 'presence', 'assocState', 'stats', 'faults'],
                chassisColumns: ['name', 'model', 'status'],

                chassisServerOptions: {
                    // see the options API
                    templates: {

                        // faults: function (h, row) {                        
                        //     return <a href="javascript:void(0)" > <span class="material-icons text-danger" style="font-size:15px;">error</span></a>
                        // }
                    }
                },

                chassisOptions: {
                    // see the options API
                    templates: {

                        // faults: function (h, row) {                        
                        //     return <a href="javascript:void(0)" > <span class="material-icons text-danger" style="font-size:15px;">error</span></a>
                        // }
                    }
                },

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

                this.initialize();
                this.getUcsInfo();
                this.fillData();
                this.getBlades();
                this.getRackUnits();
                this.getChassis();

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

            getUcsInfo() {

                axios.get('/api/get_ucsinfo')
                .then(response => {

                    this.ucs_info = JSON.parse(response.data)
                    console.log(this.ucs_info)
                })
                .catch(errors => { })

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

                axios.get(`/api/getChassisStats/${chs}`)
                .then(response => {

                    this.chassis_stats = [];
                    this.chassis_stats = JSON.parse(response.data);

                    this.createGauge('power', 'power', parseInt(this.chassis_stats.input_power_min), parseInt(this.chassis_stats.input_power))

                    this.editForm.id = client.id;
                    this.editForm.name = client.name;
                    this.editForm.redirect = client.redirect;

                    $('#modal-edit-client').modal('show');

                    this.showStats = true;

                })
                .catch(errors => { })
            },

            getBlades() {

                axios.get('/api/get_blades')
                .then(response => {

                    this.blades = []
                    this.blades = JSON.parse(response.data)
                    
                })
                .catch(errors => { })
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

            loadStats(cpustats, dn) {

                let len = cpustats.length;
                let sm = 0;

                _.each(cpustats, (val, key) => {
                    sm += parseInt(val.input_current)
                    //singlecpu

                })

                console.log(sm, sm / len)

                this.createGauge('singlecpu', 'CPU', 0, sm)


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

            <div class="title">Chassis List</div>

            <div class="chart" style="background: #004080;">

              <bar :data="barData"
              :options="{responsive: false, maintainAspectRatio: false}"
              :width="400"
              :height="200"> </bar>

          </div>

          <div class="chart">

            <bar :data="barData2"
            :options="{responsive: false, maintainAspectRatio: false}"
            :width="400"
            :height="200">

        </bar>

    </div>

</div>



<div class="widget">

    <div class="chart">

        <div id="exTab3" class="container" style="padding: 0px; margin: 0px;">

            <!-- TABS -->
            <ul class="nav nav-pills">

                <li class="active">
                    <a href="#overview"
                    data-toggle="tab">Overview</a>
                </li>

                <li>
                    <a href="#chassis_tab"
                    data-toggle="tab">Chassis</a>
                </li>

                <li>
                    <a href="#chassis_servers"
                    data-toggle="tab">Chassis Servers</a>
                </li>
                <li>
                    <a href="#rackmount"
                    data-toggle="tab">RackMounts</a>
                </li>

                <li>
                    <a href="#finterconnects"
                    data-toggle="tab">Fabric Interconnect</a>
                </li>

                <li>
                    <a href="#5a"
                    data-toggle="tab">UCS Tree</a>
                </li>

                <li>
                    <a href="#6a"
                    data-toggle="tab">ServiceProfile</a>
                </li>

                <li>
                    <a href="#6b"
                    data-toggle="tab">UCS Components</a>
                </li>

            </ul>
            <!-- / TABS -->



            <div class="tab-content clearfix">


                <!-- OVERVIEW -->
                <div class="tab-pane active" id="overview">

                    <h3>UCS-OVERVIEW</h3>

                    <!-- General UCS Information -->
                    <table class="table table-responsive table-responsive">
                     <tbody>
                         <tr>
                             <td width="30%">
                                 <div class="widget" style="margin-left: 0px; padding: 0px;">

                                     <div class="title">UCS information</div>

                                     <table class="table table-borderless">                       

                                        <tbody>
                                            <tr>
                                                <td width="30%" align="left">
                                                    <span>Name</span>
                                                </td>
                                                <td width="5%" align="center">:</td>

                                                <td align="left">
                                                    <span> {{ ucs_info.name }} </span>
                                                </td>       
                                            </tr>

                                            <tr>
                                                <td width="30%" align="left">
                                                    <span>Status</span>
                                                </td>
                                                <td width="5%" align="center">:</td>

                                                <td align="left">
                                                    <span><i class="material-icons text-success" style="font-size: 10px;">fiber_manual_record</i> {{ ucs_info.status }} Clear</span>
                                                </td>       
                                            </tr>

                                            <tr>
                                                <td width="30%" align="left">
                                                    <span>IP Address</span>
                                                </td>
                                                <td width="5%" align="center">:</td>

                                                <td align="left">
                                                    <span> {{ ucs_info.address }}</span>
                                                </td>       
                                            </tr>

                                            <tr>
                                                <td width="30%" align="left">
                                                    <span>System up time</span>
                                                </td>
                                                <td width="5%" align="center">:</td>

                                                <td align="left">
                                                    <span> {{ ucs_info.system_up_time }}</span>
                                                </td>       
                                            </tr>

                                            <tr>
                                                <td width="30%" align="left">
                                                    <span>Mode</span>
                                                </td>
                                                <td width="5%" align="center">:</td>

                                                <td align="left">
                                                    <span> {{ ucs_info.mode }}</span>
                                                </td>       
                                            </tr>

                                        </tbody>
                                    </table>

                                </div> <!-- / General UCS Information -->


                                <div class="widget" style="margin-left: 0px; padding: 0px;">

                                    <div class="title" style="background: #e4e4e4">UCS Faults</div> 


                                    <ul class="list list-group">                            

                                        <li class=" list-group-item text-success">General information</li>
                                        <li class=" list-group-item">Number of faults per type</li>
                                        <li class=" list-group-item">Power consumption</li>
                                        <li class=" list-group-item">Num of blades</li>
                                        <li class=" list-group-item" >Num of Chassis</li>
                                        <li class=" list-group-item">Availabity</li>
                                        <li class=" list-group-item">Network ports</li>
                                        <li class=" list-group-item">Packets</li>
                                        <li class=" list-group-item">Service Profiles</li>
                                    </ul> 
                                </div>


                                <div class="widget" style="margin-left: 0px; padding: 0px;">

                                    <div class="title" style="background: #e4e4e4">UCS Components</div>                       

                                     <table class="table table-borderless">                       

                                        <tbody>
                                            <tr>
                                                <td width="30%" align="left">
                                                    <span>Chassis</span>
                                                </td>
                                                <td width="5%" align="center">:</td>

                                                <td align="left">
                                                    <span class="badge"> {{ chassis.length }} </span>
                                                </td>       
                                            </tr>

                                            <tr>
                                                <td width="30%" align="left">
                                                    <span>Chassis Servers</span>
                                                </td>
                                                <td width="5%" align="center">:</td>

                                                <td align="left">
                                                    <span class="badge"> {{ blades.length }}</span>
                                                </td>       
                                            </tr>

                                            <tr>
                                                <td width="30%" align="left">
                                                    <span>IP Address</span>
                                                </td>
                                                <td width="5%" align="center">:</td>

                                                <td align="left">
                                                    <span> {{ ucs_info.address }}</span>
                                                </td>       
                                            </tr>

                                            <tr>
                                                <td width="30%" align="left">
                                                    <span>System up time</span>
                                                </td>
                                                <td width="5%" align="center">:</td>

                                                <td align="left">
                                                    <span> {{ ucs_info.system_up_time }}</span>
                                                </td>       
                                            </tr>

                                            <tr>
                                                <td width="30%" align="left">
                                                    <span>Mode</span>
                                                </td>
                                                <td width="5%" align="center">:</td>

                                                <td align="left">
                                                    <span> {{ ucs_info.mode }}</span>
                                                </td>       
                                            </tr>

                                        </tbody>
                                    </table>
                                </div>


                            </td>

                            <td width="2%"></td>


                            <td>
                                <div class="widget" style="margin-left: 0px; padding: 0px;">

                                    <div class="title">UCS Statistics</div>                       

                                    <div class="chart">

                                        <span id="powerGaugeContainer"></span>
                                        <span id="memoryGaugeContainer"></span>
                                        <span id="cpuGaugeContainer"></span>
                                        <span id="networkGaugeContainer"></span>                                       

                                    </div>

                                    <!-- <div class="chart">
                                       <canvas id="myChart" width="400" height="200"></canvas>
                                   </div> -->


                                   <ul class="list list-group">                            

                                    <li class=" list-group-item text-success">General information</li>
                                    <li class=" list-group-item">Number of faults per type</li>
                                    <li class=" list-group-item">Power consumption</li>
                                    <li class=" list-group-item">Num of blades</li>
                                    <li class=" list-group-item" >Num of Chassis</li>
                                    <li class=" list-group-item">Availabity</li>
                                    <li class=" list-group-item">Network ports</li>
                                    <li class=" list-group-item">Packets</li>
                                    <li class=" list-group-item">Service Profiles</li>
                                </ul>                           

                                <ul class="list list-group">                            

                                    <li class=" list-group-item text-success">General information</li>
                                    <li class=" list-group-item">Number of faults per type</li>
                                    <li class=" list-group-item">Power consumption</li>
                                    <li class=" list-group-item">Num of blades</li>
                                    <li class=" list-group-item" >Num of Chassis</li>
                                    <li class=" list-group-item">Availabity</li>
                                    <li class=" list-group-item">Network ports</li>
                                    <li class=" list-group-item">Packets</li>
                                    <li class=" list-group-item">Service Profiles</li>
                                </ul> 

                                <ul class="list list-group">                            

                                    <li class=" list-group-item text-success">General information</li>
                                    <li class=" list-group-item">Number of faults per type</li>
                                    <li class=" list-group-item">Power consumption</li>
                                    <li class=" list-group-item">Num of blades</li>
                                    <li class=" list-group-item" >Num of Chassis</li>
                                    <li class=" list-group-item">Availabity</li>
                                    <li class=" list-group-item">Network ports</li>
                                    <li class=" list-group-item">Packets</li>
                                    <li class=" list-group-item">Service Profiles</li>
                                </ul>


                                <ul class="list list-group">                            

                                    <li class=" list-group-item text-success">General information</li>
                                    <li class=" list-group-item">Number of faults per type</li>
                                    <li class=" list-group-item">Power consumption</li>
                                    <li class=" list-group-item">Num of blades</li>
                                    <li class=" list-group-item" >Num of Chassis</li>
                                    <li class=" list-group-item">Availabity</li>
                                    <li class=" list-group-item">Network ports</li>
                                    <li class=" list-group-item">Packets</li>
                                    <li class=" list-group-item">Service Profiles</li>
                                </ul>



                                <ul class="list list-group">                            

                                    <li class=" list-group-item text-success">General information</li>
                                    <li class=" list-group-item">Number of faults per type</li>
                                    <li class=" list-group-item">Power consumption</li>
                                    <li class=" list-group-item">Num of blades</li>
                                    <li class=" list-group-item" >Num of Chassis</li>
                                    <li class=" list-group-item">Availabity</li>
                                    <li class=" list-group-item">Network ports</li>
                                    <li class=" list-group-item">Packets</li>
                                    <li class=" list-group-item">Service Profiles</li>
                                </ul>


                                <ul class="list list-group">                            

                                    <li class=" list-group-item text-success">General information</li>
                                    <li class=" list-group-item">Number of faults per type</li>
                                    <li class=" list-group-item">Power consumption</li>
                                    <li class=" list-group-item">Num of blades</li>
                                    <li class=" list-group-item" >Num of Chassis</li>
                                    <li class=" list-group-item">Availabity</li>
                                    <li class=" list-group-item">Network ports</li>
                                    <li class=" list-group-item">Packets</li>
                                    <li class=" list-group-item">Service Profiles</li>
                                </ul>

                            </div>

                        </td>

                    </tr>

                </tbody>
            </table>                


                    <!-- <span id="memoryGaugeContainer"></span>
                    <span id="cpuGaugeContainer"></span>
                    <span id="networkGaugeContainer"></span>
                    <span id="testGaugeContainer"></span>

                    <line-chart :chart-data="datacollection"
                    :width="150"
                    :height="150"></line-chart>

                    <button @click="fillData()">Randomize</button> -->

                </div>
                <!-- / OVERVIEW -->

                <!-- CHASSIS VIEW -->
                <div class="tab-pane"
                id="chassis_tab">

                <h3>Chassis list </h3>

                <!-- LEFT SIDE STATISTICS -->
                <div class="title">STATISTICS</div>

                <div class="chart">

                    <span id="powerGaugeContainer"></span>

                    <canvas id="myChart"
                    width="400"
                    height="200"></canvas>

                </div>
                <!-- / LEFT SIDE STATISTICS -->

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


                <p>-----------------------------------</p>
                <ul class="list-group">
                    <li class="list-group-item-heading">To Add</li>

                    <li>Power Consumption</li>
                    <li>InputCurrent</li>
                    <li>Power voltage</li>
                    <li></li>
                </ul>

            </div>
            <!-- / CHASSIS VIEW -->

            <!-- CHASSIS SERVERS VIEW -->
            <div class="tab-pane"
            id="chassis_servers">
            <h3>Chassis Servers coming here</h3>

            <div id="ChassisServers">

                <v-client-table :data="blades"
                :columns="chassisServerColumns"
                :options="chassisServerOptions">
                <template slot="stats"
                scope="props">
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

    </div>
    <!-- /CHASSIS SERVERS VIEW -->

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

<div class="tab-pane" id="rackmounts">

    <h3>RackMounts coming here</h3>

</div>


<div class="tab-pane" id="4b">

    <h3>Fabric Interconnect list and details</h3>
</div>

</div>
</div>
</div>

</div>

<!-- Create Client Modal -->
<div class="modal fade" id="modal-create-company" tabindex="-1" role="dialog">

    <div class="modal-dialog">

        <div class="modal-content">

            <div class="modal-header">
                <button type="button " class="close" data-dismiss="modal" aria-hidden="true">&times;</button>

                <h4 class="modal-title"> Bedrijf toevoegen</h4>
            </div>

            <div class="modal-body">

                <h3>body</h3>

            </div>

            <!-- Modal Actions -->
            <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>

                <button type="button" class="btn btn-primary" @click="storeCompany"> Opslaan </button>
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


    #exTab3 .nav-pills > li > a {
        border-radius: 4px 4px 0 0 ;
    }

    #exTab3 .tab-content {
        color : #3a3a3a;
        background-color: #f0f5fb;
        padding : 5px 15px;
    }

    .nav-pills>li.active>a, 
    .nav-pills>li.active>a:focus, 
    .nav-pills>li.active>a:hover {

        color: #3a3a3a;
        background-color: #f0f5fb;
        
    }

    .VueTables__table tr {
        font-size: 10px !important;
    }

    .icon-small {
        font-size: 15px;
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