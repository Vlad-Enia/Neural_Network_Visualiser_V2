function addDatasetLinkHandler(){
    $('.container a').click(function(event){
        event.stopPropagation();
        event.preventDefault()
        $('.container .col').each(function(){
            $(this).removeClass('active')
        })
        $(this).parent().toggleClass("active")
        let imgName = $(this).parent()[0].id

        $.ajax({
            type: 'GET',
            url: '/default_dataset/' + imgName,
            success: function(response){
                $('.configure-dataset-plot').html(response.fig)
                configureForm(imgName, response.params)
                $('.confirm-div #confirm-dataset').removeAttr('hidden')
                $('.confirm-div #confirm-dataset-change').removeAttr('hidden')
            }
        })

    })
}

function configureForm(dataset_name, paramDict){
    $('#dataset-form #dataset-name').attr('value',dataset_name)
    $('#dataset-form .btn').removeAttr('hidden')
    $('#dataset-form input').each(function(){
        $(this).attr('type', 'hidden')
    })
    $('#dataset-form label').each(function(){
       $(this).attr('hidden','hidden')
    })
    $.each(paramDict, function(k, v){
        let inputSelector = `form #${k}`
        let labelSelector = `form #${k}-label`
        $(inputSelector).attr('type', 'number')
        $(inputSelector).attr('value', v)
        $(labelSelector).removeAttr('hidden')
    })
}

function addFormBehaviour(){
    $('#dataset-form').submit(function(event){
        event.preventDefault()
        let formData = $(this).serialize()
        let datasetName = $('#dataset-form #dataset-name').val()
        console.log(datasetName)
        $.ajax({
            type: 'POST',
            url: '/custom_dataset',
            dataType: 'json',
            data: formData,
            success: function(response){
                $('.configure-dataset-plot').html(response.fig)
                configureForm(datasetName, response.params)

            }
        })
    })
}

function addConfirmDatasetHandler(){
    $('.confirm-div #confirm-dataset').click(function(event){
        event.preventDefault()
        let formData = $('#dataset-form').serialize()
        $.ajax({
            type: 'POST',
            url: '/confirm_dataset',
            dataType: 'json',
            data: formData,
            success: function(){
                // $.notify(
                //     'Input dataset successfully configured',
                //     {
                //         position: 'bottom right',
                //         className: 'success'
                //     }
                // )
                window.location.href = '/guide/2'
            },
            error: function(){

                // $.notify(
                //     'Error at configuring input dataset',
                //     {
                //         position: 'bottom right',
                //         className: 'error'
                //     }
                // )
                window.location.href = '/guide/2'
            }
        })
    })

    $('.confirm-div #confirm-dataset-change').click(function(event){
        event.preventDefault()
        let formData = $('#dataset-form').serialize()
        $.ajax({
            type: 'POST',
            url: '/confirm_dataset',
            dataType: 'json',
            data: formData,
            success: function(){
                window.location.href = '/train'
            },
            error: function(){
                window.location.href = '/train'
            }
        })
    })
}



$(document).ready(function(){
    drawPlot('moons_dataset')
    drawPlot('moons_dataset_classified')
    addDatasetLinkHandler()
    addFormBehaviour()
    addConfirmDatasetHandler()
})