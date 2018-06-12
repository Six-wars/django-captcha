/*CSRF Code */

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

/* End CSRF Code */


$(function() {
    $('#login-form').submit(function(event) {
        event.preventDefault();

        var data = {
            'username': $('#username').val(),
            'password': $('#password').val(),
            'captcha-result': $('#captcha').val(),
            'captcha-ref-id': $('#ref-id').val()
        }

        var csrftoken = $.cookie('csrftoken');

        $.ajax({
            url: "/login-ajax",
            type: "POST",
            dataType: 'json',
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                    // Send the token to same-origin, relative URLs only.
                    // Send the token only if the method warrants CSRF protection
                    // Using the CSRFToken value acquired earlier
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }

            },
            data: JSON.stringify(data),
            success: function(response){
                if (response['status'] == 'ok') {
                    
                }

            },
            error: function(xhr){
                
            },


            });
        
/* End Ajax Call */

    });

});