"""
//js逆向通用hook集合，主要还是（console.log），结合浏览器调试使用

//1.Cookie Hook 定位 Cookie 中关键参数生成位置

// 保存原始描述符
const originalCookieDesc = Object.getOwnPropertyDescriptor(Document.prototype, 'cookie');

// 重定义cookie属性
Object.defineProperty(document, 'cookie', {
    get: function() {
        const cookies = originalCookieDesc.get.call(this);
        console.trace('读取cookie:', cookies);  // 使用trace获取调用栈
        return cookies;
    },
    set: function(val) {
        // 过滤特定cookie的设置
        if (val.includes('your_target_key')) {
            console.log('设置关键cookie:', val);
            debugger;  // 自动断点
        }
        return originalCookieDesc.set.call(this, val);
    },
    configurable: true
});



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
