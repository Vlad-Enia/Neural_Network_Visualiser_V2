function drawGraph(numberOfLayers, layerSizeList){
    const NODE_BORDER_COLOR = '#222222'
    const INPUT_OUTPUT_LAYER_COLOR = 'lightblue'
    const HIDDEN_LAYER_COLOR = 'lightgreen'
    const MAX_NB_OF_NODES_PER_LAYER_THRESHOLD = 7
    const NODE_SPACING = 17.14
    const SPRING_LENGTH = 14.28
    const MIN_CONTAINER_HEIGHT_PER_NODE = 50

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
    for (let layer = 0; layer < numberOfLayers; layer++){
        for (let nodeIndex = 0; nodeIndex < layerSizeList[layer]; nodeIndex++){
            let nodeId = `${layer}_${nodeIndex}`
            let nodeColor;
            if (layer === 0 || layer === (numberOfLayers - 1))
                nodeColor = {border:NODE_BORDER_COLOR, background:INPUT_OUTPUT_LAYER_COLOR}
            else
                nodeColor = {border:NODE_BORDER_COLOR, background:HIDDEN_LAYER_COLOR}
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
    let options = {
        configure: {
            enabled: false
        },
        nodes:{
            shape: 'circle',
            borderWidth: 2,
            scaling: {
                label: {
                    enabled: true,
                    min: 60,
                    max: 60
                }
            },
            value: 1
        },
        edges: {
            color: {
                color: 'black',
            },
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
            }
        },
        interaction: {
            dragNodes: true,
            hideEdgesOnDrag: false,
            hideNodesOnDrag: false
        },
        layout: {
            hierarchical: {
                enabled: true,
                direction: "LR",
                levelSeparation: 400,
                nodeSpacing: 200,
                blockShifting: false,
                edgeMinimization: false,
                parentCentralization: false,
                sortMethod: "hubsize"
            },
            improvedLayout: true,
            randomSeed: 0
        },
        physics: {
            enabled: true,
            stabilization: {
                enabled: true,
                fit: true,
                iterations: 1000,
                onlyDynamicEdges: false,
                updateInterval: 50
            },
            hierarchicalRepulsion: {
                nodeDistance: 120,
                springLength: 100
            },
            solver: 'hierarchicalRepulsion'
        }
    }

    let container = $('#general-nn')

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

    if(maximumNumberOfNeuronsOnALayer > MAX_NB_OF_NODES_PER_LAYER_THRESHOLD){
        let dif = (maximumNumberOfNeuronsOnALayer - MAX_NB_OF_NODES_PER_LAYER_THRESHOLD) * 5.5
        options.physics.hierarchicalRepulsion.nodeDistance += dif
        options.physics.hierarchicalRepulsion.springLength += dif
    }

    new vis.Network(container[0], data, options)
}

$(document).ready(function(){
    drawGraph(3,[20, 6, 1])
})