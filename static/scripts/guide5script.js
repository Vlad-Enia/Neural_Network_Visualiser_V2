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
            },
            error: function(){}
        })
    })
}

$(document).ready(function(){
    addFormBehaviour()
})