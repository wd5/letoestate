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

    $('.fancybox').fancybox();

    $('#send_question').live('click',function(){
        $.ajax({
            url: "/faq/checkform/",
            data: {
                name:$('#id_name').val(),
                question:$('#id_question').val(),
                email:$('#id_email').val()
            },
            type: "POST",
            success: function(data) {
                if (data=='success')
                    {$('.form').replaceWith("Спасибо за вопрос, мы постараемся ответить на него в самое ближайшее время!");}
                else{
                    $('.form').replaceWith(data);
                }
            }
        });
        return false;
    });

    $('#send_request').live('click',function(){
        $.ajax({
            url: "/countries/save_request/",
            data: {
                name:$('#id_name').val(),
                contacts:$('#id_contacts').val(),
                note:$('#id_note').val(),
                url:$('#id_url').val()
            },
            type: "POST",
            success: function(data) {
                if (data=='success')
                    {$('.form').replaceWith("Спасибо за заявку, мы свяжемся с вами в самое ближайшее время!");}
                else{
                    $('.form').replaceWith(data);
                }
            }
        });
        return false;
    });

    $('.check_subtype').live('click',function(){
        alert($(this).attr('name'));
        alert($(this).parent().parent().parent().find('.filter_curr>.check_region').attr('name'));
    });

    $('.check_region').live('click',function(){
        alert($(this).attr('name'));
        alert($(this).parent().parent().parent().find('.filter_curr>.check_subtype').attr('name'));
    });



});