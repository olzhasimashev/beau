var csrftoken = Cookies.get('csrftoken');
	function csrfSafeMethod(method) {
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});

$(document).ready(function() {
  $('#favorite-button').click(function() {
    var procedureId = $(this).data('procedure');
    var action = $(this).data('action');
    var url = $(this).data('url');

    $.ajax({
      url: url,
      type: 'POST',
      data: {
        'procedure_id': procedureId,
        'action': action
      },
      success: function(data) {
        if (data['status'] == 'ok') {
          if (action == 'add') {
            $('#favorite-button').html('Удалить из Избранного');
            $('#favorite-button').data('action', 'remove');
          } else {
            $('#favorite-button').html('Добавить в Избранное');
            $('#favorite-button').data('action', 'add');
          }
        }
      }
    });
  });

  $('#category-type-select').change(function() {
    var category_type = $(this).val();
    var url = $(this).data('url');
    $.ajax({
      url: url,
      type: 'GET',
      data: {'category_type': category_type},
      success: function(data) {
        $('#procedure_category_list').html(data)
      },
      error: function(jqXHR, textStatus, errorThrown) {
        console.error(textStatus, errorThrown);
      }
    });
  });
});