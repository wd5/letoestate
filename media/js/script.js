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

    SlideHeader();

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

    $('.load_items').live('click',function(){

        var el = $(this);
        var parent = $(this).parents('.load_block');
        $.ajax({
            url: "/load_items/",
            data: {
                load_ids: parent.find('#loaded_ids').val(),
                m_name: parent.find('#m_name').val(),
                a_name: parent.find('#a_name').val()
            },
            type: "POST",
            success: function(data) {

                parent.append(data)
                parent.find('.loaded:eq(0)').fadeIn("fast", function (){ //появление по очереди
                        $(this).next().fadeIn("fast", arguments.callee);
                    });
                //parent.find('.loaded').fadeIn('slow')  //простое появление
                parent.find('#loaded_ids').val(parent.find('#new_load_ids').val())
                parent.find('div').removeClass('loaded')
                parent.find('.show_more').appendTo(parent)
                var rctxt = parent.find('#remaining_count_text').val()
                var rc = parent.find('#remaining_count').val()
                if (rctxt!=undefined)
                    {el.html(rctxt)}
                if (rc<=0)
                    {parent.find('.show_more').remove()}
                parent.find('#remaining_count_text').remove()
                parent.find('#new_load_ids').remove()
                parent.find('#remaining_count').remove()

            }
        });

        return false;
    });

});

function SlideHeader()
{
    var delay = 3000, fade = 1000; // tweak-able
    var banners = $('.slider_img');
    var len = banners.length;
    var i = 0;

    setTimeout(cycle, delay); // <-- start

    function cycle() {
        $(banners[i%len]).fadeOut(fade, function() {
            $(banners[++i%len]).fadeIn(fade, function() { // mod ftw
                setTimeout(cycle, delay);
            });
        });
    }
}

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
            $.ajax({
                url: "/exclusive/load_catalog/",
                data: {
                    country:$("#country").val(),
                    price_min:vals[0],
                    price_max:vals[1]
                },
                type: "POST",
                success: function(data) {
                    $('.catalog').replaceWith(data);
                },
                error:function(jqXHR,textStatus,errorThrown) {
                    $('.catalog').replaceWith(jqXHR.responseText);
                }
            });
        }
    });
}

function SetCatalogPriceSlider(start, end, step, disabl)
{
    var price_label_l = $('.filter_price_pl').find('.slider_label_l')
    var price_label_r = $('.filter_price_pl').find('.slider_label_r')

    $('#catalog_price_slider').slider({
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
            $.ajax({
                url: "/countries/load_catalog/",
                data: {
                    country_id:$('#country_id').val(),
                    type:$('#re_type').val(),
                    subtype:$('.filter_curr>.check_subtype').attr('name'),
                    region:$('.filter_curr>.check_region').attr('name'),
                    price_min:vals[0],
                    price_max:vals[1]
                },
                type: "POST",
                success: function(data) {
                    $('.catalog').replaceWith(data);
                },
                error:function(jqXHR,textStatus,errorThrown) {
                    $('.catalog').replaceWith(jqXHR.responseText);
                }
            });
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
                    if ((maxp!=NaN) && (maxp!=''))
                        {price_label_r.html(maxp);}
                    else
                        {price_label_r.html(100);}
                    price_label_l.html(0);
                    SetCatalogPriceSlider(0,100,1,true);
                }
            else
                {
                    len = maxp - minp
                    stp = len/10
                    SetCatalogPriceSlider(minp,maxp,stp,false);
                    price_label_l.html(minp);
                    price_label_r.html(maxp);
                }

        },
        error:function(jqXHR,textStatus,errorThrown) {
            $('.catalog').replaceWith(jqXHR.responseText);
        }
    });
}