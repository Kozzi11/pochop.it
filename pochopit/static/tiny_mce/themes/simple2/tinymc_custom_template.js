/**
 * editor_template_src.js
 *
 * Copyright 2009, Moxiecode Systems AB
 * Released under LGPL License.
 *
 * License: http://tinymce.moxiecode.com/license
 * Contributing: http://tinymce.moxiecode.com/contributing
 */

(function() {
	var DOM = tinymce.DOM;

	// Tell it to load theme specific language pack(s)
	//tinymce.ThemeManager.requireLangPack('simple');
	tinymce.ScriptLoader.add('/static/tiny_mce/themes/simple2/langs/cs.js');
	tinymce.create('tinymce.themes.Simple2Theme', {
		init : function(ed, url) {
			var t = this, states = ['Bold', 'Italic', 'Underline', 'Codeblock', 'Strikethrough', 'InsertUnorderedList', 'InsertOrderedList'], s = ed.settings;

			t.editor = ed;
			ed.contentCSS.push(url + "/skins/" + s.skin + "/content.css");

            // Register Codeblock command
            ed.addCommand('Codeblock', function(ui, v) {
				var div = $('<div style="position:absolute; top: -1000px"></div>');
				div.html('<pre class="prettyprint"><code>' + ed.selection.getContent() + '</code></pre>');
				$(document.body).append(div);
     			PR.prettyPrint();
                ed.selection.setContent(div.html() + '<p>&nbsp;</p>');
				div.remove();
            });

			ed.onInit.add(function() {
				ed.onNodeChange.add(function(ed, cm) {
					tinymce.each(states, function(c) {
						cm.get(c.toLowerCase()).setActive(ed.queryCommandState(c));
					});
				});
			});

			DOM.loadCSS((s.editor_css ? ed.documentBaseURI.toAbsolute(s.editor_css) : '') || url + "/skins/" + s.skin + "/ui.css");
		},

		renderUI : function(o) {
			var t = this, n = o.targetNode, ic, tb, ed = t.editor, cf = ed.controlManager, sc;

			n = DOM.insertAfter(DOM.create('span', {id : ed.id + '_container', 'class' : 'mceEditor ' + ed.settings.skin + 'SimpleSkin'}), n);
			n = sc = DOM.add(n, 'table', {cellPadding : 0, cellSpacing : 0, 'class' : 'mceLayout'});
			n = tb = DOM.add(n, 'tbody');

			// Create iframe container
			n = DOM.add(tb, 'tr');
			n = ic = DOM.add(DOM.add(n, 'td'), 'div', {'class' : 'mceIframeContainer'});

			// Create toolbar container
			n = DOM.add(DOM.add(tb, 'tr', {'class' : 'last'}), 'td', {'class' : 'mceToolbar mceLast', align : 'center'});

			// Create toolbar
			tb = t.toolbar = cf.createToolbar("tools1");
			tb.add(cf.createButton('bold', {title : 'simple2.bold_desc', cmd : 'Bold'}));
			tb.add(cf.createButton('italic', {title : 'simple2.italic_desc', cmd : 'Italic'}));
			tb.add(cf.createButton('underline', {title : 'simple2.underline_desc', cmd : 'Underline'}));
			tb.add(cf.createButton('strikethrough', {title : 'simple2.striketrough_desc', cmd : 'Strikethrough'}));
			tb.add(cf.createSeparator());
            tb.add(cf.createButton('codeblock', {title : 'simple2.code', cmd : 'Codeblock'}));
            tb.add(cf.createSeparator());
			tb.add(cf.createButton('undo', {title : 'simple2.undo_desc', cmd : 'Undo'}));
			tb.add(cf.createButton('redo', {title : 'simple2.redo_desc', cmd : 'Redo'}));
			tb.add(cf.createSeparator());
			tb.add(cf.createButton('cleanup', {title : 'simple2.cleanup_desc', cmd : 'mceCleanup'}));
			tb.add(cf.createSeparator());
			tb.add(cf.createButton('insertunorderedlist', {title : 'simple2.bullist_desc', cmd : 'InsertUnorderedList'}));
			tb.add(cf.createButton('insertorderedlist', {title : 'simple2.numlist_desc', cmd : 'InsertOrderedList'}));
			tb.renderTo(n);

			return {
				iframeContainer : ic,
				editorContainer : ed.id + '_container',
				sizeContainer : sc,
				deltaHeight : -20
			};
		},

		getInfo : function() {
			return {
				longname : 'Simple2 theme',
				author : 'Moxiecode Systems AB',
				authorurl : 'http://tinymce.moxiecode.com',
				version : tinymce.majorVersion + "." + tinymce.minorVersion
			}
		}
	});

	tinymce.ThemeManager.add('simple2', tinymce.themes.Simple2Theme);
})();