let webpack = require('webpack')


let path = require('path')

module.exports = {

	performance: { hints: false },


	entry: { 


		app: './src/assets/js/app.js',

		vendor: ['vue', 'axios', 'vue-resource', 'jquery', 'lodash']

	},


	output: {

		path: path.resolve(__dirname, './static/js'),

		filename: '[name].js',

		publicPath: './static'
	},


	module: {

		rules: [

		{
			test: /\.js$/,

			exclude: /node_modules/,

			loader: 'babel-loader'
		},

		{
			test: /\.vue$/,

			loader: 'vue-loader',

			options: {

			}
		},

		{
			test: /\.s[a|c]ss$/,			
			loader: ['sass-loader', 'style', 'css', 'sass']
		}

		]
	},


	resolve: {

		alias: {

			"vue": "vue/dist/vue.common"
		}

	},


	plugins: [

	new webpack.optimize.CommonsChunkPlugin({

		names: ['vendor']
	})	

	]


}


if (process.env.NODE_ENV === 'production') {

	new webpack.optimize.UglifyJsPlugin({

		sourcemap: true,

		compress: {

			warning: false
		}
	});


	module.exports.plugins.push(

		new webpack.DefinePlugin({

			'process.env': {

				NODE_ENV: 'production'
			}
		})
		);
}

// set NODE_ENV=production -- example


