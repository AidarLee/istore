const gulp = require('gulp');
const axios = require("axios");

function defaultTask(cb) {
  // place code for your default task here
  cb();
}


var paths = {
        refresh: [
            "./layouts/**/*.*",
            "./views/**/*.*",
            "./includes/**/*.js",
            "./includes/**/*.css"
        ],
        reinit: [
            "./handlers/**/*.*",
            "./models/**/*.*",
            "./interceptors/**/*.*",
            "./config/**/*.*"
        ]
    }

gulp.task('watch', () => {
    gulp.watch(paths.refresh, (done) => {
        reload();
        done();
    });
    gulp.watch(paths.reinit, (done) => {
        console.log("Reinitializing framework");
        axios.get(url)
        .then(response => {
            console.log(response.data.trim());
            reload();
            done();
        })
        .catch(error => {
            console.log("Error:  Please ensure you have a /healthcheck route set up in /config/router.cfc!");
            console.log("Error:  Once you've done that, please shut down commandbox then try browsersync again.");
        });
    });
});

gulp.task('proxy', () => {
    bs.init({
        proxy: "localhost:80",
        port: 81,
        open: true,
        notify: false
    });
});

gulp.task('default', gulp.parallel('watch', 'proxy'));
