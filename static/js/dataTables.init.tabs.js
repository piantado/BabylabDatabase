$('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {

    var tab = $(e.target).attr("href");
    var jqTable = $(tab).find('table');
    if (jqTable.length > 0) {
        var oTableTools = TableTools.fnGetInstance(jqTable[0]);
        if (oTableTools != null && oTableTools.fnResizeRequired()) {
            /* A resize of TableTools' buttons and DataTables' columns is only required on the
             * first visible draw of the table
             */
            jqTable.dataTable().fnAdjustColumnSizing();
            oTableTools.fnResizeButtons();
        }
    }

});
