var gulp = require('gulp');
var babel = require('gulp-babel');
var sourcemaps = require('gulp-sourcemaps');
var uglify = require('gulp-uglify');
var concat = require('gulp-concat')
var fs = require("fs")
var browserify = require("browserify")
var vueify = require('vueify')

// watchify -t vueify -e src/js/main.js -o ./app/static/js/main.js -v -- How I Run this


// gulp.task('build', function() {

// 	browserify('./src/js/main.js')
// 	.transform(vueify)
// 	.bundle()
// 	.pipe(fs.createWriteStream("static/js/main.js"))
//     // return gulp.src('src/js/*.js')
//     //     .pipe(babel({ presets: ['es2015'] }))
//     //     .pipe(sourcemaps.init({ loadMaps: true }))		
//     //     .pipe(uglify())
//     //     .pipe(sourcemaps.write())
//     //     .pipe(gulp.dest('static/js'));
// });


// gulp.task('build', function() {

	browserify('./src/assets/js/app.js')
	.transform(vueify)
	.transform("babelify", {presets: ["es2015"]})
	.bundle()		
	.pipe(fs.createWriteStream("./app/static/js/app.js"))
    // return gulp.src('src/js/*.js')
    //     .pipe(babel({ presets: ['es2015'] }))
    //     .pipe(sourcemaps.init({ loadMaps: true }))		
    //     .pipe(uglify())
    //     .pipe(sourcemaps.write())
    //     .pipe(gulp.dest('static/js'));
// });

// gulp.task('watch', function() {
//     gulp.watch('src/assets/js/*.js', ['build']);
// });

// gulp.task('default', ['build']);
