module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    compress: {
      main: {
        options: {
          mode: 'gzip'
        },
        files: [
          {
            expand: true,
            src: ['static/app.min.js'],
            dest: '',
            ext: '.min.zipped.js'
          },
          {
            expand: true,
            src: ['static/design.min.css'],
            dest: '',
            ext: '.min.zipped.css'
          }
        ]
      }
    },
    concat: {
      css: {
        src: ['css/*.css'],
        dest: 'static/design.css'
      },
      js: {
        src: ['js/core/*.js', 'js/modules/*.js', 'js/init.js'],
        dest: 'static/app.js'
      }
    },
    csslint: {
      strict: {
        options: {
          'universal-selector': false,
          'box-sizing': false,
          'box-model': false,
          'unqualified-attributes': false
        },
        src: ['css/design.css']
      }
    },
    jasmine: {
      pivotal: {
        src: ['js/*/*.js'],
        options: {
          specs: 'spec/*Spec.js',
          helpers: 'spec/*Helper.js'
        }
      }
    },
    jslint: {
      client: {
        src: [
          'js/*/*.js',
          'js/*.js'
        ],
        exclude: []
      }
    },
    postcss: {
      options: {
        processors: [
          require('autoprefixer')({ browsers: 'last 2 versions' }),
          require('cssnano')()
        ]
      },
      css: {
        src: 'static/*.css'
      }
    },
    uglify: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
      },
      build: {
        src: 'static/app.js',
        dest: 'static/app.min.js'
      }
    },
    watch: {
      css: {
        files: "css/*.css",
        tasks: ["concat:css", 'postcss']
      },
      js: {
        files: ["js/*.js", "js/**/*.js"],
        tasks: ["concat:js", 'uglify']
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-compress');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-csslint');
  grunt.loadNpmTasks('grunt-contrib-jasmine');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-jslint');
  grunt.loadNpmTasks('grunt-postcss');

  grunt.registerTask('build', ['concat', 'uglify', 'postcss', 'compress']);
  grunt.registerTask('test', ['csslint', 'jslint', 'jasmine']);
  grunt.registerTask('default', ['test']);
};
