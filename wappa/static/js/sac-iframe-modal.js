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

	// public API
	var modal = {
		isActive : 0,

		template : $('<div id="sac-iframe-modal"> \
			<button id="close__sac-iframe-modal" role="button" class="icon-x-cross"> \
				<i>Close modal</i> \
			</button> \
			<iframe id="iframe__sac-iframe-modal" /> \
		</div> \
		'),

		open : function() {
			modal.template.show();
			modal.isActive = 1;
		},
		
		close : function() {
			$('iframe', modal.template)[0].src = '';
			modal.template.hide();
			modal.isActive = 1;
		},
	};



	var addTemplate = function(){
			$('body').append(modal.template);
		},

		load = function(url, callback) {
			$('iframe', modal.template)[0].src = url;
			if(callback) callback();
		};

		$(function() {

			var openBtn = $('[data-iframe-modal=open]');

			if (openBtn.length) {

				addTemplate();

				openBtn.click(function(e) {
					e.preventDefault();
					var url = this.href;
					load(url, function(){
						modal.open();
					});
				});

				$('#close__sac-iframe-modal', modal.template).click(function(e) {
					e.preventDefault();
					modal.close();
				});
			}


			// Stuff to do as soon as the DOM is ready;
		});

		return modal;

})(django.jQuery);


