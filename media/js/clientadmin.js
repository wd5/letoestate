$(function() {
    $('#id_title').syncTranslit({destination: 'id_slug'});

    if ($('#id_country') && $('#id_region'))
        {LoadRegions($('#id_country').val())}

    $('#id_country').live('change', function() {
        LoadRegions($(this).val())
    });

});

function LoadRegions(id)
{
    var selected_id = $('select[name="region"] option:selected').val()

    $.ajax({
        url: "/load_region/",
        data: {
            id_country:id
        },
        type: "POST",
        success: function(data) {
            $('#id_region').html(data)
            if (selected_id!='')
                {$('select[name="region"] option[value='+selected_id+']').attr('selected','selected')}
        },
        error:function(jqXHR,textStatus,errorThrown) {
            $('#id_region').html('<option value=""></option>');
        }
    });
}