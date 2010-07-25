<?php defined( '_JEXEC' ) or die( 'Restricted access' ); ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="<?php echo $this->language; ?>" lang="<?php echo $this->language; ?>" >
    <head>
        <jdoc:include type="head" />
        <link rel="stylesheet" href="<?php echo $this->baseurl ?>/templates/system/css/system.css" type="text/css" />
        <link rel="stylesheet" href="<?php echo $this->baseurl ?>/templates/system/css/general.css" type="text/css" />
        <link rel="stylesheet" href="<?php echo $this->baseurl ?>/templates/kay_green2/css/template.css" type="text/css" />
        <style type="text/css">
            .page_wrapper {width: <?php echo $this->params->get('width');  ?>px;}
            .content_wrapper {width: <?php echo $this->params->get('width') - 190; ?>px;}
       </style>
    </head>
    <body>
        <div class="page_wrapper">
            <div id="breadcrumb">
                <div class="mwrapper">You are here: <jdoc:include type="modules" name="breadcrumb" /></div>
            </div>
            <div class="header"></div>
            <div id="left">
                <div class="mwrapper"><jdoc:include type="modules" name="left" style="kayrounded" /></div>
            </div>
            <div class="content_wrapper">
                <div id="top_left">
                    <div class="mwrapper"><jdoc:include type="modules" name="top" /></div>
                </div>
                <div id="top_right">
                    <div class="mwrapper"><jdoc:include type="modules" name="user1" /></div>
                </div>
                <div id="main">
                    <div class="mwrapper"><jdoc:include type="component" /></div>
                </div>
            </div>
            <div id="footer">
                <div class="mwrapper">Copyright &copy; <?php echo date('Y');?> hannay.de. All rights reserved.</div>
            </div>
        </div>
    </body>
</html> 

