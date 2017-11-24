openerp.jsonRpc('/web-service', 'call',datas).then(function (respuesta) {
            console.log (respuesta);
         // lógica de retorno del servidor 
            
      }).fail(function (source, error) {
           //si hubo error
    }
)

//~ function cargar(){
            //~ var url="/web-service"
            //~ $.ajax({   
                //~ type: "GET",
                //~ url:url,
                //~ success: function(datos){       
                    //~ console.log (datos);
                //~ }
            //~ });
        //~ }
//~ 
//~ cargar();
