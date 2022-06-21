function retrieve_network_architecture(){
    $.ajax({
        method: 'GET',
        url: '/retrieve_network_architecture',
        success: function(response){
            let nrHiddenLayers = response.nr_hidden_layers
            let hiddenLayerSizeList = response.hidden_layer_size_list
            configureActivationForm(nrHiddenLayers)
            addConfirmBehaviour(nrHiddenLayers, response)
            nrHiddenLayers+=2
            hiddenLayerSizeList.unshift(2)
            hiddenLayerSizeList.push(1)
            drawCustomGraph(nrHiddenLayers, hiddenLayerSizeList, '#nn-graph-act-canvas-div')

        }
    })
}

function configureActivationForm(nrHiddenLayers){
    for(let i = 1; i <= nrHiddenLayers; i++){
        let labelSelector = '#layer-' + i + '-activation-label'
        let inputSelector = '#layer-' + i + '-activation'
        $(labelSelector).removeAttr('hidden')
        $(inputSelector).removeAttr('hidden')
    }
    $('#layer-out-activation-label').removeAttr('hidden')
    $('#layer-out-activation').removeAttr('hidden')
}

function addConfirmBehaviour(nrHiddenLayers, response){
    $('.confirm-div #confirm-network-activations').click(function(event){
        event.preventDefault()
        let hiddenLayersActivation = []
        for(let i=1; i<=nrHiddenLayers; i++){
            let inputSelector = '#layer-' + i + '-activation'
            let activation = $(inputSelector).val()
            hiddenLayersActivation.push(activation)
        }
        let outputLayerActivation = $('#layer-out-activation').val()
        $.ajax({
            method: 'POST',
            url: '/confirm_network_activations',
            dataType: 'json',
            data: {
                'hidden_layer_activation_list': hiddenLayersActivation,
                'output_layer_activation': outputLayerActivation
            },
            success: function(){
                window.location.href = '/guide/4'
            },
            error: function(){
                window.location.href = '/guide/4'
            }
        })
    })
}

$(document).ready(function() {
    drawPlot('binary_step_function_plot')
    drawPlot('linear_function_plot')
    drawPlot('sigmoid_function_plot')
    drawPlot('sigmoid_derivative_function_plot')
    drawPlot('tanh_function_plot')
    drawPlot('tanh_derivative_function_plot')
    drawPlot('relu_function_plot')
    drawPlot('relu_derivative_function_plot')
    retrieve_network_architecture()
})