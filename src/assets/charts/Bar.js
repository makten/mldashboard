import { Bar } from 'vue-chartjs'

export default Bar.extend({
    props: ['data', 'options'],
    mounted() {
        // Overwriting base render method with actual data.
        this.renderChart(this.data, this.options)
    }
})

// , Bubble, Doughnut, HorizontalBar, Line, Pie, PolarArea, Radar