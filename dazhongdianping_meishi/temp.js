!function(){"use strict";function n(n){return""}function t(){return location}function e(){return window}function r(){return document}function i(){return navigator}function u(){var n=e();return n.XMLHttpRequest}function o(){var n=ui.get(Cr);if(n){var t=n.split("|");return{mis:t[0],env:t[1]||""}}return n||{}}function a(n){var t="v2/api/"+jr+"/validate",e="validate-ocean"+Dr,r=0===I().indexOf("http:"),i=r?"http:":"https:",u=i+"//"+n+"/",a=j(),c=a.match(Tr)||[],s=o(),f=void 0,d=void 0;if(d=c&&c[1]||s.mis||""){ui.set(Cr,d+"|"+(f||""),Lr);var l=e;u=i+"//"+l+"/"+t+"?mis="+d}return u}function c(n){Nr=n}function s(){return Nr===Bt}function f(n){return Mr&&!n||(Mr=a(Er)),Mr}function d(n){if(!Vr||n){var t="wreport.meituan.net";Vr=a(t)}return Vr}function l(){}function v(n){return"undefined"==typeof n?"undefined":Br(n)}function h(n,t){return v(n)===t}function p(){return+new Date}function g(){return Math.random()}function m(n){return h(n,"number")}function _(n){return!n&&h(n,"object")}function y(n){var t="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",e=void 0,r=void 0,i=void 0,u=void 0,o=void 0,a=void 0,c=void 0,s=void 0,f=0,d=0,l="",v=[];if(!n)return n;n=w(n);do e=n.charCodeAt(f++),r=n.charCodeAt(f++),i=n.charCodeAt(f++),s=e<<16|r<<8|i,u=s>>18&63,o=s>>12&63,a=s>>6&63,c=63&s,v[d++]=t.charAt(u)+t.charAt(o)+t.charAt(a)+t.charAt(c);while(f<n.length);switch(l=v.join(""),n.length%3){case 1:l=l.slice(0,-2)+"==";break;case 2:l=l.slice(0,-1)+"="}return l}function w(n){n=(n+"").replace(/\r\n/g,"\n").replace(/\r/g,"\n");var t="",e=void 0,r=void 0,i=0,u=void 0;for(e=r=0,i=n.length,u=0;u<i;u++){var o=n.charCodeAt(u),a=null;o<128?r++:a=o>127&&o<2048?String.fromCharCode(o>>6|192,63&o|128):String.fromCharCode(o>>12|224,o>>6&63|128,63&o|128),null!==a&&(r>e&&(t+=n.substring(e,r)),t+=a,e=r=u+1)}return r>e&&(t+=n.substring(e,n.length)),t}function b(n,t){var e=void 0,r=ii.find(n,function(n){return ri.attr(n,"name")===t});return r&&(e=ri.attr(r,"content")),e}function x(){var n=Ur[Rt];return Ur[n]}function S(n){var t=void 0,e=oi.get(),r=p();if(n&&e)t=e,oi.update(r);else{var i=x(),u=Ur.performance&&Ur.performance.timing;t=u&&u.requestStart,t||(t=i?i.l:ni),oi.update(r)}return r-t}function q(n){var t={duration:S(!0===n)},e=void 0,r=ri.isFunc(Pr.quit);return r&&(e=r()),t=ri.extend(t,e||{})}function k(n,t){!t[Ke]}function A(n){return n<2036}function O(n){for(var t=n.length,e=t,r=0;r<t;r++){var i=n.charCodeAt(r);i>127&&e++}return A(1.5*e)}function I(){return Qr.protocol}function j(){return Qr.search}function C(n,t){var e=void 0,r=Ar+ai++;if(t=t||0,!(t>2))return Ur[r]=e=new Image,e.onload=function(){Ur[r]=null},e.onabort=e.onerror=function(){Ur[r]=null,C(n,++t)},e.src=n,e}function D(n){if(!n)return Kr;var t=Kr,e=/^utm_(source|medium|term|content|campaign)$/;return ii.each(n,function(n,r){e.test(r)&&(!t&&(t={}),t[r]=n)}),t}function E(){return"daum:q eniro:search_word naver:query pchome:q images.google:q google:q yahoo:p msn:q bing:q aol:query aol:q lycos:q lycos:query ask:q cnn:query virgilio:qs baidu:wd baidu:word alice:qs yandex:text najdi:q seznam:q rakuten:qt biglobe:q goo.ne:MT search.smt.docomo:MT onet:qt onet:q kvasir:q terra:query rambler:query conduit:q babylon:q search-results:q avg:q comcast:q incredimail:q startsiden:q go.mail.ru:q centrum.cz:q 360.cn:q sogou:query tut.by:query globo:q ukr:q so.com:q haosou.com:q auone:q m.baidu:word wap.baidu:word baidu:word Baidu:bs www.soso:w wap.soso:key www.sogou:query wap.sogou:keyword m.so:q m.sogou:keyword so.com:pq youdao:q sm.cn:q sm.cn:keyword haosou:q".split(" ")}function F(n){var t=ri.parseQuery(n);return D(t)}function T(n){var t=Kr,e=n.match(/^[\w-]+:\/\/([^\/]+)(?:\/([^?]+)?)?/),r=e&&e[1];if(r){var i=ri.parseQuery(n),u=E(),o="",a="";ii.each(u,function(n){var t=n.split(":"),e=t[0],u=t[1],c=i[u],s=-1<e.indexOf(".")?e:"."+e+".";if(-1<r.indexOf(s.toLowerCase())&&(a=e,o=c))return!1}),a&&(t={},t[qi]=a,t[ki]="organic",o&&(t[Ai]=o))}return t}function L(n){if(n){ji=n;var t=ri.stringifyQuery(n);return ui.del(ur,Xr),ui.top(ur,t,er,Xr),!0}return!1}function N(){var n=ui.get(ur);if(!he.test(n))return ji;var t=ri.isStr(n)?ri.parseQuery(n):null;return D(t)}function M(){var n=void 0,t=/(utmc(tr|sr|cn|md|ct))=([^|()]+)/g,e=ui.get("__utmz"),r=e&&e.match(t);return r&&ii.each(r,function(t){var e=t.split("="),r=e[0],i=void 0,u=e[1]||"";"utmcsr"===r?i=qi:"utmccn"===r?i=Oi:"utmcmd"===r?i=ki:"utmcct"===r?i=Ii:"utmctr"===r&&(i=Ai),i&&(n=n||{},n[i]=u)}),n}function V(n,t){return(!ji&&!Ci||n)&&(n=n||Qr.href,t=t||Hr.referrer,ji=F(n)||T(t),ji?L(ji):ji=N(),ji||(ji=M(),L(ji)),Ci=Vt),ji}function P(n){return Fi+n}function R(){return{length:0,_data:{},setItem:function(n,t){return this.length++,this._data[n]=String(t)},getItem:function(n){return this._data.hasOwnProperty(n)?this._data[n]:Kr},removeItem:function(n){return this.length--,delete this._data[n]},clear:function(){return this.length=0,this._data={}},key:function(n){var t=[],e=this._data;return ii.each(e,function(n){ri.hasOwn(e,n)&&t.push(n)}),t[n]}}}function B(n,t,e,r,i,u){var o={};o.c=n,o.k=t,o.v=e,o.t=r||+new Date,o.u=i||"",o.r=u||"",this.toJSON=function(){return ri.extend(!0,{},o)}}function J(n){var t=ri.now();return Bi<t-n.t}function U(n){return n}function Q(n){try{n(H(this,Qi),H(this,Ui))}catch(t){if(this._state===Hi)return z(new Q(U),Ui,t)}}function H(n,t){return function(e){return z(n,t,e)}}function X(n,t,e,r){return v(e)===Xi&&(t._onFulfilled=e),v(r)===Xi&&(t._onRejected=r),n._state===Hi?n[n._pCount++]=t:$(n,t),t}function $(n,t){return setTimeout(function(){var e=void 0,r=n._state?t._onFulfilled:t._onRejected;if(void 0===r)return void z(t,n._state,n._value);try{e=r(n._value)}catch(i){return void z(t,Ui,i)}K(t,e)})}function z(n,t,e){if(n._state===Hi){n._state=t,n._value=e;for(var r=0,i=n._pCount;r<i;)$(n,n[r++]);return n}}function K(n,t){if(t===n&&t)return void z(n,Ui,new Error("promise_circular_chain"));var e=void 0,r=v(t);if(null===t||r!==Xi&&r!==$i)z(n,Qi,t);else{try{e=t.then}catch(i){return void z(n,Ui,i)}v(e)===Xi?Y(n,t,e):z(n,Qi,t)}return n}function Y(n,t,e){try{e.call(t,function(e){t&&(t=null,K(n,e))},function(e){t&&(t=null,z(n,Ui,e))})}catch(r){t&&(z(n,Ui,r),t=null)}}function G(n,t){ii.each(Yi,function(e){e(n,t)}),Yi=[]}function W(n){var t=Ur.KNB;if(Si()){if(zt===di)n(Kr,t);else if(zi||Wi)n(Wi,t);else if(Yi.push(n),!Gi){Gi=!0;var e=pe(function(){Wi=me,G(me,t)},Ki);/meituan \d+/i.test(zr)||/meituangroup\/7\.([0-7])\./i.test(zr)?(Wi=xe,G(xe,t)):t.ready(function(){t.isApiSupported({apiName:"lxlog",success:function(n){!0===n?(zi=!0,ge(e),G(Kr,t)):(Wi=xe,G(xe,t))},fail:function(){ge(e),Wi=we,G(we)}})})}}else n(be,t)}function Z(n){var t={},e=n[re],r=e&&"0"!==e;return r||"dp"!==n.type?n[re]&&(t[re]=n[re]):t[re]=n[Gt],"dp"!==n.type&&n[Gt]&&(t[Gt]=n[Gt]),n.unionId&&(t.unionId=n.unionId),n.userId&&(t.userId=n.userId),t}function nn(){return tu?Q.resolve(tu):new Q(function(n,t){W(function(e,r){var i=Ur.DPApp,u=pe(function(){n({})},Zi);r?r.ready(function(){r.use(nu,{success:function(t){ge(u),n(Z(t))},fail:function(n){ge(u),t({code:ye})}})}):i&&i[nu]?i.ready(function(){i[nu]({success:function(t){ge(u);var e={};(t.dpid||t.userId)&&(e.dpid=t.dpid,e.userId=t.userId,e.unionId=t.unionId),n(e)},fail:function(n){ge(u),t({code:_e,res:n})}})}):t({code:_e})})})}function tn(){return ui.get(cr)}function en(n){n&&ui.top(cr,n,rr)}function rn(){var n=tn()||eu();return en(n),n}function un(){var n=Math.floor(1+65535*ri.rnd());return n.toString(16).substring(1)}function on(){var n=[],t=+new Date;return n.push(t.toString(16)),n.push(un()),n.push(un()),n.push(un()),n.join("-")}function an(){if(Kr!==ru)return ru;var n=Hr.getElementsByTagName("meta");return ru="off"===b(n,"lx:native-report")}function cn(){return iu}function sn(n){an()||(iu=n)}function fn(n,t,e){return W(function(r,i){if(r)return e(r);var u=(new Date,!1),o=pe(function(){u=!0,e(me)},uu);i.use(n,{data:t,success:function(n){if(ge(o),!u)if("success"===n.status){var t=n.data;try{ri.isStr(t)&&(t=Ei.parse(t)),e(Kr,t.data?t.data:n)}catch(r){}}else e(we)},fail:function(){ge(o),u||e(we)}})})}function dn(n){var t=n.match(/(\d+)(?:\.(\d+)(?:\.(\d+))?)?/),e=[];if(t)for(var r=1;r<t.length;r++)e.push(parseInt(t[r]||0));return e}function ln(n,t){var e=dn(n),r=dn(t);return!(e[0]<r[0])&&(!(e[0]===r[0]&&e[1]<r[1])&&!(e[0]===r[0]&&e[1]===r[1]&&e[2]<r[2]))}function vn(){return 100*ri.now()+vu++}function hn(n){var t={cb:"_lx"+vn(),mn:n._mn,cn:n._cn,data:n._d||{},ver:4};return t}function pn(n,t,e,r){var i=this;i._cn=n,i._mn=t,i._d=e,i._cb=r}function gn(n,t,e,r){if(Ve===au||Pe===au)return r(au);var i=new pn(n,t,e);if(Ne===au)i.send(function(n,t){r(n,t)});else if(Me===au){if(lu.push([i,r]),!cu){cu=!0;var u=(new Date,new pn(n,ou,{}));u.send(function(n,t){if(n)au=Ve;else{if(au=Ne,sn(Ge),ri.isStr(t))try{t=Ei.parse(t)}catch(e){}hu=t;var r=t.sdk_ver;su=ln(r,"4.0.0"),fu=ln(r,"4.3.0"),du=!ln(r,"4.8.0")}ii.each(lu,function(t){var e=t[0],r=t[1];n?r(n):e.send(function(n,t){r(n,t)})})})}}else r(Re)}function mn(){return!du}function _n(){return su}function yn(){return fu}function wn(n){var t=ui.get(or),e=t.split("."),r="";return e.length?(r=e[0],e[0]=n):e.push(n),ui.top(or,e.join("."),rr),r}function bn(n,t,e){var r=[];return r.push(n?n:qn()),r.push(t?t:kn()),r.push(e?e:An()),r.join(Su)}function xn(n){var t=ui.get(fr);return t?t.split(Su)[n]:""}function Sn(n,t,e){ui.top(fr,bn(n,t,e),ir)}function qn(){return xn(wu)}function kn(){return xn(bu)}function An(){var n=0,t=xn(xu);return isNaN(t)||(n=parseInt(t)),n<0?0:n}function On(n){var t=An();return!0===n&&(t++,In(t)),(!t||-1>t)&&(t=0,In(t)),t}function In(n){Sn(Kr,Kr,n)}function jn(n){var t={};if(he.test(n)){var e=ri.parseQuery(n);return e[Gt]&&(t[Gt]=e[Gt]),e[Zt]&&(t[Zt]=e[Zt]),e[ee]&&(t[te]=e[ee]),t}return t}function Cn(n,t){return new Q(function(e,r){pe(function(){r({code:me})},3e3),gn(n,"getEnv",{},function(n,i){if(n)r(n);else{var u={uuid:Gt,msid:Wt,uid:te,dpid:re,appnm:ie,union_id:ue};t=t||{};for(var o in u){var a=u[o];i[o]&&(t[a]=i[o])}e(t)}})})}function Dn(){var n=ui.get(dr);if(n){var t=n.split(","),e=/^\d+\.\d{5,}$/;return 3!==t.length?null:e.test(t[0])&&e.test(t[1])?{lat:t[0],lng:t[1],tm:t[2]}:null}return null}function En(){var n=ui.get(or)||ui.get("iuuid")||ui.get("uuid"),t=qn(),e=kn(),r=ui.get(sr)||ui.get(re),i={};return n&&(i[Gt]=n),t&&(i[Wt]=t),e&&(i[te]=e),r&&(i[re]=r),i}function Fn(n){yu.push(n)}function Tn(n){return ri.extend(!0,{},n)}function Ln(n){var t=document.getElementsByTagName("meta"),e=b(t,"lx:appnm"),r=b(t,"lx:defaultAppnm"),i=di,u=document.domain,o=cn();return vi?e?2===o?e:e:2===o?n:i?i:r?r:u:e?e:i?i:r?r:u}function Nn(){var n=di===$t||di===Qt,t=En(),e={},r={};n&&(r=jn(Qr.href)),e=ri.extend(t,r),e.ct=pi;var i=V();i&&(e[ne]=i);var u=rn();e[Yt]=u,e[Gt]||(e[Gt]=u,wn(u)),e[Wt]||(e[Wt]=on(),Sn(e[Wt],e.uid||""));var o=Ln();return ri.isStr(o)&&(e[ie]=o),e}function Mn(n){return function(t){var e=t;return n!==t&&(e=ri.extend(n,t)),e.dpid&&e.uid?e:nn().then(function(n){var t={};return n.dpid&&(t.dpid=n.dpid,n.userId&&(t.uid=""+n.userId),n.unionId&&(t.union_id=n.unionId)),e=ri.extend(e,t)},function(n){return e})}}function Vn(n){var t=Nn();if(n&&di||Si()){var e=Cn(n,t),r=Ut===di;return r&&(e=e.then(Mn(t),function(n){return Mn(t)()})),e.then(function(n){var e=Ln(n[ie]),r=n[Gt],i=n[re],u=n[ue],o=n;return n!==t&&(o=ri.extend(t,n)),ri.isStr(e)&&(o[ie]=e),r&&wn(r),i&&ui.top(sr,i,rr),u&&ui.top(ar,u,rr),o},function(n){return t})}var i=Tn(t);return Q.resolve(i)}function Pn(n){return tr===_u?Q.resolve(Tn(mu)):nr===_u?new Q(function(n){Fn(function(t){n(t)})}):(_u=nr,Vn(n).then(function(n){return mu=ri.extend(!0,{},n||{}),_u=tr,ii.each(yu,function(t,e){ri.isFunc(t)&&yu[e](n)}),n}))}function Rn(n,t,e,r,i){var u=[{project:"web-lx-sdk",pageUrl:Qr.href,resourceUrl:n,category:i?"jsError":"ajaxError",sec_category:t,level:"error",unionId:e,timestamp:ri.now(),content:""+r||""}],o=zn("//catfront.dianping.com/api/log?v=1","application/x-www-form-urlencoded");o&&(o.onerror=o.onreadystatechange=function(){},o.send("c="+encodeURIComponent(Ei.stringify(u))))}function Bn(n,t){if(Eu>=qu)return!1;t=ri.extend({cb:l},t||{});var e=f(),r=t.nm,i=!Pr.use_post,u=i&&(r===Ue||!li&&r===Be);try{u&&Jn(n)?t.cb(Ne):Un(e,n)?t.cb(Ne):Hn(e,n,t)||gi&&Qn(e,n,t)}catch(o){return Rn(Qr.path,"report-ajax",0,o.message,!0),!1}return!0}function Jn(n){var t=void 0,e="d",r="t",i="r",u=Yn(n);if(ii.each(u,function(n){delete n.ua}),t=Ei.stringify(u),!O(t))return ii.each(n,function(n){ii.each(n.evs,function(n){var t=ri.extend(!0,{custom:{_s:1}},n.val_lab||{});n.val_lab=t})}),!1;var o=y(t),a=Zr(o),c=d();return c+=-1<c.indexOf("?")?"&"+e+"="+a:"?"+e+"="+a,c=c+"&"+r+"=1&"+i+"="+(Iu++).toString(16),C(c),!0}function Un(n,t){var e=$r.sendBeacon;return!!e&&(n=$n(n),e&&e.call($r,n,Ei.stringify(t)))}function Qn(n,t,e,r){if(!Ur.XDomainRequest)return!1;try{var i=new XDomainRequest;return i.open(Ir,$n(n),!0),i.onload=function(){Eu=0,e&&e.cb(Ne),Cu=[]},i.onerror=function(){Eu++},i.ontimeout=function(){Eu++,r||(Xn(n,t,Qn,e),ju=!0)},i.timeout=Au,i.send(Ei.stringify(t)),!0}catch(u){return!1}}function Hn(n,t,e,r,i){if(!Fr())return!1;try{var u=zn(n,"text/plain");return u.onreadystatechange=function(){if(4===u.readyState){var o=u.status;o>=200?(Eu=0,e&&e.cb(Ne),Cu=[]):(Eu++,r||!1!==i||(Xn(n,t,Hn,e),ju=!0)),e.nm===Be&&(400<=o||0===o)&&Rn(n,"web-report-fail",t[0].union_id,o),u.onreadystatechange=null}},u.onerror=function(){u.abort(),Eu++},u.send(Ei.stringify(t)),!0}catch(o){return!1}}function Xn(n,t,e,r){Cu=Cu.concat(t);var i=void 0,u=ii.reduce(Cu,function(n,t){return t.evs=n.evs.concat(t.evs),i=t.evs.length,i>ku&&ii.slice(t.evs,i-ku,i),t});if(Cu=[u],Du.push(r),!ju)var o=setInterval(function(){return Eu>=qu?(clearInterval(o),!1):void e(n,Cu,function(n){clearInterval(o),ju=!1,ii.each(Du,function(t){t&&t(n)})},!0)},Ou)}function $n(n){var t="_lxsdk_rnd="+(Iu++).toString(16);return-1===n.indexOf("?")?n+"?"+t:n+"&"+t}function zn(n,t){var e=u(),r=new e;return r.open(Ir,$n(n),!0),r.timeout=Au,r.setRequestHeader("Content-Type",t),r}function Kn(n,t,e){return ei.call(n,t)&&n[t]&&(n[e]=n[t],delete n[t]),n}function Yn(n){var t=[],e=[{l:wr,s:br},{l:lr,s:vr},{l:hr,s:pr},{l:gr,s:mr},{l:xr,s:Sr},{l:_r,s:yr}];return ii.each(n,function(n){var r=ri.extend(!0,{},n);ii.each(e,function(n){Kn(r,n.l,n.s)}),ii.each(n.evs,function(n){n=ri.extend(!0,{},n),ii.each(n,function(t,e){if(-1<e.indexOf("val_")&&(n[e.replace("val_","")]=n[e],delete n[e]),Kn(n,"refer_url","urlr"),n[e]&&"url"===e){var r=Qr.hash;r&&(n.urlh=r),delete n[e]}})}),r[Sr]===r.uuid&&delete r.uuid,r[pr]=r[pr].replace("data_sdk_",""),t.push(r)}),t}function Gn(){function n(){return Math.floor(65536*(1+Math.random())).toString(16).substring(1)}return n()+n()+"-"+n()+"-"+n()+"-"+n()+"-"+n()+n()+n()}function Wn(){return Gn()+"."+Math.round(+new Date/1e3)}function Zn(){var n=ui.get(Tu);if(n||(n=Wn(),ui.top(Tu,n,Lu)),n){var t=n.match(Fu);return t?t[1]:""}return""}function nt(){return!Nu&&Mu&&(Nu=Zn()),Nu}function tt(n){var t=this;t.s=n;var e=void 0,r=Li.get(kr)||{s:n,d:t.d};r.s!==n?(Li.del(kr),e=t.d=[]):e=t.d=r.d||[],t.l=e&&e.length||0}function et(n){return Pu||(Pu=new tt(n)),Pu}function rt(){return Pu}function it(n,t){var e=this;e.env=t||{},e.opts=ri.extend(!0,{},n),Wu.push(e)}function ut(n){return n._ptpvs===ke}function ot(){return!eo}function at(n){return n=n||{},n&&!ri.isObj(n)&&(n={cid:""+n}),n}function ct(){return to||(to=vt()),to}function st(){return to=vt()}function ft(){var n=Li.get(oe);return n&&Li.del(oe),n}function dt(n,t){return ri.isObj(n[qr])||(n[qr]={}),n[qr][zu]=t,n}function lt(n){return!(!ri.isStr(n)&&!n.length)}function vt(){return ri.now().toString(16)+"-"+Math.floor(65535*ri.rnd())+"-"+Math.floor(65535*ri.rnd())}function ht(n){var t={};return t[$e]="order",t[ze]="pay",t[Ue]="click",t[Xe]="return",t[He]="view",t[Qe]="click",t[n]}function pt(n){var t=n.nm;Be===t?(n.nm="mpt",n.val_act="pageview"):Je===t?(n.nm="report",n.val_act="quit"):(n.nm="mge",n.event_type=ht(t)||t),n.nt=0,n.isauto=8}function gt(n){var t="data_sdk_";return 0!==n.indexOf(t)&&(n=t+n),n}function mt(n){var t="data_sdk_";return 0===n.indexOf(t)&&(n=n.replace(Ru,"")),n}function _t(n){var t=ri.extend(!0,{},n.env);t[Ru]=gt(t[Ru]);var e=t.utm,r={ua:ci,sdk_ver:Kt,ch:e&&e.utm_source?e.utm_source:"web",sc:bi};return r[wr]=Kt,ri.extend(!0,r,t)}function yt(n){var t=rt(),e=t.toJSON();return e&&(n[Ku]=e),n}function wt(n,t,e,r,i){i=i||qe;var u=On(!0),o=Dn(),a=void 0,c=Be===n,s=$e===n,f=ze===n,d={nm:n,tm:ri.now(),nt:We,isauto:i,val_cid:t,req_id:ct(),seq:u};if(c){var l=Qr.href;d.url=l,a=Zu,a&&(d.refer_url=a),i===qe&&(Zu=l)}return(s||c||f)&&li&&(d=yt(d)),r=ro(r,"_hguid",nt()),c&&(r=ro(r,"_hpid",Vu())),e&&(d[$u]=e),r&&(d[qr]=r),o&&(d[Yu]=o.lat,d[Gu]=o.lng),d}function bt(n,t,e,r,i){var u=wt(n,t,e,r,i);return xt(u)}function xt(n){if(no&&0<no.length){var t=no;return no=[],t.push(n),t}return[n]}function St(n){return fi&&mn()?n:Zr(n)}function qt(n,t,e,r,i,u){u=u||{},i=i||qe;var o=this,a=o.env.appnm,c=Dn(),s=void 0,f={nm:n,tm:ri.now(),nt:Ge,isauto:i,val_cid:t};u.sf&&(f._sf=u.sf);var d=void 0,l=ri.extend(!0,{},r||{}),v=Be===n;if(v){var h=St(Qr.href);d={ua:ci,url:h};var p=V();p&&p.utm_source&&(d.utm=p),s=Zu,s&&(d.refer_url=St(s)),i===qe&&(Zu=h)}else d={};return ii.each({web_req_id:ct(),web_sdk_ver:Kt,lxcuid:rn(),web_appnm:a},function(n,t){ri.isStr(n)&&(d[t]=n)}),u.cpi&&!l.page&&(l.page=u.cpi),l.custom=ri.extend(!0,l.custom,d),l=ro(l,"_hguid",nt()),v&&(l=ro(l,"_hpid",Vu())),n!==Qe||yn()?_n()||pt(f):_n()?f.nm=Ue:pt(f),f[qr]=l,c&&(f[Yu]=c.lat,f[Gu]=c.lng),e&&(f[$u]=e),v&&!_n()&&(f.val_val=l,delete f[qr]),f}function kt(n){return n}function At(n,t,e){return ii.isArrayLike(t)||(t=[t]),ri.run(t,function(n){n&&e&&(n.tag=e)}),n.evs=t,n}function Ot(n){return Or[n]}function It(n,t){var e={};return e[Ke]=t,ri.extend(e,n)}function jt(n,t,e){var r=null;return!ri.isStr(n)||t||e?ri.isObj(n)&&ri.isStr(t)&&!e&&(r=t,t=null):(r=n,n=null),r&&(e=ri.extend({cid:r},e||{})),{lab:n,env:t,opts:e}}function Ct(n,t,e,r){var i=jt(t,e,r),u=i.lab,o=i.env,a=i.opts;r=at(a);var c=r.cid||n.opts.cid;r=ri.extend({cid:c},r),o&&ri.isObj(o)&&ii.each(o,function(t,e){n._dt.set(e,t)}),n._dt.pageView(u,r)}function Dt(n,t){this.env=n||{},this.opts=t||{},this._t=[]}function Et(n,t){return{cb:n,cmd:t}}function Ft(n,t){if(tr===ao)n&&n(co);else if(nr===ao)n&&oo.push(Et(n,t));else{ri.now();oo=oo.concat(Et(n,t)),ao=nr;var e=Hr.getElementsByTagName("meta"),r=b(e,"lx:cid"),i=b(e,"lx:category"),u=(b(e,"lx:appnm"),b(e,"lx:defaultAppnm"),b(e,"lx:mvDelay"));u=isNaN(u)?0:parseInt(u,10);var o="off"!==b(e,"lx:autopv");Pn(i).then(function(n){var t=n.appnm;!ri.isStr(t)||t===Hr.domain,co=new Dt(n,{cid:r,isDefault:!0,mvDelay:u}),i&&co.create(i,{isDefault:!0}),n=ri.extend(!0,co._dt.env,n),co._dt.env=n;try{var e=[];ii.each(oo,function(t){var r=t.cb,i=t.cmd;"config"===i||"set"===i?r(co,n):e.push(t)}),li&&et(n.msid),o&&i&&r&&r&&co._initPV(n,r),ii.each(e,function(t){var e=t.cb;e(co,n)})}catch(a){}}).then(function(){ao=tr},function(n){throw ao=tr,n})}}function Tt(n,t,e,r,i){if(ri.isFunc(t))t.call(n,n,r,i);else if(!i&&ri.isStr(t)&&ri.isFunc(n[t]))return n[t].apply(n,e)}function Lt(){if(!fo){fo=!0;var n=void 0,t=void 0;gi&&ri.on(Hr,"mouseup",function(t){var e=t.target||t.srcElement,r=e.tagName+e.href;r=r.toLocaleLowerCase(),1===e.nodeType&&/^ajavascript:/i.test(r)&&(n=new Date)});var e=function(){if(!(gi&&new Date-n<50||t||(t=!1,s()))){var e=q();Mt("pageDisappear",e,{shouldStore:hi})}};ri.on(Ur,"beforeunload",e)}}function Nt(){function n(){var n=x();return n&&(n.q.push=function(){var n=arguments[0];Mt.apply(Kr,n)}),n&&ii.isArray(n.q)?n.q:[]}var t=n();0===t.length?Ft(function(n){so=n,Lt()}):ii.each(t,function(n){Mt.apply(Kr,n)})}function Mt(n){var t=ii.slice(arguments,1,arguments.length);try{so?Tt(so,n,t,so._dt?so._dt.env:null):Ft(function(e,r,i){so=e,Tt(e,n,t,r,i),Lt()},n)}catch(e){try{Rn("sdk","api-error","",e.stack,!0)}catch(e){}}}var Vt=!0,Pt=!1,Rt="_MeiTuanALogObject",Bt=1,Jt=0,Ut="dianping_nova",Qt="waimai",Ht="moviepro",Xt="movie",$t="group",zt="demo",Kt="4.5.1",Yt="lxcuid",Gt="uuid",Wt="msid",Zt="cityid",ne="utm",te="uid",ee="userid",re="dpid",ie="appnm",ue="union_id",oe="pd_data",ae=/dp\/com\.dianping\.[\w.]+\/([\d.]+)/i,ce=/\bmeituanwaimai-c\/\d+\./i,se=/\bmoviepro/i,fe=/\bmaoyan\b/i,de=/\bmeituan \d+|meituangroup\/\d+\./i,le=/\bandroid|mobile\b|\bhtc\b/i,ve=/\btitans(no){0,1}x\b/i,he=/^(([^? \r\n]*)\?)?([^?# \r\n]+)(#\S+)?$/,pe=setTimeout,ge=clearTimeout,me=1,_e=2,ye=3,we=4,be=5,xe=6,Se=20,qe=7,ke=6,Ae=/android/i,Oe=/iphone/i,Ie=/ipad/i,je="android",Ce="iphone",De="ipad",Ee="www",Fe="i",Te="statistics://_lx/?data=",Le="lxlog",Ne=200,Me=100,Ve=500,Pe=600,Re=-1,Be="PV",Je="PD",Ue="MC",Qe="SC",He="MV",Xe="ME",$e="BO",ze="BP",Ke="order_id",Ye=1e3,Ge=2,We=0,Ze=-1,nr=0,tr=1,er=10080,rr=1576800,ir=30,ur="_lx_utm",or="_lxsdk",ar="_lxsdk_unoinid",cr="_lxsdk_cuid",sr="_lxsdk_dpid",fr="_lxsdk_s",dr="latlng",lr="msid",vr="ms",hr="category",pr="c",gr="login_type",mr="lt",_r="locate_city_id",yr="lci",wr="sdk_ver",br="sv",xr="lxcuid",Sr="lxid",qr="val_lab",kr="sf",Ar="__$lx_beacon_",Or={union_id:Vt,lxcuid:Vt,app:Vt,sdk_ver:Vt,appnm:Vt,ch:Vt,lch:Vt,ct:Vt,did:Vt,dm:Vt,ua:Vt,msid:Vt,uuid:Vt,lat:Vt,log:Vt,net:Vt,os:Vt,idfa:Vt,pushid:Vt,subcid:Vt,mac:Vt,imsi:Vt,uid:Vt,logintype:Vt,cityid:Vt,apn:Vt,mno:Vt,pushSetting:Vt,wifi:Vt,bht:Vt,ip:Vt,vendorid:Vt,geohash:Vt,dtk:Vt,sns:Vt,android_id:Vt,version_code:Vt,brand:Vt,utm:Vt},Ir="post",jr="validation",Cr="__lx"+jr,Dr=".sankuai.com",Er="report.meituan.com",Fr=function(){var n=u(),t=n&&"withCredentials"in new n;return function(){return t}}(),Tr=/__lxvalidation=([\w.]+)/i,Lr=10,Nr=!1,Mr=void 0,Vr=void 0,Pr={pageValLab:null,pageEnv:null,use_post:!1},Rr=[];Pr.on=function(n,t){Rr.push({name:n,fn:t})},Pr.emit=function(n,t,e,r,i){ii.each(Rr,function(u){var o=u.name,a=u.fn;o===n&&a(t,e,r,i)})};var Br="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(n){return typeof n}:function(n){return n&&"function"==typeof Symbol&&n.constructor===Symbol&&n!==Symbol.prototype?"symbol":typeof n},Jr=1e3,Ur=e(),Qr=t(),Hr=r(),Xr=Hr.domain,$r=i(),zr=$r.userAgent.toString(),Kr=void 0,Yr=Array.prototype,Gr=Object.prototype,Wr=decodeURIComponent,Zr=encodeURIComponent,ni=p(),ti=Gr.toString,ei=Gr.hasOwnProperty,ri={};ri.trim=function(n){return n.replace(/^[\s\uFEFF\xA0\u3000]+|[\s\uFEFF\xA0\u3000]+$/g,"")},ri.now=p,ri.rnd=g,ri.hasOwn=function(n,t){return ei.call(n,t)},ri.extend=function lo(n,t,e){var r=void 0,i=!0===n;return i||(e=t,t=n),t&&ri.isObj(t)||(t={}),e&&ri.isObj(e)||(e={}),ii.each(e,function(n,u){i&&ri.isObj(e[u])?(r=t[u],t[u]=ri.isObj(r)?r:{},lo(i,t[u],e[u])):t[u]=e[u]}),t},ri.isObj=function(n){return n&&"[object Object]"===ti.call(n)},ri.isStr=function(n){return h(n,"string")},ri.isFunc=function(n){return h(n,"function")},ri.attr=function(n,t){return n.getAttribute(t)},ri.parseQuery=function(n){var t={};if(n){var e=n.replace(he,function(n,t,e,r){return r||""}).split("&");return ii.each(e,function(n){var e=n.split("="),r=e[0],i=e[1]||"";r&&!ei.call(t,r)&&(t[r]=Wr(i))}),t}},ri.stringifyQuery=function(n){var t=[];return ri.isObj(n)&&ii.each(n,function(n,e){ri.isFunc(n)||((Kr===n||_(n))&&(n=n||""),t.push(Zr(e)+"="+Zr(n)))}),t.join("&")},ri.genReqId=function(){return""+p()*Jr+parseInt(g()*Jr)},ri.run=function(n,t){ii.isArrayLike(n)?ii.each(n,t):t(n)},ri.on=function(n,t,e){n.addEventListener?n.addEventListener(t,e,!1):n.attachEvent&&n.attachEvent("on"+t,e)},ri.off=function(n,t,e){n.removeEventListener?n.removeEventListener(t,e,!1):n.detachEvent&&n.detachEvent("on"+t,e)};var ii={};ii.isArray=function(n){return"[object Array]"===ti.call(n)},ii.isArrayLike=function(n){if(!n)return!1;var t=n.length;return!!ii.isArray(n)||!!(n&&m(t)&&t>=0)&&(!ri.isObj(n)||(!(t>1)||t-1 in n))},ii.find=function(n,t,e){var r=void 0;return ii.isArrayLike(n)&&ii.each(n,function(i,u){if(!0===t.call(e,i,u,n))return r=i,!1}),r},ii.filter=function(n,t,e){var r=[];return ii.isArrayLike(n)&&ii.each(n,function(i,u){t.call(e,i,u,n)&&r.push(i)}),r},ii.toArray=function(n,t,e){var r=[];return ii.isArrayLike(n)&&ii.each(n,function(n){r.push(t?t.call(e,n):n)},e),r},ii.each=function(n,t,e){if(n){var r=void 0,i=void 0,u=void 0,o=void 0,a=!1;if(ii.isArrayLike(n))for(i=0,u=n.length;i<u&&(o=t.call(e,n[i],i,n),a!==o);i++);else for(r in n)if(ri.hasOwn(n,r)&&(o=t.call(e,n[r],r,n),a===o))break}},ii.slice=function(n,t,e){return Yr.slice.call(ii.toArray(n),t,e)},ii.reduce=function(n,t){if(ii.isArrayLike(n)&&ri.isFunc(t)){var e=n,r=e.length>>>0,i=0,u=void 0;if(3===arguments.length)u=arguments[2];else{for(;i<r&&!(i in e);)i++;if(i>=r)return;u=e[i++]}for(;i<r;)i in e&&(u=t(u,e[i],i,e)),i++;return u}};var ui={};ui.del=function(n,t){var e=n+"=;path=/;domain="+t,r=new Date;return r.setFullYear(1970),e+=";expires="+r.toUTCString(),Hr.cookie=e,!0},ui.get=function(n){var t=Hr.cookie.match(new RegExp("(?:^|;)\\s*"+n+"=([^;]+)"));return Wr(t?t[1]:"")},ui.set=function(n,t,e,r){r=r||Hr.domain;var i=void 0,u=void 0,o=void 0,a=n+"="+Zr(t)+";path=/;domain="+r;Kr===e||isNaN(e)||(i=new Date,u=60*parseInt(e,10)*1e3,o=i.getTime()+u,i.setTime(o),a+=";expires="+i.toUTCString());try{return Hr.cookie=a,!0}catch(c){return!1}},ui.top=function(n,t,e){var r=Hr.domain,i=r.split("."),u=i.length,o=u-1,a=void 0,c=!1;for(t=""+t;!c&&o>=0&&(r=i.slice(o,u).join("."),ui.set(n,t,e,r),a=ui.get(n),Kr!==a&&(c=a===t),o--,!c););},ui.del=function(n){return ui.top(n,"",-100)};var oi=function(){var n=void 0;return{update:function(t){n=t},get:function(){return n}}}(),ai=0,ci=zr,si=[{n:zt,r:/lingxi\/demo\/\d+/i,v:ci},{n:Ut,r:ae,v:ci},{n:Qt,r:ce,v:ci},{n:Ht,r:se,v:ci},{n:Xt,r:fe,v:ci},{n:$t,r:de,v:ci}],fi=/android/i.test(ci),di="",li=fi,vi=!1,hi=!1,pi=Ee,gi=!1,mi=-1;if(le.test(ci)){pi=Fe,li=!0,ii.each(si,function(n){if(n.r.test(n.v))return di=n.n,!1}),ve.test(ci)&&(vi=!0);var _i=Oe.test(ci),yi=Ie.test(ci);(_i||yi)&&(hi=!0),di&&(_i?pi=Ce:Ae.test(ci)?pi=je:yi&&(pi=De))}else{var wi=ci.match(/(msie) (\d+)|Trident\/(d+)/i);wi&&(gi=!0,wi&&(mi=parseInt(wi[2],10)))}var bi=Ur.screen.width+"*"+Ur.screen.height,xi=vi||/ knb\/\d+/i.test(zr),Si=function(){var n=Ur.KNB;return li&&xi&&n&&n.isApiSupported},qi=ne+"_source",ki=ne+"_medium",Ai=ne+"_term",Oi=ne+"_campaign",Ii=ne+"_content",ji=void 0,Ci=Pt,Di=Ur.JSON;Di||(Di={parse:function(n){return new Function("return ("+n+")")()},stringify:function(){var n=ii.isArray,t={'"':'\\"',"\\":"\\\\","\b":"\\b","\f":"\\f","\n":"\\n","\r":"\\r","\t":"\\t"},e=function(n){return t[n]||"\\u"+(n.charCodeAt(0)+65536).toString(16).substr(1)},r=/[\\"\u0000-\u001F\u2028\u2029]/g;return function i(t){if(null==t)return"null";if(h(t,"number"))return isFinite(t)?t.toString():"null";if(h(t,"boolean"))return t.toString();if(h(t,"object")){if("function"===v(t.toJSON))return i(t.toJSON());if(n(t)){for(var u="[",o=0;o<t.length;o++)u+=(o?", ":"")+i(t[o]);return u+"]"}if(ri.isObj(t)){var a=[];for(var c in t)t.hasOwnProperty(c)&&a.push(i(c)+": "+i(t[c]));return"{"+a.join(", ")+"}"}}return'"'+t.toString().replace(r,e)+'"'}}()});var Ei=Di,Fi="__lxsdk_",Ti=Ur.localStorage,Li={get:function(n){n=P(n);var t=Ti.getItem(n);return t=Kr!==t?Ei.parse(t):t},set:function(n,t){return Li.del(n),Ti.setItem(P(n),Ei.stringify(t))},keys:function vo(){for(var vo=[],n=void 0,t=0;t<Ti.length;t++)n=Ti.key(t),0===n.indexOf(Fi)&&vo.push(n.replace(Fi,""));return vo},del:function(n){try{return Ti.removeItem(P(n))}catch(t){}},clear:function(){for(var n=this.keys(),t=0;t<n.length;t++)this.del(n[t])}};if(Ti){if(Ti){var Ni="___lxtest";Li.nt=!0;try{Li.set(Ni,1);var Mi=Li.get(Ni);1!==Mi?Li.clear():Li.del(Ni)}catch(Vi){try{Li.clear(),Ti.setItem(Ni,1),Ti.removeItem(Ni)}catch(Vi){Ti=R(),Li.nt=!1}}}}else Ti=R(),Li.nt=!1;var Pi="ABCDEFGHIJKLMNOPQRSTUVWXYZ",Ri="tag",Bi=18e5,Ji={set:function(n,t,e){var r=void 0,i=void 0,u=[],o=Li.get(Ri)||[];if(-1===Pi.indexOf(t))return!1;for(var a=0,c=o.length;a<c;a++)r=o[a],J(r)||(n===r.c?(t===r.k&&(i=!0),i||u.push(r)):u.push(r));return r=new B(n,t,e,(+new Date)),u.push(r.toJSON()),Li.set(Ri,u),!0},get:function(n,t){var e=void 0,r=Li.get(Ri);if(r&&r.length)return e={},ii.each(r,function(n){var t={};t[n.k]=n.v,J(n)||(e[n.c]=ri.extend(!0,e[n.c]||{},t))}),n&&t?e[n]&&e[n][t]:n?e[n]:e},getAll:function(){var n=Li.get(Ri),t={},e=void 0;return ii.each(n,function(n){var r=void 0;!J(n)&&n.v&&(e=!0,r={},r[n.k]=n.v,t[n.c]=ri.extend(!0,t[n.c],r))}),e&&t},clear:function(n,t){var e=arguments.length;if(!e)return Li.set(Ri,[]);if(ri.isStr(n)){var r=Li.get(Ri),i=[];ii.each(r,function(e){(t!==Kr&&e.k!==t||n!==e.c)&&i.push(e)}),Li.set(Ri,i)}}};Q.prototype.then=function(n,t){return X(this,new Q(U),n,t)},Q.all=function(n){return new Q(function(t,e){for(var r=0,i=n.length,u=[],o=0,a=void 0,c=function(n){var t=[];for(r=0;r<i;r++)t.push(n[r]?n[r].value:void 0);return t},s=function(n){return function(e){if(n.value=e,n.state=Qi,o++,o===n.len&&!a){var r=c(u);t(r)}}},f=function(n){return function(t){n.value=t,n.state=Ui,o++,a||(a=!0,e(t))}},d=function(){var t=n[r],e={value:null,index:r,state:null,len:i};u.push(e),!function(n){t.then?t.then(s(n),f(n)):Q.resolve(t).then(s(n),f(n))}(e)};r<i;r++)d()})},Q.resolve=function(n){if(n instanceof Q)return n;if(ri.isFunc(n.then)){var t=n.then.bind(n);return new Q(function(n,e){t(n,e)})}return new Q(function(t){t(n)})},Q.reject=function(n){return new Q(function(t,e){e(n)})};var Ui=0,Qi=1,Hi=2,Xi="function",$i="object";Q.prototype._state=Hi,Q.prototype._pCount=0;var zi=!1,Ki=2e3,Yi=[],Gi=!1,Wi=void 0,Zi=500,nu="getUserInfo",tu=void 0,eu=function(){var n=function(){for(var n=1*new Date,t=0;n===1*new Date&&t<200;)t++;return n.toString(16)+t.toString(16)},t=function(){return Math.random().toString(16).replace(".","")},e=function(){function n(n,t){var e=void 0,r=0;for(e=0;e<t.length;e++)r|=i[e]<<8*e;return n^r}var t=ci,e=void 0,r=void 0,i=[],u=0;for(e=0;e<t.length;e++)r=t.charCodeAt(e),i.unshift(255&r),i.length>=4&&(u=n(u,i),i=[]);return i.length>0&&(u=n(u,i)),u.toString(16)};return function(){var r=(screen.height*screen.width).toString(16);return n()+"-"+t()+"-"+e()+"-"+r+"-"+n()}}(),ru=void 0,iu=We,uu=5e3,ou="getEnv",au=Me,cu=!1,su=!1,fu=!1,du=!1,lu=[],vu=0,hu=void 0,pu=ri.now(),gu=pn.prototype;gu.send=function(n){var t=this,e=hn(t),r=Te+Zr(Ei.stringify(e)),i=ri.now(),u=5e3<i-pu;hu&&u&&t._mn===ou&&au===Ne?n(0,hu):fn(Le,r,function(t,e){n(t,e)})};var mu={},_u=Ze,yu=[],wu=0,bu=1,xu=2,Su="|",qu=3,ku=150,Au=5e3,Ou=3500,Iu=+new Date+Math.floor(1e5*Math.random()),ju=!1,Cu=[],Du=[],Eu=0,Fu=/([a-fA-F0-9-]+)(\.\d+)/,Tu="_hc.v",Lu=525600,Nu="",Mu=/(dper|dianping|51ping)\.com/.test(Xr),Vu=function(){var n=void 0;try{var t=document;if(t.querySelectorAll){var e=t.querySelectorAll("head script"),r=t.querySelectorAll("body script"),i=[];ii.each(e,function(n){i.push(n)}),ii.each(r,function(n){i.push(n)});for(var u=0;u<i.length;u++){var o=i[u].innerHTML,a=o.match(/\[['"]\s*_setPageId\s*['"]\s*,\s*(\d+)\s*\]/);if(a){n=a[1];break}}}}catch(c){}return function(){return n}}();tt.prototype={constructor:tt,set:function(n,t,e){var r=this,i=r.l,u=r.d,o=r.indexOf(n),a=i>0?u[i-1].scid+1:0,c={scid:a,cid:n,bid:t,sf:e};-1<o?u.splice(o,i-o,c):u.push(c),r.l=u.length,Li.set(kr,{s:r.s,d:u})},indexOf:function(n){for(var t=this,e=t.d||[],r=0,i=e.length;r<i;r++){var u=e[r];if(u.cid===n)return r}return-1},toJSON:function(){var n=this.d;return n&&n.length?n:null}};var Pu=null,Ru="category",Bu="setEnv",Ju="setEvs",Uu="setTag",Qu="getTag",Hu="getSFrom",Xu=-1,$u="val_bid",zu="page",Ku="s_from",Yu="lat",Gu="lng",Wu=[],Zu=Hr.referrer,no=[],to=void 0,eo=0,ro=function(n,t,e){if(e){var r={},i={custom:r};r[t]=e,n=ri.extend(!0,n||{},i)}return n},io=it.prototype;io.set=function(n,t,e){var r=this,i=r.env;if(i[n]=t,"utm"===n&&ri.isObj(t)&&L(t),Ge!==cn()||Ot(n))ri.isFunc(e)&&e(i,r);else{var u={},o=mt(i[Ru]);u[n]=t,gn(o,Bu,u,function(){ri.isFunc(e)&&e(i,r)})}},io.get=function(n,t){var e=this;ri.isFunc(t)&&t(e.env[n],e)},io.pageView=function(t,e){e=at(e)||{};var r=void 0,i=this,u=i.opts.cid,o=e.cid||u,a=e.isauto||qe,f=e.isAutoInit,d=e.reportStatus,l=u&&!(ut(i)||f)&&!ot(),v=d===We||We===cn(),h=i.env;if(this._cpi=t,l&&!s()){var p=q(!0);r=v?wt(Je,u,null,p):qt.call(i,Je,u,null,p),c(Jt)}if(u&&(ut(i)||ot())||st(),i.opts.cid=o,v){var g=_t(i),m=kt(Ji.getAll()),_=bt(Be,o,null,t,a);
l&&r&&_.unshift(r);var y=At(g,_,m);this.send(y,{nm:Be}),f||eo++}else{var w=[qt.call(i,Be,o,null,t)];l&&r&&w.push(r),ii.each(w,function(n){n.appnm=h.appnm}),gn(mt(h[Ru]),Ju,w,function(r,u){r?(sn(We),i.pageView(t,e),Rn(Qr.href,"native-report-error",i.env.union_id,n(r))):f||eo++})}i._ptpvs=f?ke:qe},io.pageDisappear=function(n,t){t=ri.extend({},t);var e=this,r=t.cid||e.opts.cid,i=t.shouldStore;c(Bt);var u=q();if(n=ri.extend(u,n),We===cn()||i){var o=_t(e),a=wt(Je,r,null,n),s=kt(Ji.getAll()),f=At(o,a,s);i&&Li.nt?Li.set(oe,f):e.send(f)}else{var d=this.env,l=[qt.call(e,Je,r,null,n)],v=mt(d[Ru]);gn(v,Ju,l,function(r,i){r&&(sn(We),e.pageDisappear(n,t))})}},io.systemCheck=function(n,t,e){e=ri.extend({},e);var r=this,i=e.cid||r.opts.cid;if(We===cn()){var u=_t(r),o=bt(Qe,i,n,t),a=kt(Ji.getAll()),c=At(u,o,a);this.send(c)}else{var s=r.env,f=[qt.call(r,Qe,i,n,t)],d=mt(s[Ru]);gn(d,Ju,f,function(i,u){i&&(sn(We),r.systemCheck(n,t,e))})}},io.moduleView=function(n,t,e){e=ri.extend({},e);var r=this,i=r.opts.mvDelay,u=e.cid||r.opts.cid;if(We===cn()){var o=_t(r),a=bt(He,u,n,t),c=kt(Ji.getAll()),s=void 0;i?(ri.run(a,function(n){no.push(n)}),pe(function(){no.length&&(s=At(o,no,c),r.send(s),no=[])},i*Ye)):(s=At(o,a,c),r.send(s))}else{var f=r.env,d=[qt.call(r,He,u,n,t)],l=mt(f[Ru]);new Date;gn(l,Ju,d,function(i,u){i&&(sn(We),r.moduleView(n,t,e))})}},io.moduleClick=function(n,t,e){e=ri.extend({},e);var r=this,i=e.cid||r.opts.cid,u=e.sf;e&&e.isLeave&&c(Bt);var o=void 0,a=q(),s=e.withPageInfo&&ri.isObj(r._cpi)?r._cpi:Kr;if(We===cn()){var f=_t(r);o=wt(Ue,i,n,t),s&&(o=dt(o,r._cpi));var d=xt(o),l=kt(Ji.getAll()),v=At(f,d,l);if(e&&e.isLeave){var h=wt(Je,i,Kr,a);v.evs.push(h)}li&&u&&rt().set(i,n,u),r.send(v,{nm:Ue})}else{var p=r.env,g={sf:u};r._cpi&&(g.cpi=r._cpi),o=qt.call(r,Ue,i,n,t,null,g);var m=[o],_=mt(p[Ru]);if(e&&e.isLeave){var y=qt.call(r,Je,i,null,a);m.push(y)}gn(_,Ju,m,function(i,u){i&&(sn(We),r.moduleClick(n,t,e))})}},io.moduleEdit=function(n,t,e){e=ri.extend({},e);var r=this,i=e.cid||r.opts.cid;if(We===cn()){var u=_t(r),o=bt(Xe,i,n,t),a=kt(Ji.getAll()),c=At(u,o,a);this.send(c)}else{var s=this.env,f=[qt.call(r,Xe,i,n,t)],d=mt(s[Ru]);gn(d,Ju,f,function(i,u){i&&(sn(We),r.moduleEdit(n,t,e))})}},io.order=function(n,t,e){e=ri.extend({},e);var r=this,i=e.cid||r.opts.cid;if(k(n,t),We===cn()){var u=_t(this),o=bt($e,i,n,t),a=kt(Ji.getAll()),c=At(u,o,a);this.send(c)}else{var s=this.env,f=[qt.call(r,$e,i,n,t)],d=mt(s[Ru]);gn(d,Ju,f,function(i,u){i&&(sn(We),r.order(n,t,e))})}},io.pay=function(n,t,e){e=ri.extend({},e);var r=this,i=e.cid||r.opts.cid;if(k(n,t),We===cn()){var u=_t(r),o=bt(ze,i,n,t),a=kt(Ji.getAll()),c=At(u,o,a);this.send(c,{cb:function(){}}),r.clearTag()}else{var s=this.env,f=[qt.call(r,ze,i,n,t)],d=mt(s[Ru]);gn(d,Ju,f,function(i,u){i&&(sn(We),r.pay(n,t,e))})}},io.tag=function(n,t,e,r){var i=void 0,u=void 0,o=void 0,a=this.env;if(ii.each(arguments,function(n){ri.isFunc(n)&&(r=n)}),ri.isFunc(n))We!==cn()?(o=mt(a[Ru]),gn(o,Qu,{},function(t,e){n(t,e,!0)})):(i=Ji.getAll(),n(0,i,!1));else if(lt(n))if(We!==cn()){if(o=mt(a[Ru]),ri.isObj(t))u=t;else{if(!lt(t)||!lt(e))return void(r&&r(Se));u={},u[t]=e}gn(o,Uu,u,function(n,t){r&&r(n,t,!0)})}else lt(t)&&lt(e)&&Ji.set(n,t,e),r&&(i=Ji.getAll(),r(0,i,!1));else r(Xu)},io.clearTag=function(n,t,e){var r=0;We===cn()?(ri.isFunc(n)&&(e=n,n=Kr),Ji.clear(n,t),e&&e(0)):r=Xu,e&&e(r)},io.sfrom=function(n){var t=void 0,e=void 0,r=this.env;We!==cn()?(e=mt(r[Ru]),gn(e,Hu,{},function(e,r){if(r){var i=r.data?r.data:r;t=ri.isStr(i)?JSON.parse(i):i,n(e,t)}})):n(1,[])},io.send=function(n,t){var e=[];t=ri.extend({cb:function(){}},t),ri.run(n,function(n){e.push(n)});var r=ft();r&&e.unshift(r),Bn(e,t)},io.getAll=function(){return Wu};var uo=Dt.prototype;uo.create=function(n,t){var e=this,r=ri.extend({},e.env);r=ri.extend(r,{category:n});var i=ri.extend({isDefault:!1},e.opts);i=ri.extend(i,t||{});var u=new it(i,r);return e._t.push(u),t.isDefault&&(e._dt=u),u},uo.config=function(n,t){return Kr!==n&&(Pr[n]=t),Pr[n]},uo._initPV=function(n,t){var e=this,r=e.config("pageValLab");n=ri.extend(n,e.config("pageEnv")),Ct(e,r,n,{isauto:ke,reportStatus:We,cid:t,isAutoInit:!0})},uo.pageView=function(n,t,e){Ct(this,n,t,e)},uo.moduleView=function(n,t,e){var r=this;r._dt.moduleView(n,t,e)},uo.systemCheck=function(n,t,e){var r=this;r._dt.systemCheck(n,t,e)},uo.moduleClick=function(n,t,e){var r=this;r._dt.moduleClick(n,t,e)},uo.moduleEdit=function(n,t,e){var r=this;r._dt.moduleEdit(n,t,e)},uo.order=function(n,t,e,r){var i=this;i._dt.order(n,It(e,t),r)},uo.pay=function(n,t,e,r){var i=this;i._dt.pay(n,It(e,t),r)},uo.pageDisappear=function(n,t){var e=this;e._dt.pageDisappear(n,t)},uo.tag=function(n,t,e,r){this._dt.tag(n,t,e,r)},uo.sfrom=function(n){this._dt.sfrom(n)},uo.clearTag=function(n,t,e){this._dt.clearTag(n,t,e)},uo.getAll=function(n){n&&n(this._t)},uo.getTracker=function(n,t){var e=ii.find(this._t,function(t){return t.env.category===n});t&&t(e)},uo.get=function(n,t){this._dt.get(n,t)},uo.set=function(n,t,e){this._dt.set(n,t,e)};var oo=[],ao=Ze,co=void 0,so=void 0,fo=void 0;Nt()}();