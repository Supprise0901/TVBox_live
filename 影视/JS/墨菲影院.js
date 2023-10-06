muban.短视2.二级.img = '.detail-pic&&img&&data-original';
var rule = {
    title: 'MOFLIX',
    模板:'短视2',
    host: 'http://4.567.li',
    homeUrl:'/index.php/label/rb.html',
    // url: '/index.php/api/vod#type=fyclass&page=fypage',
    url: '/index.php/api/vod#type=fyfilter&page=fypage',
    filterable:1,//是否启用分类筛选,
    filter_url:'{{fl.cateId}}',
    filter: {
        "1":[{"key":"cateId","name":"分类","value":[{"n":"全部","v":"1"},{"n":"动作片","v":"27"},{"n":"喜剧片","v":"28"},{"n":"爱情片","v":"29"},{"n":"科幻片","v":"30"},{"n":"剧情片","v":"31"},{"n":"恐怖片","v":"32"},{"n":"战争片","v":"33"}]}],
        "2":[{"key":"cateId","name":"分类","value":[{"n":"全部","v":"2"},{"n":"国产剧","v":"34"},{"n":"港台剧","v":"35"},{"n":"欧美剧","v":"36"},{"n":"日韩剧","v":"37"},{"n":"东南亚剧","v":"38"},{"n":"短剧","v":"39"}]}],
        "3":[{"key":"cateId","name":"分类","value":[{"n":"全部","v":"3"},{"n":"大陆综艺","v":"39"},{"n":"港台综艺","v":"40"},{"n":"日韩综艺","v":"41"},{"n":"欧美综艺","v":"42"}]}],
        "4":[{"key":"cateId","name":"分类","value":[{"n":"全部","v":"4"},{"n":"国产动漫","v":"43"},{"n":"日韩动漫","v":"44"},{"n":"欧美动漫","v":"45"}]}]
    },
    filter_def:{
        1:{cateId:'1'},
        2:{cateId:'2'},
        3:{cateId:'3'},
        4:{cateId:'4'}
    },
    class_parse:'.swiper-wrapper&&li;a&&Text;a&&href;.*/(\\d+).html',
    class_name:'',
    class_url:'',
    detailUrl:'/index.php/vod/detail/id/fyid.html',
    tab_exclude:'高清线路C|hnm3u8',
    推荐:'.border-box .public-list-box;a&&title;.lazy&&data-original;.public-list-prb&&Text;a&&href',
    double: false, // 推荐内容是否双层定位
    一级:'js:let body=input.split("#")[1];let t=Math.round(new Date/1e3).toString();let key=md5("DS"+t+"DCC147D11943AF75");let url=input.split("#")[0];body=body+"&time="+t+"&key="+key;print(body);fetch_params.body=body;let html=post(url,fetch_params);let data=JSON.parse(html);VODS=data.list.map(function(it){it.vod_pic=it.vod_pic.replace("mac:","https:");return it});',
}
