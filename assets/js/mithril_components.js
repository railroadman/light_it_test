function Message(Msg, parent_id, root_parent_id, total_comments) {
    this.Msg = Msg;
    this.parent_id = parent_id;
    this.root_parent_id = root_parent_id
    this.total_comment = total_comment
}

var MessageComponent = {

    oninit: function (vnode) {
        this.Msg = vnode.attrs.msg;

    },
    view: function (vnode) {
        return m("div.bs-callout bs-callout-danger", [
            m("div.media"), [
                m("div.media-left", [
                    m("p"), [
                        m("img", {
                            class: "round",
                            src: "http://pbs.twimg.com/profile_images/577449834/test_normal.jpg"
                        }),
                        m("p", 'test')
                    ]
                ]),
                m("div.media-body", [
                    m("ul"), [
                        m("li", vnode.state.Msg)
                    ],
                ]),
            ]
        ]);

    }
}


var MessageAddComponent = {
    controller: function () {
        this.state = {
            value: "",
            setValue: function (v) {
                state.value = v
            }
        },
        this.new_msg = m.prop("d"),
        show_log = function () {
            console.log("dddd");
            this.new_msg = "ddd"
        }
    },
    view: function (ctrl) {
        return m("div.col-lg-10[style=margin-top:20px;]", [
            m("input[text]", {
                oninput: m.withAttr('value', ctrl.state.setValue),value:ctrl.state.value}),

            m("button", {onclick: ctrl.show_log, class: "btn btn-large btn-primary btn-success"}, "A button")
        ])
    }
}

var MessageList = {
    list: [],
    data: "11",
    users: [
        {id: 1, name: "John", email: "john@example.com"},
        {id: 2, name: "Mary", email: "mary@example.com"},
        {id: 3, name: "Bob", email: "bob@example.com"}
    ],
    oninit: function (vnode) {

        this.loadList();
    },

    loadList: function () {
        return m.request({
            method: "GET",
            url: "http://ratfactor.com/misc/lotr-fellowship.json.php",
            withCredentials: false,
        })
            .then(function (result) {
                data = result.data
                MessageList.list = result;
                console.log(MessageList.list);
                m.redraw();

            })
    },
    view: function (vnode) {
        if (vnode.state.list.members) {
            return m("div.row", [
                m("div.col-lg-10", [
                    vnode.state.list.members.map(function (member) {
                        return m(MessageComponent, {msg: member.name})
                    })

                ])
            ])
        }
    }
}

var Test = {

    view: function (ctrl) {
        return m('.row', [
            m(MessageAddComponent),
            m(MessageList)
        ]);
    }
}

m.mount(document.getElementById('output'), Test);
