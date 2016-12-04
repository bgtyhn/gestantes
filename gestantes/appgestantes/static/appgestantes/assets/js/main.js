$(function(){
	$(".clickable-row").click(function() {
        window.document.location = $(this).data("href");
    });

    $.extend($.fn.pickadate.defaults, {
	    monthsFull: [ 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre' ],
	    monthsShort: [ 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic' ],
	    weekdaysFull: [ 'Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado' ],
	    weekdaysShort: [ 'Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb' ],
	    today: 'Hoy',
	    clear: 'Borrar',
	    close: 'Cerrar',
	    firstDay: 1,
	    format: 'yyyy-mm-dd',
	    formatSubmit: 'yyyy-mm-dd'
	});

    $('#fecha_ingreso_programa').pickadate({
	    selectMonths: true,
	    selectYears: 20,
	    max: true
	});

	$("#fecha_nacimiento").pickadate({
	    selectMonths: true,
		selectYears: 60,
		max: true
	})

	$("#fecha_ultima_menstruacion").pickadate({
	    selectMonths: true,
		selectYears: 2,
		max: true
	})

	$("#fecha_probable_parto").pickadate({
	    selectMonths: true,
		selectYears: 2,
		min: true
	})

	$("#fecha_paraclinicos").pickadate({
		selectMonths: true,
		selectYears: 4
	})

	$("#fecha_pretest").pickadate({
		selectMonths: true,
		selectYears: 4,
		min: true
	})

	$("#fecha_postest").pickadate({
	    selectMonths: true,
		selectYears: 2,
		min: true
	})

	$("#fecha_citologia").pickadate({
		selectMonths: true,
		selectYears: 4
	})

	$("#fecha_odontologia").pickadate({
		selectMonths: true,
		selectYears: 2
	})

	$('select').material_select();
})