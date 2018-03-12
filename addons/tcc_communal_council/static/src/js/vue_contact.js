// Define a custom filter called "currency". 

odoo.define('tcc.vue.contact', function (require) {
'use strict';

var Model = require('web.Model');
var Componente = require('tcc.vue.componentes');
var partner=new Model('res.partner')
var partner_data=[]


var templateContact= `<div class="container">
                        <h2>Ejemplo de Contactos Vue + Odoo</h2>
                        <table class="table table-striped">
                        <thead>
                             <tr>
                                <th>Nombre</th>
                                <th>Email</th>
                              </tr>
                            </thead>
                            <tbody>
                            <tr v-for="partner in partners">
                                <td>{{partner.name}}</td>
                                <td v-if="partner.email!=false">{{partner.email}}</td>
                                <td v-else>No tiene Correo</td>
                              </tr>
                            </tbody>
                        </table>
                        </div>`;



Componente.extend.c3=Vue.component('contact', {
template: templateContact,
data: function(){
    this.fetchDataPartner();
    return {partners:[]};
    
  },
methods:{
    fetchDataPartner:function(){
        var $this=this;
        partner.call('search_read',[[],['name','email']]).then(function (data) {
            $this.partners=data;
         });
        }
    },
});

return Componente;
});
