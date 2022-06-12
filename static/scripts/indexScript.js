function addStartGuideButtonBehaviour(){
    $('#start-guide').click(function(){
        console.log('clicked start guide button')
        window.location = '/guide'
    })
}

function matchImgAndCaptionWidth(){
    $('figcaption').width($('.figure-img').width())
}

$(document).ready(function(){
    addStartGuideButtonBehaviour()
    matchImgAndCaptionWidth()
})