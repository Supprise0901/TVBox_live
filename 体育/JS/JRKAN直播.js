var rule = {
    title:'JRKAN直播',
    host:'http://www.jryyds.com',
    url:'/fyclass',
    searchUrl:'',
    searchable:0,
    quickSearch:0,
    class_name:'全部',
    class_url:'/',
    //class_url:'?live',
    headers:{
        'User-Agent':'MOBILE_UA'
    },
    timeout:5000,
    play_parse:true,
    lazy:'',
    limit:6,
    double:false,
    推荐:'*',
    // 一级播放线路x3 可自行切换
    //一级:'.loc_match .d-touch;li&&Text;img&&src;.lab_time&&Text;a:eq(0)&&href',//play.sportsteam365.com
    一级:'.loc_match:eq(2) ul;li:gt(1):lt(4)&&Text;img&&src;li:lt(2)&&Text;a:eq(1)&&href',//play.sportsteam333.com
    //一级:'.loc_match .d-touch;li&&Text;img&&src;.lab_time&&Text;a:eq(2)&&href',//play.sportsteam666.com
    二级:{title:'.sub_list li:lt(2)&&Text;.sub_list li:eq(0)&&Text',img:'img&&src',desc:';;;.lab_team_home&&Text;.lab_team_away&&Text',content:'.sub_list ul&&Text',tabs:'',tab_text:'',lists:'.sub_channel a',list_text:'a&&Text',list_url:'a&&data-play'},
    搜索:'',
}