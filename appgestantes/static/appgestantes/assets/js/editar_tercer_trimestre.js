$(function(){

	$("#fecha_VIH").pickadate({
		selectMonths: true,
	    selectYears: 3,
	    onClose : function(){
	    	checkVIHRes()
	    }
	})

	$("#ecografia_unica_fecha").pickadate({
		selectMonths: true,
	    selectYears: 3
	})

	function checkVIHRes(){
		if($("#fecha_VIH").val() == ""){
			$("#reactivo_VIH").val('Pendiente')
			$("#reactivo_VIH").attr("disabled", "disabled")
		} else {
			$("#reactivo_VIH").removeAttr("disabled")
		}
		$('select').material_select();
	}

	function checkVIHFields(){
		if(($("#factores_riesgo_VIH").is(":checked"))){
			$("#fecha_VIH").removeAttr("disabled")
		} else {
			$("#fecha_VIH").val('')
			$("#fecha_VIH").attr("disabled", "disabled")
			checkVIHRes()
		}
		$('select').material_select();
	}

	$("#factores_riesgo_VIH").on("change", function(){
		checkVIHFields()
		
	})

	checkVIHFields()
	checkVIHRes()

})