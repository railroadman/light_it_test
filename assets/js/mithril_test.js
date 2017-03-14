var state = {
    email: "",
    setEmail: function(email) {
        state.email = email.toLowerCase()
    }
}

var show_log = function(){
    console.log("here");
}

var MyComponent = {
    view: function() {
        return m("div",[m("input", {
            oninput: m.withAttr("value", state.setEmail),
            value: state.email
        },m("button",{onclick:show_log},"ok")]
    }
}

m.mount(document.body, MyComponent)
