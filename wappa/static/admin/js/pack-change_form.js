/* jshint strict: true, undef: true, unused: true, laxcomma: true, jquery: true, browser: true, devel: true */
/* global django, Mustache*/


/*
**	Wappa Pack change_form
**	© sacripant.fr

**	UI for add and remove photos to a Pack

**	Need mustache.js
*/



(function($) {
	'use strict';


	// Ajoute les images au template
	var render = function(template, data, target){
		var renderer = Mustache.render(template, {photos : data} );
		target.append(renderer);
	};

	// Récupère les infos des images via AJAX
	var imgsInfo = function(callback){
		$.ajax({
			url: '/static/admin/js/test.txt',
			// url :'/en/admin/photo/photo/informations/' + photosval + '/',
			type: 'GET',
			dataType: 'json',
		})
		.done(function(data) {
			if (callback) {
				callback(data);
			}
		});
	};

	// On Ready
	$(document).ready(function() {
		var photosInput = $('#id_photos'),
			photosval = photosInput.val(),
			template = $('#i-photo-tpl').html(),
			target = $('#l--pack_photos');

		Mustache.parse(template);

		// Charge les previews des photos exitantes
		if (photosval) {
			imgsInfo(function(data){
				render(template, data, target);
			});
		}

		// Charge une nouvelle photo (via django)
		// photosInput.change(function() {
		// 	console.log("change");
		// 	console.log(dRLP_newImg);
		// });		
    });
})(django.jQuery);