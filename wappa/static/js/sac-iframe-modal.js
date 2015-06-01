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
			'	<iframe id="iframe__sac-iframe-modal" />' +
			'</div>'
		),


		addTemplate = function(){
			$('body').append(template);
		},

		load = function(url, callback) {
			$('iframe', template)[0].src = url;
			if(callback) callback();
		};



	// public API
	var modal = {
		isActive : 0,

		show : function() {
			template.show();
			modal.isActive = 1;
		},
		
		hide : function() {
			$('iframe', modal.template)[0].src = '';
			template.hide();
			modal.isActive = 0;
		},

		open : function(el) {
			var url = el.href;
			console.log(url);
			load(url, function(){
				modal.show();
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


