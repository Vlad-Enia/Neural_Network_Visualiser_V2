function addResetBehaviour(){
    $('#reset-btn').click(function(){
        let network_architecture = retrieve_network_architecture()
        drawGraph(network_architecture, '#nn-graph-train-div')
        addActivationValuesInForm(network_architecture.nr_hidden_layers, network_architecture.hidden_layer_activation_list, network_architecture.output_layer_activation)
        $('#confirm-network-activations').removeAttr('hidden')
        $.ajax({
            method: 'GET',
            url: '/retrieve_dataset',
            async: false,
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
        let learning_rate = $('#learning-rate').val()
        $.ajax({
            method: 'POST',
            url: '/confirm_loss_and_lr',
            dataType: 'json',
            async: false,
            data:{
                loss_function: loss_function,
                learning_rate: learning_rate
            },
            success: function(){}
        })

        $.ajax({
            method: 'POST',
            url: '/train/create_nn',
            async: false,
            success: function(){
                $.notify(
                    'The neural network was created',
                    {
                        position: "bottom right",
                        className: 'success'
                    }
                )
            }
        })

        $('#train-btn').removeAttr('disabled')
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

function addTrainButtonFunctionality(){
    $('#train-btn').click(function(){
        let epochs = $('#epochs').val()
        let batch_size = $('#batch-size').val()
        $.notify(
            'Started training. Please wait',
            {
                position: "bottom right",
                className: 'success'
            }
        )
        $.ajax({
            method: 'POST',
            url: '/train/train_nn',
            dataType: 'json',
            async: false,
            data:{
                epochs: epochs,
                batch_size: batch_size
            },
            success: function(){
                $.notify(
                    'Training complete!',
                    {
                        position: "bottom right",
                        className: 'success'
                    }
                )
            }
        })
        getDecisionSurface()
        getLossPlot()
        getValLossPlot()
    })
}

function getLossPlot(){
    $.ajax({
        method: 'GET',
        async: false,
        url: '/train/get_loss',
        success: function(response){
            $('#train-loss-plot').html(response)
        }
    })
}

function getValLossPlot(){
    $.ajax({
        method: 'GET',
        async: false,
        url: '/train/get_val_loss',
        success: function(response){
            $('#test-loss-plot').html(response)
        }
    })
}

function getDecisionSurface(){
    console.log('log')
    $.ajax({
        method: 'GET',
        async: false,
        url: '/train/get_decision_surface',
        success: function(response){
            $('#configure-dataset-plot-train-div').html(response)
        }
    })
}


$(document).ready(function(){
    let network_architecture = retrieve_network_architecture()
    addResetBehaviour()
    addConfirmBehaviour(network_architecture.nr_hidden_layers, false)
    loadHyperparameters(network_architecture)
    loadLossFunction(network_architecture)
    addTrainButtonFunctionality()
})