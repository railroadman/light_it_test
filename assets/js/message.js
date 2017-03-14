var Message = function(){
    var api_url = "";
    var __name__ = "Message";
    var template_name;
    var $this;
    var msg_text;
    var page =1;
    return {
        init:function(){

            $this = this;
            $this.event();
            Logger.info("I Am initializated:"+__name__);
        },
        create:function () {
             template_name = '#message';
             csrftoken = $("input[name=csrfmiddlewaretoken]").val();
             msg_text = $("form#add_msg_form textarea[name='msg_text']").val();

             $.post("/wall/api/messages/",{'msg_text':msg_text,'parent_id':0,'csrfmiddlewaretoken':csrftoken}).done(function(data){
                    rendered = Mustache.render($(template_name).html(),{message:msg_text,photo_url:photo_url,username:username,msg_id:data})
                    html = $(".new_msg_wrapper").html()
                    html = rendered + html;
                    $(".new_msg_wrapper").html(html);
                    $("form#add_msg_form textarea[name='msg_text']").val("");

                });
                Logger.info("on clicked");

                 return false;

        },
        edit:function(form_el){
            data = form_el.serialize();
            Logger.info("EDITED DATA:",data)
            $.ajax({
                type: 'PUT',
                url: "/wall/api/messages/",
                data: data,
                success: function (data) {

                    if (data != "false") {
                        Logger.info("AFTER UPDATE data", data.msg_id);
                        $("#msg_text_" + data.msg_id).html(data.msg_text);
                        for (i = 0; i < 3; i++) {
                            $("#msg_text_" + data.msg_id).fadeTo('slow', 0.5).fadeTo('slow', 1.0);

                        }
                        $("#"+data.msg_id+"_message").hide("slow");



                    }
                }
            });



        },

        delete: function (msg_id,el_id) {
            $.ajax({
                type: 'DELETE',
                url: "/wall/api/messages/",
                data: {"msg_id": msg_id},
                success: function (data) {
                    Logger.info("AFTER DELETE DATA: ",data)
                    if (data=='deleted')
                        $('#msg_wrapper_'+msg_id).fadeOut('fast');
                    return false;
                }
            })


        },
        get_more:function(){
            page = page+1
            $.get("/wall/api/messages/",{page:page}).done(function(data){

                Logger.info("getting more")
                if (data!='0') {

                    rendered = Mustache.render($("#messages").html(), {messages: data});
                    cur_html = $(".more_msg_wrapper").html();
                    html = cur_html + rendered;
                    $(".more_msg_wrapper").html(html);
                }
                else{
                    $(".more_msg").fadeOut('fast');
                }

            })
        },
        get_comments:function(){
            Comment.get()
        },

        event:function(){
            Logger.info("EVENT INITIALIZED",__name__);
            // DELETING MESSAGE
            $(".more_msg").on("click",function(){
                $this.get_more();
                return false;
            });
            $(".pull-right").on("click",".del_msg",function(){
                $this.delete($(this).attr("data-id"),$(this).attr("id"));
                Logger.info("clicked on delete message button",$(this).attr("id"))
                return false;
            })

            $(".more_msg_wrapper").on("click",".del_msg",function(){
                $this.delete($(this).attr("data-id"),$(this).attr("id"));
                Logger.info("clicked on delete more_message button",$(this).attr("id"))
                return false;
            })

            $(document).on("submit","form#add_msg_form",function(el){
                Logger.info($(this));
                $this.create();
                return false;
            });

            $(document).on("submit","form.form_edit",function(el){
                Logger.info("edit")
                Logger.info($(this));
                $this.edit($(this));
                return false;
            });

        }

    }
}();