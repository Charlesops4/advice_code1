"""
//js逆向通用hook集合，主要还是（console.log），善用之，逆向会简单不少

//1.Cookie Hook 定位 Cookie 中关键参数生成位置，以下代码为当 Cookie 中匹配到了关键字pid， 则插入断点

(function(){
var cookieTemp =
object.defineproperty(document, 'cookie', {set:function(val){if(val.indexof('pid')!= -1){
debugger
console.log('Hook捕获到cookie设置->'，val);cookieTemp =val;return val;
get:function(){
return cookieTemp;
});
})();

//2. 针对headers的hook，这里针对（Authorization）参数

// 拦截所有请求头设置操作
(function() {
    var originalSetRequestHeader = XMLHttpRequest.prototype.setRequestHeader;
    
    XMLHttpRequest.prototype.setRequestHeader = function(header, value) {
        if (header.toLowerCase() === 'authorization') {
            console.log('设置 Authorization 头:', value);
            // 可以在这里修改 value
            // value = 'Bearer modified_token';
        }
        return originalSetRequestHeader.call(this, header, value);
    };
})();

//3.浏览器调试时候，跳过debugger的hook【涉及哪个用哪个】

(function() {
    'use strict';
    
    // 禁用debugger语句
    Function.prototype.constructor = function(a) {
        if (a && a.toLowerCase().includes('debugger')) {
            return function(){};
        }
        return Function.apply(this, arguments);
    };
    
    // 禁用console检测
    Object.defineProperty(window, 'console', {
        value: new Proxy(console, {
            get: function(target, prop) {
                if (['log', 'warn', 'error', 'debug'].includes(prop)) {
                    return function() {
                        // 过滤掉检测代码
                        if (!arguments[0] || !arguments[0].toString().includes('DevTools')) {
                            target[prop].apply(target, arguments);
                        }
                    };
                }
                return target[prop];
            }
        }),
        configurable: false,
        writable: false
    });
    
    // 禁用定时器检测
    window._setInterval = window.setInterval;
    window.setInterval = function(cb, time) {
        if (typeof cb === 'string' && cb.includes('debugger')) {
            return 0;
        }
        return window._setInterval(cb, time);
    };
    
    // 禁用DevTools窗口大小检测
    Object.defineProperty(window, 'outerWidth', {
        get: function() { return 1200; },
        configurable: false
    });
    
    // 禁用Function.toString检测
    Function.prototype.toString = function() {
        return "function() { [native code] }";
    };
})();



"""
