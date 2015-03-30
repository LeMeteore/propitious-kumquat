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

(function($){
	'use strict';

	var modal = 0;

	var template = $('<div id="sac-iframe-modal"> \
			<button id="close__sac-iframe-modal" role="button" class="icon-x-cross"> \
				<i>Close modal</i> \
			</button> \
			<iframe id="iframe__sac-iframe-modal" /> \
		</div> \
	');

	var addTemplate = function(){
		$('body').append(template);
	};

	var actions = {
		open: function() {
			template.show();
			modal = 1;
		},
		close: function() {
			$('iframe', template)[0].src = '';
			template.hide();
			modal = 0;
		},
		load: function(url, callback) {
			$('iframe', template)[0].src = url;
			if(callback) callback();
		}
	};

	$(function() {

		var openBtn = $('[data-iframe-modal=open]');

		if (openBtn.length) {
			addTemplate();

			openBtn.click(function(e) {
				e.preventDefault();
				var url = this.href;
				actions.load(url, function(){
					actions.open();
				});
			});

			$('#close__sac-iframe-modal', template).click(function(e) {
				e.preventDefault();
				actions.close();
			});
		}


		// Stuff to do as soon as the DOM is ready;
	});
})(django.jQuery);


