$(function(){
	obs_rows = $("#obs-container").children(".obs-row")

	counter = 1

	$.each(obs_rows, function(i, obs_row){
		$(obs_row).attr("id", "obs_"+(i+1))
		counter++
	})

	$.each($(".obs-del"), function(i, btn){
		$(btn).click(function(){
			id = "#obs_"+(i+1)
			$(id).fadeOut(600, function(){ 
				$(this).remove()
				check_obss()
			})
		})
	})

	function check_obss(){
		if($("#obs-container").children(".obs-row").length < 1)
			$("#no-obss").removeClass("hide")
		else
			if(!($("#no-obss").hasClass("hide")))
				$("#no-obss").addClass("hide")
			
	}

	$("#add-obs-btn").click(function(){
		$("#obs-container").append(
			"<div id='obs_"+counter+"' class='row obs-row'>"+
				"<div class='col s10'>"+
					"<input name='observacion' type='text' placeholder='Observación' class='validate'>"+
				"</div>"+
				"<div class='col s2'>"+
					"<button type='button' class='obs-del btn-floating waves-effect waves-light red lighten-2'><i class='material-icons'>delete</i></button>"+
				"</div>"+
			"</div>"
		)
		var id = "#obs_"+counter
		counter++
		$(id).find(".obs-del").click(function(){
			console.log("click "+id)
			$(id).fadeOut(600, function(){ 
				$(this).remove()
				check_obss()
			})
		})
		check_obss()
	})

})