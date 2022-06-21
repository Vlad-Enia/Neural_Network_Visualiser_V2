function addFormBehaviour(){
    $('#confirm-network-loss').click(function(event){
        event.preventDefault()
        console.log('ceva')

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
            },
            error: function(){
                window.location.href = '/guide/5'
            }
        })
    })
}

$(document).ready(function(){
    addFormBehaviour()
})