function configureForm(network_architecture){
    let nrHiddenLayers = network_architecture.nr_hidden_layers
    let hiddenLayersSizeList = network_architecture.hidden_layer_size_list


    $('#n-layers-input').val(nrHiddenLayers)
    for(let i=1; i<= nrHiddenLayers; i++){
        let inputSelector = '#layer-' + i
        let labelSelector = '#layer-' + i + '-label'
        console.log(inputSelector)
        $(inputSelector).attr('type','number')
        $(inputSelector).val(hiddenLayersSizeList[i-1])
        $(labelSelector).removeAttr('hidden')
    }

    let nrLayers = nrHiddenLayers + 2
    hiddenLayersSizeList.unshift(2)
    let outputLayerSize = network_architecture.output_layer_size
    hiddenLayersSizeList.push(outputLayerSize)

    drawCustomGraph(nrLayers, hiddenLayersSizeList, '#nn-graph-div')
}

$(document).ready(function () {
    let network_architecture = retrieve_network_architecture()
    configureForm(network_architecture)
    onInputChange()
    addFormBehaviour('#nn-graph-div', '/train')
})