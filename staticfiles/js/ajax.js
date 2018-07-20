$(document).ready(function(){
  $('#search').keyup(function() {
    $.ajax({
      type: "POST",
      url: "/search/",
      data:{
        'search_text' : $('#search').val(),
        'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
      },
      success: searchSuccess,
      dataType: 'html'
    });
  });
});
function searchSuccess(data, textStatus, jqXHR)
{
  $('.search-results').html(data);
}

$(document).ready(function(){
  $('#search2').keyup(function() {
    $.ajax({
      type: "POST",
      url: "/search/",
      data:{
        'search_text' : $('#search2').val(),
        'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
      },
      success: searchSuccess,
      dataType: 'html'
    });
  });
});
function searchSuccess(data, textStatus, jqXHR)
{
  $('.search-results').html(data);
}