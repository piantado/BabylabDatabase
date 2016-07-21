$('.input-group.date input.dateinput').each(function (e) {
    var dp = $(this).datepicker({
        //format: "yyyy-mm-dd",
        format: "mm-dd-yyyy",
        language: 'en',
        todayBtn: "linked",
        autoclose: true
    }).data('datepicker');
    $(this).parent().find('button').click(function (e) {
        dp.update(new Date());
    })
})