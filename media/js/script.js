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

    //$('div.pic').ite

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
        var type = $('#re_type').val()
        var country_id = $('#country_id').val()
        var subtype = $(this).attr('name')
        var region = $(this).parent().parent().parent().find('.filter_curr>.check_region').attr('name')
        LoadCatalog(type, subtype, region, country_id);
    });

    $('.check_region').live('click',function(){
        var type = $('#re_type').val()
        var country_id = $('#country_id').val()
        var region = $(this).attr('name')
        var subtype = $(this).parent().parent().parent().find('.filter_curr>.check_subtype').attr('name')
        LoadCatalog(type, subtype, region, country_id);
    });

    $('#select_country').live('change',function(){
        $.ajax({
            url: "/exclusive/load_catalog/",
            data: {
                country:$(this).val()
            },
            type: "POST",
            success: function(data) {
                $('.catalog').replaceWith(data);
                var minp = $('#min_price').val()
                var maxp = $('#max_price').val()
                var price_label_l = $('.filter_price_pl').find('.slider_label_l')
                var price_label_r = $('.filter_price_pl').find('.slider_label_r')

                if ((minp==maxp) || (minp==undefined) || (maxp==undefined))
                    {
                        if (maxp!=NaN)
                            {SetPriceSlider(0,100,1,true);
                            price_label_r.html(maxp);}
                        else
                            {SetPriceSlider(0,100,1,true);
                            price_label_r.html(100);}
                        price_label_l.html(0);
                    }
                else
                    {
                        len = maxp - minp
                        stp = len/10
                        SetPriceSlider(minp,maxp,stp,false);
                        price_label_l.html(minp);
                        price_label_r.html(maxp);
                    }

            },
            error:function(jqXHR,textStatus,errorThrown) {
                $('.catalog').replaceWith(jqXHR.responseText);
            }
        });
    });


});

function SetPriceSlider(start, end, step, disabl)
{
    var price_label_l = $('.filter_price_pl').find('.slider_label_l')
    var price_label_r = $('.filter_price_pl').find('.slider_label_r')

    $('#price_slider').slider({
        disabled: disabl,
        range: true,
        step: parseInt(step),
        min: parseInt(start),
        max: parseInt(end),
        values:[parseInt(start),parseInt(end)],
        change: function(event, ui) {
            vals = $(this).slider( "option", "values" )
            price_label_l.html(vals[0]);
            price_label_r.html(vals[1]);
        }
    });
}

function LoadCatalog(type, subtype, region, country_id)
{
    $.ajax({
        url: "/countries/load_catalog/",
        data: {
            type:type,
            subtype:subtype,
            region:region,
            country_id:country_id
        },
        type: "POST",
        success: function(data) {
            $('.catalog').replaceWith(data);
            var minp = $('#min_price').val()
            var maxp = $('#max_price').val()
            var price_label_l = $('.filter_price_pl').find('.slider_label_l')
            var price_label_r = $('.filter_price_pl').find('.slider_label_r')

            if ((minp==maxp) || (minp==undefined) || (maxp==undefined))
                {
                    if (maxp!=NaN)
                        {SetPriceSlider(0,100,1,true);
                        price_label_r.html(maxp);}
                    else
                        {SetPriceSlider(0,100,1,true);
                        price_label_r.html(100);}
                    price_label_l.html(0);
                }
            else
                {
                    len = maxp - minp
                    stp = len/10
                    SetPriceSlider(minp,maxp,stp,false);
                    price_label_l.html(minp);
                    price_label_r.html(maxp);
                }

        },
        error:function(jqXHR,textStatus,errorThrown) {
            $('.catalog').replaceWith(jqXHR.responseText);
        }
    });
}