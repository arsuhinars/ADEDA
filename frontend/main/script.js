import { tryToLogin } from "../js/auth.js"

$(document).ready(function() {
    $("#loginLink").click(function( event ){
           event.preventDefault();
           $(".overlay").fadeToggle("fast");
     });

    $(".overlayLink").click(function(event){
        event.preventDefault();
        var action = $(this).attr('data-action');

        $("#loginTarget").load("ajax/" + action);

        $(".overlay").fadeToggle("fast");
    });

    $(".close").click(function(){
        $(".overlay").fadeToggle("fast");
    });

    $(document).keyup(function(e) {
        if(e.keyCode == 27 && $(".overlay").css("display") != "none" ) { 
            event.preventDefault();
            $(".overlay").fadeToggle("fast");
        }
    });

    document.querySelector('#login-form').addEventListener('submit', (ev) => {
        let formData = new FormData(ev.target)

        tryToLogin(
            formData.get('login'),
            formData.get('password')
        ).then(() => {
            window.location.href = '/import'
        }).catch(() => {
            $(".overlay").fadeToggle("fast");
        })

        ev.preventDefault()
    })
});
