$(function () {
	$('.filter_exts').hide();
	$('.filter_show_more a').live('click', function() {
		$('.filter_exts').toggle(200);
		return false;
	});
	$('.filter a').live('click', function() {
		$(this).parent().parent().find('.filter_curr').removeClass('filter_curr');
		$(this).parent().addClass('filter_curr');
		return false;
	});
	$('.specs ul').cycle({fx:'fade', ctrls:'.specs_ctrls span'});
});