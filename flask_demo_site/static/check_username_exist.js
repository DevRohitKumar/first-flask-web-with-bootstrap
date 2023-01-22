$(document).ready(function() {
    $(#username).on('input', function (e) {
        $('#msg').hide();
        $('#loading').show();
        if ($('#username').val() == null || $('#username').val == '') {
            $('#msg').show();
            $('#msg').html('Username is required').css('color', 'red');
            $('#loading').hide();
        }else{
            $.ajax({
                type: "POST",
                url: "/username_check",
                data: $('#signupform').serialize(),
                dataType: "html",
                success: function (msg) {
                    $('#msg').show();
                    $('#loading').hide();
                    $('#msg').html(msg);
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    $('#msg').show();
                    $('#loading').hide();
                    $('#msg').html(textStatus+" "+errorThrown);
            });
        }
    });
});