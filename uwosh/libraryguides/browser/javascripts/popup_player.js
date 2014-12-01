/* 
 * Popup Video Panel
 * Copyright 2012, David Hietpas
 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *   http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * 
 * 
 * 
 * This doesn't work via Jquery, you can add this snippet into CSS, makes the player look shiny.
 * 
 * 		background: rgb(0,0,0);
 *		background: -moz-linear-gradient(top,  rgba(0,0,0,1) 0%, rgba(94,94,94,1) 12%, rgba(0,0,0,1) 13%, rgba(0,0,0,1) 100%); 
 *		background: -webkit-gradient(linear, left top, left bottom, color-stop(0%,rgba(0,0,0,1)), color-stop(12%,rgba(94,94,94,1)), color-stop(13%,rgba(0,0,0,1)), color-stop(100%,rgba(0,0,0,1)));
 *		background: -webkit-linear-gradient(top,  rgba(0,0,0,1) 0%,rgba(94,94,94,1) 12%,rgba(0,0,0,1) 13%,rgba(0,0,0,1) 100%); 
 *		background: -o-linear-gradient(top,  rgba(0,0,0,1) 0%,rgba(94,94,94,1) 12%,rgba(0,0,0,1) 13%,rgba(0,0,0,1) 100%); 
 *		background: -ms-linear-gradient(top,  rgba(0,0,0,1) 0%,rgba(94,94,94,1) 12%,rgba(0,0,0,1) 13%,rgba(0,0,0,1) 100%); 
 *		background: linear-gradient(to bottom,  rgba(0,0,0,1) 0%,rgba(94,94,94,1) 12%,rgba(0,0,0,1) 13%,rgba(0,0,0,1) 100%);
 *		filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#000000', endColorstr='#000000',GradientType=0 );
 *
 * 
 */



var PopPlayer = {
	
	embed_id : null,
	embed_code : null,
	embed_fn : function(){ return null; },
	player_css : {'background-color':'black','opacity':'1.0','padding':'5px 10px 5px 10px','border':'1px solid #333333',
	              'margin':'25px auto 0','display':'inline-block','border-radius':'15px','box-shadow':'0px 0px 22px 2px #000000',
				  '-webkit-box-shadow':'0px 0px 22px 2px #000000'},
	exit_css : {'background-color':'black','border':'1px solid #333333','width':'150px','height':'50px','margin':'40px auto 0',
	            'border-radius':'15px','box-shadow':'0px 0px 22px 2px #000000','-webkit-box-shadow':'0px 0px 22px 2px #000000',
				'color':'white','font-size':'2em','font-weight':'bold','cursor':'pointer'
				},
	exit_text_css : {'line-height':'50px','text-shadow':'0px 0px 5px #000000','filter':'dropshadow(color=#000000,offx=0,offy=0)'},
	exit_text : "Exit Player",
	back_general_css : {'display':'none','left':'0','top':'0','position':'fixed','width':'100%',
				'height':'5000px','text-align':'center'},
	back_fade_css : {'opacity':'0.75','background-color':'black','z-index':'100',},
	back_pane_css : {'z-index':'101'},
	
	link_css : {'color':'white','padding-top':'10px','text-decoration':'none','font-size':'1.3em'},
	
	_full_link : '',
	_full_link_title : '',
	_player_code : '',

	init : function (selector,parameters){
		for (var i in parameters) 
			if (parameters.hasOwnProperty(i)) 
				PopPlayer[i] = parameters[i];
		
		PopPlayer._set_player();
		PopPlayer._backdrop_setup();
		PopPlayer._player_setup();
		PopPlayer.open_handler(selector);
		PopPlayer.close_handler();
		PopPlayer._esc_setup();

	},
	
	open_handler : function (selector){
		jq(selector).click(function(){
			PopPlayer._start_player();
			jq('#pop_closer').show();
			jq('#pop_backdrop,#pop_pane').fadeIn('fast');
		});
	},
	
	close_handler : function () {
		jq('#pop_closer').click(function(){
			PopPlayer._stop_player();
		});
	},
	
	_set_player : function() {
		var player = PopPlayer.embed_fn();
		if(player != null)
			PopPlayer._player_code = player;
		else if (PopPlayer.embed_code != null)
			PopPlayer._player_code = PopPlayer.embed_code;
		else if (PopPlayer.embed_id != null)
			PopPlayer._player_code = jq(PopPlayer.embed_id).clone();
	},
	
	_backdrop_setup : function() {
		var backdrop = document.createElement('div');
		jq(backdrop).attr('id','pop_backdrop');
		jq(backdrop).css(PopPlayer.back_general_css);
		jq(backdrop).css(PopPlayer.back_fade_css);
		jq('body').append(backdrop);
	},
	
	_start_player : function() {
		jq('#pop_player').html(PopPlayer._player_code);
		if (PopPlayer._full_link != null) {
			var link = document.createElement('a');
			jq(link).attr({'id':'pop_link',
						   'href':PopPlayer._full_link
						   });
			jq(link).css(PopPlayer.link_css);
			jq(link).html(PopPlayer._full_link_title);
			jq('#pop_player').append("<br />");
			jq('#pop_player').append(link);
		}
	},
	
	_stop_player : function() {
		jq('#pop_player').html("");
		jq('#pop_closer').hide();
		jq('#pop_backdrop, #pop_pane').fadeOut('fast');
	},
	
	_player_setup : function() {
		var container = document.createElement('div');
		jq(container).attr('id','pop_pane');
		jq(container).css(PopPlayer.back_general_css);
		jq(container).css(PopPlayer.back_pane_css);
		
		var player = document.createElement('div');
		jq(player).attr('id','pop_player');
		jq(player).css(PopPlayer.player_css);
		PopPlayer._start_player();
		
		var closer = document.createElement('div');
		jq(closer).attr('id','pop_closer');
		jq(closer).css(PopPlayer.exit_css);
		var text = document.createElement('span');
		jq(text).css(PopPlayer.exit_text_css);
		jq(text).html(PopPlayer.exit_text)
		jq(closer).html(text);
		
		jq(container).append(player);
		jq(container).append(closer);
		jq('body').append(container);
	},
	
	_esc_setup : function() {
		jq(document).keyup( function(e){
			if (e.keyCode == 27)
				PopPlayer._stop_player();
		});
	}
	
	
	
	
	
	
}