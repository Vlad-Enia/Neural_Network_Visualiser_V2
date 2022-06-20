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

function addFormBehaviour() {
    $('.configure-nn-form').submit(function (event) {
        event.preventDefault()
        let nrLayers = parseInt($('#n-layers-input').val())
        let layerSizeList = [2]
        for (let i = 1; i <= nrLayers; i++) {
            let inputId = '#layer-' + i
            let layerSize = parseInt($(inputId).val())
            layerSizeList.push(layerSize)
        }
        nrLayers += 2;
        layerSizeList.push(1)
        drawCustomGraph(nrLayers, layerSizeList, '#nn-graph-canvas-div')
    })
}

function addConfirmBehaviour() {
    $('.confirm-div #confirm-network-architecture').click(function (event) {
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
            // dataType: 'json',
            data: {
                'nrHiddenLayers': nrHiddenLayers,
                'hiddenLayerSizeList': hiddenLayerSizeList
            },
            success: function(response){
                window.location.href = '/guide/3'
            }
        })
    })
}

$(document).ready(function () {
    onInputChange()
    addFormBehaviour()
    addConfirmBehaviour()
})