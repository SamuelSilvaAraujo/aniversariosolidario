var data_name = 'panel-height-fixed';

+function ($) {
  'use strict';

  var $panels, panels_group;

  function correctPanel($panel){
    var
      panel_group = panels_group[$panel.data(data_name)],
      half_pxs = (panel_group.size - $panel[0].scrollHeight) / 2;

    $panel
      .css('padding-top', half_pxs + 'px')
      .css('padding-bottom', half_pxs + 'px');
  }

  function render(){
    $panels = $('[data-panel-height-fixed]');
    panels_group = {};

    $panels.each(function (){
      var
        $this = $(this),
        size = $this[0].scrollHeight,
        index = $this.data(data_name);

      if(!panels_group[index])
        panels_group[index] = {
          'size': 0,
          'panels': []
        };

      if(panels_group[index].size < size)
        panels_group[index].size = size;

      panels_group[index].panels.push($this);
    });

    $panels.each(function (){
      correctPanel($(this));
    });
  }

  render();
  $(window).resize($.debounce(500, render));
}(jQuery);
