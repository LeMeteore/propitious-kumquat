module.exports = function(grunt){
    
    grunt.initConfig({
        
        pkg: grunt.file.readJSON('package.json'),
        
        files: {
            css : {
                admin : {
                    src : [
                        'static/css/src/config.css',
                        'static/css/src/wappa-icons.css',
                        'static/css/src/reset.css', 
                        'static/css/src/typography.css', 
                        'static/css/src/utils+grid.css', 
                        'static/css/src/forms.css', 
                        'static/css/src/components.css', 
                        'static/admin/css/src/adminlayout+skin.css'
                    ],
                    output : [
                        'static/css/output/wappa-icons.css',
                        'static/css/output/reset.css', 
                        'static/css/output/typography.css', 
                        'static/css/output/utils+grid.css', 
                        'static/css/output/forms.css', 
                        'static/css/output/components.css', 
                        'static/admin/css/output/adminlayout+skin.css'
                    ],  
                },
                front : {
                    src : [
                        'static/css/src/config.css',
                        'static/css/src/wappa-icons.css',
                        'static/css/src/reset.css', 
                        'static/css/src/typography.css', 
                        'static/css/src/utils+grid.css', 
                        'static/css/src/forms.css', 
                        'static/css/src/components.css', 
                        'static/css/src/layout+skin.css'
                    ],
                    output : [
                        'static/css/output/reset.css', 
                        'static/css/output/wappa-icons.css',
                        'static/css/output/typography.css', 
                        'static/css/output/utils+grid.css', 
                        'static/css/output/forms.css', 
                        'static/css/output/components.css', 
                        'static/css/output/layout+skin.css'
                    ],  
                }
            },
            html : [
                'templates/*.html',
                'templates/*/*/*.html',
                'templates/*/*.html'
            ]
        },
        
        cssmin: 
        {
            admin: 
            {
                files: {
                    'static/admin/css/admin<%= pkg.name %>.min.css' : '<%= files.css.admin.output %>'
                }
            },
            front :
            {
                files: {
                    'static/css/<%= pkg.name %>.min.css' : '<%= files.css.front.output %>'                    
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
                    src  : 'static/css/src/*.css',
                    dest : 'static/css/output/'
                }]
            },
            admin : {
                files : [{
                    expand: true,
                    flatten: true,
                    src  : 'static/admin/css/src/*.css',
                    dest : 'static/admin/css/output/'
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

        webfont: {
            icons: {
                src: 'static/img/icons/*.svg',
                dest: 'static/fonts',
                destCss: 'static/css/src',
                options: {
                    font: '<%= pkg.name %>-icons',
                    hashes: true,
                    syntax: 'bootstrap',
                    template: 'static/img/icons/icons-tmpl.css',
                    templateOptions: {
                        htmlDemoTemplate: 'static/img/icons/demoicons-tmpl.html',
                        destHtml: 'static/docs'
                    }
                }
            }
        },
        
        watch: {
            options: {
                livereload: true,
            },              
            admincss : {
                files: '<%= files.css.admin.src %>',
                tasks : ['admincss']
            },
            html : {
                files : '<%= files.html %>'
            },
            doc : {
                files : 'static/docs/*'
            }
        },
      
    });
    
    // Load plugins
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-svgmin');
    grunt.loadNpmTasks('grunt-cssnext');
    grunt.loadNpmTasks('grunt-webfont');


    
    // Run plugins
    grunt.registerTask('default', ['cssmin:vars','cssnext']);
    grunt.registerTask('frontcss', ['cssmin:vars','cssnext', 'cssmin:front']);
    grunt.registerTask('admincss', ['cssmin:vars','cssnext', 'cssmin:admin']);
    grunt.registerTask('icons', ['svgmin:icons','webfont:icons']);


};