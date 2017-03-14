
var Settings = function(){
    return {
        get:function(){
            return
        }
    }
}
var App = function () {
    var $this
    return {
        init: function () {

            $this = this;
            Logger.useDefaults();
            Logger.setLevel(Logger.On);
            if (typeof Mustache === 'undefined') {
                Logger.info("error Mustache not included or error");
            }
            Comment.init();
            Message.init();

        }
    }
}();

App.init();