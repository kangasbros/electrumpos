var exit = new Bitcoin.ExitNode("217.197.81.123", 3125, /* SSL= */ false);
exit.connect(function () {
  exit.on('blockAdd', function (data) {
    console.log('Block', data);
  });
  exit.on('txNotify', function (data) {
    var tx = new Bitcoin.Transaction(data.tx);
    applyTx(tx);
    console.log('Tx Notify', tx);
  });
  exit.on('txAdd', function (data) {
    var tx = new Bitcoin.Transaction(data.tx);
    applyTx(tx, true);
    console.log('Tx Add', tx);
  });

  var currentAddrs = $.map($('#payments .address'), function (v) {
    return $(v).text();
  });
  exit.listen(currentAddrs);
});

function applyTx(tx, isConfirmed) {
  for (var i = 0, l = tx.outs.length; i < l; i++) {
    var txout = tx.outs[i];
    var hash = txout.script.simpleOutPubKeyHash();
    var addr = new Bitcoin.Address(hash);
    var addrStr = addr.toString();
    console.log("Address", addrStr);

    var domEl = $('#payments .address:contains('+addrStr+')').parent();
    if (domEl.length) {
      var received = domEl.find('.received').attr('data-received');
      var receivedValue = Bitcoin.Util.parseValue(received);
      var receivedConfirmed = domEl.find('.received').attr('data-received-confirmed');
      var receivedConfirmedValue = Bitcoin.Util.parseValue(receivedConfirmed);
      var expected = domEl.find('.amount').attr('data-amount');
      var expectedValue = Bitcoin.Util.parseValue(expected);
      var txoutValue = Bitcoin.Util.valueToBigInt(txout.value);
      receivedValue = receivedValue.add(txoutValue);
      if (isConfirmed) {
        receivedConfirmedValue = receivedConfirmedValue.add(txoutValue);
      }
      domEl.find('.received')
        .text(Bitcoin.Util.formatValue(receivedValue))
        .attr('data-received', Bitcoin.Util.formatValue(receivedValue))
        .attr('data-received-confirmed', Bitcoin.Util.formatValue(receivedConfirmedValue));
      if (receivedConfirmedValue.compareTo(expectedValue) >= 0) {
        domEl.find('.label').removeClass('label-success label-info label-warning label-important').addClass('label-success').text('Confirmed');
      } else if (receivedValue.compareTo(expectedValue) >= 0) {
        domEl.find('.label').removeClass('label-success label-info label-warning label-important').addClass('label-info').text('Paid');
      }
    }
  }
};
