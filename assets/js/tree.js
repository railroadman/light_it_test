/**
 * Created by railr on 3/9/2017.
 */
function recursive_tree(data, tag, child_wrapper, level) {
  var html = [];
  //return html array;
  level = level || 0;

  child_wrapper = (child_wrapper != false) ? child_wrapper : 'ul';
  $.each(data, function(i, obj) {
    var el = $('<' + tag + '>');
    el.html(obj.message);
    if (obj.hasOwnProperty('childrens')) {
      var wrapper = $('<' + child_wrapper + '>');
      var els = recursive_tree(obj.childrens, tag, child_wrapper);
      wrapper.append(els);
      wrapper.appendTo(el);
    }
    html.push(el);
  });
  return html;
}

function recursive_tree2(data,nested=0) {
  var html = [];
  //return html array;

    var el = $("<div/>")
    el.addClass("media")

  $.each(data, function(i, obj) {

    var el_left = $("<div/>");
    el_left.addClass("media-left")
    if (nested==0)
      el_left.html("<img alt='32x32' class='media-object round' data-src='holder.js/32x32' src='data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9InllcyI/PjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCA2NCA2NCIgcHJlc2VydmVBc3BlY3RSYXRpbz0ibm9uZSI+PCEtLQpTb3VyY2UgVVJMOiBob2xkZXIuanMvNjR4NjQKQ3JlYXRlZCB3aXRoIEhvbGRlci5qcyAyLjYuMC4KTGVhcm4gbW9yZSBhdCBodHRwOi8vaG9sZGVyanMuY29tCihjKSAyMDEyLTIwMTUgSXZhbiBNYWxvcGluc2t5IC0gaHR0cDovL2ltc2t5LmNvCi0tPjxkZWZzPjxzdHlsZSB0eXBlPSJ0ZXh0L2NzcyI+PCFbQ0RBVEFbI2hvbGRlcl8xNWFiZjdkZDIxZCB0ZXh0IHsgZmlsbDojQUFBQUFBO2ZvbnQtd2VpZ2h0OmJvbGQ7Zm9udC1mYW1pbHk6QXJpYWwsIEhlbHZldGljYSwgT3BlbiBTYW5zLCBzYW5zLXNlcmlmLCBtb25vc3BhY2U7Zm9udC1zaXplOjEwcHQgfSBdXT48L3N0eWxlPjwvZGVmcz48ZyBpZD0iaG9sZGVyXzE1YWJmN2RkMjFkIj48cmVjdCB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIGZpbGw9IiNFRUVFRUUiLz48Zz48dGV4dCB4PSIxNCIgeT0iMzYuNSI+NjR4NjQ8L3RleHQ+PC9nPjwvZz48L3N2Zz4=' data-holder-rendered='true' style='width: 64px; height: 64px;'>")
    else{
      el_left.html("<img alt='32x32' class='media-object round' data-src='holder.js/32x32' src='http://pbs.twimg.com/profile_images/577449834/test_normal.jpg' data-holder-rendered='true' style='width: 48px; height: 48px;'>")
    }

    var el_body = $("<div/>");
    el_body.addClass("media-body")
    el_body.html("<p class='nested'>"+obj.message+"</p><div class='row'><div class='col-lg-4 pull-left'><a href='#'>Reply</a></div></div>");
    if (obj.hasOwnProperty('childrens')) {
      var el = $("<div/>")
      el.addClass("media")
      var wrapper = $("<div/>");
      wrapper.addClass("media")
      var els = recursive_tree2(obj.childrens,1);
      wrapper.append(els);
      wrapper.appendTo(el_body);
      el_left.appendTo(el)
      el_body.appendTo(el)

    }
    html.push(el);
  });
  return html;
}