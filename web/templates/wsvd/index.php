<?php defined( '_JEXEC' ) or die( 'Restricted access' ); ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="<?php echo $this->language; ?>" lang="<?php echo $this->language; ?>" >
    <head>
        <!-- <jdoc:include type="head" /> -->
        <link rel="stylesheet" href="<?php echo $this->baseurl ?>/templates/system/css/system.css" type="text/css" />
        <link rel="stylesheet" href="<?php echo $this->baseurl ?>/templates/system/css/general.css" type="text/css" />
        <link rel="stylesheet" href="<?php echo $this->baseurl ?>/templates/wsvd/css/template.css" type="text/css" />
        <?php 
            $home = 0;
            $menuitem = & JSite::getMenu();
            if ($menuitem->getActive() == $menuitem->getDefault()) {
                $home = "1";
            }
        ?>
        <?php if ($home): ?>
            <style type="text/css">
                .content_background {padding-left:0;}
            </style>
        <?php endif; ?>
    </head>
    <body>
        <div class="page">
            <div class="logo"></div>
            <div class="title">
                <div class="title1">Wasser-Sport-Verein D&uuml;sseldorf</div>
                <div class="title2">Rudergesellschaft von 1893 e.V.</div>
            </div>
            <div class="menu_container">
                <div class="menu_left">
                    <div class="menu_right">
                        <div id="main_menu">
                            <jdoc:include type="modules" name="user3" />
                        </div>
                        <div id="sub_menu">
                            <script type="text/javascript">
                            <!--
                                function getElementByClass(className) {
                                    var allHTMLTags = document.getElementsByTagName("li");
                                    var length = allHTMLTags.length;
                                    for (var i=0; i < length; i++) {
                                        if (allHTMLTags[i].className.indexOf(className) != -1) {
                                            return allHTMLTags[i];
                                        }
                                    }
                                }
                                function positionSubMenu(element) {
                                    var liElements = element.getElementsByTagName("span");
                                    for (var i = 0; i < liElements.length; i++) {
                                        liElements[i].style.fontWeight = "bold";
                                    }
                                    var browser = navigator.appName;
                                    var verString = navigator.appVersion;
                                    var verIndex = verString.indexOf("MSIE ");
                                    if(verIndex != -1) {
                                        version = verString.substring(verIndex + 5, verIndex + 6);
                                    } 
                                    var paddingX = element.offsetLeft - 29;
                                    if((browser.indexOf("Explorer") != -1) && (version < 8)) {
                                        paddingX += 19;
                                    }
                                    //document.write("Padding X: " + paddingX);
                                    //paddingX = document.getElementById('current').offsetLeft - 27;
                                    var subMenu = document.getElementById('sub_menu');
                                    subMenu.style.padding = "0px " + paddingX + "px";
                                }
                                var parentString = "parent active ";
                                var element = getElementByClass(parentString);
                                if(element != null) {
                                    positionSubMenu(element);
                                }
                            -->
                            </script>
                            <jdoc:include type="modules" name="user4" />
                        </div>
                    </div>
                </div>
            </div>
            <div class="content_area">
                <?php if (! $home) : ?>
                <div class="images">
                    <div class="image_background">
                        <jdoc:include type="modules" name="left" />
                    </div>
                </div>
                <?php endif; ?>
                <div class="content_background">
                    <?php if($home): ?>
                        <div class="frontpage_top">
                            <jdoc:include type="modules" name="user1" style="xhtml" />
                        </div>
                        <div class="frontpage_bottom"></div>
                    <?php else: ?>
                        <div class="content">
                            <jdoc:include type="component" />
                        </div>
                    <?php endif; ?>
                </div>
                <div style="height:1px; clear:both; background-color:white;"></div>
                <div class="corner_top_left"></div>
                <div class="corner_top_right"></div>
                <div class="corner_bottom_left"></div>
                <div class="corner_bottom_right"></div>
            </div>
            <div class="footer">
                &copy; 2010 WASSER-SPORT-VEREIN | D&Uuml;SSELDORF
            </div>
        </div>
    </body>
</html>
