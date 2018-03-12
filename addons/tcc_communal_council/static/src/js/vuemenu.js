// Define a custom filter called "currency". 
odoo.define('tcc.vue.website', function (require) {
'use strict';

var Model = require('web.Model');
var ajax = require("web.ajax");
var Componentes = require("tcc.vue.componentes");


ajax.jsonRpc("/menudata", "call").then(function (data) {
       var template='<div class="row">'
                        +'<div class="col-md-3 " id="vuemenu">'
                            +'<ul>'
                                +'<li v-for="menu in menus" v-on:click="toggleActive(menu)" v-bind:class="{ \'active\': menu.new_window}">'
                                    +'{{menu.name}}'
                                +'</li>'
                            +'</ul>'
                        +'</div>'
                        +'<div class="col-md-9" >'
                        +'<component v-bind:is="currentView">'
                        +'</component>'
                        +'</div>'
                    +'</div>';
        var demo = new Vue({
            el: '#app',
            template:template,
            data: {
                menus:data,
                currentView: 'home'
            },
            components:Componentes.extend,
            methods: {
                toggleActive: function(m){
                    this.currentView='c'+String(m.id)
                    this.menus.forEach(function(m){
                        if (m.new_window){
                            m.new_window = !m.new_window;
                        }
                    });
                    m.new_window = !m.new_window;
                }
            }
        });
});




});
