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



var packPhotos = (function($, modal) {
	'use strict';

	var photosInput,
		photosInputVal,
		photosWrapper,
		photosTiles,
		favPhotoInput,
		favPhotoId,
		photosList = [],



	activeFavorite = function(){
		favPhotoId = favPhotoInput.val();

		if(favPhotoId) {
			var activeTile = photosTiles.filter('[data-id=' + favPhotoId + ']');	
			activeTile.find('[data-action=favorite]').addClass('active');
		}
	},

	/*
	//	Tiles Btn action
	*/

	getTile = function(el){
		var tile = el.parents('.i--pack_photos'),
			tileID = tile.data('id');

		return {
			el: tile, 
			id: tileID
		};
	},

	removePhoto = function(e){
		var tile = getTile( $(e.target) );

		// remove photoId to photoList
		var idIndex = photosList.indexOf( tile.id+'' );
		photosList.splice(idIndex, 1);	
		photosInput.val(photosList.join(','));

		// remove tile
		tile.el.remove();
	},

	addToFavorite = function(e){
		var btn = $(e.target),
			tile = getTile( btn );
		
		photosTiles.find('[data-action=favorite].active').removeClass('active');
		btn.addClass('active');

		favPhotoInput.val(tile.id);
	},

	/*
	// Ajoute les images au template
	*/
	render = function(template, data, target, callback){
		// console.log('render');
		var renderer = Mustache.render(template, {photos : data} );
		target.append(renderer);

		photosTiles = $('.i--pack_photos');

		if (callback) callback();
	},


	// Récupère les infos des images via AJAX
	getImgInfo = function(callback){
		$.ajax({
			// url: '/static/admin/js/test.txt',
			url :'/en/admin/photo/photo/informations/' + photosInputVal + '/',
			type: 'GET',
			dataType: 'json',
		})
		.done(function(data) {
			// console.log(data);
			if (callback) {
				callback(data);
			}
		});
	},


	/*
	//	Add remove photo since Add modal
	*/

	photoInList = function(id) {
		var result = {
			inList : true,
			index : photosList.indexOf(id)
		};

		if ( result.index === -1 ) {
			result.inList = false;
		}

		return result;
	},

	addRemove = function(el, id){
		console.log('addRemove');

		var photo = photoInList(id);

		if ( photo.inList ) {
			el.removeClass('selected');
			photosList.splice(photo.index, 1);
		} else {
			el.addClass('selected');
			photosList.push(id);
		}

		console.log(photosList);
	};

	/*
	//	On Ready
	*/
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

		// remove tiles btn
		photosWrapper.on('click', '[data-action=remove]', removePhoto );
		// favorite img btn
		photosWrapper.on('click', '[data-action=favorite]', addToFavorite );
		// Edit Img btn
		photosWrapper.on('click', '[data-action=edit]', function(event){
			event.preventDefault();
			modal.open(this);
		});


		// IMPORT PHOTO

		$('#select-photo-btn').on('click', function(event) {
			event.preventDefault();

			modal.open(this, function(content){
				var photos = content.find('.i--photos');

				photos.each(function(index, el) {
					var photo = $(el),
						id = photo.data().id.toString();

					if ( photoInList(id).inList ) {
						$(el).addClass('selected');
					}

					// Add / Remove when click in photo figure
					$('.fig--i--photos', photo).click(function() {
						addRemove(photo, id);
						return false;
					});
				});



			});
		});

    });


})(django.jQuery, iframeModal);