<?php
defined('_JEXEC') or die('Restricted access');
function modChrome_kayrounded($module, &$params, &$attribs) {
    if (!empty ($module->content)) : ?>
        <div class="kayrounded<?php echo $params->get('moduleclass_sfx'); ?>">
            <div class="box_corner_tl">
                <div class="box_corner_tr">
                    <div class="box_border_t"></div>
                </div>
            </div>

            <div class="box_border_l">
                <div class="box_border_r">
                    <div class="box_body">
                        <?php if ($module->showtitle) : ?>   
                            <h3><span><?php echo $module->title; ?></span></h3>
                        <?php endif; ?>
                        <?php echo $module->content; ?>
                    </div>
                </div>
            </div>
            <div class="box_corner_bl">
                <div class="box_corner_br">
                    <div class="box_border_b"></div>
                </div>
            </div>
        </div>
    <?php endif;
}
?>

