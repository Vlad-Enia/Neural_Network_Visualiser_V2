function drawPlot(plot_name){
    $.ajax({
        url: '/plot/' + plot_name,
        method: 'GET',
        success: function (response){
            let div_id = '#plot-div-' + plot_name
            $(div_id).html(response)
        },
        error: function(){
            console.log('error')
        }
    })
}