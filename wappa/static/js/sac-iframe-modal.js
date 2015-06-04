/* jshint strict: true, undef: true, unused: true, laxcomma: true, jquery: true, browser: true, devel: true, multistr: true */
/* global django */


/*
**	Simple iframe modal window
**	© sacripant.fr

**	Need sac-modal.css
**	Only one per page

	markup :

	div#sac-iframe-modal
		a#close__sac-iframe-modal
		iframe#iframe__sac-iframe-modal
*/

var iframeModal = (function($){
	'use strict';

	var	template = $('<div id="sac-iframe-modal">' +
			'	<button id="close__sac-iframe-modal" role="button" class="icon-x-cross">' +
			'		<i>Close modal</i>' +
			'	</button>' +
			'	<div id="content__sac-iframe-modal"></div>' +
			'</div>'
		),


		addTemplate = function(){
			$('body').append(template);
		},

		load = function(url, callback) {

		    var iframe = document.createElement('iframe'),
		    	target = $('#content__sac-iframe-modal', template);
			
			iframe.src = url;

			modal.show();
			target.html(iframe);
			// console.log(iframe);

			iframe.addEventListener('load', function() {
				if(callback) callback( $(iframe).contents() );
				// return $(iframe).contents();
			});

			// console.log(content);

			// return content;

		};



	// public API
	var modal = {
		isActive : 0,

		content : null,

		show : function() {
			template.show();
			modal.isActive = 1;
		},
		
		hide : function() {
			$('#content__sac-iframe-modal', template).html('');
			template.hide();
			modal.isActive = 0;
		},

		open : function(el, callback) {
			var url = el.href;
			// console.log(url);
			load(url, function(iframeContent) {
				modal.content = iframeContent;

				if (callback) { callback(iframeContent); }
			});
		},

		close : function() {
			$('iframe', modal.template)[0].src = '';
			modal.hide();
		}
	};



	$(function() {

		addTemplate();

		var dataBtn = $('[data-iframe-modal=open]');

		if (dataBtn.length) {
			dataBtn.click(function(e) {
				e.preventDefault();
				// console.log(this);
				modal.open(this);
			});
		}

		$('#close__sac-iframe-modal', modal.template).click(function(e) {
			e.preventDefault();
			modal.close();
		});

		// Stuff to do as soon as the DOM is ready;
	});

	return modal;

})(django.jQuery);


