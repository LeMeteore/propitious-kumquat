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

	var photosInput,
		photosInputVal,
		photosWrapper,
		photosTiles,
		favPhotoInput,
		favPhotoId,
		photosList = [];



	var activeFavorite = function(){
		favPhotoId = favPhotoInput.val();

		if(favPhotoId) {
			var activeTile = photosTiles.filter('[data-id=' + favPhotoId + ']');	
			activeTile.find('[data-action=favorite]').addClass('active');
		}
	};

	/*
	//	Tiles Btn action
	*/

	var getTile = function(el){
		var tile = el.parents('.i--pack_photos'),
			tileID = tile.data('id');

		return {
			el: tile, 
			id: tileID
		};
	};

	var removePhoto = function(e){
		var tile = getTile( $(e.target) );

		// remove photoId to photoList
		var idIndex = photosList.indexOf( tile.id+'' );
		photosList.splice(idIndex, 1);	
		photosInput.val(photosList.join(','));

		// remove tile
		tile.el.remove();
	};

	var addToFavorite = function(e){
		var btn = $(e.target),
			tile = getTile( btn );
		
		photosTiles.find('[data-action=favorite].active').removeClass('active');
		btn.addClass('active');

		favPhotoInput.val(tile.id);
	};

	/*
	// Ajoute les images au template
	*/
	var render = function(template, data, target, callback){
		// console.log('render');
		var renderer = Mustache.render(template, {photos : data} );
		target.append(renderer);

		photosTiles = $('.i--pack_photos');
		console.log(photosTiles);

		if (callback) callback();
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
		photosInput = $('#id_photos');
		photosInputVal = photosInput.val();
		photosWrapper = $('#l--pack_photos');
		favPhotoInput = $('#id_image');

		if(photosInputVal) photosList = photosInputVal.split(',');
		
		var template = $('#i-photo-tpl').html();
		Mustache.parse(template);

		// Charge les previews des photos exitantes
		if (photosList.length) {
			getImgInfo(function(data){	
				render(template, data, photosWrapper, function(){
					activeFavorite();
				});
			});
		}



		// remove tiles
		photosWrapper.on('click', '[data-action=remove]', removePhoto );
		photosWrapper.on('click', '[data-action=favorite]', addToFavorite );


    });



})(django.jQuery);