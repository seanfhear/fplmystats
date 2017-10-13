var table;

$(document).ready(function() {
    table = $('table.weekly').DataTable( {
        "paging": false,
        "searching": false,
        "bInfo": false,
        "order": [[0, "desc"]]
    });
});

$(document).ready(function() {
    $('table.squad-player').DataTable( {
        "paging": false,
        "searching": false,
        "bInfo": false,
        "order": [[4, "desc"]]
    });
});

$(document).ready(function() {
    $('table.squad-team').DataTable( {
        "paging": false,
        "searching": false,
        "bInfo": false,
        "order": [[1, "desc"]]
    });
});

$(document).ready(function() {
    var t = $('table.league-general-number').DataTable( {
        "paging": false,
        "searching": false,
        "bInfo": false,
        "order": [[2, "desc"]],

        "columnDefs": [ {
            "searchable": false,
            "orderable": false,
            "targets": 0
        }]
    });

    t.on( 'order.dt search.dt', function () {
        t.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
});

$(document).ready(function() {
    var t = $('table.league-general-points').DataTable( {
        "paging": false,
        "searching": false,
        "bInfo": false,
        "order": [[2, "desc"]],

        "columnDefs": [ {
            "searchable": false,
            "orderable": false,
            "targets": 0
        }]
    });

    t.on( 'order.dt search.dt', function () {
        t.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
});

$(document).ready(function() {
    var t = $('table.league-positions').DataTable( {
        "paging": false,
        "searching": false,
        "bInfo": false,
        "order": [[1, "asc"]],

        "columnDefs": [ {
            "searchable": false,
            "orderable": false,
            "targets": 0
        }]
    });

    t.on( 'order.dt search.dt', function () {
        t.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
});

$(document).ready(function() {
    var t = $('table.league-team').DataTable( {
        "paging": false,
        "searching": false,
        "bInfo": false,
        "order": [[11, "desc"]],

        "columnDefs": [ {
            "searchable": false,
            "orderable": false,
            "targets": 0
        }]
    });

    t.on( 'order.dt search.dt', function () {
        t.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        });
    }).draw();
});

$(document).on('change', '.form-control', function() {
    var target = $(this).data('target');
    var show = $("option:selected", this).data('show');
    $(target).children().addClass('hide');
    $(show).removeClass('hide');
    table.columns.adjust().draw();
});

$(document).ready(function(){
	$('.form-control').trigger('change');
});

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
});

function toggleToPoints(){
    var number = document.getElementById('general-number');
    var number_total = document.getElementById('general-number-total');
    var points = document.getElementById('general-points');
    var points_total = document.getElementById('general-points-total');

    if (number.style.display === 'block'){
        number.style.display = 'none';
        number_total.style.display = 'none';
        points.style.display = 'block';
        points_total.style.display = 'block';
    }
    table.columns.adjust().draw();
}

function toggleToNumber(){
    var number = document.getElementById('general-number');
    var number_total = document.getElementById('general-number-total');
    var points = document.getElementById('general-points');
    var points_total = document.getElementById('general-points-total');

    if (points.style.display === 'block'){
        points.style.display = 'none';
        points_total.style.display = 'none';
        number.style.display = 'block';
        number_total.style.display = 'block';
    }
    table.columns.adjust().draw();
}