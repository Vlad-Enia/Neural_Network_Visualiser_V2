const NODE_BORDER_COLOR = '#222222'
const INPUT_OUTPUT_LAYER_COLOR = 'lightblue'
const HIDDEN_LAYER_COLOR = 'lightgreen'
const MAX_NB_OF_NODES_PER_LAYER_THRESHOLD = 7
const DEFAULT_NODE_DISTANCE = 120
const DEFAULT_SPRING_LENGTH = 100
const MIN_CONTAINER_HEIGHT_PER_NODE = 70


let options = {
        configure: {
            enabled: false
        },
        nodes:{
            shape: 'circle',
            borderWidth: 2,
            label: '',
            margin: 20,
            value: 1,
            scaling: {
                label: {
                    enabled: true,
                    min: 30,
                    max: 30
                }
            },
            color: {border: NODE_BORDER_COLOR,},
        },
        edges: {
            color: 'black',
            width: 1,
            selectionWidth: function (width) {return width*5;},
            smooth: {
                enabled: false,
                type: "horizontal"
            },
            arrows: {
                to: {
                    enabled: true,
                    scaleFactor: 0.5
                }
            },
            font: {
                size: 30,
                face: 'consolas',
                color: 'black',
                strokeWidth: 20,
                strokeColor: 'whitesmoke'
            }
        },
        layout: {
            hierarchical: {
                enabled: true,
                direction: "LR",
                levelSeparation: 400,
                blockShifting: true,
                edgeMinimization: false,
                parentCentralization: false,
            },
        },
        physics: {
            enabled: true,
            solver: 'hierarchicalRepulsion',
            hierarchicalRepulsion: {
                nodeDistance: 120,
                springLength: 100
            }
        }
    }


function drawCustomGraph(numberOfLayers, layerSizeList, containerID){
    // var nodeList = [
    //     {"id: "0_0", "level: 0, "color: {"border:NODE_BORDER_COLOR, 'background':INPUT_OUTPUT_LAYER_COLOR}},
    //     {"id: "0_1", "level: 0, "color: {"border:NODE_BORDER_COLOR, 'background':INPUT_OUTPUT_LAYER_COLOR}},
    //     {"id: "0_2", "level: 0, "color: {"border:NODE_BORDER_COLOR, 'background':INPUT_OUTPUT_LAYER_COLOR}},
    //     {"id: "0_3", "level: 0, "color: {"border:NODE_BORDER_COLOR, 'background':INPUT_OUTPUT_LAYER_COLOR}},
    //
    //     {"id: "1_0", "level: 1, "color: {"border:NODE_BORDER_COLOR, 'background':HIDDEN_LAYER_COLOR}},
    //     {"id: "1_1", "level: 1, "color: {"border:NODE_BORDER_COLOR, 'background':HIDDEN_LAYER_COLOR}},
    //     {"id: "1_2", "level: 1, "color: {"border:NODE_BORDER_COLOR, 'background':HIDDEN_LAYER_COLOR}},
    //     {"id: "1_3", "level: 1, "color: {"border:NODE_BORDER_COLOR, 'background':HIDDEN_LAYER_COLOR}},
    //     {"id: "1_4", "level: 1, "color: {"border:NODE_BORDER_COLOR, 'background':HIDDEN_LAYER_COLOR}},
    //     {"id: "1_5", "level: 1, "color: {"border:NODE_BORDER_COLOR, 'background':HIDDEN_LAYER_COLOR}},
    //
    //     {"id: "2_0", "level: 2, "color: {"border:NODE_BORDER_COLOR, 'background':INPUT_OUTPUT_LAYER_COLOR}},
    //     {"id: "2_1", "level: 2, "color: {"border:NODE_BORDER_COLOR, 'background':INPUT_OUTPUT_LAYER_COLOR}}
    // ]
    // var edges = new vis.DataSet([
    //     {"from: "0_0", "to: "1_0"},
    //     {"from: "0_0", "to: "1_1"},
    //     {"from: "0_0", "to: "1_2"},
    //     {"from: "0_0", "to: "1_3"},
    //     {"from: "0_0", "to: "1_4"},
    //     {"from: "0_0", "to: "1_5"},
    //
    //     {"from: "0_1", "to: "1_0"},
    //     {"from: "0_1", "to: "1_1"},
    //     {"from: "0_1", "to: "1_2"},
    //     {"from: "0_1", "to: "1_3"},
    //     {"from: "0_1", "to: "1_4"},
    //     {"from: "0_1", "to: "1_5"},
    //
    //     {"from: "0_2", "to: "1_0"},
    //     {"from: "0_2", "to: "1_1"},
    //     {"from: "0_2", "to: "1_2"},
    //     {"from: "0_2", "to: "1_3"},
    //     {"from: "0_2", "to: "1_4"},
    //     {"from: "0_2", "to: "1_5"},
    //
    //     {"from: "0_3", "to: "1_0"},
    //     {"from: "0_3", "to: "1_1"},
    //     {"from: "0_3", "to: "1_2"},
    //     {"from: "0_3", "to: "1_3"},
    //     {"from: "0_3", "to: "1_4"},
    //     {"from: "0_3", "to: "1_5"},
    //
    //     {"from: "1_0", "to: "2_0"},
    //     {"from: "1_0", "to: "2_1"},
    //
    //     {"from: "1_1", "to: "2_0"},
    //     {"from: "1_1", "to: "2_1"},
    //
    //     {"from: "1_2", "to: "2_0"},
    //     {"from: "1_2", "to: "2_1"},
    //
    //     {"from: "1_3", "to: "2_1"},
    //     {"from: "1_3", "to: "2_0"},
    //
    //     {"from: "1_4", "to: "2_1"},
    //     {"from: "1_4", "to: "2_0"},
    //
    //     {"from: "1_5", "to: "2_0"},
    //     {"from: "1_5", "to: "2_1"},
    // ]);
    let nodeList = []
    console.log(layerSizeList)
    for (let layer = 0; layer < numberOfLayers; layer++){
        for (let nodeIndex = 0; nodeIndex < layerSizeList[layer]; nodeIndex++){
            let nodeId = `${layer}_${nodeIndex}`
            let nodeColor;
            if (layer === 0 || layer === (numberOfLayers - 1))
                nodeColor = {background:INPUT_OUTPUT_LAYER_COLOR}
            else
                nodeColor = {background:HIDDEN_LAYER_COLOR}
            let node = {id: nodeId, level: layer, color: nodeColor}
            nodeList.push(node)
        }
    }

    let edgeList = []
    for (let layer = 0; layer < numberOfLayers-1; layer++){
        let fromLayerNodeList = nodeList.filter(element => element.level === layer)
        let toLayerNodeList = nodeList.filter(element => element.level === layer+1)

        fromLayerNodeList.forEach(function(fromNode){
            toLayerNodeList.forEach(function(toNode){
                let edgeId = `${fromNode.id}-${toNode.id}`
                let edge = {id: edgeId, from: fromNode.id, to: toNode.id}
                edgeList.push(edge)
            })
        })
    }

    let nodes = new vis.DataSet(nodeList)
    let edges = new vis.DataSet(edgeList)

    let data = {nodes: nodes, edges: edges};


    let container = $(containerID)

    let maximumNumberOfNeuronsOnALayer = Math.max.apply(null, layerSizeList)
    let containerHeight = MIN_CONTAINER_HEIGHT_PER_NODE * maximumNumberOfNeuronsOnALayer;
    container.css('height',containerHeight)

    // if(maximumNumberOfNeuronsOnALayer <= 7){
    //     options.physics.hierarchicalRepulsion.nodeDistance = 120
    //     options.physics.hierarchicalRepulsion.springLength = 100
    // }
    // else if(maximumNumberOfNeuronsOnALayer <= 10){
    //     options.physics.hierarchicalRepulsion.nodeDistance = 130
    //     options.physics.hierarchicalRepulsion.springLength = 110
    // }
    // else if(maximumNumberOfNeuronsOnALayer <= 13){
    //     options.physics.hierarchicalRepulsion.nodeDistance = 160
    //     options.physics.hierarchicalRepulsion.springLength = 160
    // }
    //
    // else if(maximumNumberOfNeuronsOnALayer <= 16){
    //     options.physics.hierarchicalRepulsion.nodeDistance = 180
    //     options.physics.hierarchicalRepulsion.springLength = 180
    // }
    //
    // else if(maximumNumberOfNeuronsOnALayer <= 20){
    //     options.physics.hierarchicalRepulsion.nodeDistance = 200
    //     options.physics.hierarchicalRepulsion.springLength = 200
    // }

    options.physics.hierarchicalRepulsion.nodeDistance = DEFAULT_NODE_DISTANCE
    options.physics.hierarchicalRepulsion.springLength = DEFAULT_SPRING_LENGTH

    if(maximumNumberOfNeuronsOnALayer > MAX_NB_OF_NODES_PER_LAYER_THRESHOLD){
        let dif = (maximumNumberOfNeuronsOnALayer - MAX_NB_OF_NODES_PER_LAYER_THRESHOLD) * 7
        options.physics.hierarchicalRepulsion.nodeDistance += dif
        options.physics.hierarchicalRepulsion.springLength += dif
    }

    new vis.Network(container[0], data, options)
}

function retrieve_network_architecture(){
    let result;
    $.ajax({
        method: 'GET',
        async: false,
        url: '/retrieve_network_architecture',
        success: function(response){
            result = response
            console.log(response)
        }
    })
    return result
}

function drawGraph(network_architecture, containerId){
    let nrHiddenLayers = network_architecture.nr_hidden_layers
    let LayerSizeList = network_architecture.hidden_layer_size_list
    let outputLayerSize = network_architecture.output_layer_size

    let nrLayers = nrHiddenLayers+=2
    LayerSizeList.unshift(2)
    LayerSizeList.push(outputLayerSize)
    drawCustomGraph(nrLayers, LayerSizeList, containerId)
}

function drawPerceptron(inputs, inputSize, weights){
    let nodeList = []
    let edgeList = []

    let perceptronNode = {
        id: 'p',
        label: 'z = '+decodeURI('%CE%A3')+' xi*wi',
        level: 1,
        color: {border: NODE_BORDER_COLOR, background: HIDDEN_LAYER_COLOR},
    }
    nodeList.push(perceptronNode)

    for (let i=0; i<inputSize; i++){
        let nodeId = `x_${i}`
        let nodeLabel = inputs[i]
        let node = {
            id: nodeId,
            label: nodeLabel,
            level: 0,
            color: {border: NODE_BORDER_COLOR, background: INPUT_OUTPUT_LAYER_COLOR},
        }
        nodeList.push(node)

        let edge = {from: nodeId, to: perceptronNode.id, label: weights[i]}
        edgeList.push(edge)
    }

    let nthInputNode = {id: 'x_n', label: 'xn', level: 0, color: {border: NODE_BORDER_COLOR, background: INPUT_OUTPUT_LAYER_COLOR},}
    let lastNumberedInputNode = nodeList[nodeList.length - 1]
    let dashedEdge = {from: lastNumberedInputNode.id, to: nthInputNode.id, dashes: [0.1, 15], arrows: {to: {enabled: false}}, width: 5}
    let nthEdge = {from: nthInputNode.id, to: perceptronNode.id, label: 'wn'}
    nodeList.push(nthInputNode)
    edgeList.push(dashedEdge)
    edgeList.push(nthEdge)

    let invisibleNode = {
        id: 'invisible',
        shape: 'box',
        label:
            '                  1, if z >= threshold \n y = f(z) =  \n                  0, otherwise',
        level: 2,
        font:{
            align: 'left'
        },
        color:{border: NODE_BORDER_COLOR, background: 'whitesmoke'}}
    nodeList.push(invisibleNode)
    let outputEdge = {from: perceptronNode.id, to: invisibleNode.id}
    edgeList.push(outputEdge)

    let data = {nodes: new vis.DataSet(nodeList), edges: new vis.DataSet(edgeList)}
    let container = $('#perceptron-div')
    let containerElement = $('#perceptron-div')[0]

    let maximumNumberOfNeuronsOnALayer = inputSize + 2
    let containerHeight = MIN_CONTAINER_HEIGHT_PER_NODE * maximumNumberOfNeuronsOnALayer;
    container.css('height',containerHeight)

    new vis.Network(containerElement, data, options)
}