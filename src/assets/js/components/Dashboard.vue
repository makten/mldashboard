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

            datacollection: null,

            chassis: [],

            blades: [],
            faults: [],

            savedSearches: '',

            tableData: {},
            features: [],
            coltypes: [],
            modifiedFeatures: [],
            rowCount: 0,
            syncedVal: '',
            chartLine: null,


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

            this.fillData();
            this.getBlades();
            this.getChassis();
            this.getBladeFaults();
            var ctx = $("#myChart");

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
            axios.get('/api/get_chassis')
                .then(response => {
                    console.log(JSON.parse(response.data))
                    this.chassis = []
                    this.chassis = JSON.parse(response.data)
                })
                .catch(errors => { })
        },

        getBlades() {
            axios.get('/api/get_blades')
                .then(response => {
                    this.blades = []
                    this.blades = JSON.parse(response.data)

                    console.log(this.blades)
                })
                .catch(errors => { })
        },

        getBladeFaults() {
            let chs = 'chassis-3'
            let bld = 'blade-1'
            axios.get(`/api/get_bladefaults/${chs}/${bld}`)
                .then(response => {
                    this.faults = []
                    this.faults = JSON.parse(response.data)
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
            var config =
                {
                    size: 150,
                    label: label,
                    min: undefined != min ? min : 0,
                    max: undefined != max ? max : 100,
                    minorTicks: 5
                }

            var range = config.max - config.min;
            config.yellowZones = [{ from: config.min + range * 0.75, to: config.min + range * 0.9 }];
            config.redZones = [{ from: config.min + range * 0.9, to: config.max }];

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
                var value = this.getRandomValue(this.gauges[key])
                this.gauges[key].redraw(value);
            }
        },

        getRandomValue(gauge) {
            var overflow = 0; //10;
            return gauge.config.min - overflow + (gauge.config.max - gauge.config.min + overflow * 2) * Math.random();
        },

        initialize() {
            this.createGauges();
            setInterval(this.updateGauges, 5000);
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
    
            <div class="title">Chassis List</div>
    
            <div class="chart">
    
                {{blades[0]}} <p>------------------</p> 
                      
    
                <span id="memoryGaugeContainer"></span>
                <span id="cpuGaugeContainer"></span>
                <span id="networkGaugeContainer"></span>
                <span id="testGaugeContainer"></span>
    
                <line-chart :chart-data="datacollection"
                            :width="250"
                            :height="150"></line-chart>
    
                <button @click="fillData()">Randomize</button>
    
                <table class="table table-striped table-bordered">
    
                    <thead>
    
                        <tr>
    
                            <th width="15%"> Id </th>
    
                            <th width="15%"> Dn </th>
    
                            <th width="15%"> Part # </th>
    
                            <th width="15%"> Operability </th>
    
                            <th width="15%"> Serial </th>
    
                        </tr>
    
                    </thead>
    
                    <tbody>
    
                        <tr v-for="chass in chassis">
    
                            <td>
    
                                <a href="#">
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    {{ chass.id}}
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    </a>
    
                            </td>
    
                            <td>
    
                                <a href="#">
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    {{ chass.dn}}
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                
                                                                                                    
                                                
                                                        
                                                
                                                            
                                                
                                                        
                                                </a>
    
                            </td>
    
                            <td>
    
                                {{ chass.part_number }}
    
                            </td>
    
                            <td>
    
                                {{ chass.operability }}
    
                            </td>
    
                            <td>
    
                                {{ chass.serial }}
    
                            </td>
    
                        </tr>
    
                    </tbody>
    
                </table>
    
            </div>
    
        </div>
    
        <div class="widget">
    
            <div class="title">Chassis List</div>
    
            <div class="chart"
                 style="background: #004080;">
    
                <bar :data="barData"
                     :options="{responsive: false, maintainAspectRatio: false}"
                     :width="400"
                     :height="200">
    
                </bar>
    
            </div>
    
            <div class="chart">
    
                <bar :data="barData2"
                     :options="{responsive: false, maintainAspectRatio: false}"
                     :width="400"
                     :height="200">
    
                </bar>
    
            </div>
    
        </div>
    
        <div class="widget"
             v-if="blades">
    
            <div class="title">Blade List</div>
    
            <div class="chart">
    
                <canvas id="myChart"
                        width="400"
                        height="200"></canvas>
    
                <table class="table table-striped table-bordered">
    
                    <thead>
    
                        <tr>
    
                            <th width="15%"> Dn </th>
    
                            <th width="15%"> Serial </th>
    
                            <th width="15%"> Operability </th>
    
                            <th width="15%"> Model </th>
    
                        </tr>
    
                    </thead>
    
                    <tbody>
    
                        <tr v-for="blade in blades">
    
                            <td>
    
                                <a href="#">
    
                                    <i class="fa fa-pencil"></i> {{ blade.dn}}
    
                                </a>
    
                            </td>
    
                            <td>
    
                                {{ blade.serial}}
    
                            </td>
    
                            <td>
    
                                {{ blade.operability }}
    
                            </td>
    
                            <td>
    
                                {{ blade.model }}
    
                            </td>
    
                        </tr>
    
                    </tbody>
    
                </table>
    
                <ul class="list-group"
                    v-for="fault in faults">
    
                    <li class="list-group-item">{{fault.code}}</li>
    
                    <li class="list-group-item">{{fault.cause}}</li>
    
                    <li class="list-group-item">{{fault.created}}</li>
    
                    <li class="list-group-item">{{fault.desc}}</li>
    
                    <li class="list-group-item">{{fault.severity}}</li>
    
                    <li class="list-group-item">{{fault.rule}}</li>
    
                    <li class="list-group-item">{{fault.status}}</li>
    
                    <li class="list-group-item">{{fault.type}}</li>
    
                </ul>
    
            </div>
    
        </div>
    
    </div>
</template>

<style lang="sass">

.small {
max-width: 150;
margin:  150px auto;
}
</style>