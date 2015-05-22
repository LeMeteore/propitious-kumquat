/* jshint strict: true, undef: true, unused: true, laxcomma: true, jquery: true, browser: true, devel: true */
/* global django, Mustache*/


/*
**	Wappa Pack change_form
**	© sacripant.fr

**	UI for add and remove photos to a Pack

**	Need mustache.js
*/


// * Ajax Call
// * Mustache render
// * Add result to target
// * remove tile
// * add new
// * favorite one.



var packPhotos = (function($) {
	'use strict';

	var photosList = [];
		// photosTiles = $();


	var removePhoto = function(e){

		var $this = $(e.target),
			tile = $this.parents('.i--pack_photos'),
			tileID = tile.data('id');

		// console.log(tileID);

		var idIndex = photosList.indexOf(tileID+'');
		photosList.splice(idIndex, 1);	
		tile.remove();

		$('#id_photos').val(photosList.join(','));


		// console.log(photosList);

	};

	// Ajoute les images au template
	var render = function(template, data, target){
		var renderer = Mustache.render(template, {photos : data} );
			
			// var html = $.parseHTML(renderer);
			// var newTiles = $(html).filter('.i--pack_photos');
			// photosTiles = photosTiles.add(newTiles);
			// target.append(newTiles);

			target.append(renderer);
	};

	// Récupère les infos des images via AJAX
	var getImgInfo = function(callback){
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
			photosWrapper = $('#l--pack_photos');

		if(photosval) photosList = photosval.split(',');

		console.log(photosList);

		// console.log(photosList);
		// console.log(photosList.length);
		
		Mustache.parse(template);

		// Charge les previews des photos exitantes
		if (photosList.length) {
			getImgInfo(function(data){
				
				render(template, data, photosWrapper);

				// stock input value in array
				// photosTiles = $('.i--pack_photos');

				// console.log( $('[data-action=remove]', data) );
				// console.log( $(data) );
			});
		}


		// remove tiles
		photosWrapper.on('click', '[data-action=remove]', removePhoto );

					// $('[data-action=remove]', html).click(function(e) {
			// 	console.log(e);
			// });

		// $('[data-action=remove]', photosTiles).click(function() {
		// 	console.log('remove tile');
		// });
    });



})(django.jQuery);