function onInputChange() {
    $('#n-layers-input').on('input', function (value) {
        let nrLayers = parseInt($('#n-layers-input').val())
        for (let i = 1; i <= nrLayers; i++) {
            let inputId = '#layer-' + i
            let labelId = '#layer-' + i + '-label'
            $(inputId).attr('type', 'number')
            $(labelId).removeAttr('hidden')
        }
        for (let i = nrLayers + 1; i <= 6; i++) {
            let inputId = '#layer-' + i
            let labelId = '#layer-' + i + '-label'
            $(inputId).attr('type', 'hidden')
            $(labelId).attr('hidden', 'hidden')
        }
    })
}

function retrieveDatasetParams(){
    let dataset_params
    $.ajax({
        async: false,
        method: 'GET',
        url: '/retrieve_dataset_params',
        success: function(response){
            dataset_params = response
        },
        error: function(){
            console.log('error')
        }
    })
    return dataset_params
}


function addFormBehaviour(containerId, href) {
    $('.configure-nn-form').submit(function (event) {
        event.preventDefault()
        let dataset_params = retrieveDatasetParams()
        let n_colors = dataset_params['n_colors']
        let nrLayers = parseInt($('#n-layers-input').val())
        let layerSizeList = [2]
        for (let i = 1; i <= nrLayers; i++) {
            let inputId = '#layer-' + i
            let layerSize = parseInt($(inputId).val())
            layerSizeList.push(layerSize)
        }
        nrLayers += 2;
        let outputLayerSize;
        if(n_colors === 2)
            outputLayerSize = 1
        else
            outputLayerSize = n_colors
        layerSizeList.push(outputLayerSize)
        drawCustomGraph(nrLayers, layerSizeList, containerId)
        addConfirmBehaviour(outputLayerSize, href)
    })
}

function addConfirmBehaviour(outputLayerSize, href) {
    let confirmButton =  $('.confirm-div #confirm-network-architecture')
    confirmButton.removeAttr('hidden')
    confirmButton.click(function (event) {
        event.preventDefault()
        let nrHiddenLayers = parseInt($('#n-layers-input').val())
        let hiddenLayerSizeList = []
        for (let i = 1; i <= nrHiddenLayers; i++){
            let inputId = '#layer-' + i
            let layerSize = parseInt($(inputId).val())
            hiddenLayerSizeList.push(layerSize)
        }
        console.log(hiddenLayerSizeList)
        $.ajax({
            type: 'POST',
            url: '/confirm_network_architecture',
            data: {
                'nr_hidden_layers': nrHiddenLayers,
                'hidden_layer_size_list': hiddenLayerSizeList,
                'output_layer_size': outputLayerSize
            },
            success: function(response){
                window.location.href = href
            },
            error: function(response){
                window.location.href = href
            }
        })
    })
}