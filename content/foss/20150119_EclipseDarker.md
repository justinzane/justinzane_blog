Title: Python Bring the Darkness to Eclipse Luna
Category: foss
Tags: python, eclipse, dark, theme
Summary: Making Eclipse Luna *Really* Dark with Python

# Python Bring the Darkness to Eclipse Luna

With the *Luna* release, Eclipse now has a built in "dark" theme. Of course, it is not really 
dark, just sorta greyish. I want **DARKNESS**; and the very nice EclipseColorTheme plugin, while 
perfect for editor windows, does nothing for the IDE itself. So, time to fix things by hand...

Since the Eclipse integrated dark theme is derived from 
[*Moonrise UI*](https://github.com/guari/eclipse-ui-theme) which is conveniently on GitHub, it 
is really pretty easy to start fixing things. Just clone the repo and get hacking...

Initially I tried adjusting the colors in `moonrise-ui.css` by hand. However, with the 
less-than-self-explanatory class names and the paucity of inline documentation; this was not a 
promising approach.

So I decided to do the following:

## Gnu Utils Prep

Since the CSS file has inconsistent use of abbreviated colors, like "#333" instead of "#333333", 
it was necessary to use *sed* to make things consistent.

	#!/usr/bin/sh
	for i in 0 1 2 3 4 5 6 7 8 9 A B C D E F a b c d e f; do
		sed -i "s/#$i$i$i;/#$i$i$i$i$i$i;/" moonrise-ui.css
	done;
	
Then, in order to get a coherent list of used colors, *grep* and *tr* come in handy.

	#!/usr/bin/sh
	grep -Eho '#[0-9a-fA-F]{6,6};' moonrise-ui.css | tr A-Z a-z | sort -u > colors.txt
	
*Note: I originally looked for colors with lengths of 6 or 8; conveniently the Eclipse css does 
not appear to use transparency in CSS colors.*

## Python, HSL

Since I was to lazy to wade through all the Eclipse theming docs to see what each color was 
used for, I decided that the simplest way to darken my IDE was to convert all the color to 
[HSL](https://en.wikipedia.org/wiki/HSL_and_HSV) space and adjust the lightness by 75% towards 
black or white for dark and light colors respectively. As an added touch, I also boosted the 
saturation as well.

	# Done Within an IPython Console using Python3
	def rgba2hsla(r, g, b, a=255):
		"""
		Utility color function; converts from RGB(A) to HCLA.
		@param r: 0-255 Red
		@param g: 0-255 Green
		@param b: 0-255 Blue
		@param a: 0-255 Alpha (Unused, passthrough parameter)
		@return (float, 0.0-2pi, Hue in radians
				float, 0.0-~7.143, Chroma
				float, 0.0-1.0,
				float, Alpha (converted from range 0-255 to 0.0-1.0) )
		"""
		rgb = {'r':r/255.0, 'g':g/255.0, 'b':b/255.0}
		mk = min(rgb, key=rgb.get)
		Mk = max(rgb, key=rgb.get)
		C = rgb[Mk] - rgb[mk]
		if C == 0.0:
			H = 0.0
		elif Mk == 'r':
			H = ((rgb['g'] - rgb['b']) / C) % 6.0
		elif Mk == 'g':
			H = ((rgb['b'] - rgb['r']) / C) + 2.0
		elif Mk == 'b':
			H = ((rgb['r'] - rgb['g']) / C) + 4.0
		L = 0.5 * (rgb[Mk] + rgb[mk])
		if L in [0.0, 1.0]:
			S = 0.0
		else:
			S = C / (1.0 - abs((2.0 * L) - 1.0))
		return (H, S, L, a/255.0)
	#
	def hsla2rgba(h, s, l, a=1.0):
		"""
		writeme
		"""
		C = s * (1.0 - abs(2.0 * l - 1.0))
		X = C * (1.0 - abs((h % 2.0) - 1.0))
		m = l - 0.5 * C
		if   0.0                 <= h and h < 1.0 * math.pi / 3.0:
			r = C + m
			g = X + m
			b = 0.0 + m
		elif 1.0 * math.pi / 3.0 <= h and h < 2.0 * math.pi / 3.0:
			r = X + m
			g = C + m
			b = 0.0 + m
		elif 2.0 * math.pi / 3.0 <= h and h < 3.0 * math.pi / 3.0:
			r = 0.0 + m
			g = C + m
			b = X + m
		elif 3.0 * math.pi / 3.0 <= h and h < 4.0 * math.pi / 3.0:
			r = 0.0 + m
			g = X + m
			b = C + m
		elif 4.0 * math.pi / 3.0 <= h and h < 5.0 * math.pi / 3.0:
			r = C + m
			g = 0.0 + m
			b = X + m
		elif 5.0 * math.pi / 3.0 <= h and h < 6.0 * math.pi / 3.0:
			r = X + m
			g = 0.0 + m
			b = C + m
		return (int(255.0 * r + 0.5),
				int(255.0 * g + 0.5),
				int(255.0 * b + 0.5),
				int(255.0 * a + 0.5))
	#
	def convert_jz():
		orig = {}
		for c in open('colors.txt', 'r').readlines():
			c = c.strip()
			r = int(c[1:3], base = 16)
			g = int(c[3:5], base = 16)
			b = int(c[5:], base = 16)
			orig[c] = [r,g,b]
	#--------
		replace = []
		for c in orig.keys():
			h,s,l,a = rgba2hsla(orig[c][0], orig[c][1], orig[c][2])
			if l > 0.5:
				diff = 1.0 - l
				diff *= 0.25
				l = 1.0 - diff
			elif l < 0.5:
				l *= 0.25
			if s > 0.0:
				diff = 1.0 - s
				diff *= 0.25
				s = 1.0 - diff
			r,g,b,a = hsla2rgba(h, s, l, a)
			new = "#%02x%02x%02x" % (r,g,b)
			replace.append([c.strip(), new])
	#---------
		mr = open("moonrise-ui-standalone.css", 'r')
		jz = open("eclipse_ui_dark_justinzane-standalone.css", 'w')
		for line in mr.readlines():
			for rep in replace:
				m = re.search(rep[0], line, flags=re.IGNORECASE)
				if m:
					line = re.sub(rep[0], rep[1], line, flags=re.IGNORECASE)
			jz.write(line)
		jz.close()
		mr.close()
	#
	convert_jz()
	
Once I had a darkened CSS file, I simply backed up the builting "dark" CSS file and replaced it 
with my own.

	#!/usr/bin/sh
	cp /path/to/eclipse/plugins/org.eclipse.ui.themes_1.0.1.v20140819-1717/css/e4-dark.css \
		/path/to/eclipse/plugins/org.eclipse.ui.themes_1.0.1.v20140819-1717/css/e4-dark.css.bak
	cp eclipse_ui_dark_justinzane.css \
		/path/to/eclipse/plugins/org.eclipse.ui.themes_1.0.1.v20140819-1717/css/e4-dark.css
		
## The Darkness

If you wish to skip the fun and just copy my derived CSS into e4-dark.css, here it is:

		/** Darkened Moonrise UI CSS */
		.MTrimmedWindow.topLevel {
			margin-top: 4px;
			margin-bottom: 2px;
			margin-left: 2px;
			margin-right: 2px;
		}
		.MPartStack {
			background-color: #030f17;
			color: #fcffff;
			swt-tab-renderer: url('bundleclass://org.eclipse.e4.ui.workbench.renderers.swt/org.eclipse.e4.ui.workbench.renderers.swt.CTabRendering');
			swt-tab-height: 32px;
			padding: 1px 6px 6px 6px; /* top left bottom right */
			swt-tab-outline: #04151c; /* border color for selected tab */
			swt-outer-keyline-color: #051c25; /* border color for whole tabs container */
			swt-unselected-tabs-color: #051c25 #04041f #030f17 99% 100%; /* title background for unselected tab */
			swt-selected-tab-fill: #030f17; /* title background for selected tab (gradient bottom color) */		
			swt-shadow-color: #030303;
			swt-shadow-visible: true;
			swt-mru-visible: true;
			swt-corner-radius: 16px;
		}
		.MPartStack.active {
			background-color: #0a0a0a;   /* ignored (<2>) */
			swt-inner-keyline-color: #ffffff;
			swt-tab-outline: #121212; /* border color for selected tab */
			swt-outer-keyline-color: #050c22; /* border color for whole tabs container */
			swt-unselected-tabs-color: #050c21 #04041d #0a0a0a 99% 100%; /* title background for unselected tab */
			swt-selected-tab-fill: #0a0a0a; /* title background for selected tab (gradient bottom color) */
		}
		.MPartStack.active > * {
			/* Workaround for (<2>) to set the color of the inner border for the active tab */
			background-color: #0a0a0a;
		}
		.MPartStack.empty {
			swt-unselected-tabs-color: #051c25 #051b24 #051b24 99% 100%; /* title background for unselected tab */
			swt-tab-outline: #050525; /* border color for selected tab */
			swt-outer-keyline-color: #051c25; /* border color for whole tabs container */
		}
		CTabItem,
		CTabItem CLabel {
			background-color: #030f17; /* HACK for background of CTabFolder inner Toolbars */
			color: #e6e6e6;
			/*font-family: 'Segoe Print';*/ /* currently, there is no way to define a fallback for font-family */
			/*font-size: 8;*/
		}
		CTabItem:selected,
		CTabItem:selected CLabel {
			color: #f7f7f7;
		}
		.MPartStack.active > CTabItem,
		.MPartStack.active > CTabItem CLabel {
			background-color: #0a0a0a; /* HACK for background of CTabFolder inner Toolbars */
			color: #eaeaea;
		}
		.MPartStack.active > CTabItem:selected,
		.MPartStack.active > CTabItem:selected CLabel {
			color: #ffffff;
		}
		CTabItem.busy {
			color: #e1e1e1;
		}
		.MTrimmedWindow {
			background-color: #051c25;
		}
		.MTrimBar {
			background-color: #051c25;
		}
		.MTrimBar .Draggable {
			handle-image: url('./dragHandle.png');
		}
		.TrimStack {
			frame-cuts: 4px 2px 5px 16px;
			handle-image: url('./dragHandle.png');
		}
		CTabFolder.MArea .MPartStack,CTabFolder.MArea .MPartStack.active {
			swt-shadow-visible: false;
		}
		.MToolControl.TrimStack {
			frame-cuts: 5px 1px 5px 16px;
		}
		/* ###################### Global Styles ########################## */
		/* ++++++ Remove these to have ONLY the main IDE shell dark ++++++ */
		Composite, ScrolledComposite, ExpandableComposite, TabFolder, CLabel, Label,
		ToolItem, Sash, Group, Hyperlink, RefactoringLocationControl, Link, FilteredTree,
		ProxyEntriesComposite, NonProxyHostsComposite, DelayedFilterCheckboxTree,
		Splitter, ScrolledPageContent, ViewForm, LaunchConfigurationFilteredTree,
		ContainerSelectionGroup, BrowseCatalogItem, EncodingSettings,
		ProgressMonitorPart, DocCommentOwnerComposite, NewServerComposite,
		NewManualServerComposite, ServerTypeComposite, FigureCanvas,
		DependenciesComposite, ListEditorComposite, WrappedPageBook,
		CompareStructureViewerSwitchingPane, CompareContentViewerSwitchingPane,
		QualifiedNameComponent, RefactoringStatusViewer, ImageHyperlink,
		Button /* SWT-BUG: checkbox inner label font color is not accessible */,
		ViewForm > ToolBar, /* SWT-BUG: ToolBar do not inherit rules from ViewForm */
		/*Shell [style~='SWT.DROP_DOWN'] > GradientCanvas,*/ /* ignored */
		/* SWT-BUG dirty workaround [Eclipse Bug 419482]: a generic rule (eg: Composite > *) needed to catch an
		element without a CSS id, a CSS class and a seekable Widget name, cannot be overridden
		by a subsequent more specific rule used to correct the style for seekable elements (<1>): */
		TabFolder > Composite > *, /* Composite > CommitSearchPage$... */
		TabFolder > Composite > * > * /* [style~='SWT.NO_BACKGROUND'] <- generate E4 non-sense bugs in apparently not related other rules */, /* Composite > ContentMergeViewer$... > TextMergeViewer$... */
		DocCommentOwnerComposite > Group > *, /* Group > DocCommentOwnerComposite$... */
		TabFolder > Composite > ScrolledComposite > *, /* ScrolledComposite > ControlListViewer$... */
		Shell > Composite > Composite > *, /* Composite > StatusDialog$MessageLine (SWT-BUG: ignored) */
		Composite > Composite > Composite > ToolBar, /* Window->Preference (top toolbar) */
		Composite > Composite > Composite > Group > *, /* Group > CreateRefactoringScriptWizardPage$... */
		Shell > Composite > Composite > Composite > *, /* Composite > FilteredPreferenceDialog$... */
		ScrolledComposite > Composite > Composite > Composite > *, /* Composite > NewKeysPreferencePage$... */
		Shell > Composite > Composite > Composite > Composite > Composite > *, /* Composite > ShowRefactoringHistoryWizardPage$... */
		Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.RESIZE'][style~='SWT.MENU'][style~='SWT.FULL_SELECTION'][style~='SWT.DATE'] > Composite > *, /* Composite > RefactoringWizardDialog$... */
		Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.RESIZE'][style~='SWT.MENU'][style~='SWT.FULL_SELECTION'][style~='SWT.DATE'] > Composite > * > * /* Composite > RefactoringWizardDialog$... */ {
			background-color:#051c25;
			color:#fbfbfb;
		}
		List,
		/* It might be useless but currently it's needed due to a strange priority
		policy used by the E4 platform to apply CSS rules to SWT widgets (see <1>): */
		Composite > List,
		TabFolder > Composite > List,
		TabFolder > Composite > * > List,
		DocCommentOwnerComposite > Group > List,
		TabFolder > Composite > ScrolledComposite > List,
		Shell > Composite > Composite > List,
		Composite > Composite > Composite > Group > List,
		Shell > Composite > Composite > Composite > List,
		ScrolledComposite > Composite > Composite > Composite > List,
		Shell > Composite > Composite > Composite > Composite > Composite > List,
		Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.RESIZE'][style~='SWT.MENU'][style~='SWT.FULL_SELECTION'][style~='SWT.DATE'] > Composite > List,
		Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.RESIZE'][style~='SWT.MENU'][style~='SWT.FULL_SELECTION'][style~='SWT.DATE'] > Composite > * > List {
			background-color: #04131f;
			color: #f7f7f7;
		}
		Combo,
		/* It might be useless but currently it's needed due to a strange priority
		policy used by the E4 platform to apply CSS rules to SWT widgets (see <1>): */
		Composite > Combo,
		TabFolder > Composite > Combo,
		TabFolder > Composite > * > Combo,
		DocCommentOwnerComposite > Group > Combo,
		TabFolder > Composite > ScrolledComposite > Combo,
		Shell > Composite > Composite > Combo,
		Composite > Composite > Composite > Group > Combo,
		Shell > Composite > Composite > Composite > Combo,
		ScrolledComposite > Composite > Composite > Composite > Combo,
		Shell > Composite > Composite > Composite > Composite > Composite > Combo,
		Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.RESIZE'][style~='SWT.MENU'][style~='SWT.FULL_SELECTION'][style~='SWT.DATE'] > Composite > Combo,
		Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.RESIZE'][style~='SWT.MENU'][style~='SWT.FULL_SELECTION'][style~='SWT.DATE'] > Composite > * > Combo {
			background-color: #04131f;
			color: #f7f7f7;
		}
		/* Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.MENU'][style~='SWT.DATE'][style~='SWT.RESIZE'][style~='SWT.TITLE'][style~='SWT.APPLICATION_MODAL'][style~='SWT.FULL_SELECTION'][style~='SWT.SMOOTH'] > Composite[style~='SWT.LEFT_TO_RIGHT'], */
		Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.MENU'][style~='SWT.DATE'][style~='SWT.RESIZE'][style~='SWT.TITLE'][style~='SWT.APPLICATION_MODAL'][style~='SWT.FULL_SELECTION'][style~='SWT.SMOOTH'] > Composite[style~='SWT.LEFT_TO_RIGHT'] > Text[style~='SWT.READ_ONLY'],
		Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.MENU'][style~='SWT.DATE'][style~='SWT.RESIZE'][style~='SWT.TITLE'][style~='SWT.APPLICATION_MODAL'][style~='SWT.FULL_SELECTION'][style~='SWT.SMOOTH'] > Composite[style~='SWT.LEFT_TO_RIGHT'] > ToolBar {
			/* Dialog windows title */
			/*background-color: #051328;*/ /* There is no way to change the background-color of the title of a Dialog without introducing artifacts in some other Dialog windows */
			color: #def5fd;
		}
		Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.MENU'][style~='SWT.DATE'][style~='SWT.RESIZE'][style~='SWT.TITLE'][style~='SWT.APPLICATION_MODAL'][style~='SWT.FULL_SELECTION'][style~='SWT.SMOOTH'] > Composite[style~='SWT.LEFT_TO_RIGHT'] > Label[style~='SWT.NO_FOCUS'] {
			/* Dialog windows title */
			/*background-color: #051328;*/
			color: #fbfbfb;
		}
		Text {
			background-color: #051c25;
			color: #f2f2f2;
		}
		Text[style~='SWT.DROP_DOWN'],
		TextSearchControl /* SWT-BUG: background color is hard-coded */,
		TextSearchControl > Label {
			/* search boxes and input fields */
			background-color: #04131f;
			color: #f7f7f7;
		}
		Text[style~='SWT.SEARCH'],
		Text[style~='SWT.SEARCH'] + Label /* SWT-BUG: adjacent sibling selector is ignored (CSS2.1) */ {
			/* search boxes */
			background-color: #d3e7f9;
			color: #ffffff;
		}
		Text[style~='SWT.POP_UP'] {
			background-color: #030f19;
			color: #f7f7f7;
		}
		Text[style~='SWT.READ_ONLY'] {
			background-color: #051c25;
			color: #eeeeee;
		}
		/* Text[style~='SWT.POP_UP'][style~='SWT.ERROR_MENU_NOT_POP_UP'][style~='SWT.ICON_WARNING'] {
			/* Dirty way to catch error popup labels
				(currently it's impossible since there's no difference
				at all from some other Text elements) */
		/*    background-color: #040223;
			color: #ffe5e5;
		} */
		DatePicker,
		DatePicker > Text,
		DatePicker > ImageHyperlink,
		ScheduleDatePicker,
		ScheduleDatePicker > Text,
		ScheduleDatePicker > ImageHyperlink {
			background-color: #04131f;
			color: #f7f7f7;
		}
		MessageLine,
		/* It might be useless but currently it's needed due to a strange priority
		policy used by the E4 platform to apply CSS rules to SWT widgets (see <1>): */
		Shell > Composite > Composite > MessageLine,
		Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.RESIZE'][style~='SWT.MENU'][style~='SWT.FULL_SELECTION'][style~='SWT.DATE'] > Composite > Composite > MessageLine {
			background-color:#051c25; /* SWT-BUG: background color is hard-coded */
			color: #fde0e0;
		}
		StyledText, 
		Spinner,
		CCombo {
			background-color: #03121a;
			color: #f7f7f7;
		}
		Composite > StyledText,
		Shell [style~='SWT.DROP_DOWN'] > StyledText, /* for eg. folded code popup (but it's ignored) */
		/* It might be useless but currently it's needed due to a strange priority
		policy used by the E4 platform to apply CSS rules to SWT widgets (see <1>): */
		ScrolledComposite > Composite > Composite > Composite > StyledText {
			background-color: #090909;
			color: #f7f7f7;
		}
		ScrolledFormText, 
		FormText {
			background-color: #062631;
			color: #fbfbfb;
		}
		ToolItem:selected {
			background-color: #030f17;
			color: #f7f7f7;
		}
		Table,
		/* It might be useless but currently it's needed due to a strange priority
		policy used by the E4 platform to apply CSS rules to SWT widgets (see <1>): */
		Composite > Table,
		TabFolder > Composite > Table,
		TabFolder > Composite > * > Table,
		DocCommentOwnerComposite > Group > Table,
		TabFolder > Composite > ScrolledComposite > Table,
		Shell > Composite > Composite > Table,
		Composite > Composite > Composite > Group > Table,
		Shell > Composite > Composite > Composite > Table,
		ScrolledComposite > Composite > Composite > Composite > Table,
		Shell > Composite > Composite > Composite > Composite > Composite > Table,
		Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.RESIZE'][style~='SWT.MENU'][style~='SWT.FULL_SELECTION'][style~='SWT.DATE'] > Composite > Table,
		Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.RESIZE'][style~='SWT.MENU'][style~='SWT.FULL_SELECTION'][style~='SWT.DATE'] > Composite > * > Table {
			background-color: #031019;
			color: #f7f7f7;
		}
		Tree,
		RegistryFilteredTree,
		/* It might be useless but currently it's needed due to a strange priority
		policy used by the E4 platform to apply CSS rules to SWT widgets (see <1>): */
		Composite > Tree,
		TabFolder > Composite > Tree,
		TabFolder > Composite > * > Tree,
		DocCommentOwnerComposite > Group > Tree,
		TabFolder > Composite > ScrolledComposite > Tree,
		Shell > Composite > Composite > Tree,
		Composite > Composite > Composite > Group > Tree,
		Shell > Composite > Composite > Composite > Tree,
		ScrolledComposite > Composite > Composite > Composite > Tree,
		Shell > Composite > Composite > Composite > Composite > Composite > Tree,
		Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.RESIZE'][style~='SWT.MENU'][style~='SWT.FULL_SELECTION'][style~='SWT.DATE'] > Composite > Tree,
		Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.RESIZE'][style~='SWT.MENU'][style~='SWT.FULL_SELECTION'][style~='SWT.DATE'] > Composite > * > Tree {
			background-color: #0c0c0c;
			color: #f2f2f2;
		}
		/* prevent CSS Spy red borders to be grayed with a generic Shell selector */
		Shell[style~='SWT.SHADOW_ETCHED_OUT'], Shell[style~='SWT.SHADOW_ETCHED_IN'],
		Shell[style~='SWT.CHECK'], Shell[style~='SWT.TITLE'], Shell[style~='SWT.OK'],
		Shell[style~='SWT.CANCEL'], Shell[style~='SWT.ABORT'], Shell[style~='SWT.DROP_DOWN'],
		Shell[style~='SWT.ARROW'], Shell[style~='SWT.RADIO'], Shell[style~='SWT.SINGLE'],
		Shell[style~='SWT.SHADOW_IN'], Shell[style~='SWT.TOOL'], Shell[style~='SWT.RESIZE'],
		Shell[style~='SWT.SHELL_TRIM'], Shell[style~='SWT.FILL'], Shell[style~='SWT.ALPHA'],
		Shell[style~='SWT.BORDER'], Shell[style~='SWT.DIALOG_TRIM'], Shell[style~='SWT.IGNORE'],
		Shell[style~='SWT.FULL_SELECTION'], Shell[style~='SWT.SMOOTH'], Shell[style~='SWT.VIRTUAL'],
		Shell[style~='SWT.APPLICATION_MODAL'], Shell[style~='SWT.MEDIUM'], Shell[style~='SWT.LONG']
		{
			background-color: #051c25;
			color: #f2f2f2;
		}
		Shell > Composite > Table[style~='SWT.DROP_DOWN'] {
			background-color: #031019;
			color: #f7f7f7;
		}
		Shell[style~='SWT.DROP_DOWN'][style~='SWT.SHADOW_IN'][style~='SWT.SHADOW_ETCHED_IN'] > Composite,
		Shell[style~='SWT.DROP_DOWN'][style~='SWT.SHADOW_IN'][style~='SWT.SHADOW_ETCHED_IN'] > Composite Composite,
		Shell[style~='SWT.DROP_DOWN'][style~='SWT.SHADOW_IN'][style~='SWT.SHADOW_ETCHED_IN'] > Composite ScrolledComposite,
		Shell[style~='SWT.DROP_DOWN'][style~='SWT.SHADOW_IN'][style~='SWT.SHADOW_ETCHED_IN'] > Composite Canvas,
		Shell[style~='SWT.DROP_DOWN'][style~='SWT.SHADOW_IN'][style~='SWT.SHADOW_ETCHED_IN'] > Composite StyledText,
		Shell[style~='SWT.DROP_DOWN'][style~='SWT.SHADOW_IN'][style~='SWT.SHADOW_ETCHED_IN'] > Composite Label {
		/* Error information popup */
			background-color: #0c0c0c;
			color: #f2f2f2;
		}
		TextSearchControl {
			background-color: #04131f;
			color: #f7f7f7;
		}
		ViewerPane,
		DrillDownComposite,
		ViewerPane > ToolBar,
		DrillDownComposite > ToolBar {
			background-color: #090909;
			color: #f2f2f2;
		}
		ProgressInfoItem,
		CompareViewerPane,
		CompareViewerPane > * {
			background-color: #0d0d0d;
			color: #fbfbfb;
		}
		ProgressIndicator {
			background-color: #1e1e1e;
			color: #fbfbfb;
		}
		DiscoveryItem,
		DiscoveryItem Label,
		DiscoveryItem Composite {
			background-color: #03121a;
			color: #f7f7f7;
		}
		DiscoveryItem StyledText {
			background-color: #03121a;
			color: #eaeaea;
		}
		DiscoveryItem Link {
			background-color: #03121a;
			color: #cfecf9;
		}
		CatalogSwitcher,
		CatalogSwitcher > ScrolledComposite > Composite > Composite /* ignored because hard-coded */,
		CategoryItem {
			background-color: #051c25;
			color: #f7f7f7;
		}
		GradientCanvas,
		GradientCanvas > Label,
		GradientCanvas > ToolBar,
		GradientCanvas > ImageHyperlink { 
			background-color: #04141e;
			color: #def5fd;
		}
		GradientCanvas {
			/* SWT-BUG workaround: GradientCanvas background-color is ignored */
			background: #04141e;
			background-image: #04141e;
		}
		CategoryItem > GradientCanvas,
		CategoryItem > GradientCanvas > Label { 
			/* SWT-BUG workaround: a style for background is not applied on GradientCanvas (CSS engine repaint issue) */
			background-color: #fefefe;
			color: #0d0d0d;
		}
		CategoryItem > GradientCanvas {
			/* SWT-BUG workaround: a style for background is not applied on GradientCanvas (CSS engine repaint issue) */
			background: #fefefe;
			background-image: #0d0d0d;
		}
		WebSite {
			background-color: #04131f;
			color: #f7f7f7;
		}
		CTabFolder {
			background-color: #0a0a0a;
			color: #fcffff;
			swt-tab-renderer: url('bundleclass://org.eclipse.e4.ui.workbench.renderers.swt/org.eclipse.e4.ui.workbench.renderers.swt.CTabRendering');
			swt-tab-height: 32px;
			padding: 0px 6px 6px 6px; /* top left bottom right */
			swt-tab-outline: #121212; /* border color for selected tab */
			swt-outer-keyline-color: #050c22; /* border color for whole tabs container */
			swt-unselected-tabs-color: #050c21 #04041d #0a0a0a 99% 100%; /* title background for unselected tab */
			swt-selected-tab-fill: #0a0a0a; /* title background for selected tab (gradient bottom color) */
			swt-shadow-color: #030303;
			swt-shadow-visible: true;
			swt-mru-visible: true;
			swt-corner-radius: 16px;
		}
		CTabFolder[style~='SWT.DOWN'][style~='SWT.BOTTOM'] {
			/* Need to restore a native renderer or the bottom inner tabs won't be displayed */
			swt-tab-renderer: null;
			swt-simple: true;
			swt-tab-height: 29px;
		}
		CTabFolder[style~='SWT.DOWN'][style~='SWT.BOTTOM'] CTabItem {
			color: #e1e1e1;
			font-weight: normal;
			/*font-family: 'Segoe Print';*/ /* currently, there is no way to define a fallback for font-family */
			/*font-size: 8;*/
		}
		CTabFolder[style~='SWT.DOWN'][style~='SWT.BOTTOM'] CTabItem:selected {
			background-color: #0a0a0a;
			color: #fbfbfb;
			/*font-weight: bold;*/
		}
		/* +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
		CTabFolder Tree, CTabFolder Canvas {
			background-color: #0c0c0c;
			color: #f2f2f2;
		}
		.MPartStack.active Tree,
		.MPartStack.active CTabFolder Canvas {
			background-color: #0a0a0a;
			color: #f2f2f2;
		}
		.MPartStack.active Table{
			background-color: #0c0c0c;
			color: #f2f2f2;
		}
		.View {
			background-color: #030f17;
			color: #fdfdfd;
		}
		/* not triggered
		.View.active {
			background-color: #0d0d0d;
		} */
		Form,
		FormHeading {
			background: #05172b;
			background-color: #05172b;
			background-image: #05172b;
			color: #def5fd;
		}
		Section {
			background-color: #051a24;
			color: #e2eefc;
		}
		Form > LayoutComposite > LayoutComposite > * {
			background-color: #051c25;
			color: #fbfbfb;
		}
		LayoutComposite, LayoutComposite > FormText,
		LayoutComposite > Label,
		LayoutComposite > Button {
			background-color: #051a24;
			color: #fbffff;
		}
		LayoutComposite ScrolledPageBook,
		LayoutComposite Sash {
			background-color: #051a24;
			color: #fbffff;
		}
		LayoutComposite > Text,
		LayoutComposite > Combo {
			background-color: #04171d;
			color: #fbffff;
		}
		LayoutComposite > Table {
			background-color: #0d0d0d;
			color: #ffffff;
		}
		Twistie {
			color: #fef9f3;
		}
		#SearchField {
			/* background-image: url('./searchbox.png'); */
			/* SWT-BUG: textures are applied as a label over the native ones, */
			/* in this way textures with alpha color are not usable; */
			/* default margins and padding cannot be modified and textures are not */
			/* scaled properly to fit the container size: this makes the result ugly, */
			/* moreover a texture is drawn over the widget, so also the text is covered */
			color: #fbfbfb;
		}
		/* Button {
			background-color: inherit;  /* ignored */
			/* background-image: url('./button_bg.png') */
		/* } */
		/* Button[style~='SWT.CHECK'] { */
			/* currently, Button object isn't consistent (eg. also a checkbox/radio is seen as Button) */
			/* so, css rules applied to Button have to be overridden for non-Button matches */
		/* }
		Button:disabled {
			/* SWT-BUG: currently, a disabled button cannot be styled with any window manager (gtk, win32, cocoa) */
		/* }
		Button:hover {
			/* SWT-BUG: currently, an hovered button cannot be styled with any window manager (gtk, win32, cocoa) */
		/* } */
		.MPartSashContainer {
			background-color: #051c25;
			color: #fbfbfb;
		}
		PageSiteComposite, PageSiteComposite > CImageLabel {
			color: #fbfbfb;
		}
		PageSiteComposite > PropertyTable {
			background-color: #0d0d0d;
			color: #fbfbfb;
		}
		PageSiteComposite > PropertyTable:disabled {
		/* SWT-BUG: event is triggered but styles for PropertyTable are hard-coded */
			background-color: #111111;
			color: #fbfbfb;
		}
		FlyoutControlComposite, FlyoutControlComposite ToolBar, FlyoutControlComposite CLabel {
			background-color: #04141e;
			color: #fbfbfb;
		}
		/* ###################### Top Toolbar ########################## */
		#org-eclipse-ui-main-toolbar, #PerspectiveSwitcher {
			eclipse-perspective-keyline-color: #161616;
			background-color: #051c25 #051c25 100%;
			handle-image: none;
			color: #fefaf4;
		}
		/* ######################### Views ############################# */
		.MPart {
			background-color: #031017;
			color: #f7f7f7;
		}
		.MPartStack.active .MPart {
			background-color: #0a0a0a;
			color: #f7f7f7;
		}
		.MPart Composite,
		.MPart LayoutComposite,
		.MPart Label,
		.MPart Hyperlink,
		.MPart ImageHyperlink,
		.MPart ScrolledForm,
		.MPart Form,
		.MPart Section,
		.MPart FormText,
		.MPart Link,
		.MPart Sash,
		.MPart Button,
		.MPart Group,
		.MPart SashForm,
		.MPart FilteredTree,
		.MPart RegistryFilteredTree,
		.MPart PageSiteComposite,
		.MPart DependenciesComposite,
		.MPart Text[style~='SWT.READ_ONLY'],
		.MPart FigureCanvas,
		.MPart ListEditorComposite,
		.MPart ScrolledComposite,
		.MPart ScrolledComposite ToolBar,
		.Mpart ScrolledComposite ProgressInfoItem,
		.MPart Form ScrolledPageBook,
		.MPart Form > LayoutComposite > LayoutComposite > ToolBar,
		.MPart DependenciesComposite > SashForm > Section > * /* Section > DependenciesComposite$... */,
		.MPart LayoutComposite > * > LayoutComposite > Section > LayoutComposite > * /*LayoutComposite > MasterDetailBlock$... > LayoutComposite > Section > LayoutComposite > ExtensionsSection$...*/ {
			background-color: #0c0c0c;
			color: #eaeaea;
		}
		.MPartStack.active .MPart Composite,
		.MPartStack.active .MPart LayoutComposite,
		.MPartStack.active .MPart Label,
		.MPartStack.active .MPart Hyperlink,
		.MPartStack.active .MPart ImageHyperlink,
		.MPartStack.active .MPart ScrolledForm,
		.MPartStack.active .MPart Form,
		.MPartStack.active .MPart Section,
		.MPartStack.active .MPart FormText,
		.MPartStack.active .MPart Link,
		.MPartStack.active .MPart Sash,
		.MPartStack.active .MPart Button,
		.MPartStack.active .MPart Group,
		.MPartStack.active .MPart SashForm,
		.MPartStack.active .MPart FilteredTree,
		.MPartStack.active .MPart RegistryFilteredTree,
		.MPartStack.active .MPart PageSiteComposite,
		.MPartStack.active .MPart DependenciesComposite,
		.MPartStack.active .MPart Text[style~='SWT.READ_ONLY'],
		.MPartStack.active .MPart FigureCanvas,
		.MPartStack.active .MPart ListEditorComposite,
		.MPartStack.active .MPart ScrolledComposite,
		.MPartStack.active .MPart ScrolledComposite ToolBar,
		.MPartStack.active .Mpart ScrolledComposite ProgressInfoItem,
		.MPartStack.active .MPart Form ScrolledPageBook,
		.MPartStack.active .MPart Form > LayoutComposite > LayoutComposite > ToolBar,
		.MPartStack.active .MPart DependenciesComposite > SashForm > Section > * /* Section > DependenciesComposite$... */,
		.MPartStack.active .MPart LayoutComposite > * > LayoutComposite > Section > LayoutComposite > * /*LayoutComposite > MasterDetailBlock$... > LayoutComposite > Section > LayoutComposite > ExtensionsSection$...*/ {
			background-color: #0a0a0a;
			color: #e6e6e6;
		}
		.MPart Section > Label {
			background-color: #0c0c0c;
			color: #e3f6fd;
		}
		.MPartStack.active .MPart Section > Label {
			background-color: #0a0a0a;
			color: #def4fc;
		}
		.MPart Table,
		.MPart Browser,
		.Mpart OleFrame,
		.MPart ViewForm,
		.MPart ViewForm > ToolBar,
		.MPart ViewForm > CLabel,
		.MPart PageBook > Label,
		.MPart PageBook > SashForm,
		#org-eclipse-help-ui-HelpView LayoutComposite > LayoutComposite,
		#org-eclipse-help-ui-HelpView LayoutComposite > LayoutComposite > * {
			background-color: #030f17;
			color: #f2f2f2;
		}
		.MPartStack.active .MPart Table,
		.MPartStack.active .MPart Browser,
		.MPartStack.active .Mpart OleFrame,
		.MPartStack.active .MPart ViewForm,
		.MPartStack.active .MPart ViewForm > ToolBar,
		.MPartStack.active .MPart ViewForm > CLabel,
		.MPartStack.active .MPart PageBook > Label,
		.MPartStack.active .MPart PageBook > SashForm,
		.MPartStack.active #org-eclipse-help-ui-HelpView LayoutComposite > LayoutComposite,
		.MPartStack.active #org-eclipse-help-ui-HelpView LayoutComposite > LayoutComposite > * {
			background-color: #0d0d0d;
			color: #f7f7f7;
		}
		#org-eclipse-help-ui-HelpView LayoutComposite > LayoutComposite ImageHyperlink {
			background-color: #030f17;
			color: #d8f2fe;
		}
		.MPartStack.active #org-eclipse-help-ui-HelpView LayoutComposite > LayoutComposite ImageHyperlink {
			background-color: #0d0d0d;
			color: #d7eafd;
		}
		.MPart > Label,
		#com-android-ide-eclipse-adt-internal-lint-LintViewPart > Composite > Label {
			background-color: #030f17;
			color: #d3fbf8;
		}
		.MPartStack.active .MPart > Label,
		.MPartStack.active #com-android-ide-eclipse-adt-internal-lint-LintViewPart > Composite > Label {
			background-color: #030c16;
			color: #eafaff;
		}
		.MPart Section Tree,
		.MPart LayoutComposite > * > LayoutComposite > Section > LayoutComposite > Tree {
			background-color: #031219;
			color: #f7f7f7;
		}
		.MPartStack.active .MPart Section Tree,
		.MPartStack.active .MPart LayoutComposite > * > LayoutComposite > Section > LayoutComposite > Tree {
			background-color: #031717;
			color: #f2f2f2;
		}
		.MPart DatePicker,
		.MPart DatePicker > Text,
		.MPart DatePicker > ImageHyperlink,
		.MPart ScheduleDatePicker,
		.MPart ScheduleDatePicker > Text,
		.MPart ScheduleDatePicker > ImageHyperlink,
		.MPart CCombo,
		.MPart Spinner,
		.MPart StyledText,
		.MPart PageBook > SashForm Label,
		.MPart SashForm > Text[style~='SWT.BORDER'] {
			background-color: #04141e;
			color: #eeeeee;
		}
		.MPartStack.active .MPart DatePicker,
		.MPartStack.active .MPart DatePicker > Text,
		.MPartStack.active .MPart DatePicker > ImageHyperlink,
		.MPartStack.active .MPart ScheduleDatePicker,
		.MPartStack.active .MPart ScheduleDatePicker > Text,
		.MPartStack.active .MPart ScheduleDatePicker > ImageHyperlink,
		.MPartStack.active .MPart CCombo,
		.MPartStack.active .MPart Spinner,
		.MPartStack.active .MPart StyledText,
		.MPartStack.active .MPart PageBook > SashForm Label,
		.MPartStack.active .MPart SashForm > Text[style~='SWT.BORDER'] {
			background-color: #030f17;
			color: #eaeaea;
		}
		.MPart FormHeading,
		.MPart FormHeading > ToolBar,
		.MPart FormHeading > TitleRegion,
		.MPart FormHeading > TitleRegion > Label,
		.MPart FormHeading > TitleRegion > ToolBar,
		.MPart FormHeading > TitleRegion > StyledText,
		.MPart FormHeading LayoutComposite,
		.MPart FormHeading ImageHyperlink {
			background-color: #05172b;
			color: #def5fd;
		}
		.MPart FormHeading {
			background: #05172b;
			background-image: #05172b;	
		}
		.MPartStack.active .MPart FormHeading,
		.MPartStack.active .MPart FormHeading > ToolBar,
		.MPartStack.active .MPart FormHeading > TitleRegion,
		.MPartStack.active .MPart FormHeading > TitleRegion > Label,
		.MPartStack.active .MPart FormHeading > TitleRegion > ToolBar,
		.MPartStack.active .MPart FormHeading > TitleRegion > StyledText,
		.MPartStack.active .MPart FormHeading LayoutComposite,
		.MPartStack.active .MPart FormHeading ImageHyperlink {
			background-color: #041325;
			color: #def5fd;
		}
		.MPartStack.active .MPart FormHeading {
			background: #041325;
			background-image: #041325;
		}
		.MPart FormHeading,
		.MPart FormHeading > TitleRegion {
			swt-background-mode: none;
		}
		.MPart FormHeading > CLabel {
			background-color: #05172b;
			color: #fedddd;
		}
		.MPartStack.active .MPart FormHeading > CLabel {
			background-color: #041325;
			color: #fedddd;
		}
		/* ------------------------------------------------------------- */
		#org-eclipse-jdt-ui-SourceView StyledText,
		#org-eclipse-wst-jsdt-ui-SourceView StyledText {
			background-color: #090909;
		}
		/* ------------------------------------------------------------- */
		#org-eclipse-ui-console-ConsoleView .MPart > Composite,
		#org-eclipse-ui-console-ConsoleView .MPart StyledText,
		#org-eclipse-ui-console-ConsoleView .MPart PageBook Label,
		#org-eclipse-dltk-debug-ui-ScriptDisplayView SashForm > * {
			background-color: #0c0c0c;
			color: #f2f2f2;
		}
		.MPartStack.active #org-eclipse-ui-console-ConsoleView .MPart > Composite,
		.MPartStack.active #org-eclipse-ui-console-ConsoleView .MPart StyledText,
		.MPartStack.active #org-eclipse-ui-console-ConsoleView .MPart PageBook Label,
		.MPartStack.active #org-eclipse-dltk-debug-ui-ScriptDisplayView SashForm > * {
			background-color: #0a0a0a;
			color: #f2f2f2;
		}
		/* ------------------------------------------------------------- */
		#org-eclipse-pde-runtime-LogView Text {
			background-color: #0d0d0d;
			color: #fbffff;
		}
		/* ------------------------------------------------------------- */
		#org-eclipse-pde-ui-TargetPlatformState PageBook > Composite > * {
			background-color: #0c0c0c;
			color: #f2f2f2;
		}
		/* ------------------------------------------------------------- */
		#org-eclipse-e4-ui-compatibility-editor Canvas,
		#org-eclipse-e4-ui-compatibility-editor Canvas > *,
		/* Workaround for CDT folding column SWT-BUG (styles aren't inherited) */
		#org-eclipse-e4-ui-compatibility-editor Canvas > * > * {
			background-color: #0a0a0a;
			/* SWT-BUG: background-color rule for LineNumberRulerColumn is ignored */
		}
		.MPartStack.active #org-eclipse-e4-ui-compatibility-editor Canvas,
		.MPartStack.active #org-eclipse-e4-ui-compatibility-editor Canvas > *,
		/* Workaround for CDT folding column SWT-BUG (styles aren't inherited) */
		.MPartStack.active #org-eclipse-e4-ui-compatibility-editor Canvas > * > * {
			background-color: #080808;
			/* SWT-BUG: background-color rule for LineNumberRulerColumn is ignored */
		}
		#org-eclipse-e4-ui-compatibility-editor .MPart {
			color: #fbfbfb;
		}
		#org-eclipse-e4-ui-compatibility-editor PaletteControl ScrolledComposite > Composite > * {
			background-color: #0c0c0c;
			color: #eeeeee;
		}
		.MPartStack.active #org-eclipse-e4-ui-compatibility-editor PaletteControl ScrolledComposite > Composite > * {
			background-color: #0a0a0a;
			color: #f2f2f2;
		}
		#org-eclipse-e4-ui-compatibility-editor PaletteControl CLabel {
			background-color: #0e0e0e;
			color: #f7f7f7;
		}
		#org-eclipse-e4-ui-compatibility-editor PaletteControl CLabel:hover {
		/* SWT-BUG #140210: The event is never triggered so the native rule cannot be overridden (for hover event) */
			background-color: #090909;
			color: #f7f7f7;
		}
		#org-eclipse-e4-ui-compatibility-editor FlyoutControlComposite > Composite {
			background-color: #04141e;
			color: #f7f7f7;
		}
		#org-eclipse-e4-ui-compatibility-editor LayoutCanvas {
			background-color: #090909;
			color: #f2f2f2;
		}
		/* #################### Bottom Status Bar ######################## */
		#org-eclipse-ui-StatusLine,
		#org-eclipse-ui-ProgressBar,
		#org-eclipse-ui-ProgressBar Canvas {
			color: #f2f2f2;
		}
		#org-eclipse-ui-StatusLine CLabel {
			color: #fbeee1;
		}
		StatusLine, ImageBasedFrame{
			color: #fbeee1;
		}
	/* <<<<<<<<<<<< end of content of 'moonrise-ui-standalone.css' <<<<<<<<<<<< */
	.MPartStack { 
		swt-tab-renderer:
			url('bundleclass://net.jeeeyul.eclipse.themes/net.jeeeyul.eclipse.themes.rendering.JeeeyulsTabRenderer');
		background: #030f17;
		jtab-selected-tab-background: #04151c #030f17 #030f17 99% 100%;  /* Gradient for selected tab item */	
		jtab-selected-border-color: none;  /* Gradient for the border of selected tab item */
		jtab-header-background: #051c25 #04041f #030f17 99% 100%;  /* Gradient for the background of tab header */
		jtab-unselected-border-color: none;  /* Gradient for the border of unselected tab item */
		jtab-hover-tabs-background: #04171e #04041f 100%;  /* Gradient for hover tab item */
		jtab-hover-border-color: none;  /* Gradient for the border of hover tab item */
		jtab-close-button-color: #1e1e1e;  /* Color for close button */
		jtab-close-button-hot-color: #d1cdfa;  /* Hover color for close button */
		jtab-close-button-active-color: #08032f;  /* Active color for close button */
		jtab-close-button-line-width: 2px;  /* Line width of the close button */
		jtab-chevron-color: #1e1e1e;  /* Chevron color */
		jtab-border-color: #051c25 #030f17 100%;  /* Gradient for the border of tab body */
		jtab-border-radius: 8px;  /* Radius for border of Tab and Tab Items */
		jtab-spacing: 0px;  /* Gap between each tab items */
		jtab-shadow-color: #0d0d0d;  /* Color for the shadow of tab body */
		jtab-shadow-position: 0px 2px;  /* Shadow offset for shadow of the tab body */
		jtab-shadow-radius: 10px;  /* Radius for the shadow of tab body */
		jtab-margin: 0px 2px 2px 2px;  /* Margin for the tab body */
		jtab-padding: 2px 2px 2px 2px;  /* Padding for tab body content */
		jtab-item-padding: 2px 7px 2px 7px;  /* Padding for inside area of Tab Item */
		jtab-selected-text-shadow-color: #fbfbfb;  /* Color for the shadow of selected tab item text */
		jtab-selected-text-shadow-position: 0px 0px;  /* Offset for the shadow of selected tab item text */
		jtab-unselected-text-shadow-color: #0d0d0d;  /* Color for the shadow of unselected tab item text */
		jtab-unselected-text-shadow-position: 0px 1px;  /* Offset for the shadow of unselected tab item text */
	}
	.MPartStack.active {
		background: #0a0a0a;         
		jtab-selected-tab-background: #030b13 #0a0a0a #0a0a0a 99% 100%;  /* Gradient for selected tab item */
		jtab-header-background: #050c21 #04041d #04041d 99% 100%;  /* Gradient for the background of tab header */
		jtab-hover-tabs-background: #031117 #030318 100%;  /* Gradient for hover tab item */
	}
	.TrimStack {
		frame-image: url('jeeeyul://frame?background-color=#04171e');
		frame-cuts: 4px 2px 5px 16px;
		handle-image: url('jeeeyul://drag-handle?height=27&background-color=#051c25&embossed=false');
	}
	.MTrimBar .Draggable {
		handle-image: url('jeeeyul://drag-handle?height=27&background-color=#051c25&embossed=false');
	}
	.MPartSashContainer {
		jsash-width: 4px;  /* Gap between each parts */
	}	
	/* ###################### Global Styles ########################## */
	/* ++++++ Remove these to have ONLY the main IDE shell dark ++++++ */
	CTabFolder {
		swt-tab-renderer: url('bundleclass://net.jeeeyul.eclipse.themes/net.jeeeyul.eclipse.themes.rendering.JeeeyulsTabRenderer');
		jtab-selected-tab-background: #0e0e0e #0a0a0a #0a0a0a 99% 100%;  /* Gradient for selected tab item */	
		jtab-selected-border-color: none;  /* Gradient for the border of selected tab item */
		jtab-header-background: #050c21 #04041d #04041d 99% 100%;  /* Gradient for the background of tab header */
		jtab-unselected-border-color: none;  /* Gradient for the border of unselected tab item */
		jtab-hover-tabs-background: #031117 #030318 100%;  /* Gradient for hover tab item */
		jtab-hover-border-color: none;  /* Gradient for the border of hover tab item */
		jtab-close-button-color: #1e1e1e;  /* Color for close button */
		jtab-close-button-hot-color: #d1cdfa;  /* Hover color for close button */
		jtab-close-button-active-color: #08032f;  /* Active color for close button */
		jtab-close-button-line-width: 2px;  /* Line width of the close button */
		jtab-chevron-color: #1e1e1e;  /* Chevron color */
		jtab-border-color: #051c25 #030f17 100%;  /* Gradient for the border of tab body */
		jtab-border-radius: 8px;  /* Radius for border of Tab and Tab Items */
		jtab-spacing: 0px;  /* Gap between each tab items */
		jtab-shadow-color: #0d0d0d;  /* Color for the shadow of tab body */
		jtab-shadow-position: 0px 2px;  /* Shadow offset for shadow of the tab body */
		jtab-shadow-radius: 10px;  /* Radius for the shadow of tab body */
		jtab-margin: 0px 2px 2px 2px;  /* Margin for the tab body */
		jtab-padding: 2px 2px 2px 2px;  /* Padding for tab body content */
		jtab-item-padding: 2px 7px 2px 7px;  /* Padding for inside area of Tab Item */
		jtab-selected-text-shadow-color: #fbfbfb;  /* Color for the shadow of selected tab item text */
		jtab-selected-text-shadow-position: 0px 0px;  /* Offset for the shadow of selected tab item text */
		jtab-unselected-text-shadow-color: #0d0d0d;  /* Color for the shadow of unselected tab item text */
		jtab-unselected-text-shadow-position: 0px 1px;  /* Offset for the shadow of unselected tab item text */
	}
	CTabFolder[style~='SWT.DOWN'][style~='SWT.BOTTOM'] {
		/* Need to restore a native renderer or the bottom inner tabs won't be displayed and Eclipse crashes during startup with errors */
		swt-tab-renderer: null;
		swt-simple: true; 
	}
	/* +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */	
	/* ######################### Views ############################# */
	.MPart.Editor StyledText {
		jeditor-line-style: none;     /* One of "none", "solid", "dashed", "dotted" */
		jeditor-line-color: #0d0d0d;  /* Color for the underlines in text editors */
	}

Enjoy!

## Purple!

For those who are not over fond of green, the next version is basically the same, with the 
modification that all greenish-yellow colors are shifted to red by 120 degrees and all 
greenish-cyan colors are shifted towards blue.

	/** Purple Darkened Eclipse CSS */
	.MTrimmedWindow.topLevel {
		margin-top: 4px;
		margin-bottom: 2px;
		margin-left: 2px;
		margin-right: 2px;
	}
	.MPartStack {
		background-color: #0d0317;
		color: #fffefc;
		swt-tab-renderer: url('bundleclass://org.eclipse.e4.ui.workbench.renderers.swt/org.eclipse.e4.ui.workbench.renderers.swt.CTabRendering');
		swt-tab-height: 32px;
		padding: 1px 6px 6px 6px; /* top left bottom right */
		swt-tab-outline: #12041c; /* border color for selected tab */
		swt-outer-keyline-color: #190525; /* border color for whole tabs container */
		swt-unselected-tabs-color: #190525 #07041f #0d0317 99% 100%; /* title background for unselected tab */
		swt-selected-tab-fill: #0d0317; /* title background for selected tab (gradient bottom color) */		
		swt-shadow-color: #030303;
		swt-shadow-visible: true;
		swt-mru-visible: true;
		swt-corner-radius: 16px;
	}
	.MPartStack.active {
		background-color: #0a0a0a;   /* ignored (<2>) */
		swt-inner-keyline-color: #ffffff;
		swt-tab-outline: #121212; /* border color for selected tab */
		swt-outer-keyline-color: #090522; /* border color for whole tabs container */
		swt-unselected-tabs-color: #090521 #06041d #0a0a0a 99% 100%; /* title background for unselected tab */
		swt-selected-tab-fill: #0a0a0a; /* title background for selected tab (gradient bottom color) */
	}
	.MPartStack.active > * {
		/* Workaround for (<2>) to set the color of the inner border for the active tab */
		background-color: #0a0a0a;
	}
	.MPartStack.empty {
		swt-unselected-tabs-color: #190525 #180524 #180524 99% 100%; /* title background for unselected tab */
		swt-tab-outline: #080525; /* border color for selected tab */
		swt-outer-keyline-color: #190525; /* border color for whole tabs container */
	}
	CTabItem,
	CTabItem CLabel {
		background-color: #0d0317; /* HACK for background of CTabFolder inner Toolbars */
		color: #e6e6e6;
		/*font-family: 'Segoe Print';*/ /* currently, there is no way to define a fallback for font-family */
		/*font-size: 8;*/
	}
	CTabItem:selected,
	CTabItem:selected CLabel {
		color: #f7f7f7;
	}
	.MPartStack.active > CTabItem,
	.MPartStack.active > CTabItem CLabel {
		background-color: #0a0a0a; /* HACK for background of CTabFolder inner Toolbars */
		color: #eaeaea;
	}
	.MPartStack.active > CTabItem:selected,
	.MPartStack.active > CTabItem:selected CLabel {
		color: #ffffff;
	}
	CTabItem.busy {
		color: #e1e1e1;
	}
	.MTrimmedWindow {
		background-color: #190525;
	}
	.MTrimBar {
		background-color: #190525;
	}
	.MTrimBar .Draggable {
		handle-image: url('./dragHandle.png');
	}
	.TrimStack {
		frame-cuts: 4px 2px 5px 16px;
		handle-image: url('./dragHandle.png');
	}
	CTabFolder.MArea .MPartStack,CTabFolder.MArea .MPartStack.active {
		swt-shadow-visible: false;
	}
	.MToolControl.TrimStack {
		frame-cuts: 5px 1px 5px 16px;
	}
	/* ###################### Global Styles ########################## */
	/* ++++++ Remove these to have ONLY the main IDE shell dark ++++++ */
	Composite, ScrolledComposite, ExpandableComposite, TabFolder, CLabel, Label,
	ToolItem, Sash, Group, Hyperlink, RefactoringLocationControl, Link, FilteredTree,
	ProxyEntriesComposite, NonProxyHostsComposite, DelayedFilterCheckboxTree,
	Splitter, ScrolledPageContent, ViewForm, LaunchConfigurationFilteredTree,
	ContainerSelectionGroup, BrowseCatalogItem, EncodingSettings,
	ProgressMonitorPart, DocCommentOwnerComposite, NewServerComposite,
	NewManualServerComposite, ServerTypeComposite, FigureCanvas,
	DependenciesComposite, ListEditorComposite, WrappedPageBook,
	CompareStructureViewerSwitchingPane, CompareContentViewerSwitchingPane,
	QualifiedNameComponent, RefactoringStatusViewer, ImageHyperlink,
	Button /* SWT-BUG: checkbox inner label font color is not accessible */,
	ViewForm > ToolBar, /* SWT-BUG: ToolBar do not inherit rules from ViewForm */
	/*Shell [style~='SWT.DROP_DOWN'] > GradientCanvas,*/ /* ignored */
	/* SWT-BUG dirty workaround [Eclipse Bug 419482]: a generic rule (eg: Composite > *) needed to catch an
	element without a CSS id, a CSS class and a seekable Widget name, cannot be overridden
	by a subsequent more specific rule used to correct the style for seekable elements (<1>): */
	TabFolder > Composite > *, /* Composite > CommitSearchPage$... */
	TabFolder > Composite > * > * /* [style~='SWT.NO_BACKGROUND'] <- generate E4 non-sense bugs in apparently not related other rules */, /* Composite > ContentMergeViewer$... > TextMergeViewer$... */
	DocCommentOwnerComposite > Group > *, /* Group > DocCommentOwnerComposite$... */
	TabFolder > Composite > ScrolledComposite > *, /* ScrolledComposite > ControlListViewer$... */
	Shell > Composite > Composite > *, /* Composite > StatusDialog$MessageLine (SWT-BUG: ignored) */
	Composite > Composite > Composite > ToolBar, /* Window->Preference (top toolbar) */
	Composite > Composite > Composite > Group > *, /* Group > CreateRefactoringScriptWizardPage$... */
	Shell > Composite > Composite > Composite > *, /* Composite > FilteredPreferenceDialog$... */
	ScrolledComposite > Composite > Composite > Composite > *, /* Composite > NewKeysPreferencePage$... */
	Shell > Composite > Composite > Composite > Composite > Composite > *, /* Composite > ShowRefactoringHistoryWizardPage$... */
	Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.RESIZE'][style~='SWT.MENU'][style~='SWT.FULL_SELECTION'][style~='SWT.DATE'] > Composite > *, /* Composite > RefactoringWizardDialog$... */
	Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.RESIZE'][style~='SWT.MENU'][style~='SWT.FULL_SELECTION'][style~='SWT.DATE'] > Composite > * > * /* Composite > RefactoringWizardDialog$... */ {
		background-color:#190525;
		color:#fbfbfb;
	}
	List,
	/* It might be useless but currently it's needed due to a strange priority
	policy used by the E4 platform to apply CSS rules to SWT widgets (see <1>): */
	Composite > List,
	TabFolder > Composite > List,
	TabFolder > Composite > * > List,
	DocCommentOwnerComposite > Group > List,
	TabFolder > Composite > ScrolledComposite > List,
	Shell > Composite > Composite > List,
	Composite > Composite > Composite > Group > List,
	Shell > Composite > Composite > Composite > List,
	ScrolledComposite > Composite > Composite > Composite > List,
	Shell > Composite > Composite > Composite > Composite > Composite > List,
	Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.RESIZE'][style~='SWT.MENU'][style~='SWT.FULL_SELECTION'][style~='SWT.DATE'] > Composite > List,
	Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.RESIZE'][style~='SWT.MENU'][style~='SWT.FULL_SELECTION'][style~='SWT.DATE'] > Composite > * > List {
		background-color: #10041f;
		color: #f7f7f7;
	}
	Combo,
	/* It might be useless but currently it's needed due to a strange priority
	policy used by the E4 platform to apply CSS rules to SWT widgets (see <1>): */
	Composite > Combo,
	TabFolder > Composite > Combo,
	TabFolder > Composite > * > Combo,
	DocCommentOwnerComposite > Group > Combo,
	TabFolder > Composite > ScrolledComposite > Combo,
	Shell > Composite > Composite > Combo,
	Composite > Composite > Composite > Group > Combo,
	Shell > Composite > Composite > Composite > Combo,
	ScrolledComposite > Composite > Composite > Composite > Combo,
	Shell > Composite > Composite > Composite > Composite > Composite > Combo,
	Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.RESIZE'][style~='SWT.MENU'][style~='SWT.FULL_SELECTION'][style~='SWT.DATE'] > Composite > Combo,
	Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.RESIZE'][style~='SWT.MENU'][style~='SWT.FULL_SELECTION'][style~='SWT.DATE'] > Composite > * > Combo {
		background-color: #10041f;
		color: #f7f7f7;
	}
	/* Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.MENU'][style~='SWT.DATE'][style~='SWT.RESIZE'][style~='SWT.TITLE'][style~='SWT.APPLICATION_MODAL'][style~='SWT.FULL_SELECTION'][style~='SWT.SMOOTH'] > Composite[style~='SWT.LEFT_TO_RIGHT'], */
	Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.MENU'][style~='SWT.DATE'][style~='SWT.RESIZE'][style~='SWT.TITLE'][style~='SWT.APPLICATION_MODAL'][style~='SWT.FULL_SELECTION'][style~='SWT.SMOOTH'] > Composite[style~='SWT.LEFT_TO_RIGHT'] > Text[style~='SWT.READ_ONLY'],
	Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.MENU'][style~='SWT.DATE'][style~='SWT.RESIZE'][style~='SWT.TITLE'][style~='SWT.APPLICATION_MODAL'][style~='SWT.FULL_SELECTION'][style~='SWT.SMOOTH'] > Composite[style~='SWT.LEFT_TO_RIGHT'] > ToolBar {
		/* Dialog windows title */
		/*background-color: #100528;*/ /* There is no way to change the background-color of the title of a Dialog without introducing artifacts in some other Dialog windows */
		color: #f2defd;
	}
	Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.MENU'][style~='SWT.DATE'][style~='SWT.RESIZE'][style~='SWT.TITLE'][style~='SWT.APPLICATION_MODAL'][style~='SWT.FULL_SELECTION'][style~='SWT.SMOOTH'] > Composite[style~='SWT.LEFT_TO_RIGHT'] > Label[style~='SWT.NO_FOCUS'] {
		/* Dialog windows title */
		/*background-color: #100528;*/
		color: #fbfbfb;
	}
	Text {
		background-color: #190525;
		color: #f2f2f2;
	}
	Text[style~='SWT.DROP_DOWN'],
	TextSearchControl /* SWT-BUG: background color is hard-coded */,
	TextSearchControl > Label {
		/* search boxes and input fields */
		background-color: #10041f;
		color: #f7f7f7;
	}
	Text[style~='SWT.SEARCH'],
	Text[style~='SWT.SEARCH'] + Label /* SWT-BUG: adjacent sibling selector is ignored (CSS2.1) */ {
		/* search boxes */
		background-color: #e4d3f9;
		color: #ffffff;
	}
	Text[style~='SWT.POP_UP'] {
		background-color: #0d0319;
		color: #f7f7f7;
	}
	Text[style~='SWT.READ_ONLY'] {
		background-color: #190525;
		color: #eeeeee;
	}
	/* Text[style~='SWT.POP_UP'][style~='SWT.ERROR_MENU_NOT_POP_UP'][style~='SWT.ICON_WARNING'] {
		/* Dirty way to catch error popup labels
			(currently it's impossible since there's no difference
			at all from some other Text elements) */
	/*    background-color: #040223;
		color: #ffe5e5;
	} */
	DatePicker,
	DatePicker > Text,
	DatePicker > ImageHyperlink,
	ScheduleDatePicker,
	ScheduleDatePicker > Text,
	ScheduleDatePicker > ImageHyperlink {
		background-color: #10041f;
		color: #f7f7f7;
	}
	MessageLine,
	/* It might be useless but currently it's needed due to a strange priority
	policy used by the E4 platform to apply CSS rules to SWT widgets (see <1>): */
	Shell > Composite > Composite > MessageLine,
	Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.RESIZE'][style~='SWT.MENU'][style~='SWT.FULL_SELECTION'][style~='SWT.DATE'] > Composite > Composite > MessageLine {
		background-color:#190525; /* SWT-BUG: background color is hard-coded */
		color: #fde0e0;
	}
	StyledText, 
	Spinner,
	CCombo {
		background-color: #10031a;
		color: #f7f7f7;
	}
	Composite > StyledText,
	Shell [style~='SWT.DROP_DOWN'] > StyledText, /* for eg. folded code popup (but it's ignored) */
	/* It might be useless but currently it's needed due to a strange priority
	policy used by the E4 platform to apply CSS rules to SWT widgets (see <1>): */
	ScrolledComposite > Composite > Composite > Composite > StyledText {
		background-color: #090909;
		color: #f7f7f7;
	}
	ScrolledFormText, 
	FormText {
		background-color: #220631;
		color: #fbfbfb;
	}
	ToolItem:selected {
		background-color: #0d0317;
		color: #f7f7f7;
	}
	Table,
	/* It might be useless but currently it's needed due to a strange priority
	policy used by the E4 platform to apply CSS rules to SWT widgets (see <1>): */
	Composite > Table,
	TabFolder > Composite > Table,
	TabFolder > Composite > * > Table,
	DocCommentOwnerComposite > Group > Table,
	TabFolder > Composite > ScrolledComposite > Table,
	Shell > Composite > Composite > Table,
	Composite > Composite > Composite > Group > Table,
	Shell > Composite > Composite > Composite > Table,
	ScrolledComposite > Composite > Composite > Composite > Table,
	Shell > Composite > Composite > Composite > Composite > Composite > Table,
	Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.RESIZE'][style~='SWT.MENU'][style~='SWT.FULL_SELECTION'][style~='SWT.DATE'] > Composite > Table,
	Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.RESIZE'][style~='SWT.MENU'][style~='SWT.FULL_SELECTION'][style~='SWT.DATE'] > Composite > * > Table {
		background-color: #0e0319;
		color: #f7f7f7;
	}
	Tree,
	RegistryFilteredTree,
	/* It might be useless but currently it's needed due to a strange priority
	policy used by the E4 platform to apply CSS rules to SWT widgets (see <1>): */
	Composite > Tree,
	TabFolder > Composite > Tree,
	TabFolder > Composite > * > Tree,
	DocCommentOwnerComposite > Group > Tree,
	TabFolder > Composite > ScrolledComposite > Tree,
	Shell > Composite > Composite > Tree,
	Composite > Composite > Composite > Group > Tree,
	Shell > Composite > Composite > Composite > Tree,
	ScrolledComposite > Composite > Composite > Composite > Tree,
	Shell > Composite > Composite > Composite > Composite > Composite > Tree,
	Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.RESIZE'][style~='SWT.MENU'][style~='SWT.FULL_SELECTION'][style~='SWT.DATE'] > Composite > Tree,
	Shell[style~='SWT.RADIO'][style~='SWT.CASCADE'][style~='SWT.SHADOW_ETCHED_IN'][style~='SWT.SHADOW_ETCHED_OUT'][style~='SWT.RESIZE'][style~='SWT.MENU'][style~='SWT.FULL_SELECTION'][style~='SWT.DATE'] > Composite > * > Tree {
		background-color: #0c0c0c;
		color: #f2f2f2;
	}
	/* prevent CSS Spy red borders to be grayed with a generic Shell selector */
	Shell[style~='SWT.SHADOW_ETCHED_OUT'], Shell[style~='SWT.SHADOW_ETCHED_IN'],
	Shell[style~='SWT.CHECK'], Shell[style~='SWT.TITLE'], Shell[style~='SWT.OK'],
	Shell[style~='SWT.CANCEL'], Shell[style~='SWT.ABORT'], Shell[style~='SWT.DROP_DOWN'],
	Shell[style~='SWT.ARROW'], Shell[style~='SWT.RADIO'], Shell[style~='SWT.SINGLE'],
	Shell[style~='SWT.SHADOW_IN'], Shell[style~='SWT.TOOL'], Shell[style~='SWT.RESIZE'],
	Shell[style~='SWT.SHELL_TRIM'], Shell[style~='SWT.FILL'], Shell[style~='SWT.ALPHA'],
	Shell[style~='SWT.BORDER'], Shell[style~='SWT.DIALOG_TRIM'], Shell[style~='SWT.IGNORE'],
	Shell[style~='SWT.FULL_SELECTION'], Shell[style~='SWT.SMOOTH'], Shell[style~='SWT.VIRTUAL'],
	Shell[style~='SWT.APPLICATION_MODAL'], Shell[style~='SWT.MEDIUM'], Shell[style~='SWT.LONG']
	{
		background-color: #190525;
		color: #f2f2f2;
	}
	Shell > Composite > Table[style~='SWT.DROP_DOWN'] {
		background-color: #0e0319;
		color: #f7f7f7;
	}
	Shell[style~='SWT.DROP_DOWN'][style~='SWT.SHADOW_IN'][style~='SWT.SHADOW_ETCHED_IN'] > Composite,
	Shell[style~='SWT.DROP_DOWN'][style~='SWT.SHADOW_IN'][style~='SWT.SHADOW_ETCHED_IN'] > Composite Composite,
	Shell[style~='SWT.DROP_DOWN'][style~='SWT.SHADOW_IN'][style~='SWT.SHADOW_ETCHED_IN'] > Composite ScrolledComposite,
	Shell[style~='SWT.DROP_DOWN'][style~='SWT.SHADOW_IN'][style~='SWT.SHADOW_ETCHED_IN'] > Composite Canvas,
	Shell[style~='SWT.DROP_DOWN'][style~='SWT.SHADOW_IN'][style~='SWT.SHADOW_ETCHED_IN'] > Composite StyledText,
	Shell[style~='SWT.DROP_DOWN'][style~='SWT.SHADOW_IN'][style~='SWT.SHADOW_ETCHED_IN'] > Composite Label {
	/* Error information popup */
		background-color: #0c0c0c;
		color: #f2f2f2;
	}
	TextSearchControl {
		background-color: #10041f;
		color: #f7f7f7;
	}
	ViewerPane,
	DrillDownComposite,
	ViewerPane > ToolBar,
	DrillDownComposite > ToolBar {
		background-color: #090909;
		color: #f2f2f2;
	}
	ProgressInfoItem,
	CompareViewerPane,
	CompareViewerPane > * {
		background-color: #0d0d0d;
		color: #fbfbfb;
	}
	ProgressIndicator {
		background-color: #1e1e1e;
		color: #fbfbfb;
	}
	DiscoveryItem,
	DiscoveryItem Label,
	DiscoveryItem Composite {
		background-color: #10031a;
		color: #f7f7f7;
	}
	DiscoveryItem StyledText {
		background-color: #10031a;
		color: #eaeaea;
	}
	DiscoveryItem Link {
		background-color: #10031a;
		color: #e8cff9;
	}
	CatalogSwitcher,
	CatalogSwitcher > ScrolledComposite > Composite > Composite /* ignored because hard-coded */,
	CategoryItem {
		background-color: #190525;
		color: #f7f7f7;
	}
	GradientCanvas,
	GradientCanvas > Label,
	GradientCanvas > ToolBar,
	GradientCanvas > ImageHyperlink { 
		background-color: #12041e;
		color: #f2defd;
	}
	GradientCanvas {
		/* SWT-BUG workaround: GradientCanvas background-color is ignored */
		background: #12041e;
		background-image: #12041e;
	}
	CategoryItem > GradientCanvas,
	CategoryItem > GradientCanvas > Label { 
		/* SWT-BUG workaround: a style for background is not applied on GradientCanvas (CSS engine repaint issue) */
		background-color: #fefefe;
		color: #0d0d0d;
	}
	CategoryItem > GradientCanvas {
		/* SWT-BUG workaround: a style for background is not applied on GradientCanvas (CSS engine repaint issue) */
		background: #fefefe;
		background-image: #0d0d0d;
	}
	WebSite {
		background-color: #10041f;
		color: #f7f7f7;
	}
	CTabFolder {
		background-color: #0a0a0a;
		color: #fffefc;
		swt-tab-renderer: url('bundleclass://org.eclipse.e4.ui.workbench.renderers.swt/org.eclipse.e4.ui.workbench.renderers.swt.CTabRendering');
		swt-tab-height: 32px;
		padding: 0px 6px 6px 6px; /* top left bottom right */
		swt-tab-outline: #121212; /* border color for selected tab */
		swt-outer-keyline-color: #090522; /* border color for whole tabs container */
		swt-unselected-tabs-color: #090521 #06041d #0a0a0a 99% 100%; /* title background for unselected tab */
		swt-selected-tab-fill: #0a0a0a; /* title background for selected tab (gradient bottom color) */
		swt-shadow-color: #030303;
		swt-shadow-visible: true;
		swt-mru-visible: true;
		swt-corner-radius: 16px;
	}
	CTabFolder[style~='SWT.DOWN'][style~='SWT.BOTTOM'] {
		/* Need to restore a native renderer or the bottom inner tabs won't be displayed */
		swt-tab-renderer: null;
		swt-simple: true;
		swt-tab-height: 29px;
	}
	CTabFolder[style~='SWT.DOWN'][style~='SWT.BOTTOM'] CTabItem {
		color: #e1e1e1;
		font-weight: normal;
		/*font-family: 'Segoe Print';*/ /* currently, there is no way to define a fallback for font-family */
		/*font-size: 8;*/
	}
	CTabFolder[style~='SWT.DOWN'][style~='SWT.BOTTOM'] CTabItem:selected {
		background-color: #0a0a0a;
		color: #fbfbfb;
		/*font-weight: bold;*/
	}
	/* +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */
	CTabFolder Tree, CTabFolder Canvas {
		background-color: #0c0c0c;
		color: #f2f2f2;
	}
	.MPartStack.active Tree,
	.MPartStack.active CTabFolder Canvas {
		background-color: #0a0a0a;
		color: #f2f2f2;
	}
	.MPartStack.active Table{
		background-color: #0c0c0c;
		color: #f2f2f2;
	}
	.View {
		background-color: #0d0317;
		color: #fdfdfd;
	}
	/* not triggered
	.View.active {
		background-color: #0d0d0d;
	} */
	Form,
	FormHeading {
		background: #13052b;
		background-color: #13052b;
		background-image: #13052b;
		color: #f2defd;
	}
	Section {
		background-color: #170524;
		color: #ece2fc;
	}
	Form > LayoutComposite > LayoutComposite > * {
		background-color: #190525;
		color: #fbfbfb;
	}
	LayoutComposite, LayoutComposite > FormText,
	LayoutComposite > Label,
	LayoutComposite > Button {
		background-color: #170524;
		color: #fffefb;
	}
	LayoutComposite ScrolledPageBook,
	LayoutComposite Sash {
		background-color: #170524;
		color: #fffefb;
	}
	LayoutComposite > Text,
	LayoutComposite > Combo {
		background-color: #15041d;
		color: #fffefb;
	}
	LayoutComposite > Table {
		background-color: #0d0d0d;
		color: #ffffff;
	}
	Twistie {
		color: #fef9f3;
	}
	#SearchField {
		/* background-image: url('./searchbox.png'); */
		/* SWT-BUG: textures are applied as a label over the native ones, */
		/* in this way textures with alpha color are not usable; */
		/* default margins and padding cannot be modified and textures are not */
		/* scaled properly to fit the container size: this makes the result ugly, */
		/* moreover a texture is drawn over the widget, so also the text is covered */
		color: #fbfbfb;
	}
	/* Button {
		background-color: inherit;  /* ignored */
		/* background-image: url('./button_bg.png') */
	/* } */
	/* Button[style~='SWT.CHECK'] { */
		/* currently, Button object isn't consistent (eg. also a checkbox/radio is seen as Button) */
		/* so, css rules applied to Button have to be overridden for non-Button matches */
	/* }
	Button:disabled {
		/* SWT-BUG: currently, a disabled button cannot be styled with any window manager (gtk, win32, cocoa) */
	/* }
	Button:hover {
		/* SWT-BUG: currently, an hovered button cannot be styled with any window manager (gtk, win32, cocoa) */
	/* } */
	.MPartSashContainer {
		background-color: #190525;
		color: #fbfbfb;
	}
	PageSiteComposite, PageSiteComposite > CImageLabel {
		color: #fbfbfb;
	}
	PageSiteComposite > PropertyTable {
		background-color: #0d0d0d;
		color: #fbfbfb;
	}
	PageSiteComposite > PropertyTable:disabled {
	/* SWT-BUG: event is triggered but styles for PropertyTable are hard-coded */
		background-color: #111111;
		color: #fbfbfb;
	}
	FlyoutControlComposite, FlyoutControlComposite ToolBar, FlyoutControlComposite CLabel {
		background-color: #12041e;
		color: #fbfbfb;
	}
	/* ###################### Top Toolbar ########################## */
	#org-eclipse-ui-main-toolbar, #PerspectiveSwitcher {
		eclipse-perspective-keyline-color: #161616;
		background-color: #190525 #190525 100%;
		handle-image: none;
		color: #fefaf4;
	}
	/* ######################### Views ############################# */
	.MPart {
		background-color: #0e0317;
		color: #f7f7f7;
	}
	.MPartStack.active .MPart {
		background-color: #0a0a0a;
		color: #f7f7f7;
	}
	.MPart Composite,
	.MPart LayoutComposite,
	.MPart Label,
	.MPart Hyperlink,
	.MPart ImageHyperlink,
	.MPart ScrolledForm,
	.MPart Form,
	.MPart Section,
	.MPart FormText,
	.MPart Link,
	.MPart Sash,
	.MPart Button,
	.MPart Group,
	.MPart SashForm,
	.MPart FilteredTree,
	.MPart RegistryFilteredTree,
	.MPart PageSiteComposite,
	.MPart DependenciesComposite,
	.MPart Text[style~='SWT.READ_ONLY'],
	.MPart FigureCanvas,
	.MPart ListEditorComposite,
	.MPart ScrolledComposite,
	.MPart ScrolledComposite ToolBar,
	.Mpart ScrolledComposite ProgressInfoItem,
	.MPart Form ScrolledPageBook,
	.MPart Form > LayoutComposite > LayoutComposite > ToolBar,
	.MPart DependenciesComposite > SashForm > Section > * /* Section > DependenciesComposite$... */,
	.MPart LayoutComposite > * > LayoutComposite > Section > LayoutComposite > * /*LayoutComposite > MasterDetailBlock$... > LayoutComposite > Section > LayoutComposite > ExtensionsSection$...*/ {
		background-color: #0c0c0c;
		color: #eaeaea;
	}
	.MPartStack.active .MPart Composite,
	.MPartStack.active .MPart LayoutComposite,
	.MPartStack.active .MPart Label,
	.MPartStack.active .MPart Hyperlink,
	.MPartStack.active .MPart ImageHyperlink,
	.MPartStack.active .MPart ScrolledForm,
	.MPartStack.active .MPart Form,
	.MPartStack.active .MPart Section,
	.MPartStack.active .MPart FormText,
	.MPartStack.active .MPart Link,
	.MPartStack.active .MPart Sash,
	.MPartStack.active .MPart Button,
	.MPartStack.active .MPart Group,
	.MPartStack.active .MPart SashForm,
	.MPartStack.active .MPart FilteredTree,
	.MPartStack.active .MPart RegistryFilteredTree,
	.MPartStack.active .MPart PageSiteComposite,
	.MPartStack.active .MPart DependenciesComposite,
	.MPartStack.active .MPart Text[style~='SWT.READ_ONLY'],
	.MPartStack.active .MPart FigureCanvas,
	.MPartStack.active .MPart ListEditorComposite,
	.MPartStack.active .MPart ScrolledComposite,
	.MPartStack.active .MPart ScrolledComposite ToolBar,
	.MPartStack.active .Mpart ScrolledComposite ProgressInfoItem,
	.MPartStack.active .MPart Form ScrolledPageBook,
	.MPartStack.active .MPart Form > LayoutComposite > LayoutComposite > ToolBar,
	.MPartStack.active .MPart DependenciesComposite > SashForm > Section > * /* Section > DependenciesComposite$... */,
	.MPartStack.active .MPart LayoutComposite > * > LayoutComposite > Section > LayoutComposite > * /*LayoutComposite > MasterDetailBlock$... > LayoutComposite > Section > LayoutComposite > ExtensionsSection$...*/ {
		background-color: #0a0a0a;
		color: #e6e6e6;
	}
	.MPart Section > Label {
		background-color: #0c0c0c;
		color: #f4e3fd;
	}
	.MPartStack.active .MPart Section > Label {
		background-color: #0a0a0a;
		color: #f1defc;
	}
	.MPart Table,
	.MPart Browser,
	.Mpart OleFrame,
	.MPart ViewForm,
	.MPart ViewForm > ToolBar,
	.MPart ViewForm > CLabel,
	.MPart PageBook > Label,
	.MPart PageBook > SashForm,
	#org-eclipse-help-ui-HelpView LayoutComposite > LayoutComposite,
	#org-eclipse-help-ui-HelpView LayoutComposite > LayoutComposite > * {
		background-color: #0d0317;
		color: #f2f2f2;
	}
	.MPartStack.active .MPart Table,
	.MPartStack.active .MPart Browser,
	.MPartStack.active .Mpart OleFrame,
	.MPartStack.active .MPart ViewForm,
	.MPartStack.active .MPart ViewForm > ToolBar,
	.MPartStack.active .MPart ViewForm > CLabel,
	.MPartStack.active .MPart PageBook > Label,
	.MPartStack.active .MPart PageBook > SashForm,
	.MPartStack.active #org-eclipse-help-ui-HelpView LayoutComposite > LayoutComposite,
	.MPartStack.active #org-eclipse-help-ui-HelpView LayoutComposite > LayoutComposite > * {
		background-color: #0d0d0d;
		color: #f7f7f7;
	}
	#org-eclipse-help-ui-HelpView LayoutComposite > LayoutComposite ImageHyperlink {
		background-color: #0d0317;
		color: #eed8fe;
	}
	.MPartStack.active #org-eclipse-help-ui-HelpView LayoutComposite > LayoutComposite ImageHyperlink {
		background-color: #0d0d0d;
		color: #e6d7fd;
	}
	.MPart > Label,
	#com-android-ide-eclipse-adt-internal-lint-LintViewPart > Composite > Label {
		background-color: #0d0317;
		color: #fbf4d3;
	}
	.MPartStack.active .MPart > Label,
	.MPartStack.active #com-android-ide-eclipse-adt-internal-lint-LintViewPart > Composite > Label {
		background-color: #0b0316;
		color: #f8eaff;
	}
	.MPart Section Tree,
	.MPart LayoutComposite > * > LayoutComposite > Section > LayoutComposite > Tree {
		background-color: #100319;
		color: #f7f7f7;
	}
	.MPartStack.active .MPart Section Tree,
	.MPartStack.active .MPart LayoutComposite > * > LayoutComposite > Section > LayoutComposite > Tree {
		background-color: #171603;
		color: #f2f2f2;
	}
	.MPart DatePicker,
	.MPart DatePicker > Text,
	.MPart DatePicker > ImageHyperlink,
	.MPart ScheduleDatePicker,
	.MPart ScheduleDatePicker > Text,
	.MPart ScheduleDatePicker > ImageHyperlink,
	.MPart CCombo,
	.MPart Spinner,
	.MPart StyledText,
	.MPart PageBook > SashForm Label,
	.MPart SashForm > Text[style~='SWT.BORDER'] {
		background-color: #12041e;
		color: #eeeeee;
	}
	.MPartStack.active .MPart DatePicker,
	.MPartStack.active .MPart DatePicker > Text,
	.MPartStack.active .MPart DatePicker > ImageHyperlink,
	.MPartStack.active .MPart ScheduleDatePicker,
	.MPartStack.active .MPart ScheduleDatePicker > Text,
	.MPartStack.active .MPart ScheduleDatePicker > ImageHyperlink,
	.MPartStack.active .MPart CCombo,
	.MPartStack.active .MPart Spinner,
	.MPartStack.active .MPart StyledText,
	.MPartStack.active .MPart PageBook > SashForm Label,
	.MPartStack.active .MPart SashForm > Text[style~='SWT.BORDER'] {
		background-color: #0d0317;
		color: #eaeaea;
	}
	.MPart FormHeading,
	.MPart FormHeading > ToolBar,
	.MPart FormHeading > TitleRegion,
	.MPart FormHeading > TitleRegion > Label,
	.MPart FormHeading > TitleRegion > ToolBar,
	.MPart FormHeading > TitleRegion > StyledText,
	.MPart FormHeading LayoutComposite,
	.MPart FormHeading ImageHyperlink {
		background-color: #13052b;
		color: #f2defd;
	}
	.MPart FormHeading {
		background: #13052b;
		background-image: #13052b;	
	}
	.MPartStack.active .MPart FormHeading,
	.MPartStack.active .MPart FormHeading > ToolBar,
	.MPartStack.active .MPart FormHeading > TitleRegion,
	.MPartStack.active .MPart FormHeading > TitleRegion > Label,
	.MPartStack.active .MPart FormHeading > TitleRegion > ToolBar,
	.MPartStack.active .MPart FormHeading > TitleRegion > StyledText,
	.MPartStack.active .MPart FormHeading LayoutComposite,
	.MPartStack.active .MPart FormHeading ImageHyperlink {
		background-color: #100425;
		color: #f2defd;
	}
	.MPartStack.active .MPart FormHeading {
		background: #100425;
		background-image: #100425;
	}
	.MPart FormHeading,
	.MPart FormHeading > TitleRegion {
		swt-background-mode: none;
	}
	.MPart FormHeading > CLabel {
		background-color: #13052b;
		color: #fedddd;
	}
	.MPartStack.active .MPart FormHeading > CLabel {
		background-color: #100425;
		color: #fedddd;
	}
	/* ------------------------------------------------------------- */
	#org-eclipse-jdt-ui-SourceView StyledText,
	#org-eclipse-wst-jsdt-ui-SourceView StyledText {
		background-color: #090909;
	}
	/* ------------------------------------------------------------- */
	#org-eclipse-ui-console-ConsoleView .MPart > Composite,
	#org-eclipse-ui-console-ConsoleView .MPart StyledText,
	#org-eclipse-ui-console-ConsoleView .MPart PageBook Label,
	#org-eclipse-dltk-debug-ui-ScriptDisplayView SashForm > * {
		background-color: #0c0c0c;
		color: #f2f2f2;
	}
	.MPartStack.active #org-eclipse-ui-console-ConsoleView .MPart > Composite,
	.MPartStack.active #org-eclipse-ui-console-ConsoleView .MPart StyledText,
	.MPartStack.active #org-eclipse-ui-console-ConsoleView .MPart PageBook Label,
	.MPartStack.active #org-eclipse-dltk-debug-ui-ScriptDisplayView SashForm > * {
		background-color: #0a0a0a;
		color: #f2f2f2;
	}
	/* ------------------------------------------------------------- */
	#org-eclipse-pde-runtime-LogView Text {
		background-color: #0d0d0d;
		color: #fffefb;
	}
	/* ------------------------------------------------------------- */
	#org-eclipse-pde-ui-TargetPlatformState PageBook > Composite > * {
		background-color: #0c0c0c;
		color: #f2f2f2;
	}
	/* ------------------------------------------------------------- */
	#org-eclipse-e4-ui-compatibility-editor Canvas,
	#org-eclipse-e4-ui-compatibility-editor Canvas > *,
	/* Workaround for CDT folding column SWT-BUG (styles aren't inherited) */
	#org-eclipse-e4-ui-compatibility-editor Canvas > * > * {
		background-color: #0a0a0a;
		/* SWT-BUG: background-color rule for LineNumberRulerColumn is ignored */
	}
	.MPartStack.active #org-eclipse-e4-ui-compatibility-editor Canvas,
	.MPartStack.active #org-eclipse-e4-ui-compatibility-editor Canvas > *,
	/* Workaround for CDT folding column SWT-BUG (styles aren't inherited) */
	.MPartStack.active #org-eclipse-e4-ui-compatibility-editor Canvas > * > * {
		background-color: #080808;
		/* SWT-BUG: background-color rule for LineNumberRulerColumn is ignored */
	}
	#org-eclipse-e4-ui-compatibility-editor .MPart {
		color: #fbfbfb;
	}
	#org-eclipse-e4-ui-compatibility-editor PaletteControl ScrolledComposite > Composite > * {
		background-color: #0c0c0c;
		color: #eeeeee;
	}
	.MPartStack.active #org-eclipse-e4-ui-compatibility-editor PaletteControl ScrolledComposite > Composite > * {
		background-color: #0a0a0a;
		color: #f2f2f2;
	}
	#org-eclipse-e4-ui-compatibility-editor PaletteControl CLabel {
		background-color: #0e0e0e;
		color: #f7f7f7;
	}
	#org-eclipse-e4-ui-compatibility-editor PaletteControl CLabel:hover {
	/* SWT-BUG #140210: The event is never triggered so the native rule cannot be overridden (for hover event) */
		background-color: #090909;
		color: #f7f7f7;
	}
	#org-eclipse-e4-ui-compatibility-editor FlyoutControlComposite > Composite {
		background-color: #12041e;
		color: #f7f7f7;
	}
	#org-eclipse-e4-ui-compatibility-editor LayoutCanvas {
		background-color: #090909;
		color: #f2f2f2;
	}
	/* #################### Bottom Status Bar ######################## */
	#org-eclipse-ui-StatusLine,
	#org-eclipse-ui-ProgressBar,
	#org-eclipse-ui-ProgressBar Canvas {
		color: #f2f2f2;
	}
	#org-eclipse-ui-StatusLine CLabel {
		color: #fbeee1;
	}
	StatusLine, ImageBasedFrame{
		color: #fbeee1;
	}
	/* <<<<<<<<<<<< end of content of 'moonrise-ui-standalone.css' <<<<<<<<<<<< */
	.MPartStack { 
		swt-tab-renderer:
			url('bundleclass://net.jeeeyul.eclipse.themes/net.jeeeyul.eclipse.themes.rendering.JeeeyulsTabRenderer');
		background: #0d0317;
		jtab-selected-tab-background: #12041c #0d0317 #0d0317 99% 100%;  /* Gradient for selected tab item */	
		jtab-selected-border-color: none;  /* Gradient for the border of selected tab item */
		jtab-header-background: #190525 #07041f #0d0317 99% 100%;  /* Gradient for the background of tab header */
		jtab-unselected-border-color: none;  /* Gradient for the border of unselected tab item */
		jtab-hover-tabs-background: #14041e #07041f 100%;  /* Gradient for hover tab item */
		jtab-hover-border-color: none;  /* Gradient for the border of hover tab item */
		jtab-close-button-color: #1e1e1e;  /* Color for close button */
		jtab-close-button-hot-color: #d1cdfa;  /* Hover color for close button */
		jtab-close-button-active-color: #08032f;  /* Active color for close button */
		jtab-close-button-line-width: 2px;  /* Line width of the close button */
		jtab-chevron-color: #1e1e1e;  /* Chevron color */
		jtab-border-color: #190525 #0d0317 100%;  /* Gradient for the border of tab body */
		jtab-border-radius: 8px;  /* Radius for border of Tab and Tab Items */
		jtab-spacing: 0px;  /* Gap between each tab items */
		jtab-shadow-color: #0d0d0d;  /* Color for the shadow of tab body */
		jtab-shadow-position: 0px 2px;  /* Shadow offset for shadow of the tab body */
		jtab-shadow-radius: 10px;  /* Radius for the shadow of tab body */
		jtab-margin: 0px 2px 2px 2px;  /* Margin for the tab body */
		jtab-padding: 2px 2px 2px 2px;  /* Padding for tab body content */
		jtab-item-padding: 2px 7px 2px 7px;  /* Padding for inside area of Tab Item */
		jtab-selected-text-shadow-color: #fbfbfb;  /* Color for the shadow of selected tab item text */
		jtab-selected-text-shadow-position: 0px 0px;  /* Offset for the shadow of selected tab item text */
		jtab-unselected-text-shadow-color: #0d0d0d;  /* Color for the shadow of unselected tab item text */
		jtab-unselected-text-shadow-position: 0px 1px;  /* Offset for the shadow of unselected tab item text */
	}
	.MPartStack.active {
		background: #0a0a0a;         
		jtab-selected-tab-background: #090313 #0a0a0a #0a0a0a 99% 100%;  /* Gradient for selected tab item */
		jtab-header-background: #090521 #06041d #06041d 99% 100%;  /* Gradient for the background of tab header */
		jtab-hover-tabs-background: #100317 #050318 100%;  /* Gradient for hover tab item */
	}
	.TrimStack {
		frame-image: url('jeeeyul://frame?background-color=#14041e');
		frame-cuts: 4px 2px 5px 16px;
		handle-image: url('jeeeyul://drag-handle?height=27&background-color=#190525&embossed=false');
	}
	.MTrimBar .Draggable {
		handle-image: url('jeeeyul://drag-handle?height=27&background-color=#190525&embossed=false');
	}
	.MPartSashContainer {
		jsash-width: 4px;  /* Gap between each parts */
	}	
	/* ###################### Global Styles ########################## */
	/* ++++++ Remove these to have ONLY the main IDE shell dark ++++++ */
	CTabFolder {
		swt-tab-renderer: url('bundleclass://net.jeeeyul.eclipse.themes/net.jeeeyul.eclipse.themes.rendering.JeeeyulsTabRenderer');
		jtab-selected-tab-background: #0e0e0e #0a0a0a #0a0a0a 99% 100%;  /* Gradient for selected tab item */	
		jtab-selected-border-color: none;  /* Gradient for the border of selected tab item */
		jtab-header-background: #090521 #06041d #06041d 99% 100%;  /* Gradient for the background of tab header */
		jtab-unselected-border-color: none;  /* Gradient for the border of unselected tab item */
		jtab-hover-tabs-background: #100317 #050318 100%;  /* Gradient for hover tab item */
		jtab-hover-border-color: none;  /* Gradient for the border of hover tab item */
		jtab-close-button-color: #1e1e1e;  /* Color for close button */
		jtab-close-button-hot-color: #d1cdfa;  /* Hover color for close button */
		jtab-close-button-active-color: #08032f;  /* Active color for close button */
		jtab-close-button-line-width: 2px;  /* Line width of the close button */
		jtab-chevron-color: #1e1e1e;  /* Chevron color */
		jtab-border-color: #190525 #0d0317 100%;  /* Gradient for the border of tab body */
		jtab-border-radius: 8px;  /* Radius for border of Tab and Tab Items */
		jtab-spacing: 0px;  /* Gap between each tab items */
		jtab-shadow-color: #0d0d0d;  /* Color for the shadow of tab body */
		jtab-shadow-position: 0px 2px;  /* Shadow offset for shadow of the tab body */
		jtab-shadow-radius: 10px;  /* Radius for the shadow of tab body */
		jtab-margin: 0px 2px 2px 2px;  /* Margin for the tab body */
		jtab-padding: 2px 2px 2px 2px;  /* Padding for tab body content */
		jtab-item-padding: 2px 7px 2px 7px;  /* Padding for inside area of Tab Item */
		jtab-selected-text-shadow-color: #fbfbfb;  /* Color for the shadow of selected tab item text */
		jtab-selected-text-shadow-position: 0px 0px;  /* Offset for the shadow of selected tab item text */
		jtab-unselected-text-shadow-color: #0d0d0d;  /* Color for the shadow of unselected tab item text */
		jtab-unselected-text-shadow-position: 0px 1px;  /* Offset for the shadow of unselected tab item text */
	}
	CTabFolder[style~='SWT.DOWN'][style~='SWT.BOTTOM'] {
		/* Need to restore a native renderer or the bottom inner tabs won't be displayed and Eclipse crashes during startup with errors */
		swt-tab-renderer: null;
		swt-simple: true; 
	}
	/* +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */	
	/* ######################### Views ############################# */
	.MPart.Editor StyledText {
		jeditor-line-style: none;     /* One of "none", "solid", "dashed", "dotted" */
		jeditor-line-color: #0d0d0d;  /* Color for the underlines in text editors */
	}
