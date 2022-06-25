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


//  This method takes as parameters the total number of the layers , a list containing the size of each layer and a container ID,
// and creates a Vis.js representation of it
function drawCustomGraph(numberOfLayers, layerSizeList, containerID){

    // Create the nodeList[] array, for each node generating a unique id of the form 'layer-index_node-index'
    let nodeList = []
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

    // Using the unique node ids generated above, e crate the edges
    // At each for iteration, we create an array containing the nodes on the current level, and another array containing the nodes on the next level
    // We then use these arrays correctly connect the node between the layers
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

    // Here we modify the height of the container based on the maximum number of neurons on a layer
    let maximumNumberOfNeuronsOnALayer = Math.max.apply(null, layerSizeList)
    let containerHeight = MIN_CONTAINER_HEIGHT_PER_NODE * maximumNumberOfNeuronsOnALayer;
    container.css('height',containerHeight)

    // Here we modify the spacing between the nodes on the same layer, based on the maximum number of neurons on a layer
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

// Draw a representation of the Perceptron, with inputSize inputs, followed by a n-th input, with specified labels on the input nodes and the weigh edges.
function drawPerceptron(inputs, inputSize, weights){
    let nodeList = []
    let edgeList = []

    // Configure the node of the Perceptron, with a label illustrating the fhe formula of the weighted sum of the inputs and add it to the nodeList[] array
    let perceptronNode = {
        id: 'p',
        label: 'z = '+decodeURI('%CE%A3')+' xi*wi',
        level: 1,
        color: {border: NODE_BORDER_COLOR, background: HIDDEN_LAYER_COLOR},
    }
    nodeList.push(perceptronNode)

    // Configure the input nodes of the Perceptron and the weight edges, adding them to the nodesList[] and the edgeList[] arrays
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

    // Configure the n-th node, connected with perceptron node through the n-th edge
    let nthInputNode = {id: 'x_n', label: 'xn', level: 0, color: {border: NODE_BORDER_COLOR, background: INPUT_OUTPUT_LAYER_COLOR},}
    let lastNumberedInputNode = nodeList[nodeList.length - 1]
    // The dashed edge is the 3 points between the last input node and the n-th input node
    let dashedEdge = {from: lastNumberedInputNode.id, to: nthInputNode.id, dashes: [0.1, 15], arrows: {to: {enabled: false}}, width: 5}
    let nthEdge = {from: nthInputNode.id, to: perceptronNode.id, label: 'wn'}
    nodeList.push(nthInputNode)
    edgeList.push(dashedEdge)
    edgeList.push(nthEdge)

    // The box on the right part of the figure, illustrating the binary step activation function of the perceptron
    let activationFunctionBox = {
        id: 'invisible',
        shape: 'box',
        label:
            '                  1, if z >= threshold \n y = f(z) =  \n                  0, otherwise',
        level: 2,
        font:{
            align: 'left'
        },
        color:{border: NODE_BORDER_COLOR, background: 'whitesmoke'}}
    nodeList.push(activationFunctionBox)
    let outputEdge = {from: perceptronNode.id, to: activationFunctionBox.id}
    edgeList.push(outputEdge)

    // Configure the vis.js figure, using the nodeList[] and the edgeList[] arrays that we populated above,
    // the id of the container HTML element and the options object presented in vis.js section of the second
    // chapter of the thesis
    let data = {nodes: new vis.DataSet(nodeList), edges: new vis.DataSet(edgeList)}
    let container = $('#perceptron-div')
    let containerElement = $('#perceptron-div')[0]

    let maximumNumberOfNeuronsOnALayer = inputSize + 2
    let containerHeight = MIN_CONTAINER_HEIGHT_PER_NODE * maximumNumberOfNeuronsOnALayer;
    container.css('height',containerHeight)

    new vis.Network(containerElement, data, options)
}