$(document).ready(function () {

    $("table[data!='nodatatable']").each(function (index) {
        var table = $(this).dataTable(
            {
                "order": [1, 'asc'],
                "columnDefs": [
                    {"orderable": false, "targets": 0}
                ],
                "buttons": [
                    'copy', 'excel', 'csv', 'pdf', 'print'
                    ]
            }
        );
        var tt = new $.fn.dataTable.TableTools(table, {
            "sSwfPath": STATIC_URL + "swf/copy_csv_xls_pdf.swf",
            "aButtons": [{
                "sExtends": "copy",
                "oSelectorOpts": {filter: "applied"},
                "bFooter": false,
                "mColumns": function (ctx) {
                    var api = new $.fn.dataTable.Api(ctx);

                    return api.columns(':not(.sorting_disabled)').indexes().toArray();
                }
            },
                {
                    "sExtends": "csv",
                    "oSelectorOpts": {filter: "applied"},
                    "bFooter": false,
                    "mColumns": function (ctx) {
                        var api = new $.fn.dataTable.Api(ctx);

                        return api.columns(':not(.sorting_disabled)').indexes().toArray();
                    }
                },
                {
                    "sExtends": "pdf",
                    "oSelectorOpts": {filter: "applied"},
                    "mColumns": function (ctx) {
                        var api = new $.fn.dataTable.Api(ctx);

                        return api.columns(':not(.sorting_disabled)').indexes().toArray();
                    }
                },
                {
                    "sExtends": "print",
                    "oSelectorOpts": {filter: "applied"},
                    "mColumns": function (ctx) {
                        var api = new $.fn.dataTable.Api(ctx);

                        return api.columns(':not(.sorting_disabled)').indexes().toArray();
                    }
                }
            ]


        });
        $(tt.fnContainer()).insertBefore(table.api().table().container());
    });

});