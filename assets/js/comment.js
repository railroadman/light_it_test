var Comment = function () {
    __name__ = "Comment";
    var $this;
    var comm_loaded_queue=[];
    return {

        init: function () {
            $this = this;
            Logger.info("I Am initializated:" + __name__);
            $this.event();

        },
        show_tree_comments:function(msg_id){
            Logger.info("Show tree comments:",msg_id);
            if (comm_loaded_queue.indexOf(msg_id)==-1){
                comm_loaded_queue.push(msg_id)

                html = $this._load_tree_comments(msg_id)
                $("#cmt_wrapper_" + msg_id).append(html);
            }
        },

        _refresh_comments:function(msg_id){
            if(comm_loaded_queue.indexOf(msg_id)!=-1)
            {
                comm_loaded_queue.splice(comm_loaded_queue.indexOf(msg_id),1)

            }
        },



        _load_tree_comments: function (msg_id) {
                $("#cmt_wrapper_"+msg_id).html("");
                $.getJSON("/wall/api/comments/?msg_id="+ msg_id, function (data) {
                    Logger.info("Loading json for:",msg_id);
                    //var html = recursive_tree(data, 'li', 'ul');
                    var recursive = $("#sub_comment").html();
                    var reply_block = $("#reply_comment_block").html();
                    //var html = $this.recursive_tree2(data);

                    html = Mustache.render($("#tree_comments").html(), data, {msg_id:msg_id,user_id:11,"recurse": recursive,"reply_block":reply_block});
                    $("#cmt_wrapper_" + msg_id).append(html);
                    return html;
                });


        },

        prepare_edit_comment:function(cmnt_id){

            Logger.info("i am in modal edit");

                Logger.info("PREPARE FOR EDIT EDITED COMMENT ID:", cmnt_id);
                Logger.info("Commentary text", $("#cmnt_text_" + cmnt_id).text().replace(/ /g, ''))
                $("#edit_cmt_txt_textarea").val($("#cmnt_text_" + cmnt_id).text());
                $("#edit_comment_id").val(cmnt_id)
                $('#edit_comment_modal').modal('show');
                return false;

        },

        add_comment:function(form_el){
            var dataArray = form_el.serializeArray();
            dataArray.push({"name":"csrfmiddlewaretoken","value":csrftoken})
            $.post("/wall/api/comments/",dataArray).done(function(data){
                mess_data = {};
                var form_data = form_el.serializeArray();
                mess_data  =  {"user_id":user_id,"photo":photo_url,"author":username};
                for(i=0;i<form_data.length;i++){
                    if (form_data[i]['name'] == 'msg_id'){cur_msg_id = form_data[i]['value']}
                    if (form_data[i]['name'] == 'parent_id'){mess_data["parent_id"] = form_data[i]['value']}
                    if (form_data[i]['name'] == 'msg_text'){mess_data["message"] = form_data[i]['value']}
                }
                html = Mustache.render($("#reply_").html(), mess_data);
                console.log(cur_msg_id);
                if (mess_data["parent_id"] !=0)
                    $("#reply_cmnt_"+mess_data["parent_id"]).html(html);
                else {$("#new_comment_row_"+cur_msg_id).html(html);}
                $this._refresh_comments(cur_msg_id);
                $("textarea[name='msg_text']").val("");

            });
            return false;


        },

        edit_comment:function(form_el){
            var dataArray = form_el.serializeArray();

            $.ajax({
                type: 'PUT',
                url: "/wall/api/comments/",
                data: dataArray,
                success: function (data) {
                    Logger.info("AFTER EDIT COMMENT DATA: ",data)
                    if (data !=false) {
                        $("#cmnt_text_" + data.cmnt_id).html("<span style='padding:3px 4px 4px' class='badge'>"+data.cmnt_text+"</span>");
                        $('#edit_comment_modal').modal('hide');
                        comm_loaded_queue = [];

                    }
                    return false;
                }
            })
        },

        delete: function(cmnt_id,el_id) {
            $.ajax({
                type: 'DELETE',
                url: "/wall/api/comments/",
                data: {"cmnt_id": cmnt_id},
                success: function (data) {
                    Logger.info("AFTER DELETE COMMENT DATA: ",data)
                    if (data !=false) {
                        comm_loaded_queue = [];
                        $("#cmnt_text_" + data.cmnt_id).html("<span class='badge'>Message succesfully deleted</span>");
                    }
                    return false;
                }
            })

        },


        event: function () {
            Logger.info("Event initializated:" + __name__);

            // Открывает комметраии(дерево) JSON
            $(".new_msg_wrapper").on("click", ".do_comment",function () {
                msg_id = $(this).attr('data-id');
                Logger.info("Loading comments for news",msg_id);
                $this.show_tree_comments($(this).attr('data-id'));
                $("#cmt_wrapper_" + msg_id).toggle();
                return false;

            });

            $(".more_msg_wrapper").on("click", ".do_comment",function () {
                msg_id = $(this).attr('data-id');
                Logger.info("Loading comments for news",msg_id);
                $this.show_tree_comments($(this).attr('data-id'));
                $("#cmt_wrapper_" + msg_id).toggle();
                return false;

            });

            $(".comments").on("click",".del_msg_cmnt",function(){
                Logger.info("Deleting comment");
                $this.delete($(this).attr("data-id"),$(this).attr("id"));
                return false;
            }),

             $(".comments,.more_msg_wrapper,.new_msg_wrapper").on("click",".edit_msg",function(){
                 Logger.info("Editing");
                $this.prepare_edit_comment($(this).attr("data-id"));
                return false;
             }),

            $(".do_comment").on("click",function () {
                msg_id = $(this).attr('data-id');
                Logger.info("Loading comments for news",msg_id);
                $this.show_tree_comments($(this).attr('data-id'));
                if (comm_loaded_queue.indexOf(msg_id)!=-1) {
                    $("#cmt_wrapper_" + msg_id).show();

                }
                else $("#cmt_wrapper_" + msg_id).hide();

                return false;

            });

            //  Добавляем комментарий


               $(document).on("submit","form.reply_form",function(el){
                console.log($(this));
                $this.add_comment($(this));
                return false;
            });

               $(document).on("submit","form.do_edit_comment",function(el){
                console.log($(this));
                $this.edit_comment($(this));
                return false;
            });


        }


    }

}();