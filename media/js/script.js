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
                    {$('.form').replaceWith("<div style='height: 150px;text-align: center;padding-top: 75px;'>Спасибо за вопрос, мы постараемся ответить на него в самое ближайшее время!</div>");}
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
                    {$('.form').replaceWith("<div style='height: 150px;text-align: center;padding-top: 75px;'>Спасибо за заявку, мы свяжемся с вами в самое ближайшее время!</div>");}
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
        var price_sort = $(this).parent().parent().parent().find('.filter_curr>.check_price_sort').attr('name')
        LoadCatalog(type, subtype, region, country_id, price_sort, 'check_subtype');
    });

    $('.check_region').live('click',function(){
        var type = $('#re_type').val()
        var country_id = $('#country_id').val()
        var region = $(this).attr('name')
        var subtype = $(this).parent().parent().parent().find('.filter_curr>.check_subtype').attr('name')
        var price_sort = $(this).parent().parent().parent().find('.filter_curr>.check_price_sort').attr('name')
        LoadCatalog(type, subtype, region, country_id, price_sort, 'check_region');
    });

    $('.check_price_sort').live('click',function(){
        var type = $('#re_type').val()
        var country_id = $('#country_id').val()
        var region = $(this).parent().parent().parent().find('.filter_curr>.check_region').attr('name')
        var subtype = $(this).parent().parent().parent().find('.filter_curr>.check_subtype').attr('name')
        var price_sort = $(this).attr('name')
        LoadCatalog(type, subtype, region, country_id, price_sort, 'check_price_sort');
    });

    $('#select_country').live('change',function(){
        $.ajax({
            url: "/exclusive/load_catalog/",
            data: {
                country:$(this).val(),
                price_sort:$(this).parents('.filters').find('.filter_curr>.check_price_sort_excl').attr('name')
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
                            {SetPriceSlider(0,0,1,true);
                            price_label_r.html('-');}
                        else
                            {SetPriceSlider(0,0,1,true);
                            price_label_r.html('-');}
                        price_label_l.html('-');
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

    $('.check_price_sort_excl').live('click',function(){
        var country = $('#select_country').val()
        var price_sort = $(this).attr('name')
        $.ajax({
            url: "/exclusive/load_catalog/",
            data: {
                country:country,
                price_sort:price_sort
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
                            {SetPriceSlider(0,0,1,true);
                            price_label_r.html('-');}
                        else
                            {SetPriceSlider(0,0,1,true);
                            price_label_r.html('-');}
                        price_label_l.html('-');
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

    $('.load_page a').live('click',function(){
        var el = $(this);
        var parent = $(this).parents('.load_block');
        var png_parent = $(this).parents('.load_page');

        if ($('.filter_curr>.check_price_sort_excl').attr('name'))
            {var price_sort = $('.filter_curr>.check_price_sort_excl').attr('name')}
        else
            {if($('.filter_curr>.check_price_sort'))
                {var price_sort = $('.filter_curr>.check_price_sort').attr('name')}
            else
                {var price_sort = false}
            }

        png_parent.find('.current_page').removeClass('current_page');
        el.addClass('current_page');

        $.ajax({
            url: "/load_items/",
            data: {
                load_ids: el.attr('name'),
                all_load_ids: $('#all_loaded_ids').val(),
                m_name: parent.find('#m_name').val(),
                a_name: parent.find('#a_name').val(),
                price_sort: price_sort
            },
            type: "POST",
            success: function(data) {
                $('body,html,document').animate({scrollTop:500},"slow");
                parent.find('.item').remove()
                parent.find('.load_page').remove()
                parent.append(data)
                //parent.find('.loaded:eq(0)').fadeIn("fast", function (){ //появление по очереди
                //       $(this).next().fadeIn("fast", arguments.callee);
                //   });

                //parent.find('.loaded').fadeIn('slow')  //простое появление
                parent.find('.loaded').show()  //простое появление

                //parent.find('#loaded_ids').val(parent.find('#new_load_ids').val())
                parent.find('div').removeClass('loaded')
                //parent.find('.show_more').appendTo(parent)
                //var rctxt = parent.find('#remaining_count_text').val()
                //var rc = parent.find('#remaining_count').val()
                //if (rctxt!=undefined)
                //    {el.html(rctxt)}
                //if (rc<=0)
                //   {parent.find('.show_more').remove()}
                //parent.find('#remaining_count_text').remove()
                //parent.find('#new_load_ids').remove()
                //parent.find('#remaining_count').remove()

            }
        });

        return false;

    });

/*    $('.load_items').live('click',function(){

        if ($('.filter_curr>.check_price_sort_excl').attr('name'))
            {var price_sort = $('.filter_curr>.check_price_sort_excl').attr('name')}
        else
            {if($('.filter_curr>.check_price_sort'))
                {var price_sort = $('.filter_curr>.check_price_sort').attr('name')}
            else
                {var price_sort = false}
            }

        var el = $(this);
        var parent = $(this).parents('.load_block');
        $.ajax({
            url: "/load_items/",
            data: {
                load_ids: parent.find('#loaded_ids').val(),
                m_name: parent.find('#m_name').val(),
                a_name: parent.find('#a_name').val(),
                price_sort: price_sort
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
    });*/

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
        stop: function(event, ui) {
            vals = $(this).slider( "option", "values" )
            price_label_l.html(vals[0]);
            price_label_r.html(vals[1]);
            $.ajax({
                url: "/exclusive/load_catalog/",
                data: {
                    country:$("#country").val(),
                    price_min:vals[0],
                    price_max:vals[1],
                    price_sort:$(this).parents('.filters').find('.filter_curr>.check_price_sort_excl').attr('name')
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

function SetCatalogPriceSlider(min, max, start, end, step, disabl)
{
    var price_label_l = $('.filter_price_pl').find('.slider_label_l')
    var price_label_r = $('.filter_price_pl').find('.slider_label_r')

    $('#catalog_price_slider').slider({
        disabled: disabl,
        range: true,
        step: parseInt(step),
        min: parseInt(min),
        max: parseInt(max),
        values:[parseInt(start),parseInt(end)],
        stop: function(event, ui) {

            vals = $(this).slider( "option", "values" )
            if ((vals[0]==0) && (vals[1]==0))
                {price_label_l.html('-');
                price_label_r.html('-');}
            else
                {price_label_l.html(vals[0]);
                price_label_r.html(vals[1]);}
            $.ajax({
                url: "/countries/load_catalog/",
                data: {
                    country_id:$('#country_id').val(),
                    type:$('#re_type').val(),
                    subtype:$('.filter_curr>.check_subtype').attr('name'),
                    region:$('.filter_curr>.check_region').attr('name'),
                    price_sort:$('.filter_curr>.check_price_sort').attr('name'),
                    price_min:vals[0],
                    price_max:vals[1]
                    //add_parameters_values:$('#add_parameters_values').val()
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

function SetAdditionalSlider(id, start, end, step, disabl)
{
    $('#add_slider_'+id).slider({
        disabled: disabl,
        range: true,
        step: parseInt(step),
        min: parseInt(start),
        max: parseInt(end),
        values:[parseInt(start),parseInt(end)],
        stop: function(event, ui) {
            price_vals = $('#catalog_price_slider').slider( "option", "values" )
            var slider_label_l = $(this).find('.slider_label_l')
            var slider_label_r = $(this).find('.slider_label_r')
            vals = $(this).slider( "option", "values" )
            slider_label_l.html(vals[0]);
            slider_label_r.html(vals[1]);
            var parameters = $('#add_parameters_values').val()
            parameters_array = parameters.split('|');
            length = parameters_array.length
            for (var i = 0; i <= length-1; i++)
                {
                    part = parameters_array[i].split(',')
                    if (part[0]==id)
                        {
                            part[1]=vals[0]
                            part[2]=vals[1]
                        }
                    parameters_array[i] = part.join(',')
                }
            $('#add_parameters_values').val(parameters_array.join('|'))
            $.ajax({
                url: "/countries/load_catalog/",
                data: {
                    country_id:$('#country_id').val(),
                    type:$('#re_type').val(),
                    subtype:$('.filter_curr>.check_subtype').attr('name'),
                    region:$('.filter_curr>.check_region').attr('name'),
                    price_sort:$('.filter_curr>.check_price_sort').attr('name'),
                    price_min:price_vals[0],
                    price_max:price_vals[1],
                    add_parameters_values:$('#add_parameters_values').val()
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

function LoadCatalog(type, subtype, region, country_id, price_sort, sender)
{
    if (sender=='check_price_sort') //если нажали на сортировку по цене - то учитываем цену
        {var vals = $('#catalog_price_slider').slider( "option", "values" )}
    else
        {var vals = [0,0]}
    $.ajax({
        url: "/countries/load_catalog/",
        data: {
            type:type,
            subtype:subtype,
            region:region,
            country_id:country_id,
            price_sort:price_sort,
            price_min:vals[0],
            price_max:vals[1]
            //add_parameters_values:$('#add_parameters_values').val()
        },
        type: "POST",
        success: function(data) {
            $('.catalog').replaceWith(data);
            var minp = $('#min_price').val()
            var maxp = $('#max_price').val()
            var startp = $('#start_price').val()
            var endp = $('#end_price').val()
            var price_label_l = $('.filter_price_pl').find('.slider_label_l')
            var price_label_r = $('.filter_price_pl').find('.slider_label_r')

            if ((minp==maxp) || (minp==undefined) || (maxp==undefined))
                {
                    if ((maxp!=NaN) && (maxp!=''))
                        {price_label_r.html('-');}
                    else
                        {price_label_r.html('-');}
                    price_label_l.html('-');
                    SetCatalogPriceSlider(0,0,0,0,1,true);
                }
            else
                {
                    len = maxp - minp
                    stp = len/10
                    SetCatalogPriceSlider(minp,maxp,startp,endp,stp,false);
                    price_label_l.html(startp);
                    price_label_r.html(endp);
                }

        },
        error:function(jqXHR,textStatus,errorThrown) {
            $('.catalog').replaceWith(jqXHR.responseText);
        }
    });
}