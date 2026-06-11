function addResetBehaviour(){
    $('#reset-btn').click(function(){
        updateTrainData($('#sel_task').val(), $('#sel_net').val())
        showNetworkArchitecture($('#sel_task').val(), $('#sel_net').val())
        $('#train-btn').removeAttr('disabled')
        $('#loss-plot').html('')
        $('#acc-plot').html('')
        $('#act-plot').html('')
        $('#pred-plot').html('')
        $('#acc-table').html('')
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

function drawPlot(){
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

function drawTable() {
    $.ajax({
        method: 'GET',
        async: false,
        url: '/resistance',
        success: function(response){
            values = response.data
        }
    })
    var layout = {
        with: 600,
        height: 200,
        margin: {
            l: 40,
            r: 40,
            t: 20,
            b: 0
        },
        plot_bgcolor: 'rgba(0, 0, 0, 0)',
        paper_bgcolor: 'rgba(0, 0, 0, 0)',
    }
    var data = [{
        type: 'table',
        header: {
            values: [["<b>Model</b>"], ["<b>Normal</b>"],
                ["<b>Stretched</b>"], ["<b>Translated</b>"]],
            align: "center",
            line: {color: 'darkgrey'},
            fill: {color: "rgba(80, 101, 168, 1)"},
            font: {family: "Open Sans", size: 14, color: "white"}
        },
        cells: {
            height: 30,
            values: values,
            align: "center",
            line: {color: "darkgrey"},
            font: {family: "Open Sans", size: 13, color: ["black"]}
        }
    }]
    console.log(data)
    Plotly.newPlot('acc-table', data, layout);
}

function addTrainButtonFunctionality(){
    $('#train-btn').click(function(){
        $('#train-btn').attr('disabled', 'disabled')
        $('#train-btn').html('<i class="fa fa-spinner fa-spin"></i>')
        $.notify(
            'Started training. Please wait',
            {
                position: "bottom right",
                className: 'success'
            }
        )
        let epochs = $('#epochs').val()
        let batch_size = $('#batch-size').val()
        let lr = $('#learning-rate').val()
        $.ajax({
            method: 'POST',
            url: '/train/train_nn',
            dataType: 'json',
            async: true,
            data:{
                epochs: epochs,
                batch_size: batch_size,
                lr: lr
            },
            success: function(){
                $.notify(
                    'Training complete!',
                    {
                        position: "bottom right",
                        className: 'success'
                    }
                )
                $('#train-btn').removeAttr('disabled')
                $('#train-btn').html('Train')
                drawPlot()
                drawTable()
            },
            error: function(){
                $('#train-btn').removeAttr('disabled')
                $('#train-btn').html('Train')
            }
        })
    })
}

function retrieveTrainData(){
    let result;
    $.ajax({
        method: 'GET',
        async: false,
        url: '/train/train_data',
        success: function(response){
            result = response
            $('#sel_task').val(response.task).change()
            $('#sel_net').val(response.net).change()
        }
    })
    return result
}

function updateTrainData(task, net){
    $.ajax({
        method: 'POST',
        url: '/train/train_data',
        dataType: 'json',
        async: false,
        data:{
            task: task,
            net: net
        },
        success: function(){
            $.notify(
                'Updated train data',
                {
                    position: "bottom right",
                    className: 'success'
                }
            )
        }
    })
}

$(document).ready(function(){
    let train_data = retrieveTrainData()
    addResetBehaviour()
    addTrainButtonFunctionality()
})