var CODE_SUCCESS = 1;
var CODE_FAILURE = 0;
var list_order = 1;
var pageNum = 1;
var tag1 = '';
var tag2 = '';
var BOARD_LIST_HTML = "";
var BOARD_LIST_OPTION = "";
var TAGE2_LIST_HTML = "";




/**
 * [初始进入]
 * @param  {[type]} ){                 $.post("Index/index", function(data){         result_data [description]
 * @return {[type]}     [description]
 */
$(function(){
    $.post("/Login/index", function(data){
         var res = $.parseJSON(data);
        if(res.status == CODE_SUCCESS) {
            loadfirst(res.data);
        } else {
            loadLoginPage();
        }
    });
 
});

/**
 * 加载登录页
 * @return {[type]} [description]
 */
function loadLoginPage() {
    $('body').addClass('light-gray-bg').load("pages/login.html", function (response, status, xhr) {

        $('#login-button').click(function() {
          $.ajax({
               type: "POST",
               url: "/user/auth",
               cache: false,
               data: $('#login-form').serialize(),
               success: function( res){

	               var res = $.parseJSON(res);

	               if( res.status == CODE_SUCCESS){
	              		 loadfirst(res.data);
	           		} else {
	                	$('#wrong_pass').show();
	              	}
               }
            });
          return false;
        })
    });
}

/**
 * 加载框架页
 * @return {[type]} [description]
 */
function loadfirst() {

  $('body').removeClass('light-gray-bg').load("pages/main.htm", function(response, status, xhr) {

           $('.login-out').click(function(){
                      $.ajax({
                         type: "GET",
                         url: "/user/logout",
                         cache: false,
                         success: function( res){
                              loadLoginPage();

                         }
                      });
          });
          initcontentpage();
  });

}

/**
 * 加载内容页
 * @return {[type]} [description]
 */
function initcontentpage() {
   $('#show_table').load('pages/board_list.htm', function(response, status, xhr) {
          board();
    });

  $('body #top_nav ul li:eq(1)').off('click').on('click',function() {
        $(this).find('a').addClass('selected').parent('li').siblings('li').find('a').removeClass('selected');
        $('#sidebar').html(
            '<li><a class="selected" href="javascript:;" id="guanqiaMessage">关卡信息管理</a></li><li><a href="javascript:;" id="activeMessage">活动信息管理</a><a href="javascript:;" id="guanqiaboard_mesage">排行榜信息管理</a></li><li><a href="javascript:;" id="guanqiauser_message">用户信息管理</a></li>'
          );
           $('#show_table').load('pages/guanqia_list.htm', function(response, status, xhr) {
                guanqia_list();
          });


  });

$('body').off('click','#add_guanqia').on('click','#add_guanqia',function() {

  $('#show_table').load('pages/add_guanqia.htm', function(response, status, xhr) {

            add_guanqia();
    });
});

$("body").off('click', '#add_guanqia_board').on('click', '#add_guanqia_board', function(e) {
      $(this).addClass('selected').parent('li').siblings('li').children('a').removeClass('selected');
      $('#show_table').load('pages/add_guanqiaboard.htm', function(response, status, xhr) {
          add_guanqiaboard();
      });
});

$("body").off('click', '#add_guanqia_user').on('click', '#add_guanqia_user', function(e) {
      $(this).addClass('selected').parent('li').siblings('li').children('a').removeClass('selected');
      $('#show_table').load('pages/add_guanqiauser.htm', function(response, status, xhr) {
          add_guanqiauser();
      });
});


$('body').off('click','#add_act').on('click','#add_act',function() {

  $('#show_table').load('pages/add_active.htm', function(response, status, xhr) {

            add_act();
    });
});

$('body').off('click','#guanqiaMessage').on('click','#guanqiaMessage',function() {
      $(this).addClass('selected').parent('li').siblings('li').find('a').removeClass('selected');
     $('#show_table').load('pages/guanqia_list.htm', function(response, status, xhr) {
               guanqia_list();
          });
});

$('body').off('click','#activeMessage').on('click','#activeMessage',function() {
      $(this).addClass('selected').parent('li').siblings('li').find('a').removeClass('selected');
     $('#show_table').load('pages/active_list.htm', function(response, status, xhr) {
              act_list();
          });
});


$('body').off('click','#guanqiaboard_mesage').on('click','#guanqiaboard_mesage',function() {
      $(this).addClass('selected').parent('li').siblings('li').find('a').removeClass('selected');
     $('#show_table').load('pages/guanqiaboard_list.htm', function(response, status, xhr) {
               guanqiaboard_list();
          });
});

$('body').off('click','#guanqiauser_message').on('click','#guanqiauser_message',function() {
      $(this).addClass('selected').parent('li').siblings('li').find('a').removeClass('selected');
     $('#show_table').load('pages/guanqiauser_list.htm', function(response, status, xhr) {
              guanqiauser_list();
          });
});



$('body #top_nav ul li:eq(0)').off('click').on('click',function() {
        $(this).find('a').addClass('selected').parent('li').siblings('li').find('a').removeClass('selected');
        $('#sidebar').html(
            '<li><a class="selected" href="javascript:;" id="board_list">榜单列表</a></li><li><a href="javascript:;" id="add_board">添加日/周/月/总榜单</a></li><li><a href="javascript:;" id="add_active_board">添加活动榜单</a></li>'
          );
         $('#show_table').load('pages/board_list.htm', function(response, status, xhr) {
          board();
          });
  });


 $("body").off('click', '#board_list').on('click', '#board_list', function(e) {
        $(this).addClass('selected').parent('li').siblings('li').children('a').removeClass('selected');
        initcontentpage();
  });

 $("body").off('click', '#add_board').on('click', '#add_board', function(e) {
        $(this).addClass('selected').parent('li').siblings('li').children('a').removeClass('selected');
        $('#show_table').load('pages/add_board.html', function(response, status, xhr) {
              add_board();
        });
  });

  $("body").off('click', '#add_active_board').on('click', '#add_active_board', function(e) {
        $(this).addClass('selected').parent('li').siblings('li').children('a').removeClass('selected');
        $('#show_table').load('pages/add_active_board.html', function(response, status, xhr) {
            add_active_board();
        });
  });



}


function guanqiauser_list(){
    guanqiauser_default_list();
    $('#guanqiauser_div #guanqiauser_apiversion').off('change').on('change',function(e) {
        apiversion  = $(this).find('option:selected').attr("value")
        appid = $('#guanqiauser_appid').find('option:selected').attr('value')
        if(!apiversion || !appid){
          $('#guanqiauser_table_list tbody').html('');
          return ;
        }
       
        guanqiauser_default_tableShow(apiversion,appid);
    });
     $('#guanqiauser_div #guanqiauser_appid').off('change').on('change',function(e) {
        appid  = $(this).find('option:selected').attr("value")
        apiversion = $('#guanqiauser_apiversion').find('option:selected').attr('value')
    
        if(!apiversion || !appid){
          $('#guanqiauser_table_list tbody').html('');
          return ;
        }
       
        guanqiauser_default_tableShow(apiversion,appid);
    });

    $('body').off('keypress','#guanqiauser_page').on('keypress','#guanqiauser_page',function(e) {
      if(e.keyCode == 13 || e.which == 13) {
        var curpage = $.trim($(this).val());
        var apiversion = $('#guanqiauser_apiversion').find('option:selected').attr('value');
        var appid = $('#guanqiauser_appid').find('option:selected').attr('value');
        if(!curpage || !appid || !apiversion) {
          $('#guanqiauser_table_list tbody').html('');
          return;
        }
        
       guanqiauser_default_tableShow(apiversion,appid,curpage);
      }
  });


}


function guanqiaboard_list() {
  guanqiaboard_default_list();
  $('body #guanqiaboard_search').off('keypress').on('keypress',function(e) {
      if(e.keyCode == 13 || e.which == 13) {
        var leaderboardId = $.trim($(this).val());
        var apiversion = $('#guanqiaboard_apiversion').find('option:selected').attr('value');
        var appid = $('#guanqiaboard_appid').find('option:selected').attr('value');
        if(!leaderboardId || !apiversion || !appid) {
          $('#guanqia_table_list tbody').html('');
          return;
        }
       
       guanqiaoboard_default_tableShow(leaderboardId,appid,apiversion);
      }
  });

   $('body').off('keypress','#guanqiaboard_page').on('keypress','#guanqiaboard_page',function(e) {
      if(e.keyCode == 13 || e.which == 13) {
        var curpage = $.trim($(this).val());
        var leaderboardId = $.trim($('#guanqiaboard_search').val());
        var apiversion = $('#guanqiaboard_apiversion').find('option:selected').attr('value');
        var appid = $('#guanqiaboard_appid').find('option:selected').attr('value');
        if(!curpage || !leaderboardId || !apiversion || !appid) {
          $('#guanqia_table_list tbody').html('');
          return;
        }
       guanqiaoboard_default_tableShow(leaderboardId,appid,apiversion,curpage);
      }
  });

}


function guanqiauser_default_list() {
     $.ajax({
    url:'/Level/getUserTypes',
    type:"POST",
    cache:false,
    success:function(e) {
      var res = $.parseJSON(e);
      // console.log(res);
      if(res.status) {
        var apiversion = new Array();
        var appid = new Array();
        var keys = res.data;
        for(var i in keys) {
          console.log(i);
          console.log(keys[i]);
          var v = keys[i].split(':');
          apiversion.push(v[1]);
          appid.push(v[2]);
        }
        apiversion = unique(apiversion);
        appid = unique(appid);
        var apiversion_str = '<option>API版本</option>';
        var _appid_str = '<option>APP ID</option>';
        for(var i in apiversion) {
          apiversion_str += '<option value="'+apiversion[i]+'">'+apiversion[i]+'</option>';
        }
        for (var i in appid) {
          _appid_str += '<option value="'+appid[i]+'">'+appid[i]+'</option>';
        }
        $('#guanqiauser_apiversion').html(apiversion_str);
        $('#guanqiauser_appid').html(_appid_str);
      } 
    }
  });

}

function guanqiauser_default_tableShow(apiversion,appid, curpage=1) {
     $.ajax({
          url:'/Level/getLeveluserinfo',
          type:'POST',
          data:{
            // leaderboardId:leaderboardId,
            appid:appid,
            apiversion:apiversion,
            curpage:curpage
          },
          success:function(e) {
            var res = $.parseJSON(e);
            console.log(res);
            if(!res.status) {
              // alert("no list");
               $('#guanqiauser_table_list tbody').html('');
               $('#guanqiauser_page').removeClass('hidden').attr('placeholder',"暂无数据");
              return;
            }
            var data = res.data;
            var table_str = '';
            for( var i in data) {
              table_str += '<tr><td>'+apiversion+'</td><td>'+appid+'</td><td>'+data[i]['uid']+'</td><td>'+data[i]['userInfo']+'</td><td>编辑</td></tr>';
            }
            $('#guanqiauser_table_list tbody').html(table_str);
            $('#guanqiauser_page').removeClass('hidden').attr('placeholder',"共有"+res.size+"页数据");


          }
        });
}


function guanqiaoboard_default_tableShow(leaderboardId,appid,apiversion,curpage=1) {
     $.ajax({
          url:'/Level/getBoardData',
          type:'POST',
          data:{
            leaderboardId:leaderboardId,
            appid:appid,
            apiversion:apiversion,
            curpage:curpage
          },
          success:function(e) {
            var res = $.parseJSON(e);
            console.log(res);
            if(!res.status) {
              // alert("no list");
               $('#guanqia_table_list tbody').html('');
               $('#guanqiaboard_page').removeClass('hidden').attr('placeholder',"暂无数据");
              return;
            }
            var data = res.data;
            var table_str = '';
            for( var i in data) {
              table_str += '<tr><td>'+apiversion+'</td><td>'+appid+'</td><td>'+leaderboardId+'</td><td>'+data[i]['uid']+'</td><td>'+data[i]['score']+'</td><td>编辑</td></tr>';
            }
            $('#guanqia_table_list tbody').html(table_str);
            $('#guanqiaboard_page').removeClass('hidden').attr('placeholder',"共有"+res.size+"页数据");


          }
        });
}





function guanqiaboard_default_list() {
   $.ajax({
    url:'/Level/getBoardTypes',
    type:"POST",
    cache:false,
    success:function(e) {
      var res = $.parseJSON(e);
      // console.log(res);
      if(res.status) {
        var apiversion = new Array();
        var appid = new Array();
        var keys = res.data;
        for(var i in keys) {
          var v = keys[i].split(':');
          apiversion.push(v[0]);
          appid.push(v[1]);
        }
        apiversion = unique(apiversion);
        appid = unique(appid);
        var apiversion_str = '<option>API版本</option>';
        var _appid_str = '<option>APP ID</option>';
        for(var i in apiversion) {
          apiversion_str += '<option value="'+apiversion[i]+'">'+apiversion[i]+'</option>';
        }
        for (var i in appid) {
          _appid_str += '<option value="'+appid[i]+'">'+appid[i]+'</option>';
        }
        $('#guanqiaboard_apiversion').html(apiversion_str);
        $('#guanqiaboard_appid').html(_appid_str);
      } 
    }
  });
}



function guanqia_default_list() {
  $.ajax({
        url:"/Level/getLevelTypes", 
        type:'POST',
        cache:false,
        success:function(e) {
          var res = $.parseJSON(e);
          console.log(res);
          if(!res.status) {
            // alert(res.msg);
            return;
          }
          var apiversion = new Array();
          var gameversion = new Array();
          var _appid = new Array();
          var keys = res.data;
          for(var i in keys) {
            var v = keys[i].split(":");
            apiversion.push(v[0]);
            gameversion.push(v[2]);
            _appid.push(v[1]);
          }

          apiversion = unique(apiversion);
          gameversion = unique(gameversion);
          _appid = unique(_appid);
          apiversion_str = '<option>API版本</option>';
          gameversion_str = '<option>游戏版本</option>';
          _appid_str = '<option>APP ID</option>';
          for(var i in apiversion) {
            apiversion_str += '<option value="'+apiversion[i]+'">'+apiversion[i]+'</option>';
          }
           for(var i in gameversion) {
             gameversion_str += '<option value="'+gameversion[i]+'">'+gameversion[i]+'</option>';
          }
           for(var i in _appid) {
             _appid_str += '<option value="'+_appid[i]+'">'+_appid[i]+'</option>';
          }

          $('#apiversion').html(apiversion_str);
          $('#gameversion').html(gameversion_str);
          $('#_appid').html(_appid_str);
          $('#guanqia_message').val("关卡配置信息，仅支持json格式！");
        },
        error:function () {
          alert("未知错误！");
        }
      });
}

function act_default_list() {
   $.ajax({
        url:"/Level/getActTypes", 
        type:'POST',
        cache:false,
        success:function(e) {
          var res = $.parseJSON(e);
          console.log(res);
          if(!res.status) {
            return;
          }
          var apiversion = new Array();
          // var gameversion = new Array();
          var _appid = new Array();
          var keys = res.data;
          for(var i in keys) {
            var v = keys[i].split(":");
            apiversion.push(v[0]);
            // gameversion.push(v[1]);
            _appid.push(v[1]);
          }

          apiversion = unique(apiversion);
          // gameversion = unique(gameversion);
          _appid = unique(_appid);
          apiversion_str = '<option>API版本</option>';
          // gameversion_str = '<option>游戏版本</option>';
          _appid_str = '<option>APP ID</option>';
          for(var i in apiversion) {
            apiversion_str += '<option value="'+apiversion[i]+'">'+apiversion[i]+'</option>';
          }
          //  for(var i in gameversion) {
          //    gameversion_str += '<option value="'+gameversion[i]+'">'+gameversion[i]+'</option>';
          // }
           for(var i in _appid) {
             _appid_str += '<option value="'+_appid[i]+'">'+_appid[i]+'</option>';
          }

          $('#act_apiversion').html(apiversion_str);
          // $('#gameversion').html(gameversion_str);
          $('#act_appid').html(_appid_str);
          $('#act_message').val("活动配置信息，仅支持json格式！");
        },
        error:function () {
          alert("未知错误！");
        }
      });
}


function guanqia_list() {
  guanqia_default_list();  

  $('body #guanqia_div').off('change','select').on('change','select',function() {
        var apiversion = $('#apiversion').find('option:selected').attr('value');
        var gameversion = $('#gameversion').find('option:selected').attr('value');
        var _appid = $('#_appid').find('option:selected').attr('value');
        console.log(gameversion);
        if(!apiversion || !gameversion || !_appid) {
          $('#guanqia_message').val("关卡配置信息，仅支持json格式！");
          return;
        }
        $.ajax({
          url:"/Level/getLevel2",
          type:"POST",
          cache:false,
          data:{
            appid:_appid,
            apiversion:apiversion,
            gameversion:gameversion
          },
          success:function(e) {

            var res = $.parseJSON(e);
            
            if(!res.status) {
              return;
            }
            var config = res.data;
            $('#guanqia_message').val(JSON.stringify($.parseJSON(config),null,4));

          }
        });
  });


   $('body').off('click','#pull_guanqia').on('click','#pull_guanqia',function(e) {
      var apiversion = $('#apiversion').find('option:selected').attr('value');
      var gameversion = $('#gameversion').find('option:selected').attr('value');
      var appid = $('#_appid').find('option:selected').attr('value');
      var config_message = $('#guanqia_message').val();
      if(!apiversion || !gameversion || !appid || !config_message) {
        alert("请完善信息");
        return;
      }
      $.ajax({
        url:"/Level/add_level", 
        type:'POST',
        cache:false,
        data:{
          apiversion:apiversion,
          gameversion:gameversion,
          appid:appid,
          config_message:config_message
        },
        success:function(e) {
          var res = $.parseJSON(e);
          console.log(res);
          if(!res.status) {
            alert("操作失败！");
          }
          alert("操作成功！");
        },
        error:function () {
          alert("未知错误！");
        }
      });
  });

   $('body').off('click','#del_guanqia').on('click','#del_guanqia',function(e) {
      var apiversion = $('#apiversion').find('option:selected').attr('value');
      var gameversion = $('#gameversion').find('option:selected').attr('value');
      var appid = $('#_appid').find('option:selected').attr('value');
      // var config_message = $('#guanqia_message').val();
      if(!apiversion || !gameversion || !appid) {
        alert("请完善信息");
        return;
      }
      $.ajax({
        url:"/Level/del_level", 
        type:'POST',
        cache:false,
        data:{
          apiversion:apiversion,
          gameversion:gameversion,
          appid:appid,
        },
        success:function(e) {
          var res = $.parseJSON(e);
          console.log(res);
          if(!res.status) {
            alert("操作失败！");
          }
          alert("操作成功！");
          guanqia_default_list();
        },
        error:function () {
          alert("未知错误！");
        }
      });
  });
  
}


function act_list() {

   act_default_list();  

  $('body #act_div').off('change','select').on('change','select',function() {
        var apiversion = $('#act_apiversion').find('option:selected').attr('value');
        // var gameversion = $('#gameversion').find('option:selected').attr('value');
        var _appid = $('#act_appid').find('option:selected').attr('value');
        // console.log(gameversion);
        if(!apiversion || !_appid) {
          $('#act_message').val("活动配置信息，关仅支持json格式！");
          return;
        }
        $.ajax({
          url:"/Level/getAct",
          type:"POST",
          cache:false,
          data:{
            appid:_appid,
            apiversion:apiversion,
            // gameversion:gameversion
          },
          success:function(e) {

            var res = $.parseJSON(e);
            
            if(!res.status) {
              return;
            }
            var config = res.data;
            $('#act_message').val(JSON.stringify($.parseJSON(config),null,4));

          }
        });
  });


   $('body').off('click','#pull_act').on('click','#pull_act',function(e) {
      var apiversion = $('#act_apiversion').find('option:selected').attr('value');
      // var gameversion = $('#gameversion').find('option:selected').attr('value');
      var appid = $('#act_appid').find('option:selected').attr('value');
      var config_message = $('#act_message').val();
      if(!apiversion || !appid || !config_message) {
        alert("请完善信息");
        return;
      }
      $.ajax({
        url:"/Level/add_act", 
        type:'POST',
        cache:false,
        data:{
          apiversion:apiversion,
          // gameversion:gameversion,
          appid:appid,
          config_message:config_message
        },
        success:function(e) {
          var res = $.parseJSON(e);
          console.log(res);
          if(!res.status) {
            alert("操作失败！");
          }
          alert("操作成功！");
        },
        error:function () {
          alert("未知错误！");
        }
      });
  });

   $('body').off('click','#del_act').on('click','#del_act',function(e) {
      var apiversion = $('#act_apiversion').find('option:selected').attr('value');
      // var gameversion = $('#gameversion').find('option:selected').attr('value');
      var appid = $('#act_appid').find('option:selected').attr('value');
      // var config_message = $('#guanqia_message').val();
      if(!apiversion || !appid) {
        alert("请完善信息");
        return;
      }
      $.ajax({
        url:"/Level/del_act", 
        type:'POST',
        cache:false,
        data:{
          apiversion:apiversion,
          // gameversion:gameversion,
          appid:appid,
        },
        success:function(e) {
          var res = $.parseJSON(e);
          console.log(res);
          if(!res.status) {
            alert("操作失败！");
          }
          alert("操作成功！");
          act_default_list();
        },
        error:function () {
          alert("未知错误！");
        }
      });
  });


}



function unique(arr) {
  var result = [], hash = {};
  for (var i = 0, elem; (elem = arr[i]) != null; i++) {
    if (!hash[elem]) {
      result.push(elem);
      hash[elem] = true;
    }
  }
  return result;
}


function add_guanqia() {

  $('body').off('click','#submit_guanqia').on('click','#submit_guanqia',function(e) {
      var apiversion =  $('#add_guanqia_apiversion').val();
      var gameversion = $("#add_guanqia_gameversion").val();
      var appid = $('#add_guanqia_appid').val();
      var config_message = $('#add_guanqia_message').val();
      if(!apiversion || !gameversion || !appid || !config_message) {
        alert("请完善信息");
        return;
      }
      $.ajax({
        url:"/Level/add_level", 
        type:'POST',
        cache:false,
        data:{
          apiversion:apiversion,
          gameversion:gameversion,
          appid:appid,
          config_message:config_message
        },
        success:function(e) {
          var res = $.parseJSON(e);
          console.log(res);
          if(!res.status) {
            alert("操作失败！");
            return;
          }
          alert("操作成功！");
        },
        error:function () {
          alert("未知错误！");
        }
      });
  });
}


function add_guanqiaboard() {

    $('body').off('click','#submit_guanqiaboard').on('click','#submit_guanqiaboard',function(e) {
    var apiversion =  $('#add_guanqiaboard_apiversion').val();
    var leaderboardId = $("#add_guanqiaboard_leaderboardId").val();
    var appid = $('#add_guanqiaboard_appid').val();
    var uid = $('#add_guanqiaboard_uid').val();
    var score = $('#add_guanqiaboard_score').val();
    if(!apiversion || !leaderboardId || !appid || !score || !uid) {
      alert("请完善信息");
      return;
    }
    $.ajax({
      url:"/Level/setFbScore", 
      type:'POST',
      cache:false,
      data:{
        apiversion:apiversion,
        leaderboardId:leaderboardId,
        appid:appid,
        uid:uid,
        score:score,
        token:hex_md5(uid+'_ivy')
      },
      success:function(e) {
        var res = $.parseJSON(e);
        console.log(res);
        if(res.erron !== 1000) {
          alert("操作失败！");
          return;
        }
        alert("操作成功！");
      },
      error:function () {
        alert("未知错误！");
      }
    });
  });
}


function add_guanqiauser() {

    $('body').off('click','#submit_guanqiauser').on('click','#submit_guanqiauser',function(e) {
    var apiversion =  $('#add_guanqiauser_apiversion').val();
    // var leaderboardId = $("#add_guanqiauser_leaderboardId").val();
    var appid = $('#add_guanqiauser_appid').val();
    var uid = $('#add_guanqiauser_uid').val();
    var data = $('#add_guanqiauser_info').val();
    // var token = 
    if(!apiversion || !appid || !data || !uid) {
      alert("请完善信息");
      return;
    }
    $.ajax({
      url:"/Level/setUserinfo", 
      type:'POST',
      cache:false,
      data:{
        apiversion:apiversion,
        // leaderboardId:leaderboardId,
        appid:appid,
        uid:uid,
        data:data,
        token:hex_md5(uid+'_ivy')
      },
      success:function(e) {
        var res = $.parseJSON(e);
        console.log(res);
        if(res.erron !== 1000) {
          alert("操作失败！");
          return;
        }
        alert("操作成功！");
      },
      error:function () {
        alert("未知错误！");
      }
    });
  });
}

function add_act() {

  $('body').off('click','#submit_act').on('click','#submit_act',function(e) {
      var apiversion =  $('#add_act_apiversion').val();
      // var gameversion = $("#add_guanqia_gameversion").val();
      var appid = $('#add_act_appid').val();
      var config_message = $('#add_act_message').val();
      if(!apiversion || !appid || !config_message) {
        alert("请完善信息");
        return;
      }
      $.ajax({
        url:"/Level/add_act", 
        type:'POST',
        cache:false,
        data:{
          apiversion:apiversion,
          // gameversion:gameversion,
          appid:appid,
          config_message:config_message
        },
        success:function(e) {
          var res = $.parseJSON(e);
          console.log(res);
          if(!res.status) {
            alert("操作失败！");
            return;
          }
          alert("操作成功！");
        },
        error:function () {
          alert("未知错误！");
        }
      });
  });
}




function show_paging(curpage, pages) {
    str = '';
    if(curpage > 1) {
        str += '<li><a rel="1" href="javascript:void(0)" class="pg_index">首页</a></li><li><a rel='+(parseInt(curpage)-1)+' href="javascript:void(0)">'+(parseInt(curpage)-1)+'</a></li>';
    }
    str += '<li><a href="javascript:void(0)" rel='+curpage+' class="pg_selected">'+curpage+'</a></li>';

    if(curpage < pages) {
        str += '<li><a rel='+(parseInt(curpage)+1)+' href="javascript:void(0)">'+(parseInt(curpage)+1)+'</a></li><li><a rel='+pages+' href="javascript:void(0)" class="pg_last">尾页</a></li>';
    }
    $('.page p').text("共有 "+pages+" 页数据，当前第 "+curpage+" 页");
    //console.log(str);
    $('.page ul').html(str); 
}

function board() {

  $.ajax({
      type:'POST',
      url:'/Login/getlist',
      async:true,
      cache:false,
      success:function(e) {
          var res = $.parseJSON(e);
          console.log(res);
          if(!res.status) {
              alert(res.msg);
              return;
          }
         var list = res.list;
         var data = res.data;
         var str = '';
         var td_str = '';
         for(var i in list) {
            if(i == 0){
              str += '<option checked value="'+list[i]+'">'+list[i]+'</option>';
            }else{
              str += '<option value="'+list[i]+'">'+list[i]+'</option>';
            }
         }
         BOARD_LIST_OPTION = list;
         $('#appID').html(str);

         for(var id in data) {
              var obj = data[id];
              var sum = 0;
              for(var tag in obj) {
                  sum++;
                  var day = obj[tag]['day'] ? '<a rel="day" href="javascript:;" class="templatemo-edit-btn tag"><i class="fa fa-hand-o-up" aria-hidden="true"></i></a>' : ' ';
                  var week = obj[tag]['week'] ? '<a rel="week" href="javascript:;" class="templatemo-edit-btn tag"><i class="fa fa-hand-o-up" aria-hidden="true"></i></a>' : ' ';
                  var month = obj[tag]['month'] ? '<a rel="month" href="javascript:;" class="templatemo-edit-btn tag"><i class="fa fa-hand-o-up" aria-hidden="true"></i></a>' : ' ';
                  var active = obj[tag]['st_date'] ? '<a rel="act-tag" href="javascript:;" class="templatemo-edit-btn tag"><i class="fa fa-hand-o-up" aria-hidden="true"></i></a>' : ' ';
                  var host = obj[tag]['st_date'] ? '' : '<a rel="host-tag" href="javascript:;" class="templatemo-edit-btn tag"><i class="fa fa-hand-o-up" aria-hidden="true"></i></a>';
                  if(sum % 2 != 0){
                    td_str += '<tr rel='+obj[tag]['tag']+'><td style="background:rgba(195,214,152,0.1);">'+obj[tag]['tag']+'</td><td style="background:rgba(195,214,152,0.1);">'+obj[tag]['order']+'</td><td style="background:rgba(195,214,152,0.1);">'+day+'</td><td style="background:rgba(195,214,152,0.1);">'+week+'</td><td style="background:rgba(195,214,152,0.1);">'+month+'</td><td style="background:rgba(195,214,152,0.1);">'+host+'</td><td style="background:rgba(195,214,152,0.1);">'+active+'</td><td style="background:rgba(195,214,152,0.1);"><a href="javascript:;" class="templatemo-edit-btn del-tag"><i class="fa fa-minus-square-o" aria-hidden="true"></i></a></td></tr>';
                  } else {
                    td_str += '<tr rel='+obj[tag]['tag']+'><td>'+obj[tag]['tag']+'</td><td>'+obj[tag]['order']+'</td><td>'+day+'</td><td>'+week+'</td><td>'+month+'</td><td>'+host+'</td><td>'+active+'</td><td><a href="javascript:;" class="templatemo-edit-btn del-tag"><i class="fa fa-minus-square-o" aria-hidden="true"></i></a></td></tr>';
                  }
                  
              }

              $('#tagList tbody').html(td_str);
         }
         BOARD_LIST_HTML = td_str;


      }
  });


  $('body').off('change', '#appID').on('change', '#appID', function(e) {
        var appid = $(this).val();
        getList_change(appid);
  });

  function getList_change(appid) {
    $.ajax({
        type:'POST',
        url:'/Login/getSingleList',
        async:true,
        cache:false,
        data:{
          'appid':appid,
        },
        success:function(e) {
          var res = $.parseJSON(e);
          var td_str = '';
          if(res.status) {
            var obj = res.list;
            var sum = 0;
            for(var tag in obj) {
              sum++;
              var day = obj[tag]['day'] ? '<a rel="day" href="javascript:;" class="templatemo-edit-btn tag"><i class="fa fa-hand-o-up" aria-hidden="true"></i></a>' : ' ';
              var week = obj[tag]['week'] ? '<a rel="week" href="javascript:;" class="templatemo-edit-btn tag"><i class="fa fa-hand-o-up" aria-hidden="true"></i></a>' : ' ';
              var month = obj[tag]['month'] ? '<a rel="month" href="javascript:;" class="templatemo-edit-btn tag"><i class="fa fa-hand-o-up" aria-hidden="true"></i></a>' : ' ';
              var active = obj[tag]['st_date'] ? '<a rel="act-tag" href="javascript:;" class="templatemo-edit-btn tag"><i class="fa fa-hand-o-up" aria-hidden="true"></i></a>' : ' ';
              var host = obj[tag]['st_date'] ? '' : '<a rel="host-tag" href="javascript:;" class="templatemo-edit-btn tag"><i class="fa fa-hand-o-up" aria-hidden="true"></i></a>';
              if(sum % 2 != 0){
                td_str += '<tr rel='+obj[tag]['tag']+'><td style="background:rgba(195,214,152,0.1);">'+obj[tag]['tag']+'</td><td style="background:rgba(195,214,152,0.1);">'+obj[tag]['order']+'</td><td style="background:rgba(195,214,152,0.1);">'+day+'</td><td style="background:rgba(195,214,152,0.1);">'+week+'</td><td style="background:rgba(195,214,152,0.1);">'+month+'</td><td style="background:rgba(195,214,152,0.1);">'+host+'</td><td style="background:rgba(195,214,152,0.1);">'+active+'</td><td style="background:rgba(195,214,152,0.1);"><a href="javascript:;" class="templatemo-edit-btn del-tag"><i class="fa fa-minus-square-o" aria-hidden="true"></i></a></td></tr>';
              } else {
                td_str += '<tr rel='+obj[tag]['tag']+'><td>'+obj[tag]['tag']+'</td><td>'+obj[tag]['order']+'</td><td>'+day+'</td><td>'+week+'</td><td>'+month+'</td><td>'+host+'</td><td>'+active+'</td><td><a href="javascript:;" class="templatemo-edit-btn del-tag"><i class="fa fa-minus-square-o" aria-hidden="true"></i></a></td></tr>';
              }
            }
            BOARD_LIST_HTML = td_str;
            $('#tagList tbody').html(td_str);
          }else{
             $('#tagList tbody').html('');
          }
        }
    });
  }

  $('body').off('click', 'tbody a.tag').on('click', 'tbody a.tag', function(e) {
        tag1 = $(this).parents('tr').attr('rel');
        $(this).css('background','#39ADB4').parent('td').siblings('td').children('a.tag').css('background','white').parents('tr').siblings('tr').find('a.tag').css('background','white');
        list_order = $(this).parents('tr').children('td:eq(1)').text();
        var tag = $(this).parents('tr').children('td:first').text();
        var type = $(this).attr('rel');
        var appid = $('#appID').val();
        show_getDetailList(tag, type, appid);
  });

  function show_getDetailList(tag, type, appid) {
    $.ajax({
      type:'POST',
      url:'/Login/getDetailList',
      async:true,
      cache:false,
      data:{
        'tag':tag,
        'type':type,
        'appid':appid
      },
      success:function(e) {
        var res = $.parseJSON(e);
        if(!(res.status)){
          alert(res.msg);
          return;
        }
        console.log(res);
        $('#show_table').load('pages/board.htm', function(response, status, xhr) {
            $('#board_p').attr('rel', appid);
            $('#board_p').attr('tag', tag);
            $('#board_p').attr('type', type);
        //if(res.status) {
            var list = res.list;
            var td_str = '';
            for(var index in list) {
                var pattern = new RegExp(["day"|"week"|"month"]);
                // if(pattern.test(list[index])) {
                    var pattern2 = /(day|week|month)(:\d+)/g;
                    var val = pattern2.exec(list[index]);
                    if(val) {
                      val = val[0];
                    }else{
                      val = list[index];
                    }
                    if(index % 2 == 0){
                      td_str += '<tr rel='+list[index]+'><td style="background:rgba(195,214,152,0.1);">'+val+'</td><td style="background:rgba(195,214,152,0.1);"><a href="javascript:;" class="templatemo-edit-btn tag2 test111"><i class="fa fa-hand-o-up" aria-hidden="true"></i></a></td><td style="background:rgba(195,214,152,0.1);"><a class="templatemo-edit-btn del-tag2" href="javascript:;"><i class="fa fa-minus-square-o" aria-hidden="true"></i></a></td></tr>';
                    } else {
                      td_str += '<tr rel='+list[index]+'><td>'+val+'</td><td><a href="javascript:;" class="templatemo-edit-btn tag2 test111"><i class="fa fa-hand-o-up" aria-hidden="true"></i></a></td><td><a class="templatemo-edit-btn del-tag2" href="javascript:;"><i class="fa fa-minus-square-o" aria-hidden="true"></i></a></td></tr>';
                    }
                // }
                
            }
             TAGE2_LIST_HTML = td_str;
             $('#tag2List tbody').html(td_str);
        });
      }
    });
  }

  $('body').off('click', '#show_list').on('click', '#show_list', function(){
    var appid = $('#board_p').attr('rel');
    $('#show_table').load('pages/board_list.htm', function(response, status, xhr) {
         var str = "";
         for(var i in BOARD_LIST_OPTION) {
            if(BOARD_LIST_OPTION[i] == appid){
              str += '<option selected = "selected" value="'+BOARD_LIST_OPTION[i]+'">'+BOARD_LIST_OPTION[i]+'</option>';
            }else{
              str += '<option value="'+BOARD_LIST_OPTION[i]+'">'+BOARD_LIST_OPTION[i]+'</option>';
            }
         }
         $('#appID').html(str);
         $('#tagList tbody').html(BOARD_LIST_HTML);
    }); 
  });

  $('body').off('click', '#show_tag2List').on('click', '#show_tag2List', function(){
    var appid = $('#board2_p').attr('rel');
    var type = $('#board2_p').attr('type');
    var tag = $('#board2_p').attr('tag');
    $('#show_table').load('pages/board.htm', function(response, status, xhr) {
         $('#tag2List tbody').html(TAGE2_LIST_HTML);
         $('#board_p').attr('rel', appid);
         $('#board_p').attr('type', type);
         $('#board_p').attr('tag', tag);
    }); 
  });


  //翻页
  $('body').off('click', '.page ul li').on('click', '.page ul li', function(e) {
        pageNum = $(this).children('a').attr('rel');
        console.log(pageNum);
        show_getUserInfo();

  });

  function show_getUserInfo() {
    var key = tag2;
    var appid = $('#board2_p').attr('rel');
    $.ajax({
      type:'POST',
      url:'/Login/getUserInfo',
      async:true,
      cache:false,
      data:{
       'key':key,
       'appid':appid,
       'order':list_order,
       'pageNum':pageNum
      },
      success:function(e) {
        var res = $.parseJSON(e);
        console.log(res);
        if(!(res.status)) {
          alert(res.msg);
          return;
        }
        var list = res.data;
        var td_str = '';
        for(var i in list) {
             if(i % 2 == 0){
               td_str += '<tr><td style="background:rgba(195,214,152,0.1);">'+list[i]['index']+'</td><td style="background:rgba(195,214,152,0.1);">'+list[i]['uid']+'</td><td style="background:rgba(195,214,152,0.1);">'+list[i]['score']+'</td><td style="background:rgba(195,214,152,0.1);">'+list[i]['userInfo']+'</td><td style="background:rgba(195,214,152,0.1);"><a href="javascript:;" class="templatemo-edit-btn tag3"><i class="fa fa-cog" aria-hidden="true"></i></a></td><td style="background:rgba(195,214,152,0.1);"><a href="javascript:;" class="tag3"><input type="checkbox" class="check_del" style="display:block;"/></a></td></tr>';
             } else {
               td_str += '<tr><td>'+list[i]['index']+'</td><td>'+list[i]['uid']+'</td><td>'+list[i]['score']+'</td><td>'+list[i]['userInfo']+'</td><td><a href="javascript:;" class="templatemo-edit-btn tag3"><i class="fa fa-cog" aria-hidden="true"></i></a></td><td><a href="javascript:;" class="tag3"><input type="checkbox" class="check_del" style="display:block;"/></a></td></tr>';
             }
        }
        $('#tag3List tbody').html(td_str);
         show_paging(pageNum, res.count_page);
      }
    });

  }


  

  $('body').off('click', '#tag2List tbody a.tag2').on('click', '#tag2List tbody a.tag2', function(e) {
        tag2 = $(this).parents('tr').attr("rel");
        $(this).addClass('choosed_tag').parents('tr').siblings('tr').find('a.tag2').removeClass('choosed_tag');
        $(this).css('background', '#39ADB4').parents('tr').siblings('tr').find('a.tag2').css('background','white');
        var key = $(this).parents('tr').attr('rel');
        var appid = $('#board_p').attr('rel');
        var type = $('#board_p').attr('type');
        var tag = $('#board_p').attr('tag');
        $.ajax({
          type:'POST',
          url:'/Login/getUserInfo',
          async:true,
          cache:false,
          data:{
           'key':key,
           'appid':appid,
           'order':list_order,
           'pageNum':pageNum
          },
          success:function(e) {
            var res = $.parseJSON(e);
            if(!(res.status)){
              alert(res.msg);
              return;
            }
            $('#show_table').load('pages/board2.htm', function(response, status, xhr) {
                $('#board2_p').attr('rel', appid);
                $('#board2_p').attr('type', type);
                $('#board2_p').attr('tag', tag);
                var list = res.data;
                var td_str = '';
                for(var i in list) {
                     if(i % 2 == 0){
                       td_str += '<tr><td style="background:rgba(195,214,152,0.1);">'+list[i]['index']+'</td><td style="background:rgba(195,214,152,0.1);">'+list[i]['uid']+'</td><td style="background:rgba(195,214,152,0.1);">'+list[i]['score']+'</td><td style="background:rgba(195,214,152,0.1);">'+list[i]['userInfo']+'</td><td style="background:rgba(195,214,152,0.1);"><a href="javascript:;" class="templatemo-edit-btn tag3"><i class="fa fa-cog" aria-hidden="true"></i></a></td><td style="background:rgba(195,214,152,0.1);"><a href="javascript:;" class="tag3"><input type="checkbox" class="check_del" style="display:block;"/></a></td></tr>';
                     } else {
                       td_str += '<tr><td>'+list[i]['index']+'</td><td>'+list[i]['uid']+'</td><td>'+list[i]['score']+'</td><td>'+list[i]['userInfo']+'</td><td><a href="javascript:;" class="templatemo-edit-btn tag3"><i class="fa fa-cog" aria-hidden="true"></i></a></td><td><a href="javascript:;" class="tag3"><input type="checkbox" class="check_del" style="display:block;"/></a></td></tr>';
                     } 
                }
                $('#tag3List tbody').html(td_str);
                 show_paging(pageNum, res.count_page);
            });
           
          }

         
        });
  });

  $('body').off('click', '.del-tag').on('click', '.del-tag', function(e) {

        if(!confirm('确认删除？')) {
          return;
        }
        //$(this).parents('tr').remove();
        var appid = $('#appID').val();
        var tag = $(this).parents('tr').children('td:eq(0)').text();
         $.ajax({
          type:'POST',
          url:'/Login/delTag',
          async:true,
          cache:false,
          data:{
           'appid':appid,
           'tag':tag,

          },
          success:function(e) {
            var res = $.parseJSON(e);
            if(!(res.status)){
              alert(res.msg);
              return;
            }
            alert(res.msg);
            getList_change(appid);
          }
        });
  });
  $('body').off('click', '.del-tag2').on('click', '.del-tag2', function(e) {
      if(!confirm('确认删除？')) {
        return;
      }
       //$(this).parents('tr').remove();
       var tag = $(this).parents('tr').attr('rel');
         $.ajax({
          type:'POST',
          url:'/Login/delTag2',
          async:true,
          cache:false,
          data:{
           'tag':tag,

          },
          success:function(e) {
            var res = $.parseJSON(e);
            if(!(res.status)){
              alert(res.msg);
              return;
            }
            alert(res.msg);
            var appid = $('#board_p').attr('rel');
            var type = $('#board_p').attr('type');
            var tag1 = $('#board_p').attr('tag');
            show_getDetailList(tag1, type, appid);
          }
        });
  });


　 $('body').off('click', '#select_all').on('click', '#select_all', function(){
     if($('.check_del').prop('checked') == true){
       $('.check_del').prop('checked', false);
     } else {
       $('.check_del').prop('checked', true);
     }
   });

   $('body').off('click', '#del_all_users').on('click', '#del_all_users', function(e) {
        if(!confirm("确认删除全部，无法恢复？")) {
          return;
        }
        var uids = new Array();
        for (var i = 0; i < $('.check_del').length; i++) {
          if($('.check_del:eq('+i+')').prop('checked') == false){
             continue;
          }
          uids.push($('.check_del:eq('+i+')').parents('tr').children('td:eq(1)').text());
        }
        if(uids.length == 0){
          alert('请先选择，再删除');
          return;
        }
        uids = uids.join(',');
         $.ajax({
          type:'POST',
          url:'/Login/delTag4',
          async:true,
          cache:false,
          data:{
           'tag':tag2,
           'uids':uids

          },
          success:function(e) {
            var res = $.parseJSON(e);
            if(!(res.status)){
              alert(res.msg);
              return;
            } 
            alert(res.msg);
            show_getUserInfo();
          }
        });


        
   });  

  $('body').off('click', '#addUserScore').on('click', '#addUserScore', function(e) {
      $('#mymodal').modal("show");
      $('#mymodal').on('shown.bs.modal', function () {
        $('.myinput').val("");
        $('.myinput:eq(0)').focus();
      })
  });


   $('body').off('click', '#label_save').on('click', '#label_save', function(e) {

          var uid = $('.myinput:eq(0)').val();
          var score = $('.myinput:eq(1)').val();
          var info = $('.myinput:eq(2)').val();
          var appid = $('#board2_p').attr('rel');
          if(!uid || !info){
            alert('UID与用户信息不可以为空');
            return;
          }
          $('#mymodal').modal("hide");
          $.ajax({
              type:'POST',
              url:'/Login/addUserScore',
              async:true,
              cache:false,
              data:{
                'uid':uid,
                'score':score,
                'info':info,
                'key':tag2,
                'appid':appid
              },
              success:function(e) {
                var res = $.parseJSON(e);
                if(!(res.status)){
                  alert(res.msg);
                  return;
                }
                alert(res.msg);
                show_getUserInfo();
              }

          });



   });
}


function add_board() {

    $('body').off('click', '#submit_board').on('click', '#submit_board', function(e) {
         
            var app_id = $('#app_id').val();
            var tag_name = $('#board_name').val();
            var order = $('input[name="order"]:checked').val();
            var date = new Array();
            $('input[name="date"]:checked').each(function(e) {
                date.push($(this).val());
            });
            $.ajax({
              url:'/Login/add_board',
              async:true,
              cache:false,
              type:'POST',
              data:{
                'app_id':app_id,
                'tag_name':tag_name,
                'order':order,
                'date':date
              },
              success:function(e) {
                var res = $.parseJSON(e);
                if(res.status == 1) {
                  alert("创建榜单成功！");
                  $('#board').click();
                  return;
                }
                alert('此榜单已经存在，请重新创建！');
              }
            });
    });
}


function add_active_board() {

    $('body').off('click', '#submit_active_board').on('click', '#submit_active_board', function(e) {
         
            var app_id = $('#app_active_id').val();
            var tag_name = $('#board_active_name').val();
            var order = $('input[name="order_active"]:checked').val();
            
            var start_date = $('#start_date').val();
            var end_date = $('#end_date').val();
            $.ajax({
              url:'/Login/add_board',
              async:true,
              cache:false,
              type:'POST',
              data:{
                'app_id':app_id,
                'tag_name':tag_name,
                'order':order,
                'start_date':start_date,
                'end_date':end_date
              },
              success:function(e) {
                var res = $.parseJSON(e);
                if(res.status == 1) {
                  alert("创建榜单成功！");
                  $('#board').click();
                  return;
                }
                alert('创建榜单失败！');
              }
            });
    });
}