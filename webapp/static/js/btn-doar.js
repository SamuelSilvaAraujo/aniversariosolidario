$(document).ready(function () {
    var
        $input_valor_doacao = $('.valor-doacao'),
        $input_outro_valor = $('.outro-valor'),
        numbers_ascii = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57];

    function valorDoacao(valor){
        $input_valor_doacao.val(valor);
        $('[data-btn-valor-docao]').each(function (){
            var $this = $(this);
            if(valor == $this.data('btn-valor-docao')){
                $this
                    .addClass('btn-info')
                    .removeClass('btn-default');
            } else {
                $this
                    .addClass('btn-default')
                    .removeClass('btn-info');
            }
        });
    }

    $('[data-btn-valor-docao]').each(function (){
        var $this = $(this);
        $this.click(function (){
            valorDoacao($this.data('btn-valor-docao'));
        });
    });

    function atualizaOutroValor(){
        valorDoacao($input_outro_valor.val());
    }

    $input_outro_valor
        .keypress(function (e){
            var key = (e.code || e.keyCode || e.which);
            if(numbers_ascii.indexOf(key) == -1){
                return false;
            }
        })
        .keyup(atualizaOutroValor)
        .change(atualizaOutroValor);
});