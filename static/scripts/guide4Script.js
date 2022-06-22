

function addFormBehaviour(){
    $('#confirm-network-loss').click(function(){
        let lossFunction = $('#loss-function').val()
        $.ajax({
            method: 'POST',
            url: '/confirm_network_loss',
            dataType: 'json',
            data:{
                'loss_function': lossFunction
            },
            success: function() {
                window.location.href = '/guide/5'
                // $.notify(
                //     'Loss function successfully set',
                //     {
                //         position: 'bottom right',
                //         className: 'success'
                //     }
                // )
            },
            error: function(){
                window.location.href = '/guide/5'
                // $.notify(
                //     'Error at configuring loss function',
                //     {
                //         position: 'bottom right',
                //         className: 'error'
                //     }
                // )
            }
        })
    })
}

$(document).ready(function(){
    addFormBehaviour()
})