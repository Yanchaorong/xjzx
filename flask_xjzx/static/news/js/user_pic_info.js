function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(function () {
    $('.pic_info').submit(function (e) {
        e.preventDefault();
       var avatar =$('.input_file').val()
            alert(avatar)
       if (!avatar){
           alert('请选着文件')
           return
        }
    var csrf_token=$('#csrf_token') .val()
    $.post('/user/pic',{
        'avatar':avatar,
        'csrf_token':csrf_token
    },function (data) {
        if (data.result==1){
             $('.now_user_pic').attr('src',data.avatar_for);
             $('.user_center_pic>img',parent.document).attr('src',data.avatar_for);
             $('.lgin_pic',parent.document).attr('src',data.avater_for);
             alert('修改成功')
        }
    })
         })
})