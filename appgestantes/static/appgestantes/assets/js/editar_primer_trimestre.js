$(function(){

	$("#fecha_frotis").pickadate({
		selectMonths: true,
	    selectYears: 3
	})

	$("#frotis_fecha").pickadate({
		selectMonths: true,
	    selectYears: 3
	})

	$("#fecha_factores_diabetes").pickadate({
		selectMonths: true,
	    selectYears: 3
	})

	$("#fecha_ecografia").pickadate({
		selectMonths: true,
	    selectYears: 3
	})


	frot_rows = $("#frot-container").children(".frot-row")

	counter_frot = 1

	$.each(frot_rows, function(i, frot_row){
		$(frot_row).attr("id", "frot_"+(i+1))
		counter_frot++
	})

	$.each($(".frot-del"), function(i, btn){
		$(btn).click(function(){
			id = "#frot_"+(i+1)
			$(id).fadeOut(600, function(){ 
				$(this).remove()
				check_frots()
			})
		})
	})

	function check_frots(){
		if($("#frot-container").children(".frot-row").length < 1)
			$("#no-frots").removeClass("hide")
		else
			if(!($("#no-frots").hasClass("hide")))
				$("#no-frots").addClass("hide")
			
	}

	$("#add-frot-btn").click(function(){
		$("#frot-container").append(
			"<div id='frot_"+counter_frot+"' class='row frot-row'>"+
				"<div class='col s10'>"+
					"<input name='motivo_frotis' type='text' placeholder='Motivo' class='validate'>"+
				"</div>"+
				"<div class='col s2'>"+
					"<button type='button' class='frot-del btn-floating waves-effect waves-light red lighten-2'><i class='material-icons'>delete</i></button>"+
				"</div>"+
			"</div>"
		)
		var id = "#frot_"+counter_frot
		counter_frot++
		$(id).find(".frot-del").click(function(){
			console.log("click "+id)
			$(id).fadeOut(600, function(){ 
				$(this).remove()
				check_frots()
			})
		})
		check_frots()
	})


	hem_rows = $("#hem-container").children(".hem-row")

	counter_hem = 1

	$.each(hem_rows, function(i, hem_row){
		$(hem_row).attr("id", "hem_"+(i+1))
		counter_hem++
	})

	$.each($(".hem-del"), function(i, btn){
		$(btn).click(function(){
			id = "#hem_"+(i+1)
			$(id).fadeOut(600, function(){ 
				$(this).remove()
				check_hems()
			})
		})
	})

	function check_hems(){
		if($("#hem-container").children(".hem-row").length < 1)
			$("#no-hems").removeClass("hide")
		else
			if(!($("#no-hems").hasClass("hide")))
				$("#no-hems").addClass("hide")
			
	}

	$("#add-hem-btn").click(function(){
		$("#hem-container").append(
			"<div id='hem_"+counter_hem+"' class='row hem-row'>"+
				"<div class='col s10'>"+
					"<input name='motivo_hematico' type='text' placeholder='Motivo' class='validate'>"+
				"</div>"+
				"<div class='col s2'>"+
					"<button type='button' class='hem-del btn-floating waves-effect waves-light red lighten-2'><i class='material-icons'>delete</i></button>"+
				"</div>"+
			"</div>"
		)
		var id = "#hem_"+counter_hem
		counter_hem++
		$(id).find(".hem-del").click(function(){
			console.log("click "+id)
			$(id).fadeOut(600, function(){ 
				$(this).remove()
				check_hems()
			})
		})
		check_hems()
	})

})