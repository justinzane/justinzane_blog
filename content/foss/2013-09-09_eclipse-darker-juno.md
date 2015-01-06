Title: A Darker Dark Juno for Eclipse
Category: foss
Tags: eclipse, dark, theme
Summary: A Darker Dark Juno for Eclipse

# A Darker Dark Juno for Eclipse

While it might be overstating thing to say that I love [Eclipse](http://www.eclipse.org/), I 
always find myself coming back to it as it is far and away the most comprehensive and flexible 
IDE for almost everything. One thing that sucks about it, though, is that out of the box it is 
**very** white. Which, for those who like very dark desktops is almost painful.

Fortunately, [Roger Dudler](http://rogerdudler.github.io/eclipse-ui-themes/) has developed a 
great theme extension and base theme to make things more comfortable for folks like me. My only 
tiny little gripe is that Roger's "Dark Juno" is not "Darker than Satan's Shadow". So, I've 
simply edited Roger's CSS, which lives at `eclipse/dropins/plugins/themes/css/juno.css`.

![Darker Juno](images/20130910_darkjuno_snap.png)

My version is this:

    :::CSS
    @import url("e4_basestyle.css");
    .MTrimmedWindow { 
            background-color: #000000;
    }
    .MPartStack {
            swt-simple: false;
            swt-mru-visible: false;
            swt-tab-renderer: url(bundleclass://org.eclipse.e4.ui.workbench.renderers.swt/org.eclipse.e4.ui.workbench.renderers.swt.CTabRendering);
            swt-unselected-tabs-color: #0f0700 #070707 #00070f 100% 100%;
            swt-outer-keyline-color: #007f00;
            swt-inner-keyline-color: #003f00;
            swt-mru-visible: false;
            swt-shadow-visible: false;
            swt-tab-outline: #3f0000;
    }
    .MPlaceholder {
            background-color: #070707;
            color: #ffffff;
    }
    .MTrimBar {
            background-color: #070707;
    }
    .MTrimBar CLabel {
            color: #ffaf00;
    }
    .MToolControl CLabel {
            color: #ffaf00;
    }
    .MTrimBar#org-eclipse-ui-main-toolbar {
            background-color:  #0f0000 #0f0f0f #00000f 100% 100%;
    }
    .MPartStack.active {
            swt-unselected-tabs-color: #070707 #3f0000 100% 100%;
            swt-outer-keyline-color: #007f00;
            swt-inner-keyline-color: #003f00;
            swt-shadow-visible: false;
            swt-tab-outline: #00003f;
    }
    PerspectiveSwitcher {
            background-color:  #0f0000 #0f0f0f #00000f 100% 100%;
            eclipse-perspective-keyline-color: #000;
            color: #ffffff;
    }
    org-eclipse-ui-editorss {
            swt-unselected-tabs-color: #3f0000 #070707 #070707 100% 100%;
            swt-outer-keyline-color: #007f00;
            swt-inner-keyline-color: #003f00;
            swt-tab-outline: #000;
            color: #ffffff;
            swt-tab-height: 8px;
            padding: 0px 5px 7px;
    }
    org-eclipse-jdt-ui-PackageExplorer {
            background-color: #070707;
            color: #ffffff;
    }
    CTabFolder {
            swt-tab-renderer: url(bundleclass://org.eclipse.e4.ui.workbench.renderers.swt/org.eclipse.e4.ui.workbench.renderers.swt.CTabRendering);
            swt-unselected-tabs-color: #0f0f0f;
            swt-outer-keyline-color: #007f00;
            swt-inner-keyline-color: #003f00;
            swt-tab-outline: #3f0000;
            selected-tab-fill: #3f3f3f;
            swt-shadow-visible: false;
    }
    CTabFolder Tree {
            background-color: #070707;
            color: #ffdf7f;
    }
    CTabFolder Canvas {
            background-color: #070707;
            color: #ffdf7f;
    }
    CTabItem {
            background-color: #070707;
            color: #ff7f3f;
    }
    CTabItem:selected { 
            color: #ffffff;
    }
    Label {
            color: #ffdf7f;
    }

Enjoy, and thank Roger Dudler!
