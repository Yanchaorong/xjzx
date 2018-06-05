function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(function () {

    $(".release_form").submit(function (e) {
        e.preventDefault();
        var title=$('.input_txt2').val();
        if (!title){
            alert('请填写标题')
            return
        }
        var category_id=$('.sel_opt').val();
        if (!category_id){
            alert('请选着分类')
            return
        }
        var summary=$('.input_multxt').val();
        if (!summary){
            alert("请填写摘要")
            return
        }
        var content=$('#rich_content').val();
            // alert(content.length)
        if (content.length=0){
            alert('请填写正文')
            return
        }
        var pic=$('.input').val()
        if (!pic){
            alert('请选着文件')
            return
        }

        var csrf_token=$('#csrf_token').val()
        $.post('/user/release',{
            'csrf_token':csrf_token,
            'title':title,
            'category_id':category_id,
            'summary':summary,
            'content':content,
            'pic':pic

        },function (data) {
            if (data.result==2){
                alert('修改成功')
            }
            }
        )
        // // TODO 发布完毕之后需要选中我的发布新闻
        // // 选中索引为6的左边单菜单
        // window.parent.fnChangeMenu(6)
        // // 滚动到顶部
        // window.parent.scrollTo(0, 0)
    })
})