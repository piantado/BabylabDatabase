$(document).ready(function () {

    $("table[data!='nodatatable']").each(function (index) {
        var table = $(this).dataTable(
            {
                "order": [1, 'asc'],
                "columnDefs": [
                    {"orderable": false, "targets": 0}
                ]
            }
        );


        table.api().columns( '.filter' ).every( function () {
            var column = this;
            var select = $('<select><option value=""></option></select>')
                .appendTo( $(column.footer()).empty() )
                .on( 'change', function () {
                    var val = $.fn.dataTable.util.escapeRegex(
                        $(this).val()
                    );

                    column
                        .search( val ? '^'+val+'$' : '', true, false )
                        .draw();
                } );

            column.data().unique().sort().each( function ( d, j ) {
                select.append( '<option value="'+d+'">'+d+'</option>' )
            } );
        } );

        //disability
        $('tfoot th.disability').each( function () {
            var title = 'Disability';
            $(this).html( '<input type="text" placeholder="Search '+title+'" />' );
        } );

        table.api().columns( '.text-search' ).every( function () {
        var that = this;

        $( 'input', this.footer() ).on( 'keyup change', function () {
            that
                .search( this.value )
                .draw();
        } );



    } );

        // Event listener to the two range filtering inputs to redraw on input
        $('#min_age, #max_age').keyup( function() {
            table.api().draw();
        } );

        // Event listener to the two range filtering inputs to redraw on input
        $('#min_eng, #max_eng').keyup( function() {
            table.api().draw();
        } );

        // Event listener for born early parameter for filtering to redraw on input
        $('#premature_ok').change( function() {
            table.api().draw();
        } );

        // Event listeners for disabilities parameters for filtering to redraw on input
        for (var curDisability = 0; curDisability < numDisabilities; curDisability++) {
            $('#' + disabilityHTMLNames[curDisability]).change( function() {
                table.api().draw();
            } );
        } 




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


$.fn.dataTable.ext.search.push(
    function( settings, data, dataIndex ) {
        var min = parseFloat( $('#min_age').val());
        var max = parseFloat( $('#max_age').val());
        var age = parseFloat( data[6] ) || 0; // use data for the age column

        if ( ( isNaN( min ) && isNaN( max ) ) ||
             ( isNaN( min ) && age <= max ) ||
             ( min <= age   && isNaN( max ) ) ||
             ( min <= age   && age <= max ) )
        {
            return true;
        }
        return false;
    }
);

$.fn.dataTable.ext.search.push(
    function( settings, data, dataIndex ) {
        var min = parseFloat( $('#min_eng').val());
        var max = parseFloat( $('#max_eng').val());
        var eng = parseFloat( data[7] ) || 0; // use data for the eng column

        if ( ( isNaN( min ) && isNaN( max ) ) ||
             ( isNaN( min ) && eng <= max ) ||
             ( min <= eng   && isNaN( max ) ) ||
             ( min <= eng   && eng <= max ) )
        {
            return true;
        }
        return false;
    }
);

$.fn.dataTable.ext.search.push(
    function( settings, data, dataIndex ) {
        var prematureOK = $('#premature_ok').is(':checked');
        var bornEarly = data[4] || ''; // use data for the premature column

        if (prematureOK) {
            return true;
        }
        else {
            if (bornEarly == 'No' || bornEarly == '') {
                return true;
            }
            else {
                return false;
            }
        }
    }
);

/*for (var curDisability = 0; curDisability < numDisabilities; curDisability++) {
    $.fn.dataTable.ext.search.push(
        function( settings, data, dataIndex ) {
            var disabilityOK = $('#' + disabilityNames[curDisability]).is(':checked');
            var disabilityColumn = data[5] || ''; // use data for the disability column

            console.log(disabilityOK);
            if (disabilityOK) {
                return true;
            }
            else {
                return false;
            }
        }
    );
}*/

$.fn.dataTable.ext.search.push(
    function( settings, data, dataIndex ) {

        var disabilityColumn = data[5] || ''; // use data for the disability column

        for (var i = 0; i < numDisabilities; i++) {
            if (!($('#' + disabilityHTMLNames[i]).is(':checked')) &&
                disabilityColumn.indexOf(disabilityNames[i]) != -1) {
                return false;
            }
        }

        return true;

    }
);

