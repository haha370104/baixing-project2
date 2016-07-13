$(document).ready(function () {
    setInterval(showparticipant, 5000);
});

var people = 0;
function showparticipant() {
    var url_list = location.href.split('/');
    url_list.pop();
    var meeting_ID = url_list.pop();
    $.ajax({
        type: "GET",
        url: "/get_signin_list/" + meeting_ID + '/',
        dataType: "json",
        success: function (msg) {
            if (msg.length != 0) {
                people += msg.length;
                var str = "已有 <strong>" + people + "</strong> 人加入会议";
                $("#count-people").html(str);
            }

            msg.forEach(function (e) {
                if (e.flag) {
                    $("#ntable").append('<button type="button" class="btn btn-sm btn-danger">' +
                        e.name + "</button>");
                }
                else {
                    $("#ntable").append('<button type="button" class="btn btn-sm btn-success">' +
                        e.name + "</button>");
                }
            });
        }
    });

}

