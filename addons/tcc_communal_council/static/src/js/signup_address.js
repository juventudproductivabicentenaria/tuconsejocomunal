odoo.define('tcc_communal_council.signup_address', function (require) {
    var ajax = require('web.ajax');
    $(document).ready(function () {
            var $state_id=$('#state_id');
            var $municipality=$("#municipality_id");
            if ($state_id.length){
                $state_id.select2({
                    placeholder: "Seleccione el estado",
                    }).on("change", function (e) {
                          $municipality.find('option').remove()
                          ajax.jsonRpc('/web/signup/municipality', 'call', {'state_id':e.val})
                            .then(function (resp) {
                                append_select(resp['data'],$municipality)
                                $municipality.select2()
                                
                                
                    });
                    });
              }

    var append_select=function(data,select){
         $.each(data, function (index, value) {
            select.append($('<option>', { 
                value: value[0],
                text : value[1] 
            }));
        });
        }

            
        });
});

