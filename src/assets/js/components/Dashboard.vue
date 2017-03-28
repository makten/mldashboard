<script>
    import vSelect from 'vue-select'

    export default {

        components: {
            vSelect
        },

        data() {

            return {

                blades: [],

                savedSearches: '',

                tableData: {},
                features: [],
                coltypes: [],
                modifiedFeatures: [],
                rowCount: 0,
                syncedVal: '',
                chartLine: null,

                deliveries: [{
                    name: "Normal Levering",
                    value: 0
                }, {
                    name: "Next-day",
                    value: 1
                }, {
                    name: "Express Levering",
                    value: 2
                }],

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

                forecasted: [{
                    y: 12,
                    x: '2017-01-02T00:00:00'
                }, {
                    y: 3,
                    x: '2017-01-03T00:00:00'
                }, {
                    y: 2,
                    x: '2017-01-04T00:00:00'
                }, {
                    y: 18,
                    x: '2017-01-05T00:00:00'
                }, {
                    y: 19,
                    x: '2017-01-06T00:00:00'
                }, {
                    y: 13,
                    x: '2017-01-07T00:00:00'
                }, {
                    y: 5,
                    x: '2017-01-08T00:00:00'
                }, {
                    y: 23,
                    x: '2017-01-09T00:00:00'
                }, {
                    y: 51,
                    x: '2017-01-10T00:00:00'
                }, {
                    y: 5,
                    x: '2017-01-11T00:00:00'
                }, {
                    y: 6,
                    x: '2017-01-12T00:00:00'
                }, {
                    y: 2,
                    x: '2017-01-13T00:00:00'
                }, {
                    y: 12,
                    x: '2017-01-14T00:00:00'
                }, {
                    y: 3,
                    x: '2017-01-15T00:00:00'
                }, {
                    y: -24,
                    x: '2017-01-16T00:00:00'
                }, {
                    y: 10,
                    x: '2017-01-17T00:00:00'
                }, {
                    y: 9,
                    x: '2017-01-18T00:00:00'
                }, {
                    y: 11,
                    x: '2017-01-19T00:00:00'
                }, {
                    y: 12,
                    x: '2017-01-20T00:00:00'
                }, {
                    y: 2,
                    x: '2017-01-21T00:00:00'
                }, {
                    y: 16,
                    x: '2017-01-22T00:00:00'
                }, {
                    y: 12,
                    x: '2017-01-23T00:00:00'
                }, {
                    y: 3,
                    x: '2017-01-24T00:00:00'
                }, {
                    y: 12,
                    x: '2017-01-25T00:00:00'
                }, {
                    y: 7,
                    x: '2017-01-26T00:00:00'
                }, {
                    y: 12,
                    x: '2017-01-27T00:00:00'
                }, {
                    y: 7,
                    x: '2017-01-28T00:00:00'
                }, {
                    y: 9,
                    x: '2017-01-29T00:00:00'
                }, {
                    y: 1,
                    x: '2017-01-30T00:00:00'
                }, {
                    y: 10,
                    x: '2017-01-31T00:00:00'
                }, {
                    y: 7,
                    x: '2017-02-01T00:00:00'
                }],

                dataActual: [{
                    y: 5,
                    x: '2017-01-02T00:00:00'
                }, {
                    y: 3,
                    x: '2017-01-03T00:00:00'
                }, {
                    y: 2,
                    x: '2017-01-04T00:00:00'
                }, {
                    y: 18,
                    x: '2017-01-05T00:00:00'
                }, {
                    y: 5,
                    x: '2017-01-06T00:00:00'
                }, {
                    y: 30,
                    x: '2017-01-07T00:00:00'
                }, {
                    y: 5,
                    x: '2017-01-08T00:00:00'
                }, {
                    y: 23,
                    x: '2017-01-09T00:00:00'
                }, {
                    y: 18,
                    x: '2017-01-10T00:00:00'
                }, {
                    y: 5,
                    x: '2017-01-11T00:00:00'
                }, {
                    y: 6,
                    x: '2017-01-12T00:00:00'
                }, {
                    y: 2,
                    x: '2017-01-13T00:00:00'
                }, {
                    y: -12,
                    x: '2017-01-14T00:00:00'
                }, {
                    y: 3,
                    x: '2017-01-15T00:00:00'
                }, {
                    y: 24,
                    x: '2017-01-16T00:00:00'
                }, {
                    y: 5,
                    x: '2017-01-17T00:00:00'
                }, {
                    y: 9,
                    x: '2017-01-18T00:00:00'
                }, {
                    y: 6,
                    x: '2017-01-19T00:00:00'
                }, {
                    y: 12,
                    x: '2017-01-20T00:00:00'
                }, {
                    y: 2,
                    x: '2017-01-21T00:00:00'
                }, {
                    y: 16,
                    x: '2017-01-22T00:00:00'
                }, {
                    y: 24,
                    x: '2017-01-23T00:00:00'
                }, {
                    y: 3,
                    x: '2017-01-24T00:00:00'
                }, {
                    y: 12,
                    x: '2017-01-25T00:00:00'
                }, {
                    y: 7,
                    x: '2017-01-26T00:00:00'
                }, {
                    y: -10,
                    x: '2017-01-27T00:00:00'
                }, {
                    y: 7,
                    x: '2017-01-28T00:00:00'
                }, {
                    y: 12,
                    x: '2017-01-29T00:00:00'
                }, {
                    y: 1,
                    x: '2017-01-30T00:00:00'
                }, {
                    y: 10,
                    x: '2017-01-31T00:00:00'
                }, {
                    y: 7,
                    x: '2017-02-01T00:00:00'
                }],

                predictdedForecast: [{
                    y: 5,
                    x: '2017-01-02T00:00:00'
                }, {
                    y: 6,
                    x: '2017-01-03T00:00:00'
                }, {
                    y: 2,
                    x: '2017-01-04T00:00:00'
                }, {
                    y: 9,
                    x: '2017-01-05T00:00:00'
                }, {
                    y: 19,
                    x: '2017-01-06T00:00:00'
                }, {
                    y: 50,
                    x: '2017-01-07T00:00:00'
                }, {
                    y: 5,
                    x: '2017-01-08T00:00:00'
                }, {
                    y: 10,
                    x: '2017-01-09T00:00:00'
                }, {
                    y: 18,
                    x: '2017-01-10T00:00:00'
                }, {
                    y: 5,
                    x: '2017-01-11T00:00:00'
                }, {
                    y: 6,
                    x: '2017-01-12T00:00:00'
                }, {
                    y: 2,
                    x: '2017-01-13T00:00:00'
                }, {
                    y: 43,
                    x: '2017-01-14T00:00:00'
                }, {
                    y: 3,
                    x: '2017-01-15T00:00:00'
                }, {
                    y: 24,
                    x: '2017-01-16T00:00:00'
                }, {
                    y: 2,
                    x: '2017-01-17T00:00:00'
                }, {
                    y: 9,
                    x: '2017-01-18T00:00:00'
                }, {
                    y: 11,
                    x: '2017-01-19T00:00:00'
                }, {
                    y: 10,
                    x: '2017-01-20T00:00:00'
                }, {
                    y: 2,
                    x: '2017-01-21T00:00:00'
                }, {
                    y: 2,
                    x: '2017-01-22T00:00:00'
                }, {
                    y: 24,
                    x: '2017-01-23T00:00:00'
                }, {
                    y: 3,
                    x: '2017-01-24T00:00:00'
                }, {
                    y: 13,
                    x: '2017-01-25T00:00:00'
                }, {
                    y: 7,
                    x: '2017-01-26T00:00:00'
                }, {
                    y: 10,
                    x: '2017-01-27T00:00:00'
                }, {
                    y: 7,
                    x: '2017-01-28T00:00:00'
                }, {
                    y: 6,
                    x: '2017-01-29T00:00:00'
                }, {
                    y: 1,
                    x: '2017-01-30T00:00:00'
                }, {
                    y: 9,
                    x: '2017-01-31T00:00:00'
                }, {
                    y: 10,
                    x: '2017-02-01T00:00:00'
                }],
                opt: {
                    scales: {
                        xAxes: [{
                            type: 'time',
                            position: 'bottom'
                        }]
                    }
                }

            }
        },

        mounted() {

            this.$nextTick(function() {

                this.getBlades();

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

            plotChart(ctx) {

                this.forecasted = _.drop(this.forecasted, 1)
                this.dataActual = _.drop(this.dataActual, 1)
                this.predictdedForecast = _.drop(this.predictdedForecast, 1)

                let chartLine = new Chartjs(ctx, {
                    type: 'line',
                    data: {
                        datasets: [{
                            label: "Forecasted",
                            fillColor: "rgba(220,220,220,0.5)",
                            strokeColor: "rgba(220,220,220,0.8)",
                            highlightFill: "rgba(220,220,220,0.75)",
                            highlightStroke: "rgba(220,220,220,1)",
                            borderColor: "#43ABFB",

                            data: this.forecasted
                        }, {
                            label: "Actual",
                            fillColor: "rgba(220,220,220,0.5)",
                            strokeColor: "rgba(220,220,220,0.8)",
                            highlightFill: "rgba(220,220,220,0.75)",
                            highlightStroke: "rgba(220,220,220,1)",
                            borderColor: "#14B214",
                            data: this.dataActual
                        }, {
                            label: "Baseline",
                            fillColor: "rgba(151,187,205,0.5)",
                            strokeColor: "rgba(151,187,205,0.8)",
                            highlightFill: "rgba(151,187,205,0.75)",
                            highlightStroke: "rgba(151,187,205,1)",
                            // backgroundColor: "red",
                            borderColor: "#FF3535",
                            data: this.predictdedForecast
                        }],

                    },
                    options: this.opt

                });

            },

            createFeatures(val) {
                this.modifiedFeatures = _.reject(this.features, function(f) {
                    return f == val
                })
                this.form.features = _.reject(this.form.features, function(f) {
                    return f == val
                })
            },

            createFeatureTypes() {

                for (let i = 0; i < this.features.length; i++) {
                    let x = this.tableData[i][i]
                    console.log(x)
                    this.coltypes.push({
                        'feature': this.features[i],
                        'type': x
                    })
                }

            },


            getBlades() {
                axios.get('/api/get_blades')
                    .then(response => {

                        this.blades = []
                        this.blades = JSON.parse(response.data)

                    })
                    .catch(errors => {})
            },

            getSavedSearches() {

                axios.post('api/getSavedSearches')
                    .then(response => {

                        this.savedSearches = response.data
                        console.log(response.data)

                        //this.onSuccess(response);

                    })
                    .catch(errors => {})
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



                // let fd = new FormData($('#photo')[0])				

                // this.$http.post('api/sendForm', fd)
                // .then(response => {
                // 	console.log(response.data.result)
                // 	this.api_response = response.data.result					
                // })

                // var files = e.target.files || e.dataTransfer.files;
                // if (!files.length)
                // 	return;
                // this.createImage(files[0]);


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

                    complete: function(results) {
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

            removeImage: function(e) {
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

        },

        beforeDestroy: function() {
            clearInterval(this.interval);
        }


    }
</script>


<template>


    <div class="main">
        {{ blades[0] }}

        <div class="container-fluid">
            <div class="row">

                <div class="col-md-4">
                    <div class="widget">

                        <div class="title">Campaign Prediction</div>

                        <div class="chart">

                            <div id="csvtable"></div>


                            <form class="bs-customizer" role="form" method="POST" @submit.prevent="onSubmit" @keydown="form.errors.clear($event.target.name)">

                                <fieldset>
                                    <div class="row">


                                        <div class="col-md-6">
                                            <span class="label-success">{{ rowCount }}</span>


                                            <div class="form-group">
                                                <label for="uploadCsv" class="col-md-2 control-label">File</label>

                                                <div class="col-md-10">
                                                    <input type="text" readonly="" class="form-control" placeholder="Browse...">
                                                    <input type="file" id="uploadCsv" multiple="False" @change="onFileChange">
                                                </div>
                                            </div>
                                        </div>


                                    </div>

                                    <div class="row">


                                        <div class="col-md-4">

                                            <div class="form-group">
                                                <label for="search" class="col-md-12 control-label">Target</label>

                                                <v-select :on-change="createFeatures" v-model="form.target" :options="features"></v-select>


                                                <span class="help is-danger" v-if="form.errors.has('search')" v-text="form.errors.get('search')"></span>

                                            </div>

                                        </div>


                                        <div class="col-md-6">
                                            <div class="form-group" v-if='modifiedFeatures.length > 0'>
                                                <label for="search" class="col-md-12 control-label">Saved Searches</label>

                                                <v-select multiple v-model="form.features" :options="modifiedFeatures" transition='expand'></v-select>

                                                <span class="help is-danger" v-if="form.errors.has('search')" v-text="form.errors.get('search')"></span>

                                            </div>
                                        </div>


                                    </div>


                                    <div class="form-group">
                                        <table class="table table-bordered table-hover">
                                            <tr>
                                                <th v-for="head in coltypes">
                                                    {{ head.feature }} {{ typeof head.type}}
                                                </th>
                                            </tr>

                                        </table>
                                    </div>

                                    <div class="form-group">

                                        {{tableData }}
                                        <div class="col-md-8 col-md-offset-4">
                                            <button type="button" class="btn btn-default btn-xs">Reset</button>
                                            <button type="submit" class="btn btn-primary btn-xs">Predict</button>
                                        </div>
                                    </div>

                                </fieldset>
                            </form>

                        </div>

                    </div>
                </div>
            
            
                <div class="col-md-4">
                    <div class="widget">
                        <div class="title">Departments Table</div>

                        <div class="chart">

                            <canvas id="myChart" width="400" height="200"></canvas>


                            <table class="table table-striped table-bordered">
                                <thead>
                                    <tr>
                                        <th width="15%"> Name </th>
                                        <th width="40%"> Description </th>
                                        <th width="15%"> Employee Count </th>
                                        <th width="15%"> Edit </th>
                                        <th width="15%"> Delete </th>
                                    </tr>
                                </thead>
                                <tbody>

                                    <tr v-for="blade in blades">
                                        <td>
                                            {{ blade.name}}
                                        </td>

                                        <td>
                                            {{ blade.rn}}
                                        </td>

                                        <td>
                                            {{ blade.name}}
                                        </td>

                                        <td>
                                            {{ blade.dn }}
                                        </td>

                                        <td>
                                            <a href="#">
                                                <i class="fa fa-pencil"></i> Edit
                                            </a>
                                        </td>

                                        <td>
                                            <a href="#">
                                                <i class="fa fa-trash"></i> Delete
                                            </a>
                                        </td>
                                    </tr>

                                </tbody>
                            </table>

                        </div>
                    </div>
                </div>
            </div>
        
            <div class="widget">
                <div class="title">Departments Table</div>
                

                <div class="chart">

                    <canvas id="myChart" width="400" height="200"></canvas>


                    <table class="table table-striped table-bordered">
                        <thead>
                            <tr>
                                <th width="15%"> Dn </th>
                                <th width="40%"> Serial </th>                                
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

                </div>
            </div>

        </div>


    </div>


</template>

<style>

</style>