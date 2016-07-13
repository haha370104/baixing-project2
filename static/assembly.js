$(document).ready(function () {
    $.get('/get_meeting_list/', function (data) {
        var list = JSON.parse(data);
        var tobj = $("#atable").children("tbody");
        tobj.empty();
        if (list.length == 0) {
            tobj.html("<tr><td></td><td>暂无数据</td><td></td></tr>");
        }
        for (var i = 0; i < list.length; i++) {
            var ritem = list[i];
            tobj.append(
                $(document.createElement("tr"))
                    .append($(document.createElement("td"))
                        .text(ritem['ID']))
                    .append($(document.createElement("td"))
                        .text(ritem['text']))
                    .append($(document.createElement("td"))
                        .append($(document.createElement("button"))
                            .attr("type", "button")
                            .addClass("btn btn-sm btn-default")
                            .text("开始")
                            .click(function () {
                                location.href = '/get_QR_image/' + ritem['ID'] + '/';
                            })))
            );
        }
    })
});

function loadlist() {
    var rlist = [{aname: "a", tips: "b"}, {aname: "c", tips: "d"}];
    var tobj = $("#atable").children("tbody");
    tobj.empty();
    if (rlist.length == 0) {
        tobj.html("<tr><td></td><td>暂无数据</td><td></td></tr>");
    }
    rlist.forEach(function (ritem) {
        tobj.append(
            $(document.createElement("tr"))
                .append($(document.createElement("td"))
                    .text(ritem.aname))
                .append($(document.createElement("td"))
                    .text(ritem.tips))
                .append($(document.createElement("td"))
                    .append($(document.createElement("button"))
                        .attr("type", "button")
                        .addClass("btn btn-sm btn-default")
                        .text("开始")
                        .click(function () {

                        })))
        );
    });
}

//loadlist();

