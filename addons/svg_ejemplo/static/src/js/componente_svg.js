odoo.define('snap.svg', function (require) {
'use strict';
var Componente = require('tcc.vue.componentes');

var svg=function(g,a,d,f,e,divId,w,h){
         var $div=$(divId);
         var s1=Snap().attr({
            width:w,
            height:h
             });
         s1.append(g);
         var secondScene = new Snap.Matrix();
         secondScene.a=a;
         secondScene.d=d;
         secondScene.f=f;
         secondScene.e=e;
         g.attr({transform: secondScene});
         $div.append(s1.node)
         }


var templateSvg= `<div class="jumbotron">
                      <div class="container text-center">
                        <h1>Dise&ntilde;o Imagen SVG</h1>      
                        <p>En este ejemplo se muetra un dise&ntilde;o con una imagenes vectorial en formato svg de 3.9 kb.</p>
                      </div>
                      <div class="row">
                      <div class="col-md-1" id="div1"></div>
                      <div class="col-md-2" id="div2"></div>
                      <div class="col-md-3" id="div3"></div>
                      <div class="col-md-6" id="div4"></div>
                    </div>
                      
                      <div class="row">
                      <div class="col-md-12 center" id="div5"></div>
                    </div>
                    </div>`;

Componente.extend.c10=Vue.component('pruebasvg', {
template: templateSvg,
data: function(){
    this.fetchLoadSvg();
    return {partners:[]};
    
  },
methods:{
    fetchLoadSvg:function(){
        Snap.load("/svg_ejemplo/static/img/prueba2.svg", function (f) {
         var g=f.select("#g3");
         svg(g,150,150,-10,-15,'#div1',100,100);
         var g2=g.clone()
         svg(g2,300,300,-40,-40,'#div2',200,100);
         var g3=g2.clone()
         svg(g2,600,600,-120,-130,'#div3',200,100);
         var g4=g3.clone()
         svg(g4,1200,1200 ,-240,-240,'#div4',200,160);
         var g5=g4.clone()
         svg(g5,3900,3900 ,-740,-840,'#div5',500,600);
         });
        console.log('Load svg')
        }
    },
});

return Componente;
});
