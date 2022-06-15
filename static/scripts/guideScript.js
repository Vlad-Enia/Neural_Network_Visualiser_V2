function drawPlot(plot_name){
    $.ajax({
        url: '/plot/' + plot_name,
        method: 'GET',
        success: function (response){
            let div_id = '#plot-div-' + plot_name
            $(div_id).html(response)
        }
    })
}

$(document).ready(function(){
    drawCustomGraph(4,[4, 8, 6, 2], '#general-nn')
    drawPerceptron(['x1', 'x2'], 2, ['w1', 'w2'])
    drawPlot('perceptron_AND')
    drawPlot('perceptron_XOR')
    drawPlot('moons_data_set')
    drawPlot('moons_data_set_classified')
})