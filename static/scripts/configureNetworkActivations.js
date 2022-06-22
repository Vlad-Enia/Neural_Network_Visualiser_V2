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

function addActivationValuesInForm(nrHiddenLayers,hiddenActivations, outputLayerActivation){
    for(let i = 1; i <= nrHiddenLayers; i++){
        let labelSelector = '#layer-' + i + '-activation-label'
        let inputSelector = '#layer-' + i + '-activation'
        $(inputSelector).val(hiddenActivations[i-1])
        $(inputSelector).removeAttr('hidden')
        $(labelSelector).removeAttr('hidden')
    }
    $('#layer-out-activation').val(outputLayerActivation)
    $('#layer-out-activation').removeAttr('hidden')
    $('#layer-out-activation-label').removeAttr('hidden')
}

function addConfirmBehaviour(nrHiddenLayers, redirect){
    $('#confirm-network-activations').click(function(event){
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
                if(redirect===true)
                    window.location.href = '/guide/4'
                $.notify(
                    'Activation functions set successfully',
                    {
                        position: 'bottom-right',
                        className: 'success'
                    }
                )
            },
            error: function(){
                if(redirect===true)
                    window.location.href = '/guide/4'
                $.notify(
                    'Error at setting activation functions',
                    {
                        position: 'bottom-right',
                        className: 'error'
                    }
                )
            }
        })
    })
}