// Define a custom filter called "currency". 

odoo.define('tcc.vue.componentes', function (require) {
'use strict';

var Model = require('web.Model');
var ajax = require("web.ajax");
function OdooVueComponent(){};

OdooVueComponent.extend={'c2':Vue.component('home', {
template: '<h3>Ejemplo de Propuesta FUncional Vue + Odoo! </br> {{msj}}</h3>',
data: function () {
    return {msj:'Hola mundo'}
  }
})
};

return OdooVueComponent;
});
