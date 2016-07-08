$(document).ready(function (){
    var $link_compartilhar = $('#link-compartilhar');

    $link_compartilhar
        .keypress(function (){
            return false;
        })
        .click(function (){
            $link_compartilhar.select();
        });

    var clipboard = new Clipboard('[data-clipboard-target]');
});