module.exports = function (grunt) {
    grunt.initConfig({
        less: {
            production: {
                options: {
                    paths: ['css'],
                },
                files: {
                    '../../dist/styles/style.css': 'css/style.less'
                }
            }
        },
        cssmin: {
            options: {
                mergeIntoShorthands: false,
                roundingPrecision: -1
            },
            target: {
                files: {
                    '../../dist/styles/style.min.css': ['../../dist/styles/style.css']
                }
            }
        },
        clean: ['../../dist/styles/style.css'],
        watch: {
            options: {
                livereload: true,
            },
            css: {
                files: ['css/*.less'],
                tasks: ['less', 'cssmin', 'clean'],
            },
        },
    });

    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-watch');
};