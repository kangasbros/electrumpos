var exit = new Bitcoin.ExitNode("217.197.81.123", 3125, /* SSL= */ false);
exit.connect(function () {
  exit.on('blockAdd', function (data) {
    console.log('Block', data);
  });
  exit.on('txNotify', function (data) {
    console.log('Tx Notify', data);
  });
  exit.on('txAdd', function (data) {
    console.log('Tx Notify', data);
  });

  var currentAddrs = $.map($('#payments .address'), function (v) {
    return $(v).text();
  });
  exit.listen(currentAddrs);
});
