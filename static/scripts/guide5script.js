function addFormBehaviour(){
    $('#configure-optimizer-form').submit(function(event){
        event.preventDefault()
        let formData = $('#configure-optimizer-form').serialize()

        $.ajax({
            method: 'POST',
            url: '/confirm_optimizer',
            dataType: 'json',
            async: false,
            data: formData,
            success: function(){
                window.location.href='/train'
                // $.notify(
                //     'Hyper-parameters successfully set',
                //     {
                //         position: 'bottom right',
                //         className: 'success'
                //     }
                // )
            },
            error: function(){
                // $.notify(
                //     'Error at configuring hyper-parameters',
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