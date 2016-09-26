
function initializeView()
{
    $('#add_time').click(function()
	{
		addTime()
	})
}

function addTime()
{
    // TODO This does the job but needs to be refactored

    var total_forms = $('#id_form-TOTAL_FORMS')
    var number_forms = parseInt(total_forms.attr('value'))
    total_forms.attr('value', number_forms+1)
    var field = $('.timefields').last().parent().clone()
    var new_id = "div_id_form-" + number_forms + "-time"
    var new_name = "form-" + number_forms + "-time"
    field.attr('id', new_id)
    field.children('input').attr('name', new_name)
    field.insertAfter($('.timefields').last().parent())
    $('.datetimeinput').datetimepicker();
}

$(document).ready(initializeView)
