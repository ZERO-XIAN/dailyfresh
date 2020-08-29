$(function(){

    var name = false;
    var password = false;
    var check_password = false;
    var email = false;
    var allow = false;


    $('#user_name').blur(function(){
        check_user_name()
    })
    $('#user_name').focus(function(){
        $(this).next().hide()
    })


    $('#pwd').blur(function(){
        check_pwd()
    })
    $('#pwd').focus(function(){
        $(this).next().hide()
        // $('#cpwd').prop("disabled", false)
        $('#cpwd').prop({disabled:false})
    })


    $('#cpwd').blur(function(){
        check_cpwd()
    })
    $('#cpwd').focus(function(){
        $(this).next().hide()
    })


    $('#email').blur(function(){
        check_email()
    })
    $('#email').focus(function(){
        $(this).next().hide()
    })


    // $('#allow').click(function(){
    //     check_allow()
    // })

    function check_user_name(){
        var reg = /^\w{5,15}$/
        var val = $('#user_name').val()

        if (reg.test(val)){
            $.get('/user/register_exist/?uname='+$('#user_name').val(),function(data){
                if(data.count ==1){
                    $('#user_name').next().html('用户名已经存在').show();
                    name = false
                }
                else{
                    $('#user_name').next().hide()
                    name = true
                }
            });
        }

        else{
            if (val==''){$('#user_name').next().html('用户名不能为空！')}
            else{$('#user_name').next().html('用户名必须是5到15个英文字母、数字或下划线')}
            $('#user_name').next().show()
            name = false
        }

    }



    function check_pwd(){
        var reg = /^[\w@\!\#\$\%\^\&\*\.\~]{6,22}$/
        var val = $('#pwd').val()

        if (reg.test(val)){
            $('#pwd').next().hide()
            password = true

        }
        else{
            if (val==''){$('#pwd').next().html('密码不能为空！');$('#cpwd').prop({disabled:"disabled", value:null})}
            else{$('#pwd').next().html('密码必须是6到22个英文字母、数字或@!#$%^&*.~字符')}
            $('#pwd').next().show()
            password = false
        }
    }



    function check_cpwd(){
        var pass = $('#pwd').val();
        var cpass = $('#cpwd').val();

        if(pass ==cpass){
            $('#cpwd').next().hide();
            check_password = true;
        }
        else{
            $('#cpwd').next().html('两次输入的密码不一致')
            $('#cpwd').next().show();
            check_password = false
        }       
    }


    function check_email(){
        var reg = /^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$/
        var val = $('#email').val()

        if (reg.test(val)){
            $('#email').next().hide()
            email = true
        }
        else{
            if (val==''){$('#email').next().html('邮箱不能为空！')}
            else{$('#email').next().html('你输入的邮箱格式不正确')}
            $('#email').next().show()
            email = false
        }
    }


    function check_allow(){
        var val = $('#allow').prop('checked')
        if (val){
            allow = true
            $('#allow').siblings('span').hide()
        }
        else{
            allow = false
            $('#allow').siblings('span').html('请勾选同意！')
            $('#allow').siblings('span').show()
        }
    }



    $('.reg_form').submit(function() {
        check_user_name();
        check_pwd();
        check_cpwd();
        check_email();
        check_allow()


        if(!(name == true && password == true && check_password == true && email == true && allow == true))
        {
            return false;//阻止提交
        }

        $('.reg_form form').prop({action: "login.html", method: "get" ,target: "_blank"})
    })







})