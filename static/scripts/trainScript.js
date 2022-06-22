function addResetBehaviour(network_architecture){
    $('#reset-btn').click(function(){
        drawGraph(network_architecture, '#nn-graph-train-div')
        addActivationValuesInForm(network_architecture.nr_hidden_layers, network_architecture.hidden_layer_activation_list, network_architecture.output_layer_activation)
        $('#confirm-network-activations').removeAttr('hidden')
        $.ajax({
            method: 'GET',
            url: '/retrieve_dataset',
            success: function(response){
                $('#configure-dataset-plot-train-div').html(response)
                $.notify(
                    'The neural network was reset',
                    {
                        position: "bottom right",
                        className: 'success'
                    }
                )
            }
        })
        let loss_function = $('#loss-function').val()
        if(loss_function !== network_architecture.loss_function){
            $.ajax({
                method: 'POST',
                url: '/confirm_network_loss',
                dataType: 'json',
                data:{loss_function: loss_function},
                success: function(){
                    $.notify(
                        'Loss function changed',
                        {
                            position: "bottom right",
                            className: 'success'
                        }
                    )
                }
            })
        }
    })
}

function loadHyperparameters(network_architecture){
    $('#epochs').val(network_architecture.epochs)
    $('#batch-size').val(network_architecture.batch_size)
    $('#learning-rate').val(network_architecture.learning_rate)
}

function loadLossFunction(network_architecture){
    console.log(network_architecture)
    $('#loss-function').val(network_architecture.loss_function)
}


$(document).ready(function(){
    let network_architecture = retrieve_network_architecture()
    addResetBehaviour(network_architecture)
    addConfirmBehaviour(network_architecture.nr_hidden_layers, false)
    loadHyperparameters(network_architecture)
    loadLossFunction(network_architecture)
})