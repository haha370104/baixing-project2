var count = 0;

$(document).ready(function(){
    //$.ajax({
    //    type:"GET",
    //    url:"/wechat/show_fine_list/",
    //    cache: false,
    //    dataType: 'json',
    //    success:function(msg){
    //        var tablehtml = '';
    //        var cnt = 1;
    //        count = msg.length;
    //        msg.forEach(function (e) {
    //            tablehtml += '<label class="weui_cell weui_check_label" for="' + "checkbox" + cnt + '">';
    //            tablehtml += '<div class="weui_cell_hd"><input type="checkbox" class="weui_check" name="checkbox1" id="'
    //                + "checkbox" + cnt + 's11"><i class="weui_icon_checked"></i></div><div class="weui_cell_bd weui_cell_primary">';
    //            tablehtml += '<p>' + e.text + '</p>';
    //            tablehtml += '</div></label>';
    //            cnt++;
    //        });
    //        $('#checkbox').html(tablehtml);
    //
    //    },
    //    error:function(){
    //        //alert("error");
    //    }
    //});
    alert('卧槽!')
});



function make()
{
    var result = [];
    for (var i = 1;i < count;i ++)
        if (document.getElementById("cb" + i).checked)
            result.push(i);
    $.ajax({
        type:"GET",
        url:"/wechat/",
        cache: false,
        dataType: 'json',
        success:function(msg){
        },
        error:function(){
            //alert("error");
        }
    });
}