$('.input-group.time').each(function (e) {
    var el = $(this).find('input.timeinput');
    var value = el.val();
    var tp = el.timepicker({
        minuteStep: 5,
        showSeconds: false,
        showMeridian: true,
        defaultTime: false
    }).data('timepicker');
    $(this).find('button').click(function (e) {
        tp.$element.val("");
        tp.setDefaultTime('current');
        tp.update();
    })
})