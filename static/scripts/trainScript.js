function addResetBehaviour(){
    $('#reset-btn').click(function(){
        showNetworkArchitecture($('#sel_task').val(), $('#sel_net').val() )
        drawPlot()
        // $.ajax({
        //     method: 'GET',
        //     url: '/retrieve_dataset',
        //     async: false,
        //     success: function(response){
        //         $('#configure-dataset-plot-train-div').html(response)
        //         $.notify(
        //             'The neural network was reset',
        //             {
        //                 position: "bottom right",
        //                 className: 'success'
        //             }
        //         )
        //     }
        // })
        // let loss_function = $('#loss-function').val()
        // let learning_rate = $('#learning-rate').val()
        // $.ajax({
        //     method: 'POST',
        //     url: '/confirm_loss_and_lr',
        //     dataType: 'json',
        //     async: false,
        //     data:{
        //         loss_function: loss_function,
        //         learning_rate: learning_rate
        //     },
        //     success: function(){}
        // })
        //
        // $.ajax({
        //     method: 'POST',
        //     url: '/train/create_nn',
        //     async: false,
        //     success: function(){
        //         $.notify(
        //             'The neural network was created',
        //             {
        //                 position: "bottom right",
        //                 className: 'success'
        //             }
        //         )
        //     }
        // })

        // $('#train-btn').removeAttr('disabled')
    })
}

function showNetworkArchitecture(task, net){
    $("#nn-graph-img-pointnet-class").attr('hidden','hidden')
    $("#nn-graph-img-pointnet-seg").attr('hidden','hidden')
    $("#nn-graph-img-gcn-class").attr('hidden','hidden')
    $("#nn-graph-img-gcn-seg").attr('hidden','hidden')

    const img_id = '#nn-graph-img-'+net+'-'+task
    $(img_id).removeAttr('hidden')
}

function drawPlot(path){
    $.ajax({
        method: 'GET',
        async: false,
        url: '/plot',
        success: function(response){
            $('#loss-plot').html(response.fig_loss)
            $('#acc-plot').html(response.fig_acc)
            $('#act-plot').html(response.fig_act)
            $('#pred-plot').html(response.fig_pred)
        }
    })
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

function retrieve_train_data(){
    let result;
    $.ajax({
        method: 'GET',
        async: false,
        url: '/retrieve_train_data',
        success: function(response){
            result = response
            $('#sel_task').val(response.task).change()
            $('#sel_net').val(response.net).change()
        }
    })
    return result
}

$(document).ready(function(){
    let train_data = retrieve_train_data()
    addResetBehaviour()
    // addConfirmBehaviour(network_architecture.nr_hidden_layers, false)
    // loadHyperparameters(network_architecture)
    // loadLossFunction(network_architecture)
    addTrainButtonFunctionality()
})