module.exports = function(grunt){
    
    grunt.initConfig({
        
        pkg: grunt.file.readJSON('package.json'),
        
        files: {
            css : {
                src : [
                    'static/css/src/config.css',
                    'static/css/src/reset.css', 
                    'static/css/src/typography.css', 
                    'static/css/src/utils+grid.css', 
                    'static/css/src/forms.css', 
                    'static/css/src/components.css', 
                    'static/css/src/layout+skin.css'
                ],
                output : [
                    'static/css/output/reset.css', 
                    'static/css/output/typography.css', 
                    'static/css/output/utils+grid.css', 
                    'static/css/output/forms.css', 
                    'static/css/output/components.css', 
                    'static/css/output/layout+skin.css'
                ],
            },
            html : [
                'templates/*.html',
                'templates/*/*/*.html',
                'templates/*/*.html'
            ]
        },

        // autoprefixer: {
        //     all_css: {
        //         browser : 'last 3 version',
        //         cascade : true,
        //         expand: true,
        //         flatten: true,
        //         src  : '<%= files.css.src %>',
        //         dest : 'css/output/'
        //     }
        // },
        
        cssmin: 
        {
            combine: 
            {
                files: {
                    'static/css/<%= pkg.name %>.min.css' : '<%= files.css.output %>'
                }
            },
            vars:
            {
                files: {
                    'static/css/src/config.min.css' : 'static/css/src/config.css'
                }
            }
        },

        cssnext: {
            options: {
                sourcemap: true,
                features: {
                    calc: {
                        preserve: false,
                        // precision: 3
                    },
                    autoprefixer: {
                        browsers: ['last 3 versions', 'Firefox ESR']
                    }    
                }
            },
            dist: {
                files: [{
                    expand: true,
                    flatten: true,
                    src  : '<%= files.css.src %>',
                    dest : 'static/css/output/'
                }]
            }
        },

        svgmin:
        {
            img:
            {
                files: [{
                    expand: true,
                    cwd: 'static/img/',
                    src: '*.svg',
                    dest: 'static/img/'

                }]
            },
            icons:
            {
                files: [{
                    expand: true,
                    cwd: 'static/img/icons/',
                    src: '*.svg',
                    dest: 'static/img/icons/'
                }]
            }
        },
        
        watch: {
            options: {
                livereload: true,
            },              
            css : {
                files: '<%= files.css.src %>',
                tasks : ['buildcss']
            },
            html : {
                files : '<%= files.html %>'
            }
        },
      
    });
    
    // Load plugins
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-svgmin');
    grunt.loadNpmTasks('grunt-cssnext');


    
    // Run plugins
    grunt.registerTask('default', ['cssmin:vars','cssnext']);
    grunt.registerTask('buildcss', ['cssmin:vars','cssnext', 'cssmin:combine']);


};