$(function(){

	$("#fecha_factores_diabetes").pickadate({
		selectMonths: true,
	    selectYears: 3,
	    onClose : function(){
			checkRiesDiaSt()
	    }
	})

	$("#ecografia_fecha").pickadate({
		selectMonths: true,
	    selectYears: 3,
	})

	function checkRiesDiaFields(){
		if($("#factores_riesgo_diabetes_gestacional").val() == "Si"){
			$("#fecha_factores_diabetes").removeAttr("disabled")
		} else {
			$("#fecha_factores_diabetes").val('')
			$("#fecha_factores_diabetes").attr("disabled", "disabled")
			checkRiesDiaSt()
		}
		$('select').material_select();
	}

	function checkRiesDiaSt(){
		if($("#fecha_factores_diabetes").val() == ""){
			$("#estado_factores_diabetes").val('Pendiente')
			$("#estado_factores_diabetes").attr("disabled", "disabled")
			checkRiesDiaRes()
		} else {
			$("#estado_factores_diabetes").removeAttr("disabled")
		}
		$('select').material_select();
	}

	function checkRiesDiaRes(){
		if($("#estado_factores_diabetes").val() == "Alterado"){
			$("#numero_factores_diabetes").removeAttr("disabled")
		} else {
			$("#numero_factores_diabetes").val('')
			$("#numero_factores_diabetes").attr("disabled", "disabled")
		}
		$('select').material_select();
	}

	$("#estado_factores_diabetes").on("change", function(){
		checkRiesDiaRes()
	})

	$("#factores_riesgo_diabetes_gestacional").on("change", function(){
		checkRiesDiaFields()
	})

	checkRiesDiaFields()
	checkRiesDiaSt()
	checkRiesDiaRes()
	checkEcoSem()

})