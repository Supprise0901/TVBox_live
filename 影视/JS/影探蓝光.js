var rule = {
	title: '影探[V2]', // csp_AppYsV2
	//host: 'http://big.lfytyl.com',
	host: 'http://app.lyyytv.cn/yt/yt.json',
	hostJs:'let html=request(HOST,{headers:{"User-Agent":PC_UA}});let obj=JSON.parse(html);HOST=obj.sites[0].ext;',
	homeUrl:'/api.php/app/index_video',
	url: '/api.php/app/video?tid=fyclassfyfilter&limit=18&pg=fypage',
	filter_url:'&class={{fl.class}}&area={{fl.area}}&lang={{fl.lang}}&year={{fl.year}}',
	filter: {
		"1":[{"key":"class","name":"剧情","value":[{"n":"全部","v":""}]},{"key":"area","name":"地区","value":[{"n":"全部","v":""}]},{"key":"lang","name":"语言","value":[{"n":"全部","v":""}]},{"key":"year","name":"年份","value":[{"n":"全部","v":""}]}],
		"2":[{"key":"class","name":"剧情","value":[{"n":"全部","v":""}]},{"key":"area","name":"地区","value":[{"n":"全部","v":""}]},{"key":"lang","name":"语言","value":[{"n":"全部","v":""}]},{"key":"year","name":"年份","value":[{"n":"全部","v":""}]}],
		"3":[{"key":"class","name":"剧情","value":[{"n":"全部","v":""}]},{"key":"area","name":"地区","value":[{"n":"全部","v":""}]},{"key":"lang","name":"语言","value":[{"n":"全部","v":""}]},{"key":"year","name":"年份","value":[{"n":"全部","v":""}]}],
		"4":[{"key":"class","name":"剧情","value":[{"n":"全部","v":""}]},{"key":"area","name":"地区","value":[{"n":"全部","v":""}]},{"key":"lang","name":"语言","value":[{"n":"全部","v":""}]},{"key":"year","name":"年份","value":[{"n":"全部","v":""}]}],
		"20":[{"key":"class","name":"剧情","value":[{"n":"全部","v":""}]},{"key":"area","name":"地区","value":[{"n":"全部","v":""}]},{"key":"lang","name":"语言","value":[{"n":"全部","v":""}]},{"key":"year","name":"年份","value":[{"n":"全部","v":""}]}],
		"21":[{"key":"class","name":"剧情","value":[{"n":"全部","v":""}]},{"key":"area","name":"地区","value":[{"n":"全部","v":""}]},{"key":"lang","name":"语言","value":[{"n":"全部","v":""}]},{"key":"year","name":"年份","value":[{"n":"全部","v":""}]}],
		"47":[{"key":"class","name":"剧情","value":[{"n":"全部","v":""}]},{"key":"area","name":"地区","value":[{"n":"全部","v":""}]},{"key":"lang","name":"语言","value":[{"n":"全部","v":""}]},{"key":"year","name":"年份","value":[{"n":"全部","v":""}]}]
	},
	detailUrl:'/api.php/app/video_detail?id=fyid',
	searchUrl: '/api.php/app/search?text=**&pg=fypage',
	searchable: 2,
	quickSearch: 0,
	filterable:1,
	headers:{'User-Agent':'Dart/2.14 (dart:io)'},
	timeout:5000,
	class_name:'新电影4K&新剧4K&好莱坞精选4K&电影&连续剧&动漫&综艺', // 分类筛选 /api.php/app/nav
	class_url:'20&21&47&1&2&4&3',
	play_parse:true,
	lazy:'js:if(/m3u8|mp4|mkv/.test(input)){input={jx:0,url:input.replace(/+/g, "%20"),parse:0,header:JSON.stringify({"user-agent":"Lavf/58.12.100"})}}else{let purl=request("http://bingfa.behds.cn/indexappzhuanyong.php?url="+input);input={jx:0,url:JSON.parse(purl).url,parse:0}}',
	limit:6,
	推荐:'json:list[0].vlist;*;*;*;*',
	一级:'json:list;vod_name;vod_pic;vod_remarks||vod_score;vod_id',
	二级:'js:try{let html=request(input);print(html);html=JSON.parse(html);let node=html.data;VOD={vod_id:node["vod_id"],vod_name:node["vod_name"],vod_pic:node["vod_pic"],type_name:node["vod_class"],vod_year:node["vod_year"],vod_area:node["vod_area"],vod_remarks:node["vod_remarks"],vod_actor:node["vod_actor"],vod_director:node["vod_director"],vod_content:node["vod_content"].strip()};let episodes=node.vod_url_with_player;let playMap={};if(typeof play_url==="undefined"){var play_url=""}episodes.forEach(function(ep){let source=ep["name"];if(!playMap.hasOwnProperty(source)){playMap[source]=[]}playMap[source].append(ep["url"])});let playFrom=[];let playList=[];Object.keys(playMap).forEach(function(key){playFrom.append(key);playList.append(playMap[key])});let vod_play_from=playFrom.join("$$$");let vod_play_url=playList.join("$$$");VOD["vod_play_from"]=vod_play_from;VOD["vod_play_url"]=vod_play_url}catch(e){log("获取二级详情页发生错误:"+e.message)}',
	搜索:'*',
}